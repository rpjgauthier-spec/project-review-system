import unittest

import project_review_system
from project_review_system.domain import (
    AuditEventId, BeginPassRequest, CompletePassRequest, CompletionEvidence, GateId,
    InitializationIntentId, InitializationRecord, InitializeReviewRequest, LineageToken,
    OccurrenceId, OccurrenceStatus, PassOccurrence, ProgramState, RepairKind, RepairRequest,
    ReviewId, SemanticResult, SemanticResultId, SemanticVerdict, SnapshotId, SnapshotMode,
    Stage, StateSnapshot, WorkflowDefinitionId, _controller_derived_id,
    _deserialize_controller_derived_id,
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

    def test_controller_derived_ids_require_internal_boundary(self):
        for cls in (OccurrenceId, GateId, SemanticResultId, AuditEventId):
            with self.subTest(cls=cls.__name__):
                with self.assertRaises(ValueError):
                    cls("fabricated")
                self.assertFalse(hasattr(cls, "derived"))
                self.assertFalse(hasattr(cls, "from_string"))
                self.assertEqual(_controller_derived_id(cls, "derived").to_string(), "derived")
                self.assertEqual(_deserialize_controller_derived_id(cls, "persisted").to_string(), "persisted")
        self.assertFalse(hasattr(project_review_system, "_controller_derived_id"))
        self.assertFalse(hasattr(project_review_system, "_deserialize_controller_derived_id"))

    def test_state_runtime_invariants(self):
        with self.assertRaises(ValueError): self._snapshot(stage_cursor=None)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.COMPLETE, stage_cursor=Stage.END_TO_END_VALIDATION)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.COMPLETE, stage_cursor=None, open_occurrence_id=_controller_derived_id(OccurrenceId, "o"))
        with self.assertRaises(ValueError): self._snapshot(review_revision=True)
        with self.assertRaises(ValueError): self._snapshot(program_state=ProgramState.DRAFT, stage_cursor=None)

    def test_pass_occurrence_completion_binding(self):
        common = dict(
            occurrence_id=_controller_derived_id(OccurrenceId, "occ:1"), review_id=ReviewId("review:test"),
            workflow_definition_id=WorkflowDefinitionId("workflow:test"), review_revision=0,
            snapshot_id=SnapshotId("snapshot:test"), stage=Stage.ADVERSARIAL,
            parent_lineage_token=LineageToken("lineage:0"), gate_id=_controller_derived_id(GateId, "gate:1"),
        )
        with self.assertRaises(ValueError):
            PassOccurrence(**common, status=OccurrenceStatus.COMPLETED)
        with self.assertRaises(ValueError):
            PassOccurrence(**common, status=OccurrenceStatus.FAILED, semantic_result_id=_controller_derived_id(SemanticResultId, "result:failed"))
        completed = PassOccurrence(
            **common, status=OccurrenceStatus.COMPLETED,
            semantic_result_id=_controller_derived_id(SemanticResultId, "result:1"),
        )
        self.assertEqual(completed.status, OccurrenceStatus.COMPLETED)

    def test_semantic_and_evidence_models_are_typed(self):
        result = SemanticResult(Stage.ADVERSARIAL, SemanticVerdict.SUPPORTED, (), (), ())
        self.assertEqual(result.verdict, SemanticVerdict.SUPPORTED)
        evidence = CompletionEvidence(
            _controller_derived_id(OccurrenceId, "occ:1"),
            _controller_derived_id(SemanticResultId, "result:1"),
            "{}", ("stage",), LineageToken("lineage:1"),
        )
        self.assertEqual(evidence.resulting_lineage_token, LineageToken("lineage:1"))
        init = InitializationRecord(
            ReviewId("review:test"), InitializationIntentId("intent:1"),
            WorkflowDefinitionId("workflow:test"), SnapshotId("snapshot:test"), 0,
            Stage.ADVERSARIAL, LineageToken("lineage:1"),
        )
        self.assertEqual(init.initial_review_revision, 0)

    def test_frozen_request_envelopes_validate_caller_fields(self):
        initialize = InitializeReviewRequest(
            ReviewId("review:test"), WorkflowDefinitionId("workflow:test"), b"fixture",
            SnapshotMode.CANONICAL_CLEAN, InitializationIntentId("intent:1"),
        )
        self.assertEqual(initialize.snapshot_material, b"fixture")
        begin = BeginPassRequest(
            ReviewId("review:test"), LineageToken("lineage:0"), 0,
            SnapshotId("snapshot:test"), Stage.ADVERSARIAL,
        )
        self.assertEqual(begin.expected_review_revision, 0)
        semantic = SemanticResult(Stage.ADVERSARIAL, SemanticVerdict.SUPPORTED, (), (), ())
        complete = CompletePassRequest(
            ReviewId("review:test"), LineageToken("lineage:1"), 0,
            SnapshotId("snapshot:test"), Stage.ADVERSARIAL,
            _controller_derived_id(OccurrenceId, "occ:1"),
            _controller_derived_id(GateId, "gate:1"), semantic,
        )
        self.assertEqual(complete.semantic_result, semantic)
        with self.assertRaises(ValueError):
            CompletePassRequest(
                ReviewId("review:test"), LineageToken("lineage:1"), 0,
                SnapshotId("snapshot:test"), Stage.NORMALIZATION,
                _controller_derived_id(OccurrenceId, "occ:1"),
                _controller_derived_id(GateId, "gate:1"), semantic,
            )

    def test_repair_kind_is_closed_and_mutating_repair_requires_lineage(self):
        RepairRequest(ReviewId("review:test"), RepairKind.REBUILD_PROJECTION)
        with self.assertRaises(ValueError):
            RepairRequest(ReviewId("review:test"), RepairKind.RECOVER_TRANSACTION)
        request = RepairRequest(
            ReviewId("review:test"), RepairKind.RECOVER_TRANSACTION, LineageToken("lineage:0")
        )
        self.assertEqual(request.expected_lineage_token, LineageToken("lineage:0"))


if __name__ == "__main__": unittest.main()
