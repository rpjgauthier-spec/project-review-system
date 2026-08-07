#!/usr/bin/env python3
"""Regression coverage for review-revision requirements on completed-pass redo."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = SKILL_ROOT / "scripts" / "check_execution_identity_history.py"

spec = importlib.util.spec_from_file_location("check_execution_identity_history_reopening", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def completed(revision: int, gate_sha: str, unit_id: str, boundary_id: str, pass_id: str = "stage-main"):
    return {
        "review_revision": revision,
        "execution_gates": {"Adversarial": {"gate_sha256": gate_sha}},
        "execution_completions": {
            "Adversarial": {
                "gate_sha256": gate_sha,
                "passes": [
                    {
                        "pass_id": pass_id,
                        "status": "complete",
                        "execution_unit_id": unit_id,
                        "boundary": {"kind": "declared-execution-unit", "id": boundary_id},
                        "inbound_handoff_sha256": None,
                        "handoff": {
                            "consumer": "Interdependency",
                            "findings": ["fixture"],
                            "evidence": [],
                            "unresolved_conditions": [],
                            "sha256": "fixture",
                        },
                    }
                ],
            }
        },
    }


class ExecutionIdentityReopeningTests(unittest.TestCase):
    def test_completed_pass_cannot_be_replaced_by_new_gate_in_same_revision(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        replacement = completed(8, "gate-b", "unit-b", "boundary-b")
        with self.assertRaisesRegex(ValueError, "increment review_revision"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_stage_cannot_change_gate_by_renaming_pass_in_same_revision(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a", pass_id="stage-main")
        replacement = completed(8, "gate-b", "unit-b", "boundary-b", pass_id="redo-main")
        with self.assertRaisesRegex(ValueError, "stage gate"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_pass_can_be_redone_after_revision_increment_with_new_identities(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        replacement = completed(9, "gate-b", "unit-b", "boundary-b")
        checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_stage_can_change_plan_after_revision_increment(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a", pass_id="stage-main")
        replacement = completed(9, "gate-b", "unit-b", "boundary-b", pass_id="authorization")
        checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])


if __name__ == "__main__":
    unittest.main()
