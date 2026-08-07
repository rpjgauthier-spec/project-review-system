#!/usr/bin/env python3
"""Validate declared execution-unit boundaries and bounded handoff chains.

This checker can prove structural consistency of recorded pass boundaries and
handoff consumption. It cannot prove that a host message/context boundary
actually occurred unless the host supplies an independently meaningful boundary
identifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = ROOT / "config" / "revalidation-map.json"
DEFAULT_CHANGES = ROOT / "changes"
PASS_RESULTS = {"passed", "supported", "complete"}
BEHAVIOR_NEUTRAL_CLASS = "behavior-neutral"
BOUNDARY_KINDS = {"host-message", "declared-execution-unit", "external-artifact", "isolated-context"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def require_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a nonempty string")
    return value.strip()


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
    digest = canonical_hash(handoff)
    if handoff.get("sha256") != digest:
        raise ValueError(f"{where}.handoff.sha256 is stale or invalid")
    return digest


def validate_record(record: dict[str, Any], mapping: dict[str, Any]) -> None:
    if not boundary_required(record, mapping):
        return

    stages = required_stages(record, mapping)
    results = record.get("results", {})
    gates = record.get("execution_gates", {})
    completions = record.get("execution_completions", {})
    if not isinstance(results, dict) or not isinstance(gates, dict) or not isinstance(completions, dict):
        raise ValueError(f"record {record.get('id')!r} has invalid results/gate/completion containers")

    # A later stage cannot be credited before an earlier required stage.
    seen_unpassed = False
    for stage in stages:
        passed = results.get(stage) in PASS_RESULTS
        if not passed:
            seen_unpassed = True
        elif seen_unpassed:
            raise ValueError(f"record {record.get('id')!r} credits {stage!r} before an earlier required stage is complete")

    flattened: list[tuple[str, str, str, dict[str, Any]]] = []
    for stage in stages:
        if results.get(stage) not in PASS_RESULTS:
            continue
        gate = gates.get(stage)
        completion = completions.get(stage)
        if not isinstance(gate, dict) or not isinstance(completion, dict):
            raise ValueError(f"record {record.get('id')!r} lacks gate/completion evidence for passing stage {stage!r}")
        plan = gate.get("decision", {}).get("execution_plan")
        passes = completion.get("passes")
        if not isinstance(plan, list) or not isinstance(passes, list) or len(plan) != len(passes):
            raise ValueError(f"record {record.get('id')!r} has invalid pass plan/completion for {stage!r}")
        for index, (planned, actual) in enumerate(zip(plan, passes)):
            if not isinstance(planned, dict) or not isinstance(actual, dict):
                raise ValueError(f"record {record.get('id')!r} has malformed pass {stage}[{index}]")
            pass_id = require_string(planned.get("pass_id"), f"{stage}.plan[{index}].pass_id")
            mode = require_string(planned.get("context_mode"), f"{stage}.plan[{index}].context_mode")
            if actual.get("pass_id") != pass_id or actual.get("context_mode") != mode or actual.get("status") != "complete":
                raise ValueError(f"record {record.get('id')!r} pass completion does not match plan for {stage}:{pass_id}")
            flattened.append((stage, pass_id, mode, actual))

    unit_ids: set[str] = set()
    boundary_ids: set[tuple[str, str]] = set()
    previous_handoff_sha: str | None = None

    for index, (stage, pass_id, mode, actual) in enumerate(flattened):
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

        if index + 1 < len(flattened):
            next_stage, next_pass_id, _, _ = flattened[index + 1]
            expected_consumer = f"{next_stage}:{next_pass_id}"
        else:
            expected_consumer = "review-completion"
        previous_handoff_sha = validate_handoff(actual.get("handoff"), expected_consumer, label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--changes", type=Path, default=DEFAULT_CHANGES)
    args = parser.parse_args()
    try:
        mapping = load_json(args.map)
        records = [load_json(path) for path in sorted(args.changes.glob("*.json"))]
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("change-impact record must be a JSON object")
            validate_record(record, mapping)
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print("Pass-boundary and handoff evidence is structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
