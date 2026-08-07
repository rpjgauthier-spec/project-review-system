#!/usr/bin/env python3
"""Validate a recorded Adaptive Execution gate for one semantic activity."""

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


def repository_artifact_state_sha256(
    repository_relative_paths: Iterable[str], repository_root: Path = REPOSITORY_ROOT
) -> str:
    """Hash exact repository artifact state, including intentional absence.

    The aggregate binds both path and current bytes. Missing paths are represented
    explicitly so deletion can be a stable reviewed state. Directories are not
    accepted because change-impact records enumerate files.
    """
    root = repository_root.resolve()
    digest = hashlib.sha256()
    for raw_path in sorted(set(repository_relative_paths)):
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError("artifact-state paths must be nonempty strings")
        normalized = raw_path.replace("\\", "/").lstrip("./")
        if not normalized or normalized.startswith("../") or "/../" in normalized:
            raise ValueError(f"invalid repository-relative artifact path: {raw_path!r}")
        target = (root / normalized).resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"artifact path escapes repository root: {raw_path!r}") from exc

        digest.update(normalized.encode("utf-8"))
        digest.update(b"\0")
        if target.exists():
            if not target.is_file():
                raise ValueError(f"artifact-state path is not a file: {normalized}")
            data = target.read_bytes()
            digest.update(b"FILE\0")
            digest.update(str(len(data)).encode("ascii"))
            digest.update(b"\0")
            digest.update(data)
        else:
            digest.update(b"ABSENT\0")
        digest.update(b"\0")
    return digest.hexdigest()


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
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError("execution gate workload.review_revision must be a nonnegative integer")
    if revision != expected_review_revision:
        raise ValueError(
            f"execution gate review_revision {revision} does not match current review revision {expected_review_revision}"
        )
    if expected_target_state_id is not None:
        actual_target = workload.get("target_state_id")
        if actual_target != expected_target_state_id:
            raise ValueError(
                "execution gate target_state_id does not match current governed artifact state"
            )
    if workload.get("remaining_stage_count", 0) < 1 and expected_activity != "Identity Pass":
        raise ValueError("execution gate for a review stage must include that stage in remaining_stage_count")
    return decision


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--activity", required=True)
    parser.add_argument("--review-revision", type=int, required=True)
    parser.add_argument("--target-state-id")
    args = parser.parse_args()

    try:
        gate = load_json(args.gate)
        decision = validate_execution_gate(
            gate,
            args.activity,
            args.review_revision,
            expected_target_state_id=args.target_state_id,
        )
    except (OSError, json.JSONDecodeError, ValueError, TypeError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print(
        f"Execution gate valid for {args.activity}: {decision['selected_mode']} "
        f"at review revision {args.review_revision}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
