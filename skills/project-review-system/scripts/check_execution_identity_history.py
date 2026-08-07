#!/usr/bin/env python3
"""Reject reuse of execution-unit or boundary identities across review history.

Each completed execution occurrence is identified by review revision, stage,
planned pass_id, and gate hash. When an occurrence first appears in the durable
change-record history, its execution_unit_id and boundary identity must never
have been used by an earlier occurrence. This applies equally to ordinary stage
passes, subdivided subpasses, and reopened/redo executions.

For a PR-scoped check, the history begins with the base-state snapshot when the
change record already exists there, followed by change-record commits in
base..head. Including the base snapshot is required to reject identity reuse by
a reopened change in a later PR.
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
PASS_RESULTS = {"passed", "supported", "complete"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a nonempty string")
    return value.strip()


def credited_occurrences(snapshot: dict[str, Any]) -> list[tuple[tuple[Any, ...], str, tuple[str, str]]]:
    revision = snapshot.get("review_revision")
    results = snapshot.get("results", {})
    gates = snapshot.get("execution_gates", {})
    completions = snapshot.get("execution_completions", {})
    if not isinstance(results, dict) or not isinstance(gates, dict) or not isinstance(completions, dict):
        return []

    occurrences: list[tuple[tuple[Any, ...], str, tuple[str, str]]] = []
    for stage, result in results.items():
        if result not in PASS_RESULTS:
            continue
        gate = gates.get(stage)
        completion = completions.get(stage)
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
            occurrences.append((occurrence, unit_id, (kind, boundary_id)))
    return occurrences


def validate_identity_history_snapshots(record_id: str, snapshots: list[tuple[str, dict[str, Any]]]) -> None:
    seen_occurrences: set[tuple[Any, ...]] = set()
    used_units: dict[str, tuple[Any, ...]] = {}
    used_boundaries: dict[tuple[str, str], tuple[Any, ...]] = {}

    for commit_sha, snapshot in snapshots:
        for occurrence, unit_id, boundary in credited_occurrences(snapshot):
            if occurrence in seen_occurrences:
                continue
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
            seen_occurrences.add(occurrence)
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
    print("Historical execution-unit and boundary identities are unique across review occurrences.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
