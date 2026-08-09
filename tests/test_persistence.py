import unittest

from project_review_system.domain import (
    InitializationIntentId,
    LineageToken,
    ProgramState,
    ReviewId,
    SnapshotId,
    SnapshotMode,
    Stage,
    StateSnapshot,
    WorkflowDefinitionId,
)
from project_review_system.persistence import (
    AuthoritativeRecord,
    CreateResult,
    InitializationCommit,
    TransitionCommit,
    TransitionResult,
)


class PersistenceContractTests(unittest.TestCase):
    def _state(self) -> StateSnapshot:
        return StateSnapshot(
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

    def test_authoritative_record_bundles_state_and_history_coherently(self) -> None:
        state = self._state()
        record = AuthoritativeRecord(state=state, immutable_history=("event:1",))

        self.assertIs(record.state, state)
        self.assertEqual(record.immutable_history, ("event:1",))

    def test_authoritative_record_rejects_wrong_state_and_mutable_history(self) -> None:
        with self.assertRaises(ValueError):
            AuthoritativeRecord(state="bad", immutable_history=())  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            AuthoritativeRecord(state=self._state(), immutable_history=["event:1"])  # type: ignore[arg-type]

    def test_initialization_commit_validates_all_declared_fields(self) -> None:
        state = self._state()
        with self.assertRaises(ValueError):
            InitializationCommit(state="bad", initialization_intent_id=InitializationIntentId("intent:1"))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            InitializationCommit(state=state, initialization_intent_id="intent:1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            InitializationCommit(
                state=state,
                initialization_intent_id=InitializationIntentId("intent:1"),
                immutable_events=["event:1"],  # type: ignore[arg-type]
            )

    def test_transition_commit_validates_all_declared_fields(self) -> None:
        state = self._state()
        with self.assertRaises(ValueError):
            TransitionCommit(review_id="review:test", next_state=state)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            TransitionCommit(review_id=ReviewId("review:test"), next_state="bad")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            TransitionCommit(
                review_id=ReviewId("review:test"),
                next_state=state,
                immutable_events=["event:1"],  # type: ignore[arg-type]
            )
        with self.assertRaises(ValueError):
            TransitionCommit(
                review_id=ReviewId("review:test"),
                next_state=state,
                immutable_evidence=["evidence:1"],  # type: ignore[arg-type]
            )

    def test_transition_commit_rejects_cross_review_state(self) -> None:
        with self.assertRaises(ValueError):
            TransitionCommit(
                review_id=ReviewId("review:other"),
                next_state=self._state(),
            )

    def test_create_result_requires_real_bool_and_state_snapshot(self) -> None:
        state = self._state()
        with self.assertRaises(ValueError):
            CreateResult(created=1, state=state)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            CreateResult(created=True, state="bad")  # type: ignore[arg-type]

    def test_transition_result_requires_real_bool_and_state_snapshot(self) -> None:
        state = self._state()
        with self.assertRaises(ValueError):
            TransitionResult(committed=1, state=state)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            TransitionResult(committed=True, state="bad")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
