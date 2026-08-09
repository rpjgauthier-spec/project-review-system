"""Immutable domain types owned by the Project Review System controller."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class _NonEmptyId:
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError(f"{type(self).__name__}.value must be a non-empty string")


@dataclass(frozen=True, slots=True)
class ReviewId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class WorkflowDefinitionId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class SnapshotId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class OccurrenceId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class GateId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class SemanticResultId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class LineageToken(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


@dataclass(frozen=True, slots=True)
class InitializationIntentId(_NonEmptyId):
    value: str

    def __post_init__(self) -> None:
        self._validate()


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
        if isinstance(self.review_revision, bool) or not isinstance(self.review_revision, int) or self.review_revision < 0:
            raise ValueError("review_revision must be a non-negative integer")
        if self.program_state is ProgramState.DRAFT:
            raise ValueError("draft state is reserved and non-constructible in Phase 1")
        if self.program_state is ProgramState.ACTIVE and self.stage_cursor is None:
            raise ValueError("active review requires a stage_cursor")
        if self.program_state in {ProgramState.COMPLETE, ProgramState.FAILED}:
            if self.stage_cursor is not None:
                raise ValueError("terminal review must not have a stage_cursor")
            if self.open_occurrence_id is not None:
                raise ValueError("terminal review must not have an open occurrence")
