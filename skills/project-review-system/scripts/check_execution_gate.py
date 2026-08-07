#!/usr/bin/env python3
"""Validate Adaptive Execution gates and deterministic execution completion."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
SELECTOR_PATH = ROOT / "scripts" / "select_execution_policy.py"


def _load_selector():
    spec = importlib.util.spec_from_file_location("select_execution_policy_for_gate", SELECTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load select_execution_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SELECTOR = _load_selector()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def normalize_repository_path(raw_path: str) -> str:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("artifact-state paths must be nonempty strings")
    normalized = raw_path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized or normalized.startswith("/") or normalized == ".." or normalized.startswith("../") or "/../" in normalized:
        raise ValueError(f"invalid repository-relative artifact path: {raw_path!r}")
    return normalized


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def repository_artifact_state_from_blob_ids(path_to_blob_id: dict[str, str | None]) -> str:
    digest = hashlib.sha256()
    normalized_items: list[tuple[str, str | None]] = []
    for raw_path, blob_id in path_to_blob_id.items():
        normalized = normalize_repository_path(raw_path)
        if blob_id is not None:
            if not isinstance(blob_id, str) or len(blob_id) != 40 or any(c not in "0123456789abcdef" for c in blob_id.lower()):
                raise ValueError(f"invalid Git blob id for {normalized}")
            blob_id = blob_id.lower()
        normalized_items.append((normalized, blob_id))
    for normalized, blob_id in sorted(normalized_items):
        digest.update(normalized.encode("utf-8"))
        digest.update(b"\0")
        if blob_id is None:
            digest.update(b"ABSENT\0")
        else:
            digest.update(b"BLOB\0")
            digest.update(blob_id.encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def repository_artifact_state_sha256(repository_relative_paths: Iterable[str], repository_root: Path = REPOSITORY_ROOT) -> str:
    root = repository_root.resolve()
    states: dict[str, str | None] = {}
    for raw_path in repository_relative_paths:
        normalized = normalize_repository_path(raw_path)
        target = (root / normalized).resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"artifact path escapes repository root: {normalized!r}") from exc
        if target.exists():
            if not target.is_file():
                raise ValueError(f"artifact-state path is not a file: {normalized}")
            states[normalized] = git_blob_sha1(target.read_bytes())
        else:
            states[normalized] = None
    return repository_artifact_state_from_blob_ids(states)


def validate_execution_gate(
    gate: dict[str, Any],
    expected_activity: str,
    expected_review_revision: int,
    expected_target_state_id: str | None = None,
) -> dict[str, Any]:
    if isinstance(expected_review_revision, bool) or not isinstance(expected_review_revision, int) or expected_review_revision < 0:
        raise ValueError("expected_review_revision must be a nonnegative integer")
    decision = SELECTOR.validate_gate(gate, expected_activity=expected_activity)
    workload = gate["workload"]
    revision = workload.get("review_revision")
    if revision != expected_review_revision:
        raise ValueError(f"execution gate review_revision {revision} does not match current review revision {expected_review_revision}")
    if expected_target_state_id is not None and workload.get("target_state_id") != expected_target_state_id:
        raise ValueError("execution gate target_state_id does not match current governed artifact state")
    return decision


def validate_execution_completion(completion: dict[str, Any], gate: dict[str, Any], decision: dict[str, Any] | None = None) -> None:
    """Require recorded completed passes to match the gate's execution plan exactly."""
    if not isinstance(completion, dict):
        raise ValueError("execution completion must be an object")
    if decision is None:
        decision = SELECTOR.validate_gate(gate)
    if completion.get("gate_sha256") != gate.get("gate_sha256"):
        raise ValueError("execution completion does not reference the current gate hash")
    if completion.get("target_state_id") != decision.get("target_state_id"):
        raise ValueError("execution completion target_state_id does not match the execution plan")
    passes = completion.get("passes")
    if not isinstance(passes, list):
        raise ValueError("execution completion passes must be an array")
    expected = decision.get("execution_plan")
    if not isinstance(expected, list):
        raise ValueError("execution decision has no execution_plan")
    if len(passes) != len(expected):
        raise ValueError("execution completion pass count does not match the required execution plan")
    for index, (actual, required) in enumerate(zip(passes, expected)):
        if not isinstance(actual, dict):
            raise ValueError(f"execution completion passes[{index}] must be an object")
        if actual.get("pass_id") != required.get("pass_id"):
            raise ValueError(f"execution completion pass {index} has wrong pass_id")
        if actual.get("context_mode") != required.get("context_mode"):
            raise ValueError(f"execution completion pass {required.get('pass_id')!r} used wrong context mode")
        if actual.get("status") != "complete":
            raise ValueError(f"execution completion pass {required.get('pass_id')!r} is not complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--activity", required=True)
    parser.add_argument("--review-revision", type=int, required=True)
    parser.add_argument("--target-state-id")
    parser.add_argument("--completion", type=Path)
    args = parser.parse_args()
    try:
        gate = load_json(args.gate)
        decision = validate_execution_gate(gate, args.activity, args.review_revision, expected_target_state_id=args.target_state_id)
        if args.completion:
            validate_execution_completion(load_json(args.completion), gate, decision)
    except (OSError, json.JSONDecodeError, ValueError, TypeError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    suffix = " with matching completion" if args.completion else ""
    print(f"Execution gate valid for {args.activity}: {decision['selected_mode']} / {decision['plan_kind']}{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
