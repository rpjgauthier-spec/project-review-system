#!/usr/bin/env python3
"""Regression tests for the generic Identity Pass abstraction boundary."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
IDENTITY = ROOT / "references" / "identity-pass.md"
OLD_IDENTITY = ROOT / "references" / "repository-identity-pass.md"
IDENTITY_EVAL = ROOT / "evals" / "identity-discovery.md"
OLD_IDENTITY_EVAL = ROOT / "evals" / "repository-identity-discovery.md"
ABSTRACTION_EVAL = ROOT / "evals" / "abstraction-boundary.md"
STRUCTURAL = ROOT / "references" / "structural-optimization-review.md"


class IdentityAbstractionRegressionTests(unittest.TestCase):
    def test_generic_identity_paths_are_canonical(self) -> None:
        self.assertTrue(IDENTITY.is_file())
        self.assertTrue(IDENTITY_EVAL.is_file())
        self.assertTrue(ABSTRACTION_EVAL.is_file())
        self.assertFalse(OLD_IDENTITY.exists())
        self.assertFalse(OLD_IDENTITY_EVAL.exists())

    def test_runtime_docs_reference_generic_identity_module(self) -> None:
        for path in (SKILL, README):
            text = path.read_text(encoding="utf-8")
            self.assertIn("references/identity-pass.md", text)
            self.assertNotIn("references/repository-identity-pass.md", text)

    def test_semantic_and_repository_specific_boundaries_are_separate(self) -> None:
        identity_text = IDENTITY.read_text(encoding="utf-8")
        structural_text = STRUCTURAL.read_text(encoding="utf-8")
        self.assertIn("medium-independent", identity_text)
        self.assertIn("Git repository", identity_text)
        self.assertIn("environment-specific evidence", structural_text)
        self.assertIn("implementation assumption", structural_text)


if __name__ == "__main__":
    unittest.main()
