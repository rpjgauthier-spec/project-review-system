#!/usr/bin/env python3
"""Regression tests for execution-gate enforcement in the revalidation queue."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = SKILL_ROOT / "scripts" / "update_revalidation_queue.py"
SELECTOR_PATH = SKILL_ROOT / "scripts" / "select_execution_policy.py"
DEFAULT_CAPABILITY_PATH = SKILL_ROOT / "config" / "default-execution-capability.json"

queue_spec = importlib.util.spec_from_file_location("queue_gate_test", QUEUE_PATH)
assert queue_spec and queue_spec.loader
queue = importlib.util.module_from_spec(queue_spec)
queue_spec.loader.exec_module(queue)

selector_spec = importlib.util.spec_from_file_location("selector_queue_gate_test", SELECTOR_PATH)
assert selector_spec and selector_spec.loader
selector = importlib.util.module_from_spec(selector_spec)
selector_spec.loader.exec_module(selector)

CAPABILITY = json.loads(DEFAULT_CAPABILITY_PATH.read_text(encoding="utf-8"))
MAPPING = {
    "stages": ["Adversarial", "End-to-end validation"],
    "execution_gate": {"legacy_exempt_change_ids": ["legacy"]},
    "change_classes": {
        "authorization": {
            "stages": ["Adversarial", "End-to-end validation"],
            "evaluations": ["unauthorized-action"],
        }
    },
}


def workload(activity="Adversarial", revision=2):
    return {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": activity,
        "review_revision": revision,
        "artifact_count": 2,
        "content_bytes": 2000,
        "remaining_stage_count": 2,
        "remaining_evaluation_count": 1,
        "dependency_count": 1,
        "protected_control_count": 0,
        "unresolved_uncertainty_count": 0,
        "material_findings_count": 0,
        "unexpected_dependency_count": 0,
        "self_referential": False,
        "exhaustive_claim": False,
        "checkpoint": "test",
    }


def record(record_id="current"):
    return {
        "id": record_id,
        "summary": "Test authorization change.",
        "change_classes": ["authorization"],
        "claimed_earliest_stage": "Adversarial",
        "status": "in_progress",
        "review_revision": 2,
        "results": {},
        "execution_gates": {},
    }


class QueueExecutionGateTests(unittest.TestCase):
    def test_passing_stage_without_gate_is_rejected(self) -> None:
        value = record()
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "without a current execution gate"):
            queue.normalize_record(value, MAPPING)

    def test_passing_stage_with_valid_gate_is_accepted(self) -> None:
        value = record()
        value["execution_gates"]["Adversarial"] = selector.build_gate(
            workload(), CAPABILITY
        )
        value["results"]["Adversarial"] = "supported"
        normalized = queue.normalize_record(value, MAPPING)
        self.assertTrue(normalized["derived_execution_gate_required"])

    def test_reopening_revision_invalidates_old_gate(self) -> None:
        value = record()
        value["execution_gates"]["Adversarial"] = selector.build_gate(
            workload(revision=1), CAPABILITY
        )
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "review_revision 1 does not match current review revision 2"):
            queue.normalize_record(value, MAPPING)

    def test_gate_for_wrong_stage_is_rejected(self) -> None:
        value = record()
        value["execution_gates"]["Adversarial"] = selector.build_gate(
            workload(activity="End-to-end validation"), CAPABILITY
        )
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "does not match expected"):
            queue.normalize_record(value, MAPPING)

    def test_legacy_record_remains_exempt(self) -> None:
        value = record("legacy")
        value["results"]["Adversarial"] = "supported"
        normalized = queue.normalize_record(value, MAPPING)
        self.assertFalse(normalized["derived_execution_gate_required"])


if __name__ == "__main__":
    unittest.main()
