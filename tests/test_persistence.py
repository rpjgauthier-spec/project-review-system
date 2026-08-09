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
from project_review_system.persistence import AuthoritativeRecord


class PersistenceContractTests(unittest.TestCase):
    def test_authoritative_record_bundles_state_and_history_coherently(self) -> None:
        state = StateSnapshot(
            review_id=ReviewId("review:test"),
            program_state=ProgramState.ACTIVE,
            review_revision=0,
            snapshot_id=SnapshotId("snapshot:test"),
            snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
            workflow_definition_id=WorkflowDefinitionId("workflow:test"),
            stage_cursor=Stage.ADVERSARIAL,
            open_occurrence_id=None,
            lineage_token=LineageToken("lineage:0"),
        )
        record = AuthoritativeRecord(state=state, immutable_history=("event:1",))

        self.assertIs(record.state, state)
        self.assertEqual(record.immutable_history, ("event:1",))


if __name__ == "__main__":
    unittest.main()
