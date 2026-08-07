#!/usr/bin/env python3
"""Validate declared execution-unit boundaries, handoffs, and Git chronology.

The structural checks prove consistency of recorded pass boundaries and handoff
consumption. Repository history additionally proves that the current gate existed
before a pass received credit and that separate passes first received credit in
distinct change-record commits. Neither mechanism proves a host message/context
boundary unless the host supplies an independently meaningful boundary identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
DEFAULT_MAP = ROOT / "config" / "revalidation-map.json"
DEFAULT_CHANGES = ROOT / "changes"
PASS_RESULTS = {"passed", "supported", "complete"}
BEHAVIOR_NEUTRAL_CLASS = "behavior-neutral"
BOUNDARY_KINDS = {"host-message", "declared-execution-unit", "external-artifact", "isolated-context"}
CLOSED_PASS_BOUNDARY_EXEMPTIONS = {
    "2026-08-07-dot-github-path-normalization",
    "2026-08-07-exhaustive-semantic-coverage",
    "2026-08-07-identity-abstraction-boundary",
    "2026-08-07-public-repository-bootstrap",
    "2026-08-07-repository-identity-pass",
    "2026-08-07-adaptive-review-execution",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def require_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a nonempty string")
    return value.strip()


def validate_pass_boundary_policy(mapping: dict[str, Any]) -> None:
    policy = mapping.get("pass_boundary")
    if not isinstance(policy, dict) or policy.get("enabled") is not True:
        raise ValueError("pass_boundary policy must be enabled")
    configured = policy.get("legacy_exempt_change_ids")
    if not isinstance(configured, list) or not all(isinstance(v, str) and v for v in configured):
        raise ValueError("pass_boundary legacy_exempt_change_ids must be an array of nonempty strings")
    if set(configured) != CLOSED_PASS_BOUNDARY_EXEMPTIONS or len(configured) != len(CLOSED_PASS_BOUNDARY_EXEMPTIONS):
        raise ValueError("pass-boundary legacy exemption list is closed and may contain only the fixed historical records")


def required_stages(record: dict[str, Any], mapping: dict[str, Any]) -> list[str]:
    selected = set(record.get("additional_stages", []))
    for change_class in record.get("change_classes", []):
        rule = mapping.get("change_classes", {}).get(change_class)
        if isinstance(rule, dict):
            selected.update(rule.get("stages", []))
    return [stage for stage in mapping.get("stages", []) if stage in selected]


def boundary_required(record: dict[str, Any], mapping: dict[str, Any]) -> bool:
    classes = record.get("change_classes", [])
    if classes == [BEHAVIOR_NEUTRAL_CLASS]:
        return False
    policy = mapping.get("pass_boundary", {})
    if not isinstance(policy, dict) or not policy.get("enabled", False):
        return False
    return record.get("id") not in set(policy.get("legacy_exempt_change_ids", []))


def validate_handoff(handoff: Any, expected_consumer: str, where: str) -> str:
    if not isinstance(handoff, dict):
        raise ValueError(f"{where}.handoff must be an object")
    consumer = require_string(handoff.get("consumer"), f"{where}.handoff.consumer")
    if consumer != expected_consumer:
        raise ValueError(f"{where}.handoff.consumer must be {expected_consumer!r}")
    findings = handoff.get("findings")
    if not isinstance(findings, list) or not findings or not all(isinstance(v, str) and v.strip() for v in findings):
        raise ValueError(f"{where}.handoff.findings must be a nonempty array of nonempty strings")
    for key in ("evidence", "unresolved_conditions"):
        values = handoff.get(key, [])
        if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
            raise ValueError(f"{where}.handoff.{key} must be an array of nonempty strings")
    payload = {key: value for key, value in handoff.items() if key != "sha256"}
    digest = canonical_hash(payload)
    if handoff.get("sha256") != digest:
        raise ValueError(f"{where}.handoff.sha256 is stale or invalid")
    return digest


def flattened_current_passes(record: dict[str, Any], mapping: dict[str, Any]) -> list[tuple[str, str, str, dict[str, Any], str, str]]:
    """Return credited current passes with expected consumer and current gate hash."""
    stages = required_stages(record, mapping)
    results = record.get("results", {})
    gates = record.get("execution_gates", {})
    completions = record.get("execution_completions", {})
    flattened: list[tuple[str, str, str, dict[str, Any], str, str]] = []
    for stage_index, stage in enumerate(stages):
        if results.get(stage) not in PASS_RESULTS:
            continue
        gate = gates.get(stage)
        completion = completions.get(stage)
        if not isinstance(gate, dict) or not isinstance(completion, dict):
            raise ValueError(f"record {record.get('id')!r} lacks gate/completion evidence for passing stage {stage!r}")
        gate_sha = require_string(gate.get("gate_sha256"), f"{stage}.gate_sha256")
        plan = gate.get("decision", {}).get("execution_plan")
        passes = completion.get("passes")
        if not isinstance(plan, list) or not isinstance(passes, list) or len(plan) != len(passes):
            raise ValueError(f"record {record.get('id')!r} has invalid pass plan/completion for {stage!r}")
        for pass_index, (planned, actual) in enumerate(zip(plan, passes)):
            if not isinstance(planned, dict) or not isinstance(actual, dict):
                raise ValueError(f"record {record.get('id')!r} has malformed pass {stage}[{pass_index}]")
            pass_id = require_string(planned.get("pass_id"), f"{stage}.plan[{pass_index}].pass_id")
            mode = require_string(planned.get("context_mode"), f"{stage}.plan[{pass_index}].context_mode")
            if actual.get("pass_id") != pass_id or actual.get("context_mode") != mode or actual.get("status") != "complete":
                raise ValueError(f"record {record.get('id')!r} pass completion does not match plan for {stage}:{pass_id}")
            if pass_index + 1 < len(plan):
                next_pass_id = require_string(plan[pass_index + 1].get("pass_id"), f"{stage}.plan[{pass_index + 1}].pass_id")
                expected_consumer = f"{stage}:{next_pass_id}"
            elif stage_index + 1 < len(stages):
                expected_consumer = stages[stage_index + 1]
            else:
                expected_consumer = "review-completion"
            flattened.append((stage, pass_id, mode, actual, expected_consumer, gate_sha))
    return flattened


def validate_record(record: dict[str, Any], mapping: dict[str, Any]) -> None:
    if not boundary_required(record, mapping):
        return

    stages = required_stages(record, mapping)
    results = record.get("results", {})
    gates = record.get("execution_gates", {})
    completions = record.get("execution_completions", {})
    if not isinstance(results, dict) or not isinstance(gates, dict) or not isinstance(completions, dict):
        raise ValueError(f"record {record.get('id')!r} has invalid results/gate/completion containers")

    seen_unpassed = False
    for stage in stages:
        passed = results.get(stage) in PASS_RESULTS
        if not passed:
            seen_unpassed = True
        elif seen_unpassed:
            raise ValueError(f"record {record.get('id')!r} credits {stage!r} before an earlier required stage is complete")

    flattened = flattened_current_passes(record, mapping)
    unit_ids: set[str] = set()
    boundary_ids: set[tuple[str, str]] = set()
    previous_handoff_sha: str | None = None

    for index, (stage, pass_id, mode, actual, expected_consumer, _) in enumerate(flattened):
        label = f"{stage}:{pass_id}"
        unit_id = require_string(actual.get("execution_unit_id"), f"{label}.execution_unit_id")
        if unit_id in unit_ids:
            raise ValueError(f"duplicate execution_unit_id {unit_id!r} in record {record.get('id')!r}")
        unit_ids.add(unit_id)

        boundary = actual.get("boundary")
        if not isinstance(boundary, dict):
            raise ValueError(f"{label}.boundary must be an object")
        kind = require_string(boundary.get("kind"), f"{label}.boundary.kind")
        boundary_id = require_string(boundary.get("id"), f"{label}.boundary.id")
        if kind not in BOUNDARY_KINDS:
            raise ValueError(f"{label}.boundary.kind is not recognized")
        key = (kind, boundary_id)
        if key in boundary_ids:
            raise ValueError(f"duplicate execution boundary {key!r} in record {record.get('id')!r}")
        boundary_ids.add(key)
        if mode == "ISOLATED" and kind != "isolated-context":
            raise ValueError(f"{label} requires boundary.kind 'isolated-context' for ISOLATED execution")
        if mode != "ISOLATED" and kind == "isolated-context":
            raise ValueError(f"{label} may not claim isolated-context when the plan mode is {mode}")

        inbound = actual.get("inbound_handoff_sha256")
        if index == 0:
            if inbound is not None:
                raise ValueError(f"first credited pass {label} must have null inbound_handoff_sha256")
        elif inbound != previous_handoff_sha:
            raise ValueError(f"{label}.inbound_handoff_sha256 does not consume the previous pass handoff")

        previous_handoff_sha = validate_handoff(actual.get("handoff"), expected_consumer, label)


def _pass_credit(snapshot: dict[str, Any], stage: str, pass_id: str, gate_sha: str) -> dict[str, Any] | None:
    gate = snapshot.get("execution_gates", {}).get(stage)
    completion = snapshot.get("execution_completions", {}).get(stage)
    if not isinstance(gate, dict) or gate.get("gate_sha256") != gate_sha or not isinstance(completion, dict):
        return None
    if completion.get("gate_sha256") != gate_sha:
        return None
    for item in completion.get("passes", []):
        if isinstance(item, dict) and item.get("pass_id") == pass_id and item.get("status") == "complete":
            return item
    return None


def _gate_present(snapshot: dict[str, Any], stage: str, gate_sha: str) -> bool:
    gate = snapshot.get("execution_gates", {}).get(stage)
    return isinstance(gate, dict) and gate.get("gate_sha256") == gate_sha


def validate_history_snapshots(record: dict[str, Any], mapping: dict[str, Any], snapshots: list[tuple[str, dict[str, Any]]]) -> None:
    """Require current pass credit to appear sequentially in distinct durable states."""
    if not boundary_required(record, mapping):
        return
    flattened = flattened_current_passes(record, mapping)
    if not flattened:
        return
    if not snapshots:
        raise ValueError(f"record {record.get('id')!r} has credited passes but no Git history")

    first_credit_indexes: list[int] = []
    previous_handoff_sha: str | None = None
    for stage, pass_id, _, actual, _, gate_sha in flattened:
        label = f"{stage}:{pass_id}"
        credit_index = None
        for index, (_, snapshot) in enumerate(snapshots):
            if _pass_credit(snapshot, stage, pass_id, gate_sha) is not None:
                credit_index = index
                break
        if credit_index is None:
            raise ValueError(f"{label} has no durable Git-history state containing its current gate/pass credit")
        if credit_index == 0:
            raise ValueError(f"{label} received credit before a prior durable state could contain its gate")
        if first_credit_indexes and credit_index <= first_credit_indexes[-1]:
            raise ValueError(f"{label} first received credit in the same or an earlier change-record commit as the previous pass")

        prior_snapshot = snapshots[credit_index - 1][1]
        if not _gate_present(prior_snapshot, stage, gate_sha):
            raise ValueError(f"{label} current execution gate did not exist in the prior durable change-record state")
        if previous_handoff_sha is not None:
            previous_stage, previous_pass_id, _, _, _, previous_gate_sha = flattened[len(first_credit_indexes) - 1]
            prior_previous = _pass_credit(prior_snapshot, previous_stage, previous_pass_id, previous_gate_sha)
            if prior_previous is None:
                raise ValueError(f"{label} received credit before the previous pass was durably complete")
            prior_handoff = prior_previous.get("handoff")
            if not isinstance(prior_handoff, dict) or prior_handoff.get("sha256") != previous_handoff_sha:
                raise ValueError(f"{label} received credit before the exact previous handoff was durably recorded")
            if actual.get("inbound_handoff_sha256") != previous_handoff_sha:
                raise ValueError(f"{label} does not consume the durably prior handoff")

        first_credit_indexes.append(credit_index)
        handoff = actual.get("handoff")
        previous_handoff_sha = handoff.get("sha256") if isinstance(handoff, dict) else None


def load_git_history(record_id: str) -> list[tuple[str, dict[str, Any]]]:
    path = f"skills/project-review-system/changes/{record_id}.json"
    try:
        log = subprocess.run(
            ["git", "log", "--format=%H", "--reverse", "--", path],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot read Git history for {record_id!r}") from exc
    snapshots: list[tuple[str, dict[str, Any]]] = []
    for sha in [line.strip() for line in log.splitlines() if line.strip()]:
        try:
            raw = subprocess.run(
                ["git", "show", f"{sha}:{path}"],
                cwd=REPOSITORY_ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            value = json.loads(raw)
        except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            snapshots.append((sha, value))
    return snapshots


def changed_record_ids(base: str, head: str) -> set[str]:
    try:
        output = subprocess.run(
            ["git", "diff", "--name-only", base, head, "--", "skills/project-review-system/changes"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("cannot determine change records modified in the current review range") from exc
    prefix = "skills/project-review-system/changes/"
    ids: set[str] = set()
    for raw in output.splitlines():
        path = raw.strip().replace("\\", "/")
        if path.startswith(prefix) and path.endswith(".json"):
            ids.add(path[len(prefix):-5])
    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--changes", type=Path, default=DEFAULT_CHANGES)
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--skip-git-history", action="store_true", help="test-only/portable structural validation without repository chronology")
    args = parser.parse_args()
    try:
        if bool(args.base) != bool(args.head):
            raise ValueError("--base and --head must be supplied together")
        mapping = load_json(args.map)
        validate_pass_boundary_policy(mapping)
        records = [load_json(path) for path in sorted(args.changes.glob("*.json"))]
        history_ids = changed_record_ids(args.base, args.head) if args.base and args.head else {
            record.get("id") for record in records if isinstance(record, dict) and record.get("status") != "complete"
        }
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("change-impact record must be a JSON object")
            validate_record(record, mapping)
            record_id = require_string(record.get("id"), "record.id")
            if not args.skip_git_history and boundary_required(record, mapping) and record_id in history_ids:
                validate_history_snapshots(record, mapping, load_git_history(record_id))
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print("Pass-boundary, handoff, and durable chronology evidence is structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
