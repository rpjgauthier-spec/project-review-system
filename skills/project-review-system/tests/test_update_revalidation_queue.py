#!/usr/bin/env python3
"""Regression tests for update_revalidation_queue.py."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_revalidation_queue.py"
SPEC = importlib.util.spec_from_file_location("update_revalidation_queue", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

MAPPING = {
    "stages": ["Adversarial", "Interdependency", "Normalization", "Structural Optimization", "End-to-end validation"],
    "change_classes": {
        "authorization": {"stages": ["Adversarial", "End-to-end validation"], "evaluations": ["unauthorized-action"]},
        "status-or-schema": {"stages": ["Normalization", "Interdependency", "End-to-end validation"], "evaluations": ["status-semantics"]},
        "behavior-neutral": {"stages": [], "evaluations": ["confirm-behavior-neutral"]},
    },
}

GATED_MAPPING = {
    **MAPPING,
    "execution_gate": {"enabled": True, "legacy_exempt_change_ids": []},
}


def partial_record(target_state: str = "sha256:current") -> dict:
    return {
        "id": "partial",
        "summary": "Partial subdivided execution",
        "changed_files": ["artifact.txt", "skills/project-review-system/changes/partial.json"],
        "change_classes": ["authorization"],
        "claimed_earliest_stage": "Adversarial",
        "status": "in_progress",
        "review_revision": 3,
        "results": {},
        "execution_gates": {
            "Adversarial": {
                "gate_sha256": "gate-a",
            }
        },
        "execution_completions": {
            "Adversarial": {
                "gate_sha256": "gate-a",
                "target_state_id": target_state,
                "passes": [{"pass_id": "subpass-a", "status": "complete"}],
            }
        },
    }


class QueueRegressionTests(unittest.TestCase):
    def test_derives_earliest_stage_union_and_behavior(self) -> None:
        record = {"id": "change-1", "summary": "Change authorization and status meanings.", "change_classes": ["status-or-schema", "authorization"], "claimed_earliest_stage": "Adversarial", "status": "pending"}
        normalized = MODULE.normalize_record(record, MAPPING)
        self.assertTrue(normalized["derived_behavioral"])
        self.assertEqual(normalized["derived_stages"], ["Adversarial", "Interdependency", "Normalization", "End-to-end validation"])
        self.assertEqual(normalized["derived_earliest_stage"], "Adversarial")
        self.assertEqual(normalized["derived_evaluations"], ["status-semantics", "unauthorized-action"])

    def test_wrong_earliest_stage_is_rejected(self) -> None:
        record = {"id": "change-2", "summary": "Change authorization.", "change_classes": ["authorization"], "claimed_earliest_stage": "Interdependency", "status": "pending"}
        with self.assertRaisesRegex(ValueError, "derived stage is 'Adversarial'"):
            MODULE.normalize_record(record, MAPPING)

    def test_unknown_change_class_is_rejected(self) -> None:
        record = {"id": "change-3", "summary": "Unknown classification.", "change_classes": ["mystery"], "claimed_earliest_stage": "Adversarial", "status": "pending"}
        with self.assertRaisesRegex(ValueError, "unknown change class"):
            MODULE.normalize_record(record, MAPPING)

    def test_behavior_neutral_record_has_no_stage(self) -> None:
        record = {"id": "change-4", "summary": "Correct a spelling error.", "change_classes": ["behavior-neutral"], "claimed_earliest_stage": "None", "status": "complete", "results": {"confirm-behavior-neutral": "passed"}}
        normalized = MODULE.normalize_record(record, MAPPING)
        self.assertFalse(normalized["derived_behavioral"])
        self.assertEqual(normalized["derived_stages"], [])
        self.assertEqual(normalized["derived_earliest_stage"], "None")

    def test_behavior_neutral_cannot_mix_with_behavioral_class(self) -> None:
        record = {"id": "change-5", "summary": "Contradictory classification.", "change_classes": ["behavior-neutral", "authorization"], "claimed_earliest_stage": "Adversarial", "status": "pending"}
        with self.assertRaisesRegex(ValueError, "mixes behavior-neutral"):
            MODULE.normalize_record(record, MAPPING)

    def test_render_prompts_unresolved_work_and_canonical_suite(self) -> None:
        record = {"id": "change-6", "summary": "Change authorization.", "change_classes": ["authorization"], "claimed_earliest_stage": "Adversarial", "status": "pending", "results": {}}
        rendered = MODULE.render(MAPPING, [record])
        self.assertIn("## Final completion gate", rendered)
        self.assertIn("**OPEN:**", rendered)
        self.assertIn("before final completion or merge", rendered)
        self.assertIn("Ordered revalidation may continue", rendered)
        self.assertNotIn("## Advancement gate", rendered)
        self.assertNotIn("**BLOCKED:**", rendered)
        self.assertIn("derived from change classes", rendered)
        self.assertIn("Revalidate **Adversarial**", rendered)
        self.assertIn("Run evaluation `unauthorized-action`", rendered)
        self.assertIn("python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'", rendered)
        self.assertNotIn("test_validate_review_state.py", rendered)
        self.assertNotIn("test_update_revalidation_queue.py", rendered)
        self.assertNotIn("test_check_change_impact_coverage.py", rendered)

    def test_check_requires_explicit_base_and_head(self) -> None:
        with patch("sys.argv", ["update_revalidation_queue.py", "--check"]):
            self.assertEqual(MODULE.main(), 2)

    def test_complete_record_requires_all_results(self) -> None:
        record = {"id": "change-7", "summary": "Falsely claim completion.", "change_classes": ["authorization"], "claimed_earliest_stage": "Adversarial", "status": "complete", "results": {}}
        with self.assertRaisesRegex(ValueError, "is complete but lacks passing results"):
            MODULE.normalize_record(record, MAPPING)

    def test_complete_record_accepts_all_results(self) -> None:
        record = {"id": "change-8", "summary": "Complete authorization revalidation.", "change_classes": ["authorization"], "claimed_earliest_stage": "Adversarial", "status": "complete", "results": {"Adversarial": "supported", "End-to-end validation": "complete", "unauthorized-action": "passed"}}
        normalized = MODULE.normalize_record(record, MAPPING)
        self.assertEqual(normalized["derived_incomplete_results"], [])

    def test_collect_records_rejects_id_filename_mismatch(self) -> None:
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "current.json").write_text(json.dumps({"id": "historical"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "id must match filename stem"):
                MODULE.collect_records(directory)

    def test_escalated_record_requires_resumption_contract(self) -> None:
        record = {"id": "change-9", "summary": "Escalate an authorization concern.", "change_classes": ["authorization"], "claimed_earliest_stage": "Adversarial", "status": "escalated", "results": {}}
        with self.assertRaisesRegex(ValueError, "has no escalation object"):
            MODULE.normalize_record(record, MAPPING)

    def test_partial_completed_pass_requires_current_artifact_bound_gate(self) -> None:
        record = partial_record()
        with patch.object(MODULE, "current_record_target_state_id", return_value="sha256:current"), patch.object(
            MODULE.GATE_CHECKER,
            "validate_execution_gate",
            side_effect=ValueError("target state mismatch"),
        ) as validate_gate:
            with self.assertRaisesRegex(ValueError, "invalid execution gate"):
                MODULE.normalize_record(record, GATED_MAPPING)
        validate_gate.assert_called_once()

    def test_partial_completed_pass_rejects_stale_completion_target(self) -> None:
        record = partial_record(target_state="sha256:old")
        with patch.object(MODULE, "current_record_target_state_id", return_value="sha256:current"), patch.object(
            MODULE.GATE_CHECKER,
            "validate_execution_gate",
            return_value={},
        ):
            with self.assertRaisesRegex(ValueError, "completion target state does not match its execution gate"):
                MODULE.normalize_record(record, GATED_MAPPING)


if __name__ == "__main__":
    unittest.main()
