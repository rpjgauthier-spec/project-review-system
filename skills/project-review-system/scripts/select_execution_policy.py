#!/usr/bin/env python3
"""Select review execution separation from workload and capability envelopes.

The selector changes only how much semantic work may share context. It does not
change required review stages, evaluations, stage order, or independent-review
requirements.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPABILITY = ROOT / "config" / "default-execution-capability.json"
DEFAULT_PROFILE_ID = "default-conservative-v1"

MODES = ("FUSED", "SEPARATED", "ISOLATED")
MODE_INDEX = {mode: index for index, mode in enumerate(MODES)}
NUMERIC_DIMENSIONS = (
    "artifact_count",
    "semantic_units",
    "required_stage_count",
    "required_evaluation_count",
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

    # Relax at most one level per checkpoint to avoid oscillation and to ensure
    # a later checkpoint confirms that lighter execution remains justified.
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
    base, evidence = base_mode(workload, capability)
    selected, transition = apply_transition_policy(base, current_mode)
    return {
        "schema_version": 1,
        "selected_mode": selected,
        "base_mode": base,
        "current_mode": current_mode,
        "transition_reason": transition,
        "capability_profile_id": capability["profile_id"],
        "capability_subject_id": capability["subject_id"],
        "capability_validation_status": capability["validation_status"],
        "capability_benchmark_suite": capability["benchmark_suite"],
        "checkpoint": workload.get("checkpoint", "unspecified"),
        "envelope_evidence": evidence,
        "assurance_boundary": (
            "Execution mode changes context separation only; required stages, evaluations, "
            "stage order, evidence obligations, and independent-review requirements are unchanged. "
            "The selector validates declared workload/profile structure but cannot prove workload "
            "truthfulness or benchmark validity."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--capability", type=Path)
    parser.add_argument("--current-mode", choices=MODES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        workload = load_json(args.workload)
        capability_path = args.capability or DEFAULT_CAPABILITY
        capability = load_json(capability_path)
        validate_workload(workload)
        validate_capability(capability, custom_profile=args.capability is not None)
        decision = select_policy(workload, capability, args.current_mode)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    rendered = json.dumps(decision, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
