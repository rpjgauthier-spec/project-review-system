#!/usr/bin/env python3
"""Regression tests for adaptive review execution selection."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "select_execution_policy.py"
DEFAULT_CAPABILITY_PATH = SKILL_ROOT / "config" / "default-execution-capability.json"

spec = importlib.util.spec_from_file_location("select_execution_policy", SCRIPT_PATH)
assert spec and spec.loader
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)


def workload(**overrides):
    value = {
        "schema_version": 1,
        "artifact_count": 1,
        "semantic_units": 100,
        "required_stage_count": 1,
        "required_evaluation_count": 1,
        "dependency_count": 1,
        "protected_control_count": 0,
        "unresolved_uncertainty_count": 0,
        "material_findings_count": 0,
        "unexpected_dependency_count": 0,
        "self_referential": False,
        "exhaustive_claim": False,
        "checkpoint": "test",
    }
    value.update(overrides)
    return value


def strong_capability():
    limits = {
        "artifact_count": 100,
        "semantic_units": 100000,
        "required_stage_count": 5,
        "required_evaluation_count": 50,
        "dependency_count": 100,
        "protected_control_count": 20,
        "unresolved_uncertainty_count": 20,
        "material_findings_count": 20,
        "unexpected_dependency_count": 20,
        "allow_self_referential": True,
        "allow_exhaustive_claim": True,
    }
    return {
        "schema_version": 1,
        "profile_id": "validated-strong-test",
        "subject_id": "test-reviewer-runtime-v2",
        "validation_status": "VALIDATED",
        "benchmark_suite": "fixture-suite-v1",
        "benchmark_evidence": "fixture:validated-strong-test",
        "fused_limits": dict(limits),
        "separated_limits": dict(limits),
    }


class ExecutionPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.default_capability = json.loads(DEFAULT_CAPABILITY_PATH.read_text(encoding="utf-8"))

    def test_small_workload_is_fused_under_default_profile(self) -> None:
        decision = selector.select_policy(workload(), self.default_capability)
        self.assertEqual(decision["selected_mode"], "FUSED")

    def test_five_stage_workload_is_separated_under_default_profile(self) -> None:
        decision = selector.select_policy(
            workload(required_stage_count=5, required_evaluation_count=10, artifact_count=12),
            self.default_capability,
        )
        self.assertEqual(decision["selected_mode"], "SEPARATED")

    def test_large_workload_is_isolated_under_default_profile(self) -> None:
        decision = selector.select_policy(
            workload(artifact_count=40, semantic_units=20000, dependency_count=25),
            self.default_capability,
        )
        self.assertEqual(decision["selected_mode"], "ISOLATED")

    def test_stronger_validated_profile_can_reduce_separation(self) -> None:
        subject = workload(
            required_stage_count=5,
            required_evaluation_count=10,
            artifact_count=12,
            self_referential=True,
        )
        default_decision = selector.select_policy(subject, self.default_capability)
        strong_decision = selector.select_policy(subject, strong_capability())
        self.assertEqual(default_decision["selected_mode"], "SEPARATED")
        self.assertEqual(strong_decision["selected_mode"], "FUSED")

    def test_new_complexity_tightens_immediately(self) -> None:
        initial = selector.select_policy(workload(), self.default_capability)
        self.assertEqual(initial["selected_mode"], "FUSED")
        later = selector.select_policy(
            workload(artifact_count=40, material_findings_count=8),
            self.default_capability,
            current_mode="FUSED",
        )
        self.assertEqual(later["selected_mode"], "ISOLATED")

    def test_relaxation_is_limited_to_one_level_per_checkpoint(self) -> None:
        decision = selector.select_policy(
            workload(), strong_capability(), current_mode="ISOLATED"
        )
        self.assertEqual(decision["base_mode"], "FUSED")
        self.assertEqual(decision["selected_mode"], "SEPARATED")

    def test_custom_profile_must_be_validated(self) -> None:
        invalid = strong_capability()
        invalid["validation_status"] = "DEFAULT_CONSERVATIVE"
        with self.assertRaises(ValueError):
            selector.validate_capability(invalid, custom_profile=True)

    def test_nondefault_profile_cannot_impersonate_default_conservative(self) -> None:
        invalid = strong_capability()
        invalid["validation_status"] = "DEFAULT_CONSERVATIVE"
        with self.assertRaises(ValueError):
            selector.select_policy(workload(), invalid)

    def test_capability_requires_subject_and_benchmark_suite(self) -> None:
        invalid = strong_capability()
        invalid["subject_id"] = ""
        with self.assertRaises(ValueError):
            selector.validate_capability(invalid, custom_profile=True)
        invalid = strong_capability()
        invalid["benchmark_suite"] = ""
        with self.assertRaises(ValueError):
            selector.validate_capability(invalid, custom_profile=True)

    def test_envelopes_must_be_monotonic(self) -> None:
        invalid = strong_capability()
        invalid["fused_limits"]["artifact_count"] = 101
        invalid["separated_limits"]["artifact_count"] = 100
        with self.assertRaises(ValueError):
            selector.validate_capability(invalid, custom_profile=True)

    def test_cli_rejects_unvalidated_custom_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            workload_path = temp / "workload.json"
            capability_path = temp / "capability.json"
            workload_path.write_text(json.dumps(workload()), encoding="utf-8")
            invalid = strong_capability()
            invalid["validation_status"] = "DEFAULT_CONSERVATIVE"
            capability_path.write_text(json.dumps(invalid), encoding="utf-8")
            loaded_workload = selector.load_json(workload_path)
            loaded_capability = selector.load_json(capability_path)
            selector.validate_workload(loaded_workload)
            with self.assertRaises(ValueError):
                selector.validate_capability(loaded_capability, custom_profile=True)

    def test_assurance_boundary_is_explicit(self) -> None:
        decision = selector.select_policy(workload(), self.default_capability)
        boundary = decision["assurance_boundary"]
        self.assertIn("required stages", boundary)
        self.assertIn("independent-review requirements", boundary)
        self.assertIn("cannot prove workload truthfulness", boundary)

    def test_decision_records_capability_subject(self) -> None:
        decision = selector.select_policy(workload(), strong_capability())
        self.assertEqual(decision["capability_subject_id"], "test-reviewer-runtime-v2")
        self.assertEqual(decision["capability_benchmark_suite"], "fixture-suite-v1")


if __name__ == "__main__":
    unittest.main()
