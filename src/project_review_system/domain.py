"""Immutable domain types owned by the Project Review System controller."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class _NonEmptyId:
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError(f"{type(self).__name__}.value must be a non-empty string")

    def to_string(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str):
        return cls(value)


@dataclass(frozen=True, slots=True)
class ReviewId(_NonEmptyId):
    value: str
    def __post_init__(self) -> None: self._validate()

@dataclass(frozen=True, slots=True)
class WorkflowDefinitionId(_NonEmptyId):
    value: str
    def __post_init__(self) -> None: self._validate()

@dataclass(frozen=True, slots=True)
class SnapshotId(_NonEmptyId):
    value: str
    def __post_init__(self) -> None: self._validate()

@dataclass(frozen=True, slots=True)
class LineageToken(_NonEmptyId):
    value: str
    def __post_init__(self) -> None: self._validate()

@dataclass(frozen=True, slots=True)
class InitializationIntentId(_NonEmptyId):
    value: str
    def __post_init__(self) -> None: self._validate()


_DERIVED_ID_AUTHORITY = object()


class _ControllerDerivedId:
    value: str

    @classmethod
    def derived(cls, value: str):
        return cls(value, _authority=_DERIVED_ID_AUTHORITY)

    @classmethod
    def from_string(cls, value: str):
        """Trusted persistence/deserialization boundary."""
        return cls(value, _authority=_DERIVED_ID_AUTHORITY)

    def to_string(self) -> str:
        return self.value

    def _validate_derived(self, authority: object | None) -> None:
        if authority is not _DERIVED_ID_AUTHORITY:
            raise ValueError(f"{type(self).__name__} is controller-derived; use derived()/from_string()")
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError(f"{type(self).__name__}.value must be a non-empty string")


@dataclass(frozen=True, slots=True, init=False)
class OccurrenceId(_ControllerDerivedId):
    value: str
    def __init__(self, value: str, *, _authority: object | None = None) -> None:
        object.__setattr__(self, "value", value)
        self._validate_derived(_authority)

@dataclass(frozen=True, slots=True, init=False)
class GateId(_ControllerDerivedId):
    value: str
    def __init__(self, value: str, *, _authority: object | None = None) -> None:
        object.__setattr__(self, "value", value)
        self._validate_derived(_authority)

@dataclass(frozen=True, slots=True, init=False)
class SemanticResultId(_ControllerDerivedId):
    value: str
    def __init__(self, value: str, *, _authority: object | None = None) -> None:
        object.__setattr__(self, "value", value)
        self._validate_derived(_authority)

@dataclass(frozen=True, slots=True, init=False)
class AuditEventId(_ControllerDerivedId):
    value: str
    def __init__(self, value: str, *, _authority: object | None = None) -> None:
        object.__setattr__(self, "value", value)
        self._validate_derived(_authority)


class ProgramState(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETE = "complete"
    FAILED = "failed"

class SnapshotMode(str, Enum):
    CANONICAL_CLEAN = "canonical-clean"
    CAPTURED_DIRTY = "captured-dirty"

class Stage(str, Enum):
    ADVERSARIAL = "Adversarial"
    INTERDEPENDENCY = "Interdependency"
    NORMALIZATION = "Normalization"
    STRUCTURAL_OPTIMIZATION = "Structural Optimization"
    END_TO_END_VALIDATION = "End-to-end validation"

class OccurrenceStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"
    FAILED = "failed"

class SemanticVerdict(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class StateSnapshot:
    review_id: ReviewId
    program_state: ProgramState
    review_revision: int
    snapshot_id: SnapshotId
    snapshot_mode: SnapshotMode
    workflow_definition_id: WorkflowDefinitionId
    stage_cursor: Stage | None
    open_occurrence_id: OccurrenceId | None
    lineage_token: LineageToken

    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.program_state, ProgramState): raise ValueError("program_state must be a ProgramState")
        if isinstance(self.review_revision, bool) or not isinstance(self.review_revision, int) or self.review_revision < 0: raise ValueError("review_revision must be a non-negative integer")
        if not isinstance(self.snapshot_id, SnapshotId): raise ValueError("snapshot_id must be a SnapshotId")
        if not isinstance(self.snapshot_mode, SnapshotMode): raise ValueError("snapshot_mode must be a SnapshotMode")
        if not isinstance(self.workflow_definition_id, WorkflowDefinitionId): raise ValueError("workflow_definition_id must be a WorkflowDefinitionId")
        if self.stage_cursor is not None and not isinstance(self.stage_cursor, Stage): raise ValueError("stage_cursor must be a Stage or None")
        if self.open_occurrence_id is not None and not isinstance(self.open_occurrence_id, OccurrenceId): raise ValueError("open_occurrence_id must be an OccurrenceId or None")
        if not isinstance(self.lineage_token, LineageToken): raise ValueError("lineage_token must be a LineageToken")
        if self.program_state is ProgramState.DRAFT: raise ValueError("draft state is reserved and non-constructible in Phase 1")
        if self.program_state is ProgramState.ACTIVE and self.stage_cursor is None: raise ValueError("active review requires a stage_cursor")
        if self.program_state in {ProgramState.COMPLETE, ProgramState.FAILED}:
            if self.stage_cursor is not None: raise ValueError("terminal review must not have a stage_cursor")
            if self.open_occurrence_id is not None: raise ValueError("terminal review must not have an open occurrence")


@dataclass(frozen=True, slots=True)
class PassOccurrence:
    occurrence_id: OccurrenceId
    review_id: ReviewId
    workflow_definition_id: WorkflowDefinitionId
    review_revision: int
    snapshot_id: SnapshotId
    stage: Stage
    parent_lineage_token: LineageToken
    gate_id: GateId
    status: OccurrenceStatus
    semantic_result_id: SemanticResultId | None = None

    def __post_init__(self) -> None:
        checks = ((self.occurrence_id, OccurrenceId, "occurrence_id"), (self.review_id, ReviewId, "review_id"), (self.workflow_definition_id, WorkflowDefinitionId, "workflow_definition_id"), (self.snapshot_id, SnapshotId, "snapshot_id"), (self.stage, Stage, "stage"), (self.parent_lineage_token, LineageToken, "parent_lineage_token"), (self.gate_id, GateId, "gate_id"), (self.status, OccurrenceStatus, "status"))
        for value, expected, name in checks:
            if not isinstance(value, expected): raise ValueError(f"{name} must be a {expected.__name__}")
        if isinstance(self.review_revision, bool) or not isinstance(self.review_revision, int) or self.review_revision < 0: raise ValueError("review_revision must be a non-negative integer")
        if self.semantic_result_id is not None and not isinstance(self.semantic_result_id, SemanticResultId): raise ValueError("semantic_result_id must be a SemanticResultId or None")
        if self.status is OccurrenceStatus.OPEN and self.semantic_result_id is not None: raise ValueError("open occurrence cannot have semantic_result_id")
        if self.status is OccurrenceStatus.COMPLETED and self.semantic_result_id is None: raise ValueError("completed occurrence requires semantic_result_id")


@dataclass(frozen=True, slots=True)
class SemanticResult:
    stage: Stage
    verdict: SemanticVerdict
    findings: tuple[str, ...]
    unresolved_conditions: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.stage, Stage): raise ValueError("stage must be a Stage")
        if not isinstance(self.verdict, SemanticVerdict): raise ValueError("verdict must be a SemanticVerdict")
        for name, value in (("findings", self.findings), ("unresolved_conditions", self.unresolved_conditions), ("evidence_refs", self.evidence_refs)):
            if not isinstance(value, tuple) or not all(isinstance(item, str) for item in value): raise ValueError(f"{name} must be an immutable tuple of strings")


@dataclass(frozen=True, slots=True)
class CompletionEvidence:
    occurrence_id: OccurrenceId
    semantic_result_id: SemanticResultId
    canonical_semantic_payload: str
    accepted_binding: tuple[str, ...]
    resulting_lineage_token: LineageToken

    def __post_init__(self) -> None:
        if not isinstance(self.occurrence_id, OccurrenceId): raise ValueError("occurrence_id must be an OccurrenceId")
        if not isinstance(self.semantic_result_id, SemanticResultId): raise ValueError("semantic_result_id must be a SemanticResultId")
        if not isinstance(self.canonical_semantic_payload, str): raise ValueError("canonical_semantic_payload must be a string")
        if not isinstance(self.accepted_binding, tuple) or not all(isinstance(item, str) for item in self.accepted_binding): raise ValueError("accepted_binding must be an immutable tuple of strings")
        if not isinstance(self.resulting_lineage_token, LineageToken): raise ValueError("resulting_lineage_token must be a LineageToken")


@dataclass(frozen=True, slots=True)
class InitializationRecord:
    review_id: ReviewId
    initialization_intent_id: InitializationIntentId
    workflow_definition_id: WorkflowDefinitionId
    snapshot_id: SnapshotId
    initial_review_revision: int
    initial_stage: Stage
    resulting_lineage_token: LineageToken

    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.initialization_intent_id, InitializationIntentId): raise ValueError("initialization_intent_id must be an InitializationIntentId")
        if not isinstance(self.workflow_definition_id, WorkflowDefinitionId): raise ValueError("workflow_definition_id must be a WorkflowDefinitionId")
        if not isinstance(self.snapshot_id, SnapshotId): raise ValueError("snapshot_id must be a SnapshotId")
        if isinstance(self.initial_review_revision, bool) or not isinstance(self.initial_review_revision, int) or self.initial_review_revision < 0: raise ValueError("initial_review_revision must be a non-negative integer")
        if not isinstance(self.initial_stage, Stage): raise ValueError("initial_stage must be a Stage")
        if not isinstance(self.resulting_lineage_token, LineageToken): raise ValueError("resulting_lineage_token must be a LineageToken")
