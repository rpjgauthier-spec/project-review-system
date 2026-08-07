#!/usr/bin/env python3
"""Regression tests for exhaustive review manifest and coverage validation."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MANIFEST = load_module("build_review_manifest", ROOT / "scripts" / "build_review_manifest.py")
COVERAGE = load_module("check_review_coverage", ROOT / "scripts" / "check_review_coverage.py")


class ReviewCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "guide.md").write_text("one\ntwo\nthree\n", encoding="utf-8")
        (self.repo / "data.json").write_text('{"ok": true}\n', encoding="utf-8")
        (self.repo / "empty.txt").write_text("", encoding="utf-8")
        (self.repo / "binary.bin").write_bytes(b"\x00\x01\x02\x03")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.repo, check=True)
        self.manifest = MANIFEST.build_manifest(self.repo, "HEAD")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def entry(self, path: str) -> dict:
        return next(item for item in self.manifest["entries"] if item["path"] == path)

    def complete_coverage(self) -> dict:
        entries = []
        for expected in self.manifest["entries"]:
            total = expected["coverage_total"]
            ranges = [] if total == 0 else [[1, total]]
            entries.append(
                {
                    "path": expected["path"],
                    "object_sha": expected["object_sha"],
                    "review_method": expected["review_method"],
                    "coverage_unit": expected["coverage_unit"],
                    "semantic_status": "COMPLETE",
                    "ranges": ranges,
                }
            )
        return {
            "schema_version": 1,
            "resolved_commit": self.manifest["resolved_commit"],
            "entries": entries,
        }

    def test_manifest_includes_tree_and_all_tracked_files(self) -> None:
        paths = {entry["path"] for entry in self.manifest["entries"]}
        self.assertEqual(paths, {"binary.bin", "data.json", "docs", "docs/guide.md", "empty.txt"})
        self.assertEqual(self.entry("docs")["review_method"], "STRUCTURE_SEMANTIC")

    def test_manifest_assigns_semantic_methods_and_full_units(self) -> None:
        self.assertEqual(self.entry("docs/guide.md")["review_method"], "DOCUMENT_SEMANTIC")
        self.assertEqual(self.entry("docs/guide.md")["coverage_unit"], "line")
        self.assertEqual(self.entry("docs/guide.md")["coverage_total"], 3)
        self.assertEqual(self.entry("data.json")["review_method"], "STRUCTURED_DATA_SEMANTIC")
        self.assertEqual(self.entry("binary.bin")["review_method"], "BINARY_ANALYSIS")
        self.assertEqual(self.entry("binary.bin")["coverage_total"], 4)

    def test_complete_coverage_passes(self) -> None:
        self.assertEqual(COVERAGE.validate(self.manifest, self.complete_coverage()), [])

    def test_missing_object_fails(self) -> None:
        coverage = self.complete_coverage()
        coverage["entries"] = [e for e in coverage["entries"] if e["path"] != "data.json"]
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("Missing coverage entries" in error for error in errors), errors)

    def test_partial_range_fails(self) -> None:
        coverage = self.complete_coverage()
        target = next(e for e in coverage["entries"] if e["path"] == "docs/guide.md")
        target["ranges"] = [[1, 1], [3, 3]]
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("missing coverage range 2..2" in error for error in errors), errors)

    def test_wrong_blob_identity_fails(self) -> None:
        coverage = self.complete_coverage()
        target = next(e for e in coverage["entries"] if e["path"] == "data.json")
        target["object_sha"] = "0" * 40
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("object_sha does not match" in error for error in errors), errors)

    def test_noncomplete_semantic_status_fails(self) -> None:
        coverage = self.complete_coverage()
        target = next(e for e in coverage["entries"] if e["path"] == "binary.bin")
        target["semantic_status"] = "INACCESSIBLE"
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("semantic_status must be COMPLETE" in error for error in errors), errors)

    def test_zero_length_object_requires_no_fake_range(self) -> None:
        coverage = self.complete_coverage()
        target = next(e for e in coverage["entries"] if e["path"] == "empty.txt")
        target["ranges"] = [[1, 1]]
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("zero-length object" in error for error in errors), errors)

    def test_coverage_commit_must_match_manifest(self) -> None:
        coverage = self.complete_coverage()
        coverage["resolved_commit"] = "deadbeef"
        errors = COVERAGE.validate(self.manifest, coverage)
        self.assertTrue(any("resolved_commit does not match" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
