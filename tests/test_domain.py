import unittest

from project_review_system.domain import (
    AuditEventId, CompletionEvidence, GateId, InitializationIntentId, InitializationRecord,
    LineageToken, OccurrenceId, OccurrenceStatus, PassOccurrence, ProgramState, ReviewId,
    SemanticResult, SemanticResultId, SemanticVerdict, SnapshotId, SnapshotMode, Stage,
    StateSnapshot, WorkflowDefinitionId,
)


class DomainTests(unittest.TestCase):
    def _snapshot(self, *, program_state=ProgramState.ACTIVE, review_revision=0, stage_cursor=Stage.ADVERSARIAL, open_occurrence_id=None):
        return StateSnapshot(
            review_id=ReviewId("review:test"), program_state=program_state, review_revision=review_revision,
            snapshot_id=SnapshotId("snapshot:test"), snapshot_mode=SnapshotMode.CANONICAL_CLEAN,
            workflow_definition_id=WorkflowDefinitionId("workflow:test"), stage_cursor=stage_cursor,
            open_occurrence_id=open_occurrence_id, lineage_token=LineageToken("lineage:0"),
        )

    def test_plain_id_serialization_boundary(self):
        value = ReviewId.from_string("review:test")
        self.assertEqual(value.to_string(), "review:test")

    def test_controller_derived_ids_reject_ordinary_construction(self):
        for cls in (OccurrenceId, GateId, SemanticResultId, AuditEventId):
            with self.subTest(cls=cls.__name__):
                with self.assertRaises(ValueError): cls("fabricated")
                self.assertEqual(cls.derived("derived").to_string(), "derived")
                self.assertEqual(cls.from_string("persisted").to_string(), "persisted")

    def test_state_runtime_invariants(self):
        with self.assertRaises(ValueError): self._snapshot(stage_cursor=None)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.COMPLETE, stage_cursor=Stage.END_TO_END_VALIDATION)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.COMPLETE, stage_cursor=None, open_occurrence_id=OccurrenceId.derived("o"))
        with self.assertRaises(ValueError): self._snapshot(review_revision=True)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.DRAFT, stage_cursor=None)

    def test_pass_occurrence_completion_binding(self):
        common = dict(
            occurrence_id=OccurrenceId.derived("occ:1"), review_id=ReviewId("review:test"),
            workflow_definition_id=WorkflowDefinitionId("workflow:test"), review_revision=0,
            snapshot_id=SnapshotId("snapshot:test"), stage=Stage.ADVERSARIAL,
            parent_lineage_token=LineageToken("lineage:0"), gate_id=GateId.derived("gate:1"),
        )
        with self.assertRaises(ValueError):
            PassOccurrence(**common, status=OccurrenceStatus.COMPLETED)
        completed = PassOccurrence(**common, status=OccurrenceStatus.COMPLETED, semantic_result_id=SemanticResultId.derived("result:1"))
        self.assertEqual(completed.status, OccurrenceStatus.COMPLETED)

    def test_semantic_and_evidence_models_are_typed(self):
        result = SemanticResult(Stage.ADVERSARIAL, SemanticVerdict.SUPPORTED, (), (), ())
        self.assertEqual(result.verdict, SemanticVerdict.SUPPORTED)
        evidence = CompletionEvidence(OccurrenceId.derived("occ:1"), SemanticResultId.derived("result:1"), "{}", ("stage",), LineageToken("lineage:1"))
        self.assertEqual(evidence.resulting_lineage_token, LineageToken("lineage:1"))
        init = InitializationRecord(ReviewId("review:test"), InitializationIntentId("intent:1"), WorkflowDefinitionId("workflow:test"), SnapshotId("snapshot:test"), 0, Stage.ADVERSARIAL, LineageToken("lineage:1"))
        self.assertEqual(init.initial_review_revision, 0)


if __name__ == "__main__": unittest.main()
