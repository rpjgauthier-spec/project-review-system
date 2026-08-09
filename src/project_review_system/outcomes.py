"""Machine-readable operation outcomes frozen by the execution contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from .domain import GateId, LineageToken, OccurrenceId, ReviewId, Stage


class OutcomeCode(str, Enum):
    INITIALIZED = "initialized"
    ALREADY_INITIALIZED = "already_initialized"
    STATUS = "status"
    PASS_OPENED = "pass_opened"
    PASS_ALREADY_OPEN = "pass_already_open"
    PASS_COMPLETED = "pass_completed"
    PASS_ALREADY_COMPLETED = "pass_already_completed"
    PROJECTION_REBUILT = "projection_rebuilt"
    NO_REPAIR_NEEDED = "no_repair_needed"


class ErrorCode(str, Enum):
    REVIEW_NOT_FOUND = "review_not_found"
    REVIEW_ALREADY_EXISTS_CONFLICT = "review_already_exists_conflict"
    STALE_LINEAGE = "stale_lineage"
    WORKFLOW_DEFINITION_MISMATCH = "workflow_definition_mismatch"
    REVISION_MISMATCH = "revision_mismatch"
    SNAPSHOT_MISMATCH = "snapshot_mismatch"
    WRONG_STAGE = "wrong_stage"
    OCCURRENCE_MISMATCH = "occurrence_mismatch"
    GATE_MISMATCH = "gate_mismatch"
    CONFLICTING_COMPLETION = "conflicting_completion"
    INVALID_SEMANTIC_RESULT = "invalid_semantic_result"
    TERMINAL_STATE = "terminal_state"
    REPAIR_REQUIRES_SEMANTIC_JUDGMENT = "repair_requires_semantic_judgment"
    INTEGRITY_ERROR = "integrity_error"
    PERSISTENCE_UNAVAILABLE = "persistence_unavailable"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"
    SNAPSHOT_STALE = "snapshot_stale"
    LINEAGE_UNREADABLE = "lineage_unreadable"
    CONFLICTING_OPEN_OCCURRENCE = "conflicting_open_occurrence"
    PREREQUISITE_INCOMPLETE = "prerequisite_incomplete"
    GATE_INPUTS_INVALID = "gate_inputs_invalid"
    OCCURRENCE_REPLAY_CONFLICT = "occurrence_replay_conflict"
    AUTHORITATIVE_STATE_UNREADABLE = "authoritative_state_unreadable"
    PERSISTENCE_CONFLICT = "persistence_conflict"


@dataclass(frozen=True, slots=True)
class InitializationData:
    review_id: ReviewId
    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")


@dataclass(frozen=True, slots=True)
class StatusData:
    review_id: ReviewId
    next_stage: Stage | None
    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if self.next_stage is not None and not isinstance(self.next_stage, Stage): raise ValueError("next_stage must be a Stage or None")


@dataclass(frozen=True, slots=True)
class BeginPassData:
    occurrence_id: OccurrenceId
    gate_id: GateId
    def __post_init__(self) -> None:
        if not isinstance(self.occurrence_id, OccurrenceId): raise ValueError("occurrence_id must be an OccurrenceId")
        if not isinstance(self.gate_id, GateId): raise ValueError("gate_id must be a GateId")


@dataclass(frozen=True, slots=True)
class CompletePassData:
    occurrence_id: OccurrenceId
    next_stage: Stage | None
    def __post_init__(self) -> None:
        if not isinstance(self.occurrence_id, OccurrenceId): raise ValueError("occurrence_id must be an OccurrenceId")
        if self.next_stage is not None and not isinstance(self.next_stage, Stage): raise ValueError("next_stage must be a Stage or None")


@dataclass(frozen=True, slots=True)
class RepairData:
    changed: bool
    def __post_init__(self) -> None:
        if not isinstance(self.changed, bool): raise ValueError("changed must be a bool")


OperationData = InitializationData | StatusData | BeginPassData | CompletePassData | RepairData
T = TypeVar("T", bound=OperationData)


_SUCCESS_PAYLOAD_TYPES = {
    OutcomeCode.INITIALIZED: InitializationData,
    OutcomeCode.ALREADY_INITIALIZED: InitializationData,
    OutcomeCode.STATUS: StatusData,
    OutcomeCode.PASS_OPENED: BeginPassData,
    OutcomeCode.PASS_ALREADY_OPEN: BeginPassData,
    OutcomeCode.PASS_COMPLETED: CompletePassData,
    OutcomeCode.PASS_ALREADY_COMPLETED: CompletePassData,
    OutcomeCode.PROJECTION_REBUILT: RepairData,
    OutcomeCode.NO_REPAIR_NEEDED: RepairData,
}


@dataclass(frozen=True, slots=True)
class OperationResult(Generic[T]):
    ok: bool
    outcome: OutcomeCode | ErrorCode
    review_id: ReviewId | None = None
    lineage_token: LineageToken | None = None
    data: T | None = None
    error: ErrorCode | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.ok, bool): raise ValueError("ok must be a bool")
        if not isinstance(self.outcome, (OutcomeCode, ErrorCode)): raise ValueError("outcome must be an OutcomeCode or ErrorCode")
        if self.review_id is not None and not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId or None")
        if self.lineage_token is not None and not isinstance(self.lineage_token, LineageToken): raise ValueError("lineage_token must be a LineageToken or None")
        if self.data is not None and not isinstance(self.data, (InitializationData, StatusData, BeginPassData, CompletePassData, RepairData)): raise ValueError("data must be a typed operation payload or None")
        if self.error is not None and not isinstance(self.error, ErrorCode): raise ValueError("error must be an ErrorCode or None")

        if self.ok:
            if isinstance(self.outcome, ErrorCode) or self.error is not None: raise ValueError("successful result cannot carry an ErrorCode")
            expected_payload = _SUCCESS_PAYLOAD_TYPES[self.outcome]
            if self.data is not None and not isinstance(self.data, expected_payload):
                raise ValueError(f"{self.outcome.value} requires {expected_payload.__name__} when data is present")
        else:
            if isinstance(self.outcome, OutcomeCode): raise ValueError("failed result cannot carry an OutcomeCode")
            if self.error is not None and self.error is not self.outcome: raise ValueError("error must match failure outcome")

        payload_review_id = getattr(self.data, "review_id", None)
        if self.review_id is not None and payload_review_id is not None and self.review_id != payload_review_id:
            raise ValueError("result review_id must match payload review_id")


__all__ = [
    "OutcomeCode", "ErrorCode",
    "InitializationData", "StatusData", "BeginPassData", "CompletePassData", "RepairData",
    "OperationData", "OperationResult",
]
