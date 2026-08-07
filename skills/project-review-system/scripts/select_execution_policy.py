#!/usr/bin/env python3
"""Build and validate Adaptive Execution plans.

Default execution is SEPARATED. Semantic stage assessment may require bounded
subpasses and may mark individual subpasses ISOLATED. FUSED execution is allowed
only through an exact permission in an externally VALIDATED capability profile.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPABILITY = ROOT / "config" / "default-execution-capability.json"
DEFAULT_PROFILE_ID = "default-separated-v1"
VALID_PROFILE_STATUSES = {"DEFAULT_SEPARATED", "VALIDATED"}
PASS_MODES = {"SEPARATED", "ISOLATED", "FUSED"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def require_nonempty_string(container: dict[str, Any], key: str, where: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}.{key} is required")
    return value.strip()


def validate_subpasses(subpasses: Any, single_pass_suitable: bool) -> list[dict[str, Any]]:
    if not isinstance(subpasses, list):
        raise ValueError("workload.stage_assessment.subpasses must be an array")
    if single_pass_suitable:
        if subpasses:
            raise ValueError("single-pass-suitable stage must not predeclare subdivision subpasses")
        return []
    if len(subpasses) < 2:
        raise ValueError("single-pass-unsuitable stage requires at least two bounded subpasses")

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(subpasses):
        if not isinstance(item, dict):
            raise ValueError(f"stage_assessment.subpasses[{index}] must be an object")
        pass_id = require_nonempty_string(item, "pass_id", f"stage_assessment.subpasses[{index}]")
        scope = require_nonempty_string(item, "scope", f"stage_assessment.subpasses[{index}]")
        if pass_id in seen:
            raise ValueError(f"duplicate subpass id: {pass_id}")
        seen.add(pass_id)
        isolation_required = item.get("isolation_required")
        if not isinstance(isolation_required, bool):
            raise ValueError(f"stage_assessment.subpasses[{index}].isolation_required must be boolean")
        reasons = item.get("reasons", [])
        if not isinstance(reasons, list) or not all(isinstance(v, str) and v.strip() for v in reasons):
            raise ValueError(f"stage_assessment.subpasses[{index}].reasons must be an array of nonempty strings")
        normalized.append({
            "pass_id": pass_id,
            "scope": scope,
            "isolation_required": isolation_required,
            "reasons": reasons,
        })
    return normalized


def validate_workload(workload: dict[str, Any]) -> None:
    if workload.get("schema_version") != 1:
        raise ValueError("workload.schema_version must be 1")
    require_nonempty_string(workload, "reviewer_subject_id", "workload")
    require_nonempty_string(workload, "activity", "workload")
    require_nonempty_string(workload, "target_state_id", "workload")
    revision = workload.get("review_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError("workload.review_revision must be a nonnegative integer")
    require_nonempty_string(workload, "workload_class", "workload")

    assessment = workload.get("stage_assessment")
    if not isinstance(assessment, dict):
        raise ValueError("workload.stage_assessment must be an object")
    suitable = assessment.get("single_pass_suitable")
    if not isinstance(suitable, bool):
        raise ValueError("workload.stage_assessment.single_pass_suitable must be boolean")
    reasons = assessment.get("reasons", [])
    if not isinstance(reasons, list) or not all(isinstance(v, str) and v.strip() for v in reasons):
        raise ValueError("workload.stage_assessment.reasons must be an array of nonempty strings")
    validate_subpasses(assessment.get("subpasses", []), suitable)

    fused = workload.get("fused_authorization")
    if fused is not None:
        if not isinstance(fused, dict):
            raise ValueError("workload.fused_authorization must be null or an object")
        require_nonempty_string(fused, "permission_id", "workload.fused_authorization")
        require_nonempty_string(fused, "group_id", "workload.fused_authorization")
        activities = fused.get("activities")
        if not isinstance(activities, list) or len(activities) < 2 or not all(isinstance(v, str) and v.strip() for v in activities):
            raise ValueError("workload.fused_authorization.activities must contain at least two activity names")
        if workload["activity"] not in activities:
            raise ValueError("workload activity must be included in fused_authorization.activities")


def validate_capability(capability: dict[str, Any], custom_profile: bool) -> None:
    if capability.get("schema_version") != 1:
        raise ValueError("capability.schema_version must be 1")
    profile_id = require_nonempty_string(capability, "profile_id", "capability")
    require_nonempty_string(capability, "subject_id", "capability")
    status = capability.get("validation_status")
    if status not in VALID_PROFILE_STATUSES:
        raise ValueError("capability.validation_status must be DEFAULT_SEPARATED or VALIDATED")
    require_nonempty_string(capability, "benchmark_suite", "capability")
    require_nonempty_string(capability, "benchmark_evidence", "capability")
    permissions = capability.get("fused_permissions", [])
    if not isinstance(permissions, list):
        raise ValueError("capability.fused_permissions must be an array")
    seen: set[str] = set()
    for index, permission in enumerate(permissions):
        if not isinstance(permission, dict):
            raise ValueError(f"capability.fused_permissions[{index}] must be an object")
        permission_id = require_nonempty_string(permission, "permission_id", f"capability.fused_permissions[{index}]")
        if permission_id in seen:
            raise ValueError(f"duplicate fused permission id: {permission_id}")
        seen.add(permission_id)
        activities = permission.get("activities")
        if not isinstance(activities, list) or len(activities) < 2 or not all(isinstance(v, str) and v.strip() for v in activities):
            raise ValueError(f"capability.fused_permissions[{index}].activities must contain at least two activity names")
        require_nonempty_string(permission, "workload_class", f"capability.fused_permissions[{index}]")
        require_nonempty_string(permission, "benchmark_evidence", f"capability.fused_permissions[{index}]")

    if status == "DEFAULT_SEPARATED":
        if profile_id != DEFAULT_PROFILE_ID:
            raise ValueError("DEFAULT_SEPARATED is reserved for default-separated-v1")
        if permissions:
            raise ValueError("default separated profile cannot grant fused permissions")
    if custom_profile and status != "VALIDATED":
        raise ValueError("custom capability profiles must have validation_status VALIDATED")


def find_fused_permission(workload: dict[str, Any], capability: dict[str, Any]) -> dict[str, Any] | None:
    request = workload.get("fused_authorization")
    if request is None:
        return None
    if capability.get("validation_status") != "VALIDATED":
        raise ValueError("FUSED execution requires a VALIDATED capability profile")
    if capability.get("subject_id") != workload.get("reviewer_subject_id"):
        raise ValueError("validated fused capability subject does not match workload reviewer_subject_id")
    for permission in capability.get("fused_permissions", []):
        if permission["permission_id"] != request["permission_id"]:
            continue
        if permission["activities"] != request["activities"]:
            raise ValueError("fused permission activities do not exactly match the requested activity group")
        if permission["workload_class"] != workload["workload_class"]:
            raise ValueError("fused permission workload_class does not match workload")
        return permission
    raise ValueError("requested fused permission is not present in the validated capability profile")


def select_policy(workload: dict[str, Any], capability: dict[str, Any]) -> dict[str, Any]:
    validate_workload(workload)
    validate_capability(capability, custom_profile=False)
    fused_permission = find_fused_permission(workload, capability)
    assessment = workload["stage_assessment"]

    if fused_permission is not None:
        if not assessment["single_pass_suitable"]:
            raise ValueError("FUSED execution cannot override a stage assessment requiring subdivision")
        plan = [{"pass_id": "fused-group", "scope": "validated fused activity group", "context_mode": "FUSED"}]
        selected_mode = "FUSED"
        plan_kind = "FUSED_GROUP"
        permission_id = fused_permission["permission_id"]
    elif assessment["single_pass_suitable"]:
        plan = [{"pass_id": "stage-main", "scope": workload["activity"], "context_mode": "SEPARATED"}]
        selected_mode = "SEPARATED"
        plan_kind = "ONE_PASS"
        permission_id = None
    else:
        subpasses = validate_subpasses(assessment["subpasses"], False)
        plan = [
            {
                "pass_id": item["pass_id"],
                "scope": item["scope"],
                "context_mode": "ISOLATED" if item["isolation_required"] else "SEPARATED",
            }
            for item in subpasses
        ]
        selected_mode = "SEPARATED"
        plan_kind = "SUBDIVIDED"
        permission_id = None

    return {
        "schema_version": 1,
        "activity": workload["activity"],
        "target_state_id": workload["target_state_id"],
        "review_revision": workload["review_revision"],
        "reviewer_subject_id": workload["reviewer_subject_id"],
        "workload_class": workload["workload_class"],
        "selected_mode": selected_mode,
        "plan_kind": plan_kind,
        "execution_plan": plan,
        "fused_permission_id": permission_id,
        "capability_profile_id": capability["profile_id"],
        "capability_subject_id": capability["subject_id"],
        "capability_validation_status": capability["validation_status"],
        "capability_benchmark_suite": capability["benchmark_suite"],
        "workload_sha256": canonical_hash(workload),
        "capability_sha256": canonical_hash(capability),
        "assurance_boundary": (
            "Semantic judgment determines whether one pass is suitable and which bounded subpasses require isolation. "
            "Deterministic policy defaults to SEPARATED, converts declared isolation requirements into ISOLATED subpasses, "
            "and permits FUSED only through exact pre-existing VALIDATED capability permission. The gate and completion "
            "validator enforce the recorded plan but do not prove the semantic assessment itself was correct."
        ),
    }


def build_gate(workload: dict[str, Any], capability: dict[str, Any]) -> dict[str, Any]:
    decision = select_policy(workload, capability)
    payload = {"activity": workload["activity"], "workload": workload, "capability": capability, "decision": decision}
    return {"schema_version": 1, **payload, "gate_sha256": canonical_hash(payload)}


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
        raise ValueError(f"execution gate activity {activity!r} does not match expected {expected_activity!r}")
    if workload.get("activity") != activity:
        raise ValueError("execution gate workload activity does not match gate activity")
    recomputed = select_policy(workload, capability)
    if decision != recomputed:
        raise ValueError("execution gate decision does not match current workload/capability inputs")
    payload = {"activity": activity, "workload": workload, "capability": capability, "decision": recomputed}
    if gate.get("gate_sha256") != canonical_hash(payload):
        raise ValueError("execution gate hash is stale or invalid")
    return recomputed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--capability", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--gate", action="store_true", help="emit a verifiable execution gate record")
    args = parser.parse_args()
    try:
        workload = load_json(args.workload)
        capability_path = args.capability or DEFAULT_CAPABILITY
        capability = load_json(capability_path)
        validate_workload(workload)
        validate_capability(capability, custom_profile=args.capability is not None)
        value = build_gate(workload, capability) if args.gate else select_policy(workload, capability)
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
