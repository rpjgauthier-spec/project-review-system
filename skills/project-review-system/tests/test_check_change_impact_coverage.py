#!/usr/bin/env python3
"""Regression tests for check_change_impact_coverage.py."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_change_impact_coverage.py"
SPEC = importlib.util.spec_from_file_location("check_change_impact_coverage", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CoverageRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        (self.root / "skills/project-review-system/changes").mkdir(parents=True)
        (self.root / "skills/project-review-system/SKILL.md").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.root, check=True)
        self.base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self) -> list[str]:
        old = Path.cwd()
        try:
            import os
            os.chdir(self.root)
            return MODULE.validate(self.base, "HEAD")
        finally:
            os.chdir(old)

    def commit_change(self, *, declared: list[str] | None) -> None:
        skill = self.root / "skills/project-review-system/SKILL.md"
        skill.write_text("changed\n", encoding="utf-8")
        if declared is not None:
            record_path = self.root / "skills/project-review-system/changes/change.json"
            record = {
                "id": "change",
                "summary": "test",
                "changed_files": declared,
                "change_classes": ["status-or-schema"],
                "claimed_earliest_stage": "Interdependency",
                "status": "pending",
            }
            record_path.write_text(json.dumps(record), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "change"], cwd=self.root, check=True)

    def test_dotgithub_path_keeps_leading_dot(self) -> None:
        workflow = ".github/workflows/project-review-system-revalidation.yml"
        self.assertEqual(MODULE.normalize_declared(workflow), workflow)
        self.assertEqual(MODULE.normalize_declared("./" + workflow), workflow)

    def test_rejects_unrecorded_change(self) -> None:
        self.commit_change(declared=None)
        errors = self.validate()
        self.assertTrue(any("no impact record" in error for error in errors), errors)

    def test_accepts_complete_coverage(self) -> None:
        self.commit_change(declared=["SKILL.md", "changes/change.json"])
        self.assertEqual(self.validate(), [])

    def test_rejects_record_that_does_not_list_itself(self) -> None:
        self.commit_change(declared=["SKILL.md"])
        errors = self.validate()
        self.assertTrue(any("must list itself" in error for error in errors), errors)

    def test_rejects_stale_claim_on_new_record(self) -> None:
        self.commit_change(declared=["SKILL.md", "README.md", "changes/change.json"])
        errors = self.validate()
        self.assertTrue(any("not present in this diff" in error for error in errors), errors)

    def test_existing_record_may_retain_historical_claims(self) -> None:
        record_path = self.root / "skills/project-review-system/changes/existing.json"
        record = {
            "id": "existing",
            "summary": "historical change",
            "changed_files": ["SKILL.md", "README.md", "changes/existing.json"],
            "change_classes": ["status-or-schema"],
            "claimed_earliest_stage": "Interdependency",
            "status": "pending",
        }
        record_path.write_text(json.dumps(record), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "add historical record"], cwd=self.root, check=True)
        self.base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

        (self.root / "skills/project-review-system/SKILL.md").write_text("changed\n", encoding="utf-8")
        record["status"] = "complete"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "record later results"], cwd=self.root, check=True)

        self.assertEqual(self.validate(), [])


if __name__ == "__main__":
    unittest.main()
