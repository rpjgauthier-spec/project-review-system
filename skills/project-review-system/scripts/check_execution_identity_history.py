#!/usr/bin/env python3
"""Reject reuse or mutation of execution evidence across review history.

Each completed execution occurrence is identified by review revision, stage,
planned pass_id, and gate hash. Completed subpasses are occurrences even before
the enclosing semantic stage receives a passing result. When an occurrence first
appears in durable change-record history, its execution_unit_id and boundary must
never have been used by an earlier occurrence, and the complete recorded pass
evidence must remain unchanged in later snapshots.

A logical pass slot is the tuple (review_revision, stage, pass_id). Once that slot
has durable completion evidence, a different gate may not create a replacement
occurrence in the same review revision. More strongly, once any pass in a stage
has durable completion evidence, the tuple (review_revision, stage) is bound to
that gate hash for all later completed subpasses in that revision. Changing the
stage gate or execution plan after durable completion therefore requires a new
review revision.

For a PR-scoped check, history begins with the base-state snapshot when the change
record already exists there, followed by change-record commits in base..head.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
DEFAULT_MAP = ROOT / "config" / "revalidation-map.json"
CHANGES_PREFIX = "skills/project-review-system/changes/"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def require_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a nonempty string")
    return value.strip()


def completed_occurrences(snapshot: dict[str, Any]) -> list[tuple[tuple[Any, ...], str, tuple[str, str], str]]:
    revision = snapshot.get("review_revision")
    gates = snapshot.get("execution_gates", {})
    completions = snapshot.get("execution_completions", {})
    if not isinstance(gates, dict) or not isinstance(completions, dict):
        return []

    occurrences: list[tuple[tuple[Any, ...], str, tuple[str, str], str]] = []
    for stage, completion in completions.items():
        gate = gates.get(stage)
        if not isinstance(gate, dict) or not isinstance(completion, dict):
            continue
        gate_sha = gate.get("gate_sha256")
        if not isinstance(gate_sha, str) or completion.get("gate_sha256") != gate_sha:
            continue
        for item in completion.get("passes", []):
            if not isinstance(item, dict) or item.get("status") != "complete":
                continue
            pass_id = require_string(item.get("pass_id"), f"{stage}.pass_id")
            unit_id = require_string(item.get("execution_unit_id"), f"{stage}:{pass_id}.execution_unit_id")
            boundary = item.get("boundary")
            if not isinstance(boundary, dict):
                raise ValueError(f"{stage}:{pass_id}.boundary must be an object")
            kind = require_string(boundary.get("kind"), f"{stage}:{pass_id}.boundary.kind")
            boundary_id = require_string(boundary.get("id"), f"{stage}:{pass_id}.boundary.id")
            occurrence = (revision, stage, pass_id, gate_sha)
            occurrences.append((occurrence, unit_id, (kind, boundary_id), canonical_text(item)))
    return occurrences


def validate_identity_history_snapshots(record_id: str, snapshots: list[tuple[str, dict[str, Any]]]) -> None:
    occurrence_evidence: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}
    logical_slots: dict[tuple[Any, ...], tuple[Any, ...]] = {}
    stage_gates: dict[tuple[Any, ...], str] = {}
    used_units: dict[str, tuple[Any, ...]] = {}
    used_boundaries: dict[tuple[str, str], tuple[Any, ...]] = {}

    for commit_sha, snapshot in snapshots:
        for occurrence, unit_id, boundary, evidence in completed_occurrences(snapshot):
            prior = occurrence_evidence.get(occurrence)
            if prior is not None:
                if prior != (unit_id, boundary, evidence):
                    raise ValueError(
                        f"record {record_id!r} mutates completed pass evidence for {occurrence!r} at {commit_sha!r}"
                    )
                continue

            revision, stage, pass_id, gate_sha = occurrence
            stage_slot = (revision, stage)
            previous_gate = stage_gates.get(stage_slot)
            if previous_gate is not None and previous_gate != gate_sha:
                raise ValueError(
                    f"record {record_id!r} replaces the completed stage gate for {stage_slot!r} at {commit_sha!r}; "
                    f"increment review_revision before changing a stage gate or execution plan after durable completion"
                )

            logical_slot = (revision, stage, pass_id)
            previous_occurrence = logical_slots.get(logical_slot)
            if previous_occurrence is not None and previous_occurrence != occurrence:
                raise ValueError(
                    f"record {record_id!r} replaces completed logical pass {logical_slot!r} with a different gate "
                    f"at {commit_sha!r}; increment review_revision before redoing a durably completed pass"
                )

            previous = used_units.get(unit_id)
            if previous is not None and previous != occurrence:
                raise ValueError(
                    f"record {record_id!r} reuses execution_unit_id {unit_id!r} for {occurrence!r}; "
                    f"it was already used by {previous!r}"
                )
            previous_boundary = used_boundaries.get(boundary)
            if previous_boundary is not None and previous_boundary != occurrence:
                raise ValueError(
                    f"record {record_id!r} reuses execution boundary {boundary!r} for {occurrence!r}; "
                    f"it was already used by {previous_boundary!r}"
                )
            occurrence_evidence[occurrence] = (unit_id, boundary, evidence)
            stage_gates[stage_slot] = gate_sha
            logical_slots[logical_slot] = occurrence
            used_units[unit_id] = occurrence
            used_boundaries[boundary] = occurrence


def changed_record_ids(base: str, head: str) -> set[str]:
    try:
        output = subprocess.run(
            ["git", "diff", "--name-only", base, head, "--", CHANGES_PREFIX.rstrip("/")],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("cannot determine change records modified in the current review range") from exc
    ids: set[str] = set()
    for raw in output.splitlines():
        path = raw.strip().replace("\\", "/")
        if path.startswith(CHANGES_PREFIX) and path.endswith(".json"):
            ids.add(path[len(CHANGES_PREFIX):-5])
    return ids


def snapshot_at_ref(record_id: str, ref: str) -> dict[str, Any] | None:
    path = f"{CHANGES_PREFIX}{record_id}.json"
    try:
        raw = subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"change record {record_id!r} at {ref!r} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"change record {record_id!r} at {ref!r} must contain an object")
    return value


def load_pr_history(record_id: str, base: str, head: str) -> list[tuple[str, dict[str, Any]]]:
    path = f"{CHANGES_PREFIX}{record_id}.json"
    snapshots: list[tuple[str, dict[str, Any]]] = []

    base_snapshot = snapshot_at_ref(record_id, base)
    if base_snapshot is not None:
        snapshots.append((base, base_snapshot))

    try:
        log = subprocess.run(
            ["git", "log", "--format=%H", "--reverse", f"{base}..{head}", "--", path],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot read PR history for {record_id!r}") from exc

    for sha in [line.strip() for line in log.splitlines() if line.strip()]:
        snapshot = snapshot_at_ref(record_id, sha)
        if snapshot is not None:
            snapshots.append((sha, snapshot))
    return snapshots


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    try:
        mapping = load_json(args.map)
        policy = mapping.get("pass_boundary", {})
        exemptions = set(policy.get("legacy_exempt_change_ids", [])) if isinstance(policy, dict) else set()
        for record_id in sorted(changed_record_ids(args.base, args.head)):
            if record_id in exemptions:
                continue
            snapshots = load_pr_history(record_id, args.base, args.head)
            validate_identity_history_snapshots(record_id, snapshots)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print("Completed execution evidence is historically unique and immutable across review occurrences.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
