#!/usr/bin/env python3
"""Regression tests for declared pass boundaries and handoff chaining."""

from __future__ import annotations

import copy
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
        "authority-or-propagation": {"stages": ["Adversarial", "Interdependency"], "evaluations": []}
    },
}


def workload(activity: str, subdivided: bool = False):
    assessment = (
        {
            "single_pass_suitable": False,
            "reasons": ["requires subdivision"],
            "subpasses": [
                {"pass_id": "authorization", "scope": "authorization", "isolation_required": False, "reasons": []},
                {"pass_id": "trust-boundary", "scope": "trust boundary", "isolation_required": True, "reasons": ["fresh context"]},
            ],
        }
        if subdivided
        else {"single_pass_suitable": True, "reasons": ["bounded"], "subpasses": []}
    )
    return {
        "schema_version": 1,
        "reviewer_subject_id": "test-reviewer",
        "activity": activity,
        "target_state_id": "sha256:fixture",
        "review_revision": 7,
        "workload_class": "boundary-test-v1",
        "stage_assessment": assessment,
        "fused_authorization": None,
    }


def handoff(consumer: str, finding: str):
    value = {"consumer": consumer, "findings": [finding], "evidence": ["fixture"], "unresolved_conditions": []}
    value["sha256"] = checker.canonical_hash(value)
    return value


def pass_item(planned, unit_id: str, boundary_id: str, inbound, consumer: str, finding: str, kind: str | None = None):
    context_mode = planned["context_mode"]
    boundary_kind = kind or ("isolated-context" if context_mode == "ISOLATED" else "declared-execution-unit")
    return {
        "pass_id": planned["pass_id"],
        "context_mode": context_mode,
        "status": "complete",
        "execution_unit_id": unit_id,
        "boundary": {"kind": boundary_kind, "id": boundary_id},
        "inbound_handoff_sha256": inbound,
        "handoff": handoff(consumer, finding),
    }


def completion(gate, passes):
    return {
        "gate_sha256": gate["gate_sha256"],
        "target_state_id": gate["decision"]["target_state_id"],
        "passes": passes,
        "scratch_materialized": False,
        "scratch_cleanup_status": "not_applicable",
        "retained_subpass_artifacts": [],
    }


def base_record():
    a_gate = selector.build_gate(workload("Adversarial"), CAPABILITY)
    i_gate = selector.build_gate(workload("Interdependency"), CAPABILITY)
    a_plan = a_gate["decision"]["execution_plan"][0]
    a_item = pass_item(a_plan, "unit-a", "message-a", None, "Interdependency", "Adversarial finding")
    i_plan = i_gate["decision"]["execution_plan"][0]
    i_item = pass_item(i_plan, "unit-i", "message-i", a_item["handoff"]["sha256"], "review-completion", "Interdependency finding")
    return {
        "id": "current",
        "change_classes": ["authority-or-propagation"],
        "status": "in_progress",
        "review_revision": 7,
        "results": {"Adversarial": "supported", "Interdependency": "supported"},
        "execution_gates": {"Adversarial": a_gate, "Interdependency": i_gate},
        "execution_completions": {"Adversarial": completion(a_gate, [a_item]), "Interdependency": completion(i_gate, [i_item])},
    }


def history_snapshots():
    current = base_record()
    initial = copy.deepcopy(current)
    initial["results"] = {}
    initial["execution_gates"] = {}
    initial["execution_completions"] = {}
    gate_a = copy.deepcopy(initial)
    gate_a["execution_gates"]["Adversarial"] = copy.deepcopy(current["execution_gates"]["Adversarial"])
    complete_a = copy.deepcopy(gate_a)
    complete_a["execution_completions"]["Adversarial"] = copy.deepcopy(current["execution_completions"]["Adversarial"])
    result_a = copy.deepcopy(complete_a)
    result_a["results"]["Adversarial"] = "supported"
    gate_i = copy.deepcopy(result_a)
    gate_i["execution_gates"]["Interdependency"] = copy.deepcopy(current["execution_gates"]["Interdependency"])
    complete_i = copy.deepcopy(gate_i)
    complete_i["execution_completions"]["Interdependency"] = copy.deepcopy(current["execution_completions"]["Interdependency"])
    return [("c0", initial), ("c1", gate_a), ("c2", complete_a), ("c3", result_a), ("c4", gate_i), ("c5", complete_i), ("c6", current)]


def subdivided_states():
    gate = selector.build_gate(workload("Adversarial", subdivided=True), CAPABILITY)
    plan = gate["decision"]["execution_plan"]
    first = pass_item(plan[0], "unit-sub-a", "message-sub-a", None, "Adversarial:trust-boundary", "authorization finding")
    second = pass_item(plan[1], "unit-sub-b", "context-sub-b", first["handoff"]["sha256"], "Interdependency", "trust finding")
    initial = {"id": "current", "change_classes": ["authority-or-propagation"], "status": "in_progress", "review_revision": 7, "results": {}, "execution_gates": {}, "execution_completions": {}}
    gate_state = copy.deepcopy(initial)
    gate_state["execution_gates"]["Adversarial"] = gate
    first_state = copy.deepcopy(gate_state)
    first_state["execution_completions"]["Adversarial"] = completion(gate, [first])
    second_state = copy.deepcopy(first_state)
    second_state["execution_completions"]["Adversarial"] = completion(gate, [first, second])
    result_state = copy.deepcopy(second_state)
    result_state["results"]["Adversarial"] = "supported"
    return gate, [("c0", initial), ("c1", gate_state), ("c2", first_state), ("c3", second_state), ("c4", result_state)]


class PassBoundaryTests(unittest.TestCase):
    def test_valid_chain_passes(self):
        checker.validate_record(base_record(), MAPPING)

    def test_valid_durable_history_passes(self):
        checker.validate_history_snapshots(base_record(), MAPPING, history_snapshots())

    def test_subdivided_stage_can_record_passes_sequentially_before_stage_result(self):
        _, states = subdivided_states()
        checker.validate_record(states[2][1], MAPPING)
        checker.validate_record(states[3][1], MAPPING)
        checker.validate_record(states[4][1], MAPPING)
        checker.validate_history_snapshots(states[4][1], MAPPING, states)

    def test_subdivided_completion_must_be_plan_prefix(self):
        _, states = subdivided_states()
        value = copy.deepcopy(states[3][1])
        value["execution_completions"]["Adversarial"]["passes"] = [value["execution_completions"]["Adversarial"]["passes"][1]]
        with self.assertRaisesRegex(ValueError, "does not match plan"):
            checker.validate_record(value, MAPPING)

    def test_stage_result_requires_full_plan(self):
        _, states = subdivided_states()
        value = copy.deepcopy(states[2][1])
        value["results"]["Adversarial"] = "supported"
        with self.assertRaisesRegex(ValueError, "full execution plan"):
            checker.validate_record(value, MAPPING)

    def test_two_passes_first_completed_in_same_commit_are_rejected(self):
        _, states = subdivided_states()
        snapshots = [states[0], states[1], states[3], states[4]]
        with self.assertRaisesRegex(ValueError, "same or an earlier change-record commit"):
            checker.validate_history_snapshots(states[4][1], MAPPING, snapshots)

    def test_gate_must_preexist_pass_completion(self):
        value = base_record()
        initial = history_snapshots()[0][1]
        bad = copy.deepcopy(initial)
        bad["execution_gates"]["Adversarial"] = copy.deepcopy(value["execution_gates"]["Adversarial"])
        bad["execution_completions"]["Adversarial"] = copy.deepcopy(value["execution_completions"]["Adversarial"])
        with self.assertRaisesRegex(ValueError, "gate did not exist in the prior durable"):
            checker.validate_history_snapshots(bad, MAPPING, [("c0", initial), ("c1", bad)])

    def test_duplicate_execution_unit_rejected(self):
        value = base_record()
        value["execution_completions"]["Interdependency"]["passes"][0]["execution_unit_id"] = "unit-a"
        with self.assertRaisesRegex(ValueError, "duplicate execution_unit_id"):
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

    def test_later_stage_cannot_start_before_prior_stage_result(self):
        value = base_record()
        value["results"].pop("Adversarial")
        with self.assertRaisesRegex(ValueError, "before the prior required stage"):
            checker.validate_record(value, MAPPING)

    def test_isolated_plan_requires_isolated_boundary(self):
        _, states = subdivided_states()
        value = copy.deepcopy(states[3][1])
        value["execution_completions"]["Adversarial"]["passes"][1]["boundary"]["kind"] = "declared-execution-unit"
        with self.assertRaisesRegex(ValueError, "isolated-context"):
            checker.validate_record(value, MAPPING)

    def test_legacy_record_exempt(self):
        checker.validate_record({"id": "legacy", "change_classes": ["authority-or-propagation"]}, MAPPING)


if __name__ == "__main__":
    unittest.main()
