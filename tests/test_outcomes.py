import unittest

from project_review_system.domain import LineageToken, ReviewId
from project_review_system.outcomes import ErrorCode, OperationResult, OutcomeCode


class OutcomeTests(unittest.TestCase):
    def test_success_cannot_carry_error_code(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=ErrorCode.STALE_LINEAGE)

    def test_failure_cannot_carry_success_code(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=False, outcome=OutcomeCode.PASS_OPENED)

    def test_ok_must_be_real_bool(self) -> None:
        for value in (1, 0, "true", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    OperationResult(ok=value, outcome=OutcomeCode.STATUS)  # type: ignore[arg-type]

    def test_outcome_must_use_closed_enum_taxonomy(self) -> None:
        for value in ("status", "stale_lineage", "unknown"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    OperationResult(ok=True, outcome=value)  # type: ignore[arg-type]

    def test_optional_identity_fields_are_runtime_validated(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=OutcomeCode.STATUS, review_id="review:raw")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=OutcomeCode.STATUS, lineage_token="lineage:raw")  # type: ignore[arg-type]

    def test_data_must_be_mapping(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=OutcomeCode.STATUS, data=[])  # type: ignore[arg-type]

        result = OperationResult(
            ok=True,
            outcome=OutcomeCode.STATUS,
            review_id=ReviewId("review:test"),
            lineage_token=LineageToken("lineage:test"),
            data={"status": "active"},
        )
        self.assertEqual(result.data["status"], "active")

    def test_commit_outcome_unknown_is_machine_readable(self) -> None:
        self.assertEqual(ErrorCode.COMMIT_OUTCOME_UNKNOWN.value, "commit_outcome_unknown")

    def test_integrity_error_is_machine_readable(self) -> None:
        self.assertEqual(ErrorCode.INTEGRITY_ERROR.value, "integrity_error")


if __name__ == "__main__":
    unittest.main()
