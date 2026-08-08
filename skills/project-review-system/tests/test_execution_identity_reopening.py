#!/usr/bin/env python3
"""Regression coverage for review-revision and durable execution-occurrence history."""

from __future__ import annotations

import copy
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


def ledger_entry(value):
    revision = value["review_revision"]
    stage = "Adversarial"
    gate_sha = value["execution_gates"][stage]["gate_sha256"]
    item = value["execution_completions"][stage]["passes"][0]
    return {
        "review_revision": revision,
        "stage": stage,
        "pass_id": item["pass_id"],
        "gate_sha256": gate_sha,
        "execution_unit_id": item["execution_unit_id"],
        "boundary": copy.deepcopy(item["boundary"]),
        "pass_evidence_sha256": checker.canonical_sha256(item),
    }


def preserved_without_live_completion(value):
    result = {"review_revision": value["review_revision"], "execution_gates": {}, "execution_completions": {}}
    result["execution_occurrence_history"] = [ledger_entry(value)]
    return result


class ExecutionIdentityReopeningTests(unittest.TestCase):
    def test_completed_pass_cannot_be_replaced_by_new_gate_in_same_revision(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        first["execution_occurrence_history"] = [ledger_entry(first)]
        replacement = completed(8, "gate-b", "unit-b", "boundary-b")
        replacement["execution_occurrence_history"] = [ledger_entry(first), ledger_entry(replacement)]
        with self.assertRaisesRegex(ValueError, "increment review_revision"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_stage_cannot_change_gate_by_renaming_pass_in_same_revision(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a", pass_id="stage-main")
        first["execution_occurrence_history"] = [ledger_entry(first)]
        replacement = completed(8, "gate-b", "unit-b", "boundary-b", pass_id="redo-main")
        replacement["execution_occurrence_history"] = [ledger_entry(first), ledger_entry(replacement)]
        with self.assertRaisesRegex(ValueError, "stage gate"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_pass_can_be_redone_after_revision_increment_with_new_identities(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        first["execution_occurrence_history"] = [ledger_entry(first)]
        replacement = completed(9, "gate-b", "unit-b", "boundary-b")
        replacement["execution_occurrence_history"] = [ledger_entry(first), ledger_entry(replacement)]
        checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_completed_stage_can_change_plan_after_revision_increment(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a", pass_id="stage-main")
        first["execution_occurrence_history"] = [ledger_entry(first)]
        replacement = completed(9, "gate-b", "unit-b", "boundary-b", pass_id="authorization")
        replacement["execution_occurrence_history"] = [ledger_entry(first), ledger_entry(replacement)]
        checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", replacement)])

    def test_final_state_must_preserve_observed_completion_in_ledger(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        cleared = {"review_revision": 8, "execution_gates": {}, "execution_completions": {}}
        with self.assertRaisesRegex(ValueError, "does not preserve completed occurrence"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", cleared)], require_final_ledger=True)

    def test_final_ledger_can_preserve_occurrence_after_live_completion_is_cleared(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        final = preserved_without_live_completion(first)
        checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", final)], require_final_ledger=True)

    def test_ledger_is_append_only_once_present(self):
        first = completed(8, "gate-a", "unit-a", "boundary-a")
        with_ledger = preserved_without_live_completion(first)
        removed = {"review_revision": 8, "execution_gates": {}, "execution_completions": {}, "execution_occurrence_history": []}
        with self.assertRaisesRegex(ValueError, "removes or mutates durable execution occurrence ledger"):
            checker.validate_identity_history_snapshots("current", [("c1", with_ledger), ("c2", removed)], require_final_ledger=True)

    def test_squash_like_base_ledger_blocks_future_identity_reuse(self):
        old = completed(8, "gate-a", "unit-shared", "boundary-a")
        base = preserved_without_live_completion(old)
        redo = completed(9, "gate-b", "unit-shared", "boundary-b")
        redo["execution_occurrence_history"] = [ledger_entry(old), ledger_entry(redo)]
        with self.assertRaisesRegex(ValueError, "reuses execution_unit_id"):
            checker.validate_identity_history_snapshots("current", [("base", base), ("head", redo)], require_final_ledger=True)


if __name__ == "__main__":
    unittest.main()
