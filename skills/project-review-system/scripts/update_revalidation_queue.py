#!/usr/bin/env python3
"""Generate or verify the Project Review System revalidation queue.

Inputs are JSON change-impact records in changes/*.json plus the canonical
config/revalidation-map.json. The generated Markdown queue is the reviewer's
prompt and the tracker/CI handoff. This script does not decide whether a change
record is truthful; it deterministically expands declared change classes and
enforces recorded Adaptive Execution plans at the stage-result boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = ROOT / "config" / "revalidation-map.json"
DEFAULT_CHANGES = ROOT / "changes"
DEFAULT_OUTPUT = ROOT / "reviews" / "revalidation-queue.md"
VALID_STATUSES = {"pending", "in_progress", "complete", "failed", "escalated"}
PASS_RESULTS = {"passed", "supported", "complete"}
BEHAVIOR_NEUTRAL_CLASS = "behavior-neutral"
GATE_CHECKER_PATH = ROOT / "scripts" / "check_execution_gate.py"
QUEUE_REPOSITORY_PATH = "skills/project-review-system/reviews/revalidation-queue.md"


def _load_gate_checker():
    spec = importlib.util.spec_from_file_location("execution_gate_checker_for_queue", GATE_CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load check_execution_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GATE_CHECKER = _load_gate_checker()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def source_hash(mapping: dict[str, Any], records: list[dict[str, Any]]) -> str:
    payload = json.dumps({"mapping": mapping, "records": records}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def execution_gate_required(record: dict[str, Any], mapping: dict[str, Any], behavioral: bool) -> bool:
    if not behavioral:
        return False
    policy = mapping.get("execution_gate")
    if not isinstance(policy, dict) or not policy.get("enabled", False):
        return False
    exempt = set(policy.get("legacy_exempt_change_ids", []))
    return record["id"] not in exempt


def record_artifact_paths(record: dict[str, Any]) -> list[str]:
    changed_files = record.get("changed_files")
    if not isinstance(changed_files, list) or not all(isinstance(path, str) and path.strip() for path in changed_files):
        raise ValueError(f"record {record['id']!r} requires changed_files for artifact-state binding")
    record_path = f"skills/project-review-system/changes/{record['id']}.json"
    excluded = {record_path, QUEUE_REPOSITORY_PATH}
    return sorted(set(path for path in changed_files if path not in excluded))


def current_record_target_state_id(record: dict[str, Any]) -> str:
    paths = record_artifact_paths(record)
    if not paths:
        raise ValueError(f"record {record['id']!r} has no governed artifact files after state exclusions")
    return f"sha256:{GATE_CHECKER.repository_artifact_state_sha256(paths)}"


def validate_stage_execution(record: dict[str, Any], mapping: dict[str, Any], stages: list[str], results: dict[str, Any], behavioral: bool) -> None:
    if not execution_gate_required(record, mapping, behavioral):
        return
    revision = record.get("review_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError(f"record {record['id']!r} requires nonnegative integer review_revision for adaptive execution gating")
    gates = record.get("execution_gates", {})
    completions = record.get("execution_completions", {})
    if not isinstance(gates, dict):
        raise ValueError(f"record {record['id']!r} execution_gates must be an object")
    if not isinstance(completions, dict):
        raise ValueError(f"record {record['id']!r} execution_completions must be an object")
    expected_target_state_id = current_record_target_state_id(record)

    for stage in stages:
        if results.get(stage) not in PASS_RESULTS:
            continue
        gate = gates.get(stage)
        if not isinstance(gate, dict):
            raise ValueError(f"record {record['id']!r} has passing result for {stage!r} without a current execution gate")
        completion = completions.get(stage)
        if not isinstance(completion, dict):
            raise ValueError(f"record {record['id']!r} has passing result for {stage!r} without execution completion evidence")
        try:
            decision = GATE_CHECKER.validate_execution_gate(gate, stage, revision, expected_target_state_id=expected_target_state_id)
            GATE_CHECKER.validate_execution_completion(completion, gate, decision)
        except (ValueError, TypeError, RuntimeError) as exc:
            raise ValueError(f"record {record['id']!r} has invalid execution evidence for {stage!r}: {exc}") from exc


def normalize_record(record: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    required = {"id", "summary", "change_classes", "status"}
    missing = sorted(required - record.keys())
    if missing:
        raise ValueError(f"record missing required fields: {', '.join(missing)}")
    if record["status"] not in VALID_STATUSES:
        raise ValueError(f"record {record['id']!r} has invalid status {record['status']!r}")
    classes = record["change_classes"]
    if not isinstance(classes, list) or not classes:
        raise ValueError(f"record {record['id']!r} must declare at least one change class")
    if BEHAVIOR_NEUTRAL_CLASS in classes and classes != [BEHAVIOR_NEUTRAL_CLASS]:
        raise ValueError(f"record {record['id']!r} mixes behavior-neutral with behavioral change classes")
    behavioral = classes != [BEHAVIOR_NEUTRAL_CLASS]

    stage_order = mapping["stages"]
    selected_stages: set[str] = set(record.get("additional_stages", []))
    evaluations: set[str] = set(record.get("additional_evaluations", []))
    for change_class in classes:
        if change_class not in mapping["change_classes"]:
            raise ValueError(f"record {record['id']!r} has unknown change class {change_class!r}")
        rule = mapping["change_classes"][change_class]
        selected_stages.update(rule["stages"])
        evaluations.update(rule["evaluations"])

    stages = [stage for stage in stage_order if stage in selected_stages]
    earliest = stages[0] if stages else "None"
    claimed = record.get("claimed_earliest_stage", "None")
    if behavioral and earliest == "None":
        raise ValueError(f"behavioral record {record['id']!r} maps to no review stage")
    if claimed != earliest:
        raise ValueError(f"record {record['id']!r} claims earliest stage {claimed!r}; derived stage is {earliest!r}")

    results = record.get("results", {})
    if not isinstance(results, dict):
        raise ValueError(f"record {record['id']!r} results must be an object")
    validate_stage_execution(record, mapping, stages, results, behavioral)

    required_result_keys = [*stages, *sorted(evaluations)]
    incomplete_results = [key for key in required_result_keys if results.get(key) not in PASS_RESULTS]
    if record["status"] == "complete" and incomplete_results:
        raise ValueError(f"record {record['id']!r} is complete but lacks passing results for: " + ", ".join(incomplete_results))

    if record["status"] == "escalated":
        escalation = record.get("escalation")
        if not isinstance(escalation, dict):
            raise ValueError(f"record {record['id']!r} is escalated but has no escalation object")
        required_escalation = {"blocked_scope", "controlling_review", "resumption_condition"}
        missing_escalation = sorted(key for key in required_escalation if not str(escalation.get(key, "")).strip())
        if missing_escalation:
            raise ValueError(f"record {record['id']!r} escalation is missing: " + ", ".join(missing_escalation))

    return {
        **record,
        "derived_behavioral": behavioral,
        "derived_stages": stages,
        "derived_evaluations": sorted(evaluations),
        "derived_earliest_stage": earliest,
        "derived_incomplete_results": incomplete_results,
        "derived_execution_gate_required": execution_gate_required(record, mapping, behavioral),
    }


def render(mapping: dict[str, Any], records: list[dict[str, Any]]) -> str:
    digest = source_hash(mapping, records)
    normalized = [normalize_record(record, mapping) for record in records]
    pending = [r for r in normalized if r["status"] not in {"complete", "escalated"}]
    lines = ["# Generated Revalidation Queue", "", "> Generated by `scripts/update_revalidation_queue.py`. Do not edit manually.", f"> Source hash: `{digest}`", "", "## Advancement gate", ""]
    lines.append(f"**BLOCKED:** {len(pending)} change-impact record(s) still require evaluation or correction." if pending else "**CLEAR:** all declared change-impact records are complete or escalated.")
    lines.extend(["", "## Required reviewer actions", ""])
    if not normalized:
        lines.append("No change-impact records were found.")
    for record in normalized:
        lines.extend([
            f"### {record['id']} — {record['summary']}", "",
            f"- **Status:** `{record['status']}`",
            f"- **Behavioral:** `{str(record['derived_behavioral']).lower()}` (derived from change classes)",
            f"- **Execution gate required:** `{str(record['derived_execution_gate_required']).lower()}`",
            f"- **Change classes:** {', '.join(f'`{c}`' for c in record['change_classes'])}",
            f"- **Earliest affected stage:** {record['derived_earliest_stage']}",
            "- **Required stages:** " + (", ".join(record["derived_stages"]) or "None"),
            "- **Required evaluations:** " + (", ".join(record["derived_evaluations"]) or "None"),
            f"- **Reason:** {record.get('reason', 'Not recorded')}", "", "Checklist:"
        ])
        results = record.get("results", {})
        for stage in record["derived_stages"]:
            mark = "x" if results.get(stage) in PASS_RESULTS else " "
            gate_note = " with a valid artifact-bound execution gate and matching execution completion" if record["derived_execution_gate_required"] else ""
            lines.append(f"- [{mark}] Revalidate **{stage}**{gate_note} and record the result.")
        for evaluation in record["derived_evaluations"]:
            mark = "x" if results.get(evaluation) in PASS_RESULTS else " "
            lines.append(f"- [{mark}] Run evaluation `{evaluation}` and record the result.")
        lines.append("")
    lines.extend(["## Commands", "", "```bash", "python skills/project-review-system/scripts/update_revalidation_queue.py", "python skills/project-review-system/scripts/update_revalidation_queue.py --check", "python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'", "```", "", "`--check` exits nonzero when the generated queue is stale, a completed record lacks passing results, an execution-gated stage has absent/stale/invalid gate or completion evidence, an escalation lacks a resumption contract, or any record remains pending, in progress, or failed."])
    return "\n".join(lines) + "\n"


def collect_records(directory: Path) -> list[dict[str, Any]]:
    if not directory.exists():
        return []
    return [load_json(path) for path in sorted(directory.glob("*.json"))]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--changes", type=Path, default=DEFAULT_CHANGES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        mapping = load_json(args.map)
        records = collect_records(args.changes)
        generated = render(mapping, records)
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    unresolved = any(record.get("status") not in {"complete", "escalated"} for record in records)
    if args.check:
        try:
            current = args.output.read_text(encoding="utf-8")
        except OSError:
            print(f"ERROR: generated queue is missing: {args.output}")
            return 1
        if current != generated:
            print("ERROR: generated revalidation queue is stale. Run the generator.")
            return 1
        if unresolved:
            print("ERROR: generated revalidation queue contains unresolved work.")
            return 1
        print("Revalidation queue is current and clear.")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generated, encoding="utf-8")
    print(f"Updated {args.output}")
    if unresolved:
        print("ACTION REQUIRED: run the evaluations listed in the generated queue before advancing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
