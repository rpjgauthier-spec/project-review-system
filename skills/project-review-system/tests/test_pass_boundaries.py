#!/usr/bin/env python3
"""Regression tests for declared pass boundaries and handoff chaining."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = SKILL_ROOT / "scripts" / "check_pass_boundaries.py"
SELECTOR_PATH = SKILL_ROOT / "scripts" / "select_execution_policy.py"
DEFAULT_CAPABILITY_PATH = SKILL_ROOT / "config" / "default-execution-capability.json"

checker_spec = importlib.util.spec_from_file_location("check_pass_boundaries", CHECKER_PATH)
assert checker_spec and checker_spec.loader
checker = importlib.util.module_from_spec(checker_spec)
checker_spec.loader.exec_module(checker)
selector_spec = importlib.util.spec_from_file_location("selector_for_boundary_test", SELECTOR_PATH)
assert selector_spec and selector_spec.loader
selector = importlib.util.module_from_spec(selector_spec)
selector_spec.loader.exec_module(selector)
CAPABILITY = json.loads(DEFAULT_CAPABILITY_PATH.read_text(encoding="utf-8"))

MAPPING = {
    "stages": ["Adversarial", "Interdependency"],
    "pass_boundary": {"enabled": True, "legacy_exempt_change_ids": ["legacy"]},
    "change_classes": {
        "authority-or-propagation": {
            "stages": ["Adversarial", "Interdependency"],
            "evaluations": [],
        }
    },
}


def workload(activity: str):
    return {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": activity,
        "target_state_id": "sha256:fixture",
        "review_revision": 7,
        "workload_class": "boundary-test-v1",
        "stage_assessment": {"single_pass_suitable": True, "reasons": ["bounded"], "subpasses": []},
        "fused_authorization": None,
    }


def handoff(consumer: str, finding: str):
    value = {
        "consumer": consumer,
        "findings": [finding],
        "evidence": ["fixture"],
        "unresolved_conditions": [],
    }
    value["sha256"] = checker.canonical_hash(value)
    return value


def completion(gate, unit_id: str, boundary_id: str, inbound, consumer: str, finding: str, kind: str = "declared-execution-unit"):
    planned = gate["decision"]["execution_plan"][0]
    return {
        "gate_sha256": gate["gate_sha256"],
        "target_state_id": gate["decision"]["target_state_id"],
        "passes": [
            {
                "pass_id": planned["pass_id"],
                "context_mode": planned["context_mode"],
                "status": "complete",
                "execution_unit_id": unit_id,
                "boundary": {"kind": kind, "id": boundary_id},
                "inbound_handoff_sha256": inbound,
                "handoff": handoff(consumer, finding),
            }
        ],
        "scratch_materialized": False,
        "scratch_cleanup_status": "not_applicable",
        "retained_subpass_artifacts": [],
    }


def base_record():
    a_gate = selector.build_gate(workload("Adversarial"), CAPABILITY)
    i_gate = selector.build_gate(workload("Interdependency"), CAPABILITY)
    a_completion = completion(
        a_gate,
        "unit-a",
        "message-a",
        None,
        "Interdependency",
        "Adversarial finding",
    )
    i_completion = completion(
        i_gate,
        "unit-i",
        "message-i",
        a_completion["passes"][0]["handoff"]["sha256"],
        "review-completion",
        "Interdependency finding",
    )
    return {
        "id": "current",
        "summary": "Boundary test",
        "change_classes": ["authority-or-propagation"],
        "claimed_earliest_stage": "Adversarial",
        "status": "in_progress",
        "review_revision": 7,
        "results": {"Adversarial": "supported", "Interdependency": "supported"},
        "execution_gates": {"Adversarial": a_gate, "Interdependency": i_gate},
        "execution_completions": {"Adversarial": a_completion, "Interdependency": i_completion},
    }


class PassBoundaryTests(unittest.TestCase):
    def test_valid_chain_passes(self):
        checker.validate_record(base_record(), MAPPING)

    def test_duplicate_execution_unit_rejected(self):
        value = base_record()
        value["execution_completions"]["Interdependency"]["passes"][0]["execution_unit_id"] = "unit-a"
        with self.assertRaisesRegex(ValueError, "duplicate execution_unit_id"):
            checker.validate_record(value, MAPPING)

    def test_duplicate_boundary_rejected(self):
        value = base_record()
        value["execution_completions"]["Interdependency"]["passes"][0]["boundary"]["id"] = "message-a"
        with self.assertRaisesRegex(ValueError, "duplicate execution boundary"):
            checker.validate_record(value, MAPPING)

    def test_broken_handoff_chain_rejected(self):
        value = base_record()
        value["execution_completions"]["Interdependency"]["passes"][0]["inbound_handoff_sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, "does not consume"):
            checker.validate_record(value, MAPPING)

    def test_tampered_handoff_rejected(self):
        value = base_record()
        value["execution_completions"]["Adversarial"]["passes"][0]["handoff"]["findings"][0] = "tampered"
        with self.assertRaisesRegex(ValueError, "handoff.sha256 is stale or invalid"):
            checker.validate_record(value, MAPPING)

    def test_later_stage_cannot_skip_earlier_stage(self):
        value = base_record()
        value["results"].pop("Adversarial")
        with self.assertRaisesRegex(ValueError, "before an earlier required stage"):
            checker.validate_record(value, MAPPING)

    def test_isolated_plan_requires_isolated_boundary(self):
        value = base_record()
        gate = value["execution_gates"]["Adversarial"]
        gate["decision"]["execution_plan"][0]["context_mode"] = "ISOLATED"
        value["execution_completions"]["Adversarial"]["passes"][0]["context_mode"] = "ISOLATED"
        with self.assertRaisesRegex(ValueError, "isolated-context"):
            checker.validate_record(value, MAPPING)

    def test_legacy_record_exempt(self):
        value = {"id": "legacy", "change_classes": ["authority-or-propagation"]}
        checker.validate_record(value, MAPPING)


if __name__ == "__main__":
    unittest.main()
