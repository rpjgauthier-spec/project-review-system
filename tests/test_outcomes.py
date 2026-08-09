import unittest

from project_review_system.outcomes import ErrorCode, OperationResult, OutcomeCode


class OutcomeTests(unittest.TestCase):
    def test_success_cannot_carry_error_code(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=True, outcome=ErrorCode.STALE_LINEAGE)

    def test_failure_cannot_carry_success_code(self) -> None:
        with self.assertRaises(ValueError):
            OperationResult(ok=False, outcome=OutcomeCode.PASS_OPENED)

    def test_commit_outcome_unknown_is_machine_readable(self) -> None:
        self.assertEqual(ErrorCode.COMMIT_OUTCOME_UNKNOWN.value, "commit_outcome_unknown")

    def test_integrity_error_is_machine_readable(self) -> None:
        self.assertEqual(ErrorCode.INTEGRITY_ERROR.value, "integrity_error")


if __name__ == "__main__":
    unittest.main()
