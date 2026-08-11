#!/usr/bin/env python3
"""Validate Adaptive Execution gates and deterministic execution completion."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import posixpath
import re
import stat
import subprocess
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
SELECTOR_PATH = ROOT / "scripts" / "select_execution_policy.py"
REGULAR_FILE_MODES = {"100644", "100755"}
OBJECT_ID_LENGTHS = {40, 64}
WINDOWS_DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")
UNSUPPORTED_CONTENT_ATTRIBUTES = ("filter", "ident", "working-tree-encoding")


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
    if "\x00" in raw_path:
        raise ValueError("artifact-state paths must not contain NUL bytes")
    normalized = raw_path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized or normalized.startswith("/") or WINDOWS_DRIVE_PREFIX.match(normalized):
        raise ValueError(f"invalid repository-relative artifact path: {raw_path!r}")
    if any(part == ".." for part in normalized.split("/")):
        raise ValueError(f"invalid repository-relative artifact path: {raw_path!r}")
    normalized = posixpath.normpath(normalized)
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        raise ValueError(f"invalid repository-relative artifact path: {raw_path!r}")
    return normalized


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _valid_object_id(value: str) -> bool:
    return (
        isinstance(value, str)
        and len(value) in OBJECT_ID_LENGTHS
        and all(c in "0123456789abcdef" for c in value.lower())
    )


def _sanitized_git_environment() -> dict[str, str]:
    """Remove caller-controlled Git routing overrides and disable replace refs."""
    environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _run_git(repository_root: Path, args: list[str], purpose: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
            env=_sanitized_git_environment(),
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot {purpose}: {exc}") from exc
    return completed.stdout


def _verified_repository_root(repository_root: Path) -> Path:
    root = repository_root.resolve()
    reported = _run_git(root, ["rev-parse", "--show-toplevel"], f"verify Git repository root {root}").strip()
    if not reported:
        raise RuntimeError(f"Git did not report a repository root for {root}")
    actual_root = Path(reported).resolve()
    if actual_root != root:
        raise RuntimeError(f"artifact-state repository root {root} is not the Git toplevel {actual_root}")
    return root


def _parse_head_entry(repository_root: Path, normalized_path: str) -> tuple[str, str] | None:
    output = _run_git(
        repository_root,
        ["ls-tree", "-z", "HEAD", "--", f":(literal){normalized_path}"],
        f"read committed Git entry for {normalized_path!r}",
    )
    entries = [entry for entry in output.split("\0") if entry]
    if not entries:
        return None
    if len(entries) != 1 or "\t" not in entries[0]:
        raise RuntimeError(f"Git returned ambiguous committed entry data for {normalized_path!r}")
    metadata, returned_path = entries[0].split("\t", 1)
    if returned_path != normalized_path:
        raise RuntimeError(f"Git returned noncanonical committed path for {normalized_path!r}")
    parts = metadata.split()
    if len(parts) != 3:
        raise RuntimeError(f"Git returned malformed committed entry data for {normalized_path!r}")
    mode, object_type, object_id = parts
    object_id = object_id.lower()
    if object_type != "blob" or mode not in REGULAR_FILE_MODES:
        raise ValueError(f"artifact-state path is not a supported regular Git file: {normalized_path}")
    if not _valid_object_id(object_id):
        raise RuntimeError(f"Git returned an invalid object id for {normalized_path!r}")
    return mode, object_id


def _parse_index_entry(repository_root: Path, normalized_path: str) -> tuple[str, str] | None:
    output = _run_git(
        repository_root,
        ["ls-files", "--stage", "-z", "--", f":(literal){normalized_path}"],
        f"read Git index entry for {normalized_path!r}",
    )
    entries = [entry for entry in output.split("\0") if entry]
    if not entries:
        return None
    if len(entries) != 1 or "\t" not in entries[0]:
        raise ValueError(f"artifact-state path has conflicted or ambiguous index state: {normalized_path}")
    metadata, returned_path = entries[0].split("\t", 1)
    if returned_path != normalized_path:
        raise RuntimeError(f"Git returned noncanonical index path for {normalized_path!r}")
    parts = metadata.split()
    if len(parts) != 3:
        raise RuntimeError(f"Git returned malformed index data for {normalized_path!r}")
    mode, object_id, stage_number = parts
    object_id = object_id.lower()
    if stage_number != "0" or mode not in REGULAR_FILE_MODES or not _valid_object_id(object_id):
        raise ValueError(f"artifact-state path has unsupported index state: {normalized_path}")
    return mode, object_id


def _content_transform_attributes(repository_root: Path, normalized_path: str) -> dict[str, str]:
    output = _run_git(
        repository_root,
        ["check-attr", "-z", *UNSUPPORTED_CONTENT_ATTRIBUTES, "--", normalized_path],
        f"read Git content-transform attributes for {normalized_path!r}",
    )
    parts = output.split("\0")
    if parts and parts[-1] == "":
        parts.pop()
    expected_count = len(UNSUPPORTED_CONTENT_ATTRIBUTES) * 3
    if len(parts) != expected_count:
        raise RuntimeError(f"Git returned malformed attribute data for {normalized_path!r}")
    attributes: dict[str, str] = {}
    for index in range(0, len(parts), 3):
        returned_path, attribute, value = parts[index:index + 3]
        if returned_path != normalized_path or attribute not in UNSUPPORTED_CONTENT_ATTRIBUTES:
            raise RuntimeError(f"Git returned malformed attribute data for {normalized_path!r}")
        attributes[attribute] = value
    if set(attributes) != set(UNSUPPORTED_CONTENT_ATTRIBUTES):
        raise RuntimeError(f"Git omitted content-transform attribute data for {normalized_path!r}")
    return attributes


def _reject_unsupported_content_transforms(repository_root: Path, normalized_path: str) -> None:
    attributes = _content_transform_attributes(repository_root, normalized_path)
    active = {
        name: value
        for name, value in attributes.items()
        if value not in {"unspecified", "unset"}
    }
    if active:
        rendered = ", ".join(f"{name}={value}" for name, value in sorted(active.items()))
        raise ValueError(
            f"governed artifact uses unsupported Git content transformation(s) and cannot receive review credit: "
            f"{normalized_path} ({rendered})"
        )


def _reject_symlink_components(repository_root: Path, normalized_path: str) -> Path:
    candidate = repository_root
    for part in normalized_path.split("/"):
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError(f"artifact-state path must not traverse a symlink: {normalized_path}")
    target = candidate.resolve()
    try:
        target.relative_to(repository_root)
    except ValueError as exc:
        raise ValueError(f"artifact path escapes repository root: {normalized_path!r}") from exc
    return candidate


def git_worktree_blob_id(repository_root: Path, normalized_path: str) -> str:
    """Hash current regular-file content using only supported Git path conversions."""
    blob_id = _run_git(
        repository_root,
        ["hash-object", f"--path={normalized_path}", "--", normalized_path],
        f"derive Git blob identity for {normalized_path!r}",
    ).strip().lower()
    if not _valid_object_id(blob_id):
        raise RuntimeError(f"Git returned an invalid blob id for {normalized_path!r}")
    return blob_id


def repository_artifact_state_from_blob_ids(path_to_blob_id: dict[str, str | None]) -> str:
    """Legacy blob-only state helper retained for historical fixtures and callers."""
    digest = hashlib.sha256()
    normalized_items: list[tuple[str, str | None]] = []
    for raw_path, blob_id in path_to_blob_id.items():
        normalized = normalize_repository_path(raw_path)
        if blob_id is not None:
            if not _valid_object_id(blob_id):
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


def repository_artifact_state_from_git_entries(
    path_to_entry: dict[str, tuple[str, str] | None],
) -> str:
    digest = hashlib.sha256()
    normalized_items: list[tuple[str, tuple[str, str] | None]] = []
    for raw_path, entry in path_to_entry.items():
        normalized = normalize_repository_path(raw_path)
        if entry is not None:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise ValueError(f"invalid Git entry for {normalized}")
            mode, object_id = entry
            if mode not in REGULAR_FILE_MODES or not _valid_object_id(object_id):
                raise ValueError(f"invalid Git entry for {normalized}")
            entry = (mode, object_id.lower())
        normalized_items.append((normalized, entry))
    for normalized, entry in sorted(normalized_items):
        digest.update(normalized.encode("utf-8"))
        digest.update(b"\0")
        if entry is None:
            digest.update(b"ABSENT\0")
        else:
            mode, object_id = entry
            digest.update(b"MODE\0")
            digest.update(mode.encode("ascii"))
            digest.update(b"\0BLOB\0")
            digest.update(object_id.encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def repository_artifact_state_sha256(repository_relative_paths: Iterable[str], repository_root: Path = REPOSITORY_ROOT) -> str:
    root = _verified_repository_root(repository_root)
    states: dict[str, tuple[str, str] | None] = {}
    for raw_path in repository_relative_paths:
        normalized = normalize_repository_path(raw_path)
        candidate = _reject_symlink_components(root, normalized)
        head_entry = _parse_head_entry(root, normalized)
        index_entry = _parse_index_entry(root, normalized)

        if head_entry is None:
            if index_entry is not None:
                raise ValueError(f"governed artifact index state does not match HEAD: {normalized}")
            if os.path.lexists(candidate):
                raise ValueError(f"untracked governed artifact cannot receive review credit: {normalized}")
            states[normalized] = None
            continue

        if index_entry != head_entry:
            raise ValueError(f"governed artifact index state does not match HEAD: {normalized}")
        if not candidate.exists() or not candidate.is_file():
            raise ValueError(f"committed governed artifact is missing from the worktree: {normalized}")

        _reject_unsupported_content_transforms(root, normalized)

        mode, committed_blob_id = head_entry
        current_blob_id = git_worktree_blob_id(root, normalized)
        if current_blob_id != committed_blob_id:
            raise ValueError(f"governed artifact worktree content does not match committed Git content: {normalized}")

        if os.name != "nt":
            actual_executable = bool(candidate.stat().st_mode & stat.S_IXUSR)
            expected_executable = mode == "100755"
            if actual_executable != expected_executable:
                raise ValueError(f"governed artifact worktree mode does not match committed Git mode: {normalized}")

        states[normalized] = head_entry
    return repository_artifact_state_from_git_entries(states)


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


def validate_cleanup_record(completion: dict[str, Any]) -> None:
    """Require scratch-work cleanup or explicit justified durable retention."""
    scratch_materialized = completion.get("scratch_materialized")
    if not isinstance(scratch_materialized, bool):
        raise ValueError("execution completion scratch_materialized must be boolean")

    cleanup_status = completion.get("scratch_cleanup_status")
    if scratch_materialized:
        if cleanup_status != "complete":
            raise ValueError("materialized scratch workspace must be deleted before completion is accepted")
    elif cleanup_status != "not_applicable":
        raise ValueError("non-materialized scratch workspace must use cleanup status not_applicable")

    retained = completion.get("retained_subpass_artifacts", [])
    if not isinstance(retained, list):
        raise ValueError("retained_subpass_artifacts must be an array")
    for index, item in enumerate(retained):
        if not isinstance(item, dict):
            raise ValueError(f"retained_subpass_artifacts[{index}] must be an object")
        artifact = item.get("artifact")
        consumer = item.get("consumer")
        reason = item.get("reason")
        if not isinstance(artifact, str) or not artifact.strip():
            raise ValueError(f"retained_subpass_artifacts[{index}].artifact is required")
        if not isinstance(consumer, str) or not consumer.strip():
            raise ValueError(f"retained_subpass_artifacts[{index}].consumer is required")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"retained_subpass_artifacts[{index}].reason is required")


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
    validate_cleanup_record(completion)


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
