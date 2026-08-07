#!/usr/bin/env python3
"""Build a deterministic exhaustive-review manifest for a pinned Git tree.

The manifest inventories every tracked tree entry reachable from the selected
commit. Blobs are assigned a semantic review method and a deterministic coverage
unit. Trees and gitlinks are represented explicitly so repository structure and
submodule references cannot disappear from an exhaustive-coverage claim.

This script proves inventory and source identity only. It does not prove that an
AI or human understood the content.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = 1

CODE_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".h", ".cc",
    ".cpp", ".cxx", ".hpp", ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt",
    ".kts", ".scala", ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".sql", ".lua", ".r", ".m", ".mm", ".pl", ".pm", ".ex", ".exs", ".erl",
    ".hrl", ".fs", ".fsx", ".vb", ".asm", ".s", ".sol", ".dart", ".vue",
}
STRUCTURED_EXTENSIONS = {
    ".json", ".jsonl", ".yaml", ".yml", ".toml", ".xml", ".csv", ".tsv",
    ".ini", ".cfg", ".conf", ".properties", ".lock",
}
DOCUMENT_EXTENSIONS = {
    ".md", ".markdown", ".rst", ".adoc", ".asciidoc", ".txt", ".org", ".tex",
}
IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg",
    ".ico",
}
DOCUMENT_BINARY_EXTENSIONS = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz", ".7z", ".rar", ".jar", ".war"}


def run_git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip() or "git command failed"
        raise RuntimeError(message)
    return result.stdout


def resolve_commit(repo: Path, ref: str) -> str:
    return run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()


def read_blob(repo: Path, sha: str) -> bytes:
    return run_git(repo, "cat-file", "blob", sha)


def is_text_blob(data: bytes) -> bool:
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def classify_blob(path: str, data: bytes) -> tuple[str, str, int]:
    suffix = PurePosixPath(path).suffix.lower()
    size = len(data)
    text = is_text_blob(data)

    if suffix in CODE_EXTENSIONS and text:
        method = "CODE_SEMANTIC"
    elif suffix in STRUCTURED_EXTENSIONS and text:
        method = "STRUCTURED_DATA_SEMANTIC"
    elif suffix in DOCUMENT_EXTENSIONS and text:
        method = "DOCUMENT_SEMANTIC"
    elif suffix in IMAGE_EXTENSIONS:
        method = "IMAGE_SEMANTIC"
    elif suffix in DOCUMENT_BINARY_EXTENSIONS:
        method = "DOCUMENT_SEMANTIC"
    elif suffix in ARCHIVE_EXTENSIONS:
        method = "ARCHIVE_EXPANSION"
    elif text:
        method = "TEXT_SEMANTIC"
    else:
        method = "BINARY_ANALYSIS"

    if text:
        line_count = len(data.decode("utf-8").splitlines())
        return method, "line", line_count
    return method, "byte", size


def parse_tree(repo: Path, commit: str) -> list[dict[str, Any]]:
    raw = run_git(repo, "ls-tree", "-r", "-t", "-z", commit)
    entries: list[dict[str, Any]] = []
    for record in raw.split(b"\x00"):
        if not record:
            continue
        meta, path_bytes = record.split(b"\t", 1)
        mode_b, object_type_b, sha_b = meta.split(b" ", 2)
        path = path_bytes.decode("utf-8", errors="surrogateescape")
        mode = mode_b.decode()
        object_type = object_type_b.decode()
        sha = sha_b.decode()

        entry: dict[str, Any] = {
            "path": path,
            "mode": mode,
            "object_type": object_type,
            "object_sha": sha,
        }

        if object_type == "tree":
            entry.update(
                {
                    "size_bytes": None,
                    "review_method": "STRUCTURE_SEMANTIC",
                    "coverage_unit": "object",
                    "coverage_total": 1,
                }
            )
        elif object_type == "blob":
            data = read_blob(repo, sha)
            method, unit, total = classify_blob(path, data)
            entry.update(
                {
                    "size_bytes": len(data),
                    "review_method": method,
                    "coverage_unit": unit,
                    "coverage_total": total,
                }
            )
        elif object_type == "commit":
            # Git submodule/gitlink entries point at another commit object.
            entry.update(
                {
                    "size_bytes": None,
                    "review_method": "GITLINK_SEMANTIC",
                    "coverage_unit": "object",
                    "coverage_total": 1,
                }
            )
        else:
            entry.update(
                {
                    "size_bytes": None,
                    "review_method": "OBJECT_SEMANTIC",
                    "coverage_unit": "object",
                    "coverage_total": 1,
                }
            )
        entries.append(entry)

    return sorted(entries, key=lambda item: item["path"])


def build_manifest(repo: Path, ref: str) -> dict[str, Any]:
    repo = repo.resolve()
    commit = resolve_commit(repo, ref)
    return {
        "schema_version": SCHEMA_VERSION,
        "repository": str(repo),
        "requested_ref": ref,
        "resolved_commit": commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "coverage_policy": "EXHAUSTIVE_NO_EXCLUSIONS",
        "entries": parse_tree(repo, commit),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True, help="Path to a Git repository")
    parser.add_argument("--ref", default="HEAD", help="Commit-ish to pin for review")
    parser.add_argument("--output", type=Path, required=True, help="Manifest JSON output path")
    args = parser.parse_args()

    try:
        manifest = build_manifest(args.repo, args.ref)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"Wrote exhaustive review manifest for {len(manifest['entries'])} tracked object(s) "
        f"at commit {manifest['resolved_commit']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
