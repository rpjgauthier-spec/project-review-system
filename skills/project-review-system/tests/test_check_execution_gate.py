#!/usr/bin/env python3
"""Regression tests for adaptive execution gate validation."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = SKILL_ROOT / "scripts" / "check_execution_gate.py"
SELECTOR_PATH = SKILL_ROOT / "scripts" / "select_execution_policy.py"
DEFAULT_CAPABILITY_PATH = SKILL_ROOT / "config" / "default-execution-capability.json"

checker_spec = importlib.util.spec_from_file_location("check_execution_gate", CHECKER_PATH)
assert checker_spec and checker_spec.loader
checker = importlib.util.module_from_spec(checker_spec)
checker_spec.loader.exec_module(checker)

selector_spec = importlib.util.spec_from_file_location("selector_for_gate_test", SELECTOR_PATH)
assert selector_spec and selector_spec.loader
selector = importlib.util.module_from_spec(selector_spec)
selector_spec.loader.exec_module(selector)

CAPABILITY = json.loads(DEFAULT_CAPABILITY_PATH.read_text(encoding="utf-8"))


def workload(**overrides):
    value = {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": "Adversarial",
        "target_state_id": "sha256:fixture",
        "review_revision": 2,
        "artifact_count": 2,
        "content_bytes": 2000,
        "remaining_stage_count": 5,
        "remaining_evaluation_count": 10,
        "dependency_count": 2,
        "protected_control_count": 0,
        "unresolved_uncertainty_count": 0,
        "material_findings_count": 0,
        "unexpected_dependency_count": 0,
        "self_referential": True,
        "exhaustive_claim": False,
        "checkpoint": "reopened-adversarial",
    }
    value.update(overrides)
    return value


class ExecutionGateTests(unittest.TestCase):
    def test_valid_gate_passes(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY, current_mode="SEPARATED")
        decision = checker.validate_execution_gate(
            gate, "Adversarial", 2, expected_target_state_id="sha256:fixture"
        )
        self.assertEqual(decision["activity"], "Adversarial")

    def test_stale_review_revision_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        with self.assertRaisesRegex(ValueError, "does not match current review revision"):
            checker.validate_execution_gate(gate, "Adversarial", 3)

    def test_stale_target_state_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        with self.assertRaisesRegex(ValueError, "does not match current governed artifact state"):
            checker.validate_execution_gate(
                gate, "Adversarial", 2, expected_target_state_id="sha256:new-state"
            )

    def test_zero_remaining_stage_count_fails_for_stage(self) -> None:
        gate = selector.build_gate(workload(remaining_stage_count=0), CAPABILITY)
        with self.assertRaisesRegex(ValueError, "must include that stage"):
            checker.validate_execution_gate(gate, "Adversarial", 2)

    def test_identity_pass_may_have_zero_remaining_stage_count(self) -> None:
        gate = selector.build_gate(
            workload(activity="Identity Pass", remaining_stage_count=0), CAPABILITY
        )
        checker.validate_execution_gate(gate, "Identity Pass", 2)

    def test_repository_artifact_state_changes_when_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "a.txt"
            target.write_text("one", encoding="utf-8")
            first = checker.repository_artifact_state_sha256(["a.txt"], root)
            target.write_text("two", encoding="utf-8")
            second = checker.repository_artifact_state_sha256(["a.txt"], root)
            self.assertNotEqual(first, second)

    def test_repository_artifact_state_represents_absence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            absent = checker.repository_artifact_state_sha256(["gone.txt"], root)
            (root / "gone.txt").write_text("present", encoding="utf-8")
            present = checker.repository_artifact_state_sha256(["gone.txt"], root)
            self.assertNotEqual(absent, present)


if __name__ == "__main__":
    unittest.main()
