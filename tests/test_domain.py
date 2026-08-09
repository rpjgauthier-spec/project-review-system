import unittest

from project_review_system.domain import (
    LineageToken,
    OccurrenceId,
    ProgramState,
    ReviewId,
    SnapshotId,
    SnapshotMode,
    Stage,
    StateSnapshot,
    WorkflowDefinitionId,
)


class DomainTests(unittest.TestCase):
    def _snapshot(
        self,
        *,
        program_state: ProgramState = ProgramState.ACTIVE,
        review_revision: int = 0,
        stage_cursor: Stage | None = Stage.ADVERSARIAL,
        open_occurrence_id: OccurrenceId | None = None,
    ) -> StateSnapshot:
        return StateSnapshot(
            review_id=ReviewId("review:test"),
            program_state=program_state,
            review_revision=review_revision,
            snapshot_id=SnapshotId("snapshot:test"),
            snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
            workflow_definition_id=WorkflowDefinitionId("workflow:test"),
            stage_cursor=stage_cursor,
            open_occurrence_id=open_occurrence_id,
            lineage_token=LineageToken("lineage:0"),
        )

    def test_id_rejects_blank_value(self) -> None:
        with self.assertRaises(ValueError):
            ReviewId("   ")

    def test_active_state_requires_stage_cursor(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(stage_cursor=None)

    def test_terminal_state_rejects_stage_cursor(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(
                program_state=ProgramState.COMPLETE,
                stage_cursor=Stage.END_TO_END_VALIDATION,
            )

    def test_terminal_state_rejects_open_occurrence(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(
                program_state=ProgramState.COMPLETE,
                stage_cursor=None,
                open_occurrence_id=OccurrenceId("occurrence:test"),
            )

    def test_review_revision_rejects_bool(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(review_revision=True)

    def test_review_revision_rejects_non_integer(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(review_revision="1")  # type: ignore[arg-type]

    def test_draft_state_is_reserved_and_non_constructible(self) -> None:
        with self.assertRaises(ValueError):
            self._snapshot(program_state=ProgramState.DRAFT, stage_cursor=None)


if __name__ == "__main__":
    unittest.main()
