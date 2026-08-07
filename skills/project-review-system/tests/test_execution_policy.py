#!/usr/bin/env python3
"""Regression tests for separated-default Adaptive Execution."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "select_execution_policy.py"
DEFAULT_CAPABILITY_PATH = SKILL_ROOT / "config" / "default-execution-capability.json"

spec = importlib.util.spec_from_file_location("select_execution_policy", SCRIPT_PATH)
assert spec and spec.loader
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)
DEFAULT = json.loads(DEFAULT_CAPABILITY_PATH.read_text(encoding="utf-8"))


def workload(**overrides):
    value = {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": "Adversarial",
        "target_state_id": "sha256:fixture",
        "review_revision": 1,
        "workload_class": "ordinary-review-v1",
        "stage_assessment": {
            "single_pass_suitable": True,
            "reasons": ["bounded stage scope"],
            "subpasses": [],
        },
        "fused_authorization": None,
    }
    value.update(overrides)
    return value


def validated_capability():
    return {
        "schema_version": 1,
        "profile_id": "validated-test",
        "subject_id": "test-reviewer",
        "validation_status": "VALIDATED",
        "benchmark_suite": "suite-v1",
        "benchmark_evidence": "fixture:whole-profile",
        "fused_permissions": [
            {
                "permission_id": "adv-inter-v1",
                "activities": ["Adversarial", "Interdependency"],
                "workload_class": "ordinary-review-v1",
                "benchmark_evidence": "fixture:fused-pair",
            }
        ],
    }


class ExecutionPolicyTests(unittest.TestCase):
    def test_default_is_separated_one_pass(self) -> None:
        decision = selector.select_policy(workload(), DEFAULT)
        self.assertEqual(decision["selected_mode"], "SEPARATED")
        self.assertEqual(decision["plan_kind"], "ONE_PASS")
        self.assertEqual(decision["execution_plan"][0]["context_mode"], "SEPARATED")

    def test_unsuitable_stage_requires_subdivision(self) -> None:
        assessment = {
            "single_pass_suitable": False,
            "reasons": ["multiple distinct analytical lenses"],
            "subpasses": [
                {"pass_id": "authority", "scope": "authority relationships", "isolation_required": False, "reasons": ["bounded"]},
                {"pass_id": "propagation", "scope": "state propagation", "isolation_required": True, "reasons": ["large dependency surface"]},
            ],
        }
        decision = selector.select_policy(workload(stage_assessment=assessment), DEFAULT)
        self.assertEqual(decision["plan_kind"], "SUBDIVIDED")
        self.assertEqual([p["context_mode"] for p in decision["execution_plan"]], ["SEPARATED", "ISOLATED"])

    def test_unsuitable_stage_cannot_skip_subpasses(self) -> None:
        assessment = {"single_pass_suitable": False, "reasons": ["too broad"], "subpasses": []}
        with self.assertRaisesRegex(ValueError, "at least two bounded subpasses"):
            selector.select_policy(workload(stage_assessment=assessment), DEFAULT)

    def test_default_profile_cannot_grant_fused(self) -> None:
        fused = {"permission_id": "adv-inter-v1", "group_id": "g1", "activities": ["Adversarial", "Interdependency"]}
        with self.assertRaisesRegex(ValueError, "VALIDATED"):
            selector.select_policy(workload(fused_authorization=fused), DEFAULT)

    def test_validated_exact_permission_allows_fused(self) -> None:
        fused = {"permission_id": "adv-inter-v1", "group_id": "g1", "activities": ["Adversarial", "Interdependency"]}
        decision = selector.select_policy(workload(fused_authorization=fused), validated_capability())
        self.assertEqual(decision["selected_mode"], "FUSED")
        self.assertEqual(decision["plan_kind"], "FUSED_GROUP")

    def test_fused_permission_is_subject_bound(self) -> None:
        fused = {"permission_id": "adv-inter-v1", "group_id": "g1", "activities": ["Adversarial", "Interdependency"]}
        cap = validated_capability()
        cap["subject_id"] = "other-reviewer"
        with self.assertRaisesRegex(ValueError, "subject"):
            selector.select_policy(workload(fused_authorization=fused), cap)

    def test_fused_cannot_override_subdivision_assessment(self) -> None:
        fused = {"permission_id": "adv-inter-v1", "group_id": "g1", "activities": ["Adversarial", "Interdependency"]}
        assessment = {
            "single_pass_suitable": False,
            "reasons": ["too broad"],
            "subpasses": [
                {"pass_id": "a", "scope": "a", "isolation_required": False, "reasons": ["bounded"]},
                {"pass_id": "b", "scope": "b", "isolation_required": False, "reasons": ["bounded"]},
            ],
        }
        with self.assertRaisesRegex(ValueError, "cannot override"):
            selector.select_policy(workload(stage_assessment=assessment, fused_authorization=fused), validated_capability())

    def test_gate_rejects_tampering(self) -> None:
        gate = selector.build_gate(workload(), DEFAULT)
        selector.validate_gate(gate, expected_activity="Adversarial")
        gate["decision"]["plan_kind"] = "SUBDIVIDED"
        with self.assertRaises(ValueError):
            selector.validate_gate(gate, expected_activity="Adversarial")

    def test_default_profile_cannot_hide_fused_permission(self) -> None:
        invalid = dict(DEFAULT)
        invalid["fused_permissions"] = [{"permission_id": "x", "activities": ["A", "B"], "workload_class": "c", "benchmark_evidence": "e"}]
        with self.assertRaises(ValueError):
            selector.validate_capability(invalid, custom_profile=False)


if __name__ == "__main__":
    unittest.main()
