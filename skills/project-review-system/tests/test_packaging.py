#!/usr/bin/env python3
"""Regression tests for Project Review System packaging."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]
BUNDLED_WORKFLOW = SKILL_ROOT / "templates" / "project-review-system-revalidation.yml"
ACTIVE_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "project-review-system-revalidation.yml"
INSTALL_GUIDE = SKILL_ROOT / "INSTALL.md"


class PackagingRegressionTests(unittest.TestCase):
    def test_bundled_workflow_matches_active_workflow(self) -> None:
        self.assertTrue(BUNDLED_WORKFLOW.is_file(), "bundled workflow template is missing")
        self.assertTrue(ACTIVE_WORKFLOW.is_file(), "active repository workflow is missing")
        self.assertEqual(
            BUNDLED_WORKFLOW.read_text(encoding="utf-8"),
            ACTIVE_WORKFLOW.read_text(encoding="utf-8"),
            "bundled workflow template drifted from the active repository workflow",
        )

    def test_installation_guide_names_both_layers(self) -> None:
        text = INSTALL_GUIDE.read_text(encoding="utf-8")
        self.assertIn("skills/project-review-system/", text)
        self.assertIn(".github/workflows/project-review-system-revalidation.yml", text)
        self.assertIn("validate-revalidation-controls", text)
        self.assertIn("Repository rules do not travel automatically", text)


if __name__ == "__main__":
    unittest.main()
