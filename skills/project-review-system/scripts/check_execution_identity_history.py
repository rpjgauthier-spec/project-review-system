#!/usr/bin/env python3
"""Reject reuse or mutation of execution evidence across review history.

Completed execution occurrences are tracked by review revision, stage, planned
pass_id, and gate hash. Once an occurrence receives durable completion evidence,
its execution identity and complete pass evidence are immutable. A stage/revision
is also bound to one gate after any pass completes, so changing the gate or plan
requires a new review revision.

PR commit history alone is not durable across squash/rebase merges. Therefore a
change record may carry `execution_occurrence_history`, an append-only ledger of
completed occurrences. The final PR state must preserve every completed occurrence
observed in the PR history. Future PR base snapshots then retain those identities
even when the original unsquashed commits are no longer reachable from main.
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
CHANGES_PREFIX = "skills/project-review-system/changes/"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()


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
            occurrences.append((occurrence, unit_id, (kind, boundary_id), canonical_sha256(item)))
    return occurrences


def ledger_occurrences(snapshot: dict[str, Any]) -> dict[tuple[Any, ...], tuple[str, tuple[str, str], str]]:
    raw = snapshot.get("execution_occurrence_history", [])
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise ValueError("execution_occurrence_history must be an array")

    entries: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"execution_occurrence_history[{index}] must be an object")
        revision = item.get("review_revision")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
            raise ValueError(f"execution_occurrence_history[{index}].review_revision must be a nonnegative integer")
        stage = require_string(item.get("stage"), f"execution_occurrence_history[{index}].stage")
        pass_id = require_string(item.get("pass_id"), f"execution_occurrence_history[{index}].pass_id")
        gate_sha = require_string(item.get("gate_sha256"), f"execution_occurrence_history[{index}].gate_sha256")
        unit_id = require_string(item.get("execution_unit_id"), f"execution_occurrence_history[{index}].execution_unit_id")
        boundary = item.get("boundary")
        if not isinstance(boundary, dict):
            raise ValueError(f"execution_occurrence_history[{index}].boundary must be an object")
        kind = require_string(boundary.get("kind"), f"execution_occurrence_history[{index}].boundary.kind")
        boundary_id = require_string(boundary.get("id"), f"execution_occurrence_history[{index}].boundary.id")
        evidence_sha = require_string(item.get("pass_evidence_sha256"), f"execution_occurrence_history[{index}].pass_evidence_sha256")
        if len(evidence_sha) != 64 or any(c not in "0123456789abcdef" for c in evidence_sha.lower()):
            raise ValueError(f"execution_occurrence_history[{index}].pass_evidence_sha256 must be a SHA-256 hex digest")
        occurrence = (revision, stage, pass_id, gate_sha)
        value = (unit_id, (kind, boundary_id), evidence_sha.lower())
        previous = entries.get(occurrence)
        if previous is not None and previous != value:
            raise ValueError(f"execution_occurrence_history contains conflicting entries for {occurrence!r}")
        entries[occurrence] = value
    return entries


def validate_identity_history_snapshots(record_id: str, snapshots: list[tuple[str, dict[str, Any]]]) -> None:
    occurrence_evidence: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}
    logical_slots: dict[tuple[Any, ...], tuple[Any, ...]] = {}
    stage_gates: dict[tuple[Any, ...], str] = {}
    used_units: dict[str, tuple[Any, ...]] = {}
    used_boundaries: dict[tuple[str, str], tuple[Any, ...]] = {}
    observed_completed: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}
    previous_ledger: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}
    final_ledger: dict[tuple[Any, ...], tuple[str, tuple[str, str], str]] = {}

    def register(occurrence: tuple[Any, ...], unit_id: str, boundary: tuple[str, str], evidence_sha: str, where: str) -> None:
        prior = occurrence_evidence.get(occurrence)
        if prior is not None:
            if prior != (unit_id, boundary, evidence_sha):
                raise ValueError(f"record {record_id!r} mutates completed pass evidence for {occurrence!r} at {where!r}")
            return

        logical_slot = occurrence[:3]
        previous_occurrence = logical_slots.get(logical_slot)
        if previous_occurrence is not None and previous_occurrence != occurrence:
            raise ValueError(
                f"record {record_id!r} replaces completed logical pass {logical_slot!r} with a different gate "
                f"at {where!r}; increment review_revision before redoing a durably completed pass"
            )

        stage_slot = occurrence[:2]
        gate_sha = occurrence[3]
        previous_gate = stage_gates.get(stage_slot)
        if previous_gate is not None and previous_gate != gate_sha:
            raise ValueError(
                f"record {record_id!r} changes completed stage gate for {stage_slot!r} from {previous_gate!r} "
                f"to {gate_sha!r} at {where!r}; increment review_revision before changing the stage gate or execution plan"
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
        occurrence_evidence[occurrence] = (unit_id, boundary, evidence_sha)
        logical_slots[logical_slot] = occurrence
        stage_gates[stage_slot] = gate_sha
        used_units[unit_id] = occurrence
        used_boundaries[boundary] = occurrence

    for commit_sha, snapshot in snapshots:
        ledger = ledger_occurrences(snapshot)
        for occurrence, prior_value in previous_ledger.items():
            if ledger.get(occurrence) != prior_value:
                raise ValueError(
                    f"record {record_id!r} removes or mutates durable execution occurrence ledger entry "
                    f"{occurrence!r} at {commit_sha!r}"
                )
        for occurrence, (unit_id, boundary, evidence_sha) in ledger.items():
            register(occurrence, unit_id, boundary, evidence_sha, commit_sha)

        for occurrence, unit_id, boundary, evidence_sha in completed_occurrences(snapshot):
            register(occurrence, unit_id, boundary, evidence_sha, commit_sha)
            prior_observed = observed_completed.get(occurrence)
            if prior_observed is not None and prior_observed != (unit_id, boundary, evidence_sha):
                raise ValueError(f"record {record_id!r} mutates observed completion {occurrence!r} at {commit_sha!r}")
            observed_completed[occurrence] = (unit_id, boundary, evidence_sha)

        previous_ledger = ledger
        final_ledger = ledger

    for occurrence, value in observed_completed.items():
        if final_ledger.get(occurrence) != value:
            raise ValueError(
                f"record {record_id!r} does not preserve completed occurrence {occurrence!r} in final "
                "execution_occurrence_history; PR commit history may disappear after squash/rebase merge"
            )


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
    print("Completed execution evidence and its durable occurrence ledger are historically unique and immutable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
