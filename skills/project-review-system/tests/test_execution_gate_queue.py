#!/usr/bin/env python3
"""Regression tests for execution-plan enforcement in the revalidation queue."""

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
    "execution_gate": {"enabled": True, "legacy_exempt_change_ids": ["legacy"]},
    "change_classes": {"authorization": {"stages": ["Adversarial", "End-to-end validation"], "evaluations": ["unauthorized-action"]}},
}


def workload(activity="Adversarial", revision=2, target="sha256:fixture"):
    return {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": activity,
        "target_state_id": target,
        "review_revision": revision,
        "workload_class": "ordinary-review-v1",
        "stage_assessment": {"single_pass_suitable": True, "reasons": ["bounded"], "subpasses": []},
        "fused_authorization": None,
    }


def record(record_id="current"):
    return {
        "id": record_id,
        "summary": "Test authorization change.",
        "changed_files": ["skills/project-review-system/tests/fixture.txt", f"skills/project-review-system/changes/{record_id}.json"],
        "change_classes": ["authorization"],
        "claimed_earliest_stage": "Adversarial",
        "status": "in_progress",
        "review_revision": 2,
        "results": {},
        "execution_gates": {},
        "execution_completions": {},
    }


def completion_for(gate):
    return {
        "gate_sha256": gate["gate_sha256"],
        "target_state_id": gate["decision"]["target_state_id"],
        "passes": [
            {"pass_id": p["pass_id"], "context_mode": p["context_mode"], "status": "complete"}
            for p in gate["decision"]["execution_plan"]
        ],
        "scratch_materialized": False,
        "scratch_cleanup_status": "not_applicable",
        "retained_subpass_artifacts": [],
    }


class QueueExecutionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_target = queue.current_record_target_state_id
        queue.current_record_target_state_id = lambda value: "sha256:fixture"

    def tearDown(self) -> None:
        queue.current_record_target_state_id = self.original_target

    def test_passing_stage_without_gate_is_rejected(self) -> None:
        value = record()
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "without a current execution gate"):
            queue.normalize_record(value, MAPPING)

    def test_passing_stage_without_completion_is_rejected(self) -> None:
        value = record()
        gate = selector.build_gate(workload(), CAPABILITY)
        value["execution_gates"]["Adversarial"] = gate
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "without an execution completion object"):
            queue.normalize_record(value, MAPPING)

    def test_valid_gate_and_completion_are_accepted(self) -> None:
        value = record()
        gate = selector.build_gate(workload(), CAPABILITY)
        value["execution_gates"]["Adversarial"] = gate
        value["execution_completions"]["Adversarial"] = completion_for(gate)
        value["results"]["Adversarial"] = "supported"
        normalized = queue.normalize_record(value, MAPPING)
        self.assertTrue(normalized["derived_execution_gate_required"])

    def test_wrong_completion_mode_is_rejected(self) -> None:
        value = record()
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["passes"][0]["context_mode"] = "ISOLATED"
        value["execution_gates"]["Adversarial"] = gate
        value["execution_completions"]["Adversarial"] = completion
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "wrong context mode"):
            queue.normalize_record(value, MAPPING)

    def test_stale_revision_is_rejected(self) -> None:
        value = record()
        gate = selector.build_gate(workload(revision=1), CAPABILITY)
        value["execution_gates"]["Adversarial"] = gate
        value["execution_completions"]["Adversarial"] = completion_for(gate)
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "review_revision 1 does not match"):
            queue.normalize_record(value, MAPPING)

    def test_materialized_scratch_without_cleanup_is_rejected(self) -> None:
        value = record()
        gate = selector.build_gate(workload(), CAPABILITY)
        completion = completion_for(gate)
        completion["scratch_materialized"] = True
        completion["scratch_cleanup_status"] = "pending"
        value["execution_gates"]["Adversarial"] = gate
        value["execution_completions"]["Adversarial"] = completion
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "must be deleted"):
            queue.normalize_record(value, MAPPING)

    def test_legacy_record_remains_exempt(self) -> None:
        value = record("legacy")
        value["results"]["Adversarial"] = "supported"
        normalized = queue.normalize_record(value, MAPPING)
        self.assertFalse(normalized["derived_execution_gate_required"])


if __name__ == "__main__":
    unittest.main()
