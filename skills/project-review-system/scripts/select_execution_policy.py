#!/usr/bin/env python3
"""Select review execution separation from workload and capability envelopes.

The selector changes only how much semantic work may share context. It does not
change required review stages, evaluations, stage order, or independent-review
requirements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPABILITY = ROOT / "config" / "default-execution-capability.json"
DEFAULT_PROFILE_ID = "default-conservative-v1"
SUPPORTED_ENVELOPE_MODEL = "rectangular-v1"

MODES = ("FUSED", "SEPARATED", "ISOLATED")
MODE_INDEX = {mode: index for index, mode in enumerate(MODES)}
NUMERIC_DIMENSIONS = (
    "artifact_count",
    "content_bytes",
    "remaining_stage_count",
    "remaining_evaluation_count",
    "dependency_count",
    "protected_control_count",
    "unresolved_uncertainty_count",
    "material_findings_count",
    "unexpected_dependency_count",
)
BOOLEAN_DIMENSIONS = {
    "self_referential": "allow_self_referential",
    "exhaustive_claim": "allow_exhaustive_claim",
}
VALID_PROFILE_STATUSES = {"DEFAULT_CONSERVATIVE", "VALIDATED"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def require_nonnegative_int(container: dict[str, Any], key: str, where: str) -> int:
    value = container.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{where}.{key} must be a nonnegative integer")
    return value


def require_nonempty_string(container: dict[str, Any], key: str, where: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}.{key} is required")
    return value.strip()


def validate_workload(workload: dict[str, Any]) -> None:
    if workload.get("schema_version") != 1:
        raise ValueError("workload.schema_version must be 1")
    require_nonempty_string(workload, "reviewer_subject_id", "workload")
    require_nonempty_string(workload, "activity", "workload")
    require_nonempty_string(workload, "target_state_id", "workload")
    for key in NUMERIC_DIMENSIONS:
        require_nonnegative_int(workload, key, "workload")
    for key in BOOLEAN_DIMENSIONS:
        if not isinstance(workload.get(key), bool):
            raise ValueError(f"workload.{key} must be boolean")


def validate_envelope(envelope: dict[str, Any], name: str) -> None:
    if not isinstance(envelope, dict):
        raise ValueError(f"capability.{name} must be an object")
    for key in NUMERIC_DIMENSIONS:
        require_nonnegative_int(envelope, key, f"capability.{name}")
    for key in BOOLEAN_DIMENSIONS.values():
        if not isinstance(envelope.get(key), bool):
            raise ValueError(f"capability.{name}.{key} must be boolean")


def validate_capability(capability: dict[str, Any], custom_profile: bool) -> None:
    if capability.get("schema_version") != 1:
        raise ValueError("capability.schema_version must be 1")
    status = capability.get("validation_status")
    if status not in VALID_PROFILE_STATUSES:
        raise ValueError(
            "capability.validation_status must be DEFAULT_CONSERVATIVE or VALIDATED"
        )

    profile_id = require_nonempty_string(capability, "profile_id", "capability")
    require_nonempty_string(capability, "subject_id", "capability")
    require_nonempty_string(capability, "benchmark_suite", "capability")
    require_nonempty_string(capability, "benchmark_evidence", "capability")
    envelope_model = require_nonempty_string(capability, "envelope_model", "capability")
    if envelope_model != SUPPORTED_ENVELOPE_MODEL:
        raise ValueError(
            f"capability.envelope_model must be {SUPPORTED_ENVELOPE_MODEL}"
        )

    if status == "DEFAULT_CONSERVATIVE" and profile_id != DEFAULT_PROFILE_ID:
        raise ValueError(
            "DEFAULT_CONSERVATIVE is reserved for the built-in default-conservative-v1 profile"
        )
    if custom_profile and status != "VALIDATED":
        raise ValueError("custom capability profiles must have validation_status VALIDATED")

    validate_envelope(capability.get("fused_limits"), "fused_limits")
    validate_envelope(capability.get("separated_limits"), "separated_limits")

    fused = capability["fused_limits"]
    separated = capability["separated_limits"]
    for key in NUMERIC_DIMENSIONS:
        if fused[key] > separated[key]:
            raise ValueError(
                f"capability fused limit for {key} exceeds separated limit"
            )
    for workload_key, allow_key in BOOLEAN_DIMENSIONS.items():
        if fused[allow_key] and not separated[allow_key]:
            raise ValueError(
                f"capability fused envelope allows {workload_key} while separated envelope forbids it"
            )


def validate_subject_binding(workload: dict[str, Any], capability: dict[str, Any]) -> None:
    """Prevent validated capability evidence from silently transferring subjects."""
    if capability["validation_status"] != "VALIDATED":
        return
    workload_subject = require_nonempty_string(workload, "reviewer_subject_id", "workload")
    capability_subject = require_nonempty_string(capability, "subject_id", "capability")
    if workload_subject != capability_subject:
        raise ValueError(
            "validated capability subject does not match workload reviewer_subject_id"
        )


def envelope_failures(
    workload: dict[str, Any], envelope: dict[str, Any]
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for key in NUMERIC_DIMENSIONS:
        actual = workload[key]
        limit = envelope[key]
        if actual > limit:
            failures.append({"dimension": key, "actual": actual, "limit": limit})
    for workload_key, allow_key in BOOLEAN_DIMENSIONS.items():
        if workload[workload_key] and not envelope[allow_key]:
            failures.append(
                {
                    "dimension": workload_key,
                    "actual": True,
                    "limit": False,
                }
            )
    return failures


def base_mode(workload: dict[str, Any], capability: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    fused_failures = envelope_failures(workload, capability["fused_limits"])
    separated_failures = envelope_failures(workload, capability["separated_limits"])
    if not fused_failures:
        mode = "FUSED"
    elif not separated_failures:
        mode = "SEPARATED"
    else:
        mode = "ISOLATED"
    return mode, {
        "fused_failures": fused_failures,
        "separated_failures": separated_failures,
    }


def apply_transition_policy(base: str, current: str | None) -> tuple[str, str]:
    if current is None:
        return base, "initial decision"
    if current not in MODE_INDEX:
        raise ValueError(f"current mode must be one of: {', '.join(MODES)}")

    base_index = MODE_INDEX[base]
    current_index = MODE_INDEX[current]
    if base_index >= current_index:
        if base_index > current_index:
            return base, "tightened immediately because workload exceeded the current envelope"
        return current, "current mode remains within its envelope"

    relaxed_index = max(base_index, current_index - 1)
    selected = MODES[relaxed_index]
    if selected == base:
        return selected, "relaxed one level to the lightest currently validated mode"
    return selected, "relaxed by one level; further relaxation requires a later checkpoint"


def select_policy(
    workload: dict[str, Any], capability: dict[str, Any], current_mode: str | None = None
) -> dict[str, Any]:
    validate_workload(workload)
    validate_capability(capability, custom_profile=False)
    validate_subject_binding(workload, capability)
    base, evidence = base_mode(workload, capability)
    selected, transition = apply_transition_policy(base, current_mode)
    return {
        "schema_version": 1,
        "activity": workload["activity"],
        "target_state_id": workload["target_state_id"],
        "selected_mode": selected,
        "base_mode": base,
        "current_mode": current_mode,
        "transition_reason": transition,
        "reviewer_subject_id": workload["reviewer_subject_id"],
        "capability_profile_id": capability["profile_id"],
        "capability_subject_id": capability["subject_id"],
        "capability_validation_status": capability["validation_status"],
        "capability_benchmark_suite": capability["benchmark_suite"],
        "capability_envelope_model": capability["envelope_model"],
        "checkpoint": workload.get("checkpoint", "unspecified"),
        "workload_sha256": canonical_hash(workload),
        "capability_sha256": canonical_hash(capability),
        "envelope_evidence": evidence,
        "assurance_boundary": (
            "Execution mode changes context separation only; required stages, evaluations, "
            "stage order, evidence obligations, and independent-review requirements are unchanged. "
            "The selector binds the decision to a declared target_state_id and validates declared "
            "workload/profile structure plus validated-profile subject binding, but it cannot prove "
            "that the target-state identifier, workload facts, combined-envelope benchmark, or "
            "reviewer independence are truthful. Environment-specific enforcement must verify the "
            "target_state_id against the actual governed artifacts."
        ),
    }


def build_gate(
    workload: dict[str, Any], capability: dict[str, Any], current_mode: str | None = None
) -> dict[str, Any]:
    decision = select_policy(workload, capability, current_mode)
    payload = {
        "activity": workload["activity"],
        "workload": workload,
        "capability": capability,
        "current_mode": current_mode,
        "decision": decision,
    }
    return {
        "schema_version": 1,
        **payload,
        "gate_sha256": canonical_hash(payload),
    }


def validate_gate(gate: dict[str, Any], expected_activity: str | None = None) -> dict[str, Any]:
    if not isinstance(gate, dict) or gate.get("schema_version") != 1:
        raise ValueError("execution gate must be a schema_version 1 object")
    workload = gate.get("workload")
    capability = gate.get("capability")
    decision = gate.get("decision")
    if not isinstance(workload, dict) or not isinstance(capability, dict) or not isinstance(decision, dict):
        raise ValueError("execution gate must include workload, capability, and decision objects")
    activity = require_nonempty_string(gate, "activity", "execution_gate")
    if expected_activity is not None and activity != expected_activity:
        raise ValueError(
            f"execution gate activity {activity!r} does not match expected {expected_activity!r}"
        )
    if workload.get("activity") != activity:
        raise ValueError("execution gate workload activity does not match gate activity")
    recomputed = select_policy(workload, capability, gate.get("current_mode"))
    if decision != recomputed:
        raise ValueError("execution gate decision does not match current workload/capability inputs")
    payload = {
        "activity": activity,
        "workload": workload,
        "capability": capability,
        "current_mode": gate.get("current_mode"),
        "decision": recomputed,
    }
    if gate.get("gate_sha256") != canonical_hash(payload):
        raise ValueError("execution gate hash is stale or invalid")
    return recomputed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--capability", type=Path)
    parser.add_argument("--current-mode", choices=MODES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--gate", action="store_true", help="emit a verifiable execution gate record")
    args = parser.parse_args()

    try:
        workload = load_json(args.workload)
        capability_path = args.capability or DEFAULT_CAPABILITY
        capability = load_json(capability_path)
        validate_workload(workload)
        validate_capability(capability, custom_profile=args.capability is not None)
        value = (
            build_gate(workload, capability, args.current_mode)
            if args.gate
            else select_policy(workload, capability, args.current_mode)
        )
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
