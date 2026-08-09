import inspect
import unittest

from project_review_system.domain import (
    InitializationIntentId, LineageToken, ProgramState, ReviewId, SnapshotId,
    SnapshotMode, Stage, StateSnapshot, WorkflowDefinitionId,
)
from project_review_system.persistence import (
    AuthoritativeRecord, CreateResult, InitializationCommit, PersistenceBackend,
    PersistenceOutcome, TransitionCommit, TransitionResult,
)


class PersistenceContractTests(unittest.TestCase):
    def _state(self, review_id: str = "review:test") -> StateSnapshot:
        return StateSnapshot(
            review_id=ReviewId(review_id), program_state=ProgramState.ACTIVE, review_revision=0,
            snapshot_id=SnapshotId("snapshot:test"), snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
            workflow_definition_id=WorkflowDefinitionId("workflow:test"), stage_cursor=Stage.ADVERSARIAL,
            open_occurrence_id=None, lineage_token=LineageToken("lineage:0"),
        )

    def test_authoritative_record_requires_coherent_state(self):
        state = self._state()
        self.assertIs(AuthoritativeRecord(state).state, state)
        with self.assertRaises(ValueError): AuthoritativeRecord("bad")
        with self.assertRaises(ValueError): AuthoritativeRecord(state, ["event"])

    def test_history_and_evidence_reject_mutable_members(self):
        state = self._state()
        mutable_value = bytearray(b"mutable")
        with self.assertRaises(ValueError): AuthoritativeRecord(state, (mutable_value,))
        with self.assertRaises(ValueError):
            InitializationCommit(
                ReviewId("review:test"), state, InitializationIntentId("intent:1"),
                immutable_events=(mutable_value,),
            )
        with self.assertRaises(ValueError):
            TransitionCommit(ReviewId("review:test"), state, immutable_evidence=(mutable_value,))
        record = AuthoritativeRecord(state, ("audit:event",))
        self.assertEqual(record.immutable_history, ("audit:event",))

    def test_initialization_commit_binds_review(self):
        state = self._state()
        commit = InitializationCommit(ReviewId("review:test"), state, InitializationIntentId("intent:1"))
        self.assertEqual(commit.review_id, state.review_id)
        with self.assertRaises(ValueError):
            InitializationCommit(ReviewId("review:other"), state, InitializationIntentId("intent:1"))

    def test_transition_commit_binds_review(self):
        state = self._state()
        TransitionCommit(ReviewId("review:test"), state)
        with self.assertRaises(ValueError): TransitionCommit(ReviewId("review:other"), state)

    def test_persistence_results_preserve_outcome_distinctions(self):
        state = self._state()
        self.assertEqual(CreateResult(PersistenceOutcome.CREATED, state).outcome, PersistenceOutcome.CREATED)
        self.assertEqual(CreateResult(PersistenceOutcome.OUTCOME_UNKNOWN, None).outcome, PersistenceOutcome.OUTCOME_UNKNOWN)
        self.assertEqual(TransitionResult(PersistenceOutcome.CONFLICT, state).outcome, PersistenceOutcome.CONFLICT)
        self.assertEqual(TransitionResult(PersistenceOutcome.ALREADY_APPLIED, state).outcome, PersistenceOutcome.ALREADY_APPLIED)
        self.assertEqual(TransitionResult(PersistenceOutcome.OUTCOME_UNKNOWN, None).outcome, PersistenceOutcome.OUTCOME_UNKNOWN)
        with self.assertRaises(ValueError): CreateResult(PersistenceOutcome.COMMITTED, state)
        with self.assertRaises(ValueError): TransitionResult(PersistenceOutcome.COMMITTED, None)

    def test_protocol_exposes_frozen_readback_and_review_binding(self):
        names = {name for name, _ in inspect.getmembers(PersistenceBackend, inspect.isfunction)}
        self.assertTrue({"read", "create_if_absent", "commit_transition", "read_occurrence", "read_completion", "read_initialization"}.issubset(names))
        parameters = list(inspect.signature(PersistenceBackend.commit_transition).parameters)
        self.assertEqual(parameters[:4], ["self", "review_id", "expected_lineage_token", "commit"])


if __name__ == "__main__": unittest.main()
