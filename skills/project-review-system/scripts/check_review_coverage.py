#!/usr/bin/env python3
"""Verify exhaustive semantic-review coverage against a pinned manifest.

A passing result means every manifest entry has a matching COMPLETE semantic
coverage record whose ranges cover the entire declared unit range. It does not
prove comprehension, semantic correctness, or reviewer independence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VALID_STATUS = "COMPLETE"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def covered_fully(total: int, ranges: list[list[int]]) -> tuple[bool, str | None]:
    if total < 0:
        return False, "coverage_total cannot be negative"
    if total == 0:
        if ranges:
            return False, "zero-length object must use an empty ranges list"
        return True, None

    normalized: list[tuple[int, int]] = []
    for item in ranges:
        if not isinstance(item, list) or len(item) != 2:
            return False, f"invalid range {item!r}"
        start, end = item
        if not isinstance(start, int) or not isinstance(end, int):
            return False, f"range endpoints must be integers: {item!r}"
        if start < 1 or end < start or end > total:
            return False, f"range outside 1..{total}: {item!r}"
        normalized.append((start, end))

    normalized.sort()
    cursor = 1
    for start, end in normalized:
        if start > cursor:
            return False, f"missing coverage range {cursor}..{start - 1}"
        if end >= cursor:
            cursor = end + 1
        if cursor > total:
            break
    if cursor <= total:
        return False, f"missing coverage range {cursor}..{total}"
    return True, None


def validate(manifest: dict[str, Any], coverage: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if manifest.get("schema_version") != 1:
        errors.append("Unsupported manifest schema_version.")
    if coverage.get("schema_version") != 1:
        errors.append("Unsupported coverage schema_version.")

    expected_commit = manifest.get("resolved_commit")
    if coverage.get("resolved_commit") != expected_commit:
        errors.append("Coverage resolved_commit does not match the manifest.")

    manifest_entries = manifest.get("entries")
    coverage_entries = coverage.get("entries")
    if not isinstance(manifest_entries, list):
        errors.append("Manifest entries must be a list.")
        return errors
    if not isinstance(coverage_entries, list):
        errors.append("Coverage entries must be a list.")
        return errors

    manifest_by_path: dict[str, dict[str, Any]] = {}
    for entry in manifest_entries:
        path = entry.get("path") if isinstance(entry, dict) else None
        if not isinstance(path, str) or not path:
            errors.append("Manifest contains an entry without a valid path.")
            continue
        if path in manifest_by_path:
            errors.append(f"Manifest contains duplicate path: {path}")
        manifest_by_path[path] = entry

    coverage_by_path: dict[str, dict[str, Any]] = {}
    for entry in coverage_entries:
        path = entry.get("path") if isinstance(entry, dict) else None
        if not isinstance(path, str) or not path:
            errors.append("Coverage contains an entry without a valid path.")
            continue
        if path in coverage_by_path:
            errors.append(f"Coverage contains duplicate path: {path}")
        coverage_by_path[path] = entry

    missing = sorted(set(manifest_by_path) - set(coverage_by_path))
    extras = sorted(set(coverage_by_path) - set(manifest_by_path))
    if missing:
        errors.append("Missing coverage entries: " + ", ".join(missing))
    if extras:
        errors.append("Coverage contains paths absent from manifest: " + ", ".join(extras))

    for path in sorted(set(manifest_by_path) & set(coverage_by_path)):
        expected = manifest_by_path[path]
        actual = coverage_by_path[path]

        if actual.get("object_sha") != expected.get("object_sha"):
            errors.append(f"{path}: object_sha does not match manifest")
        if actual.get("review_method") != expected.get("review_method"):
            errors.append(f"{path}: review_method does not match manifest")
        if actual.get("coverage_unit") != expected.get("coverage_unit"):
            errors.append(f"{path}: coverage_unit does not match manifest")
        if actual.get("semantic_status") != VALID_STATUS:
            errors.append(f"{path}: semantic_status must be COMPLETE")

        ranges = actual.get("ranges")
        if not isinstance(ranges, list):
            errors.append(f"{path}: ranges must be a list")
            continue

        total = expected.get("coverage_total")
        if not isinstance(total, int):
            errors.append(f"{path}: manifest coverage_total must be an integer")
            continue
        complete, reason = covered_fully(total, ranges)
        if not complete:
            errors.append(f"{path}: {reason}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--coverage", type=Path, required=True)
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
        coverage = load_json(args.coverage)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors = validate(manifest, coverage)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Exhaustive review coverage is complete for every manifest entry. "
        "This proves inventory/range processing records, not semantic comprehension or correctness."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
