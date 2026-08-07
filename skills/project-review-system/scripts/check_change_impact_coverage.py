#!/usr/bin/env python3
"""Verify that every changed Project Review System file is declared in a changed impact record.

The checker compares two git refs, identifies watched files, identifies impact
records added or modified in the same diff, and requires those records to cover
every watched change. Existing impact records may retain historical file claims
when they are updated later for results or status; stale claims are rejected for
newly added impact records. The checker does not decide whether classifications
are truthful; that remains a semantic review responsibility.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

SKILL_PREFIX = "skills/project-review-system/"
CHANGE_PREFIX = SKILL_PREFIX + "changes/"
WORKFLOW_PATH = ".github/workflows/project-review-system-revalidation.yml"
WATCHED_PREFIXES = (SKILL_PREFIX,)
WATCHED_EXACT = {WORKFLOW_PATH}


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def changed_files(base: str, head: str) -> set[str]:
    return set(git_lines("diff", "--name-only", "--diff-filter=ACMRD", base, head, "--"))


def existed_at_ref(ref: str, path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def is_watched(path: str) -> bool:
    return path in WATCHED_EXACT or path.startswith(WATCHED_PREFIXES)


def normalize_declared(path: str) -> str:
    clean = path.strip().lstrip("./")
    if clean.startswith(SKILL_PREFIX) or clean.startswith(".github/"):
        return clean
    return SKILL_PREFIX + clean


def load_changed_records(paths: set[str]) -> list[tuple[str, dict]]:
    records: list[tuple[str, dict]] = []
    for path in sorted(paths):
        if not path.startswith(CHANGE_PREFIX) or not path.endswith(".json"):
            continue
        file_path = Path(path)
        if not file_path.exists():
            raise ValueError(f"changed impact record was deleted: {path}")
        try:
            record = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read impact record {path}: {exc}") from exc
        declared = record.get("changed_files")
        if not isinstance(declared, list) or not declared:
            raise ValueError(f"impact record {path} must contain a non-empty changed_files list")
        records.append((path, record))
    return records


def validate(base: str, head: str) -> list[str]:
    errors: list[str] = []
    changed = changed_files(base, head)
    watched = {path for path in changed if is_watched(path)}
    if not watched:
        return []

    try:
        records = load_changed_records(changed)
    except ValueError as exc:
        return [str(exc)]

    if not records:
        return [
            "Project Review System files changed, but no impact record was added or updated in the same diff."
        ]

    covered: dict[str, set[str]] = {}
    for record_path, record in records:
        for declared in record["changed_files"]:
            normalized = normalize_declared(str(declared))
            covered.setdefault(normalized, set()).add(record_path)

    missing = sorted(watched - covered.keys())
    if missing:
        errors.append("Unrecorded changed files: " + ", ".join(missing))

    record_paths = {record_path for record_path, _ in records}
    for record_path, record in records:
        normalized_declared = {normalize_declared(str(p)) for p in record["changed_files"]}
        if record_path not in normalized_declared:
            errors.append(f"Impact record must list itself in changed_files: {record_path}")

    new_record_paths = {
        record_path for record_path, _ in records if not existed_at_ref(base, record_path)
    }
    stale_claims = sorted(
        path
        for path, claimers in covered.items()
        if path not in watched
        and path not in record_paths
        and any(record_path in new_record_paths for record_path in claimers)
    )
    if stale_claims:
        errors.append(
            "New impact records claim files not present in this diff: " + ", ".join(stale_claims)
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base git ref or SHA")
    parser.add_argument("--head", required=True, help="Head git ref or SHA")
    args = parser.parse_args()

    try:
        errors = validate(args.base, args.head)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Every changed Project Review System file is covered by a changed impact record.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
