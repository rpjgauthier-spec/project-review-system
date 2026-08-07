#!/usr/bin/env python3
"""Regression tests for Adaptive Execution gate and completion validation."""

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


def workload(assessment=None):
    return {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": "Adversarial",
        "target_state_id": "sha256:fixture",
        "review_revision": 2,
        "workload_class": "ordinary-review-v1",
        "stage_assessment": assessment or {"single_pass_suitable": True, "reasons": ["bounded"], "subpasses": []},
        "fused_authorization": None,
    }


def completion_for(gate):
    decision = gate["decision"]
    return {
        "gate_sha256": gate["gate_sha256"],
        "target_state_id": decision["target_state_id"],
        "passes": [
            {"pass_id": item["pass_id"], "context_mode": item["context_mode"], "status": "complete"}
            for item in decision["execution_plan"]
        ],
        "scratch_materialized": False,
        "scratch_cleanup_status": "not_applicable",
        "retained_subpass_artifacts": [],
    }


class ExecutionGateTests(unittest.TestCase):
    def test_valid_gate_passes(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        decision = checker.validate_execution_gate(gate, "Adversarial", 2, "sha256:fixture")
        self.assertEqual(decision["plan_kind"], "ONE_PASS")

    def test_stale_revision_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        with self.assertRaisesRegex(ValueError, "does not match current review revision"):
            checker.validate_execution_gate(gate, "Adversarial", 3)

    def test_stale_target_state_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        with self.assertRaisesRegex(ValueError, "does not match current governed artifact state"):
            checker.validate_execution_gate(gate, "Adversarial", 2, "sha256:new")

    def test_matching_completion_passes(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        checker.validate_execution_completion(completion_for(gate), gate)

    def test_wrong_context_mode_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["passes"][0]["context_mode"] = "ISOLATED"
        with self.assertRaisesRegex(ValueError, "wrong context mode"):
            checker.validate_execution_completion(completion, gate)

    def test_missing_subpass_fails(self) -> None:
        assessment = {
            "single_pass_suitable": False,
            "reasons": ["broad"],
            "subpasses": [
                {"pass_id": "a", "scope": "a", "isolation_required": False, "reasons": ["bounded"]},
                {"pass_id": "b", "scope": "b", "isolation_required": True, "reasons": ["large"]},
            ],
        }
        gate = selector.build_gate(workload(assessment), CAPABILITY)
        completion = completion_for(gate)
        completion["passes"].pop()
        with self.assertRaisesRegex(ValueError, "pass count"):
            checker.validate_execution_completion(completion, gate)

    def test_incomplete_pass_fails(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["passes"][0]["status"] = "pending"
        with self.assertRaisesRegex(ValueError, "not complete"):
            checker.validate_execution_completion(completion, gate)

    def test_materialized_scratch_requires_cleanup(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["scratch_materialized"] = True
        completion["scratch_cleanup_status"] = "pending"
        with self.assertRaisesRegex(ValueError, "must be deleted"):
            checker.validate_execution_completion(completion, gate)

    def test_materialized_scratch_with_cleanup_passes(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["scratch_materialized"] = True
        completion["scratch_cleanup_status"] = "complete"
        checker.validate_execution_completion(completion, gate)

    def test_retained_artifact_requires_consumer(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["retained_subpass_artifacts"] = [
            {"artifact": "evidence.md", "consumer": "", "reason": "needed later"}
        ]
        with self.assertRaisesRegex(ValueError, "consumer is required"):
            checker.validate_execution_completion(completion, gate)

    def test_retained_artifact_with_consumer_passes(self) -> None:
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["retained_subpass_artifacts"] = [
            {"artifact": "evidence.md", "consumer": "End-to-end validation", "reason": "required evidence"}
        ]
        checker.validate_execution_completion(completion, gate)

    def test_artifact_state_changes_with_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "a.txt"
            target.write_text("one", encoding="utf-8")
            first = checker.repository_artifact_state_sha256(["a.txt"], root)
            target.write_text("two", encoding="utf-8")
            second = checker.repository_artifact_state_sha256(["a.txt"], root)
            self.assertNotEqual(first, second)

    def test_leading_dot_path_is_preserved(self) -> None:
        self.assertEqual(checker.normalize_repository_path(".github/workflow.yml"), ".github/workflow.yml")


if __name__ == "__main__":
    unittest.main()
