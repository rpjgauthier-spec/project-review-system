import unittest

from project_review_system.domain import (
    LineageToken,
    ProgramState,
    ReviewId,
    SnapshotId,
    SnapshotMode,
    Stage,
    StateSnapshot,
    WorkflowDefinitionId,
)


class DomainTests(unittest.TestCase):
    def test_id_rejects_blank_value(self) -> None:
        with self.assertRaises(ValueError):
            ReviewId("   ")

    def test_active_state_requires_stage_cursor(self) -> None:
        with self.assertRaises(ValueError):
            StateSnapshot(
                review_id=ReviewId("review:test"),
                program_state=ProgramState.ACTIVE,
                review_revision=0,
                snapshot_id=SnapshotId("snapshot:test"),
                snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
                workflow_definition_id=WorkflowDefinitionId("workflow:test"),
                stage_cursor=None,
                open_occurrence_id=None,
                lineage_token=LineageToken("lineage:0"),
            )

    def test_terminal_state_rejects_stage_cursor(self) -> None:
        with self.assertRaises(ValueError):
            StateSnapshot(
                review_id=ReviewId("review:test"),
                program_state=ProgramState.COMPLETE,
                review_revision=0,
                snapshot_id=SnapshotId("snapshot:test"),
                snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
                workflow_definition_id=WorkflowDefinitionId("workflow:test"),
                stage_cursor=Stage.END_TO_END_VALIDATION,
                open_occurrence_id=None,
                lineage_token=LineageToken("lineage:9"),
            )


if __name__ == "__main__":
    unittest.main()
