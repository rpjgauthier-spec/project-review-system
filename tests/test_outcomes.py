import unittest

from project_review_system.domain import LineageToken, ReviewId, Stage
from project_review_system.outcomes import (
    ErrorCode, OperationResult, OutcomeCode, RepairData, StatusData,
)


class OutcomeTests(unittest.TestCase):
    def test_frozen_error_names_are_preserved(self):
        self.assertEqual(ErrorCode.TERMINAL_STATE.value, "terminal_state")
        self.assertEqual(ErrorCode.CONFLICTING_COMPLETION.value, "conflicting_completion")
        self.assertEqual(ErrorCode.INVALID_SEMANTIC_RESULT.value, "invalid_semantic_result")
        self.assertEqual(ErrorCode.COMMIT_OUTCOME_UNKNOWN.value, "commit_outcome_unknown")

    def test_success_and_failure_taxonomy_are_coherent(self):
        with self.assertRaises(ValueError): OperationResult(ok=True, outcome=ErrorCode.STALE_LINEAGE)
        with self.assertRaises(ValueError): OperationResult(ok=False, outcome=OutcomeCode.STATUS)
        with self.assertRaises(ValueError): OperationResult(ok=1, outcome=OutcomeCode.STATUS)  # type: ignore[arg-type]
        with self.assertRaises(ValueError): OperationResult(ok=True, outcome="status")  # type: ignore[arg-type]

    def test_data_requires_typed_payload(self):
        with self.assertRaises(ValueError): OperationResult(ok=True, outcome=OutcomeCode.STATUS, data={"status": "active"})  # type: ignore[arg-type]
        result = OperationResult(
            ok=True, outcome=OutcomeCode.STATUS, review_id=ReviewId("review:test"),
            lineage_token=LineageToken("lineage:test"),
            data=StatusData(review_id=ReviewId("review:test"), next_stage=Stage.ADVERSARIAL),
        )
        self.assertEqual(result.data.next_stage, Stage.ADVERSARIAL)

    def test_error_field_matches_failure_outcome(self):
        with self.assertRaises(ValueError):
            OperationResult(ok=False, outcome=ErrorCode.STALE_LINEAGE, error=ErrorCode.INTEGRITY_ERROR)
        result = OperationResult(ok=False, outcome=ErrorCode.STALE_LINEAGE, error=ErrorCode.STALE_LINEAGE)
        self.assertEqual(result.error, ErrorCode.STALE_LINEAGE)

    def test_repair_payload_requires_real_bool(self):
        payload = RepairData(changed=False)
        self.assertFalse(payload.changed)


if __name__ == "__main__": unittest.main()
