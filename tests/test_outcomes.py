import unittest

import project_review_system as prs
from project_review_system.domain import (
    GateId, LineageToken, OccurrenceId, ReviewId, Stage, _controller_derived_id,
)
from project_review_system.outcomes import (
    BeginPassData, ErrorCode, InitializationData, OperationResult, OutcomeCode,
    RepairData, StatusData,
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
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=OutcomeCode.STATUS, data={"status": "active"})  # type: ignore[arg-type]
        result = OperationResult(
            ok=True, outcome=OutcomeCode.STATUS, review_id=ReviewId("review:test"),
            lineage_token=LineageToken("lineage:test"),
            data=StatusData(review_id=ReviewId("review:test"), next_stage=Stage.ADVERSARIAL),
        )
        self.assertEqual(result.data.next_stage, Stage.ADVERSARIAL)

    def test_success_outcome_requires_compatible_payload_type(self):
        with self.assertRaises(ValueError):
            OperationResult(
                ok=True, outcome=OutcomeCode.STATUS,
                data=RepairData(changed=False),
            )
        begin = BeginPassData(
            _controller_derived_id(OccurrenceId, "occ:1"),
            _controller_derived_id(GateId, "gate:1"),
        )
        result = OperationResult(ok=True, outcome=OutcomeCode.PASS_OPENED, data=begin)
        self.assertIs(result.data, begin)

    def test_result_and_payload_review_identity_must_match(self):
        with self.assertRaises(ValueError):
            OperationResult(
                ok=True, outcome=OutcomeCode.STATUS, review_id=ReviewId("review:A"),
                data=StatusData(review_id=ReviewId("review:B"), next_stage=Stage.ADVERSARIAL),
            )
        with self.assertRaises(ValueError):
            OperationResult(
                ok=True, outcome=OutcomeCode.INITIALIZED, review_id=ReviewId("review:A"),
                data=InitializationData(review_id=ReviewId("review:B")),
            )

    def test_error_field_matches_failure_outcome(self):
        with self.assertRaises(ValueError):
            OperationResult(ok=False, outcome=ErrorCode.STALE_LINEAGE, error=ErrorCode.INTEGRITY_ERROR)
        result = OperationResult(ok=False, outcome=ErrorCode.STALE_LINEAGE, error=ErrorCode.STALE_LINEAGE)
        self.assertEqual(result.error, ErrorCode.STALE_LINEAGE)

    def test_repair_payload_requires_real_bool(self):
        payload = RepairData(changed=False)
        self.assertFalse(payload.changed)

    def test_package_root_exports_only_declared_module_surface(self):
        self.assertIs(prs.OperationResult, OperationResult)
        self.assertTrue(hasattr(prs, "PersistenceBackend"))
        for leaked_name in ("Generic", "TypeVar", "Protocol", "runtime_checkable"):
            self.assertFalse(hasattr(prs, leaked_name), leaked_name)


if __name__ == "__main__": unittest.main()
