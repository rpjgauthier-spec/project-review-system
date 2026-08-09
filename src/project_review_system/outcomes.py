"""Machine-readable operation outcomes frozen by the execution contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .domain import LineageToken, ReviewId


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
    PROGRAM_NOT_ACTIVE = "program_not_active"
    REVISION_MISMATCH = "revision_mismatch"
    SNAPSHOT_MISMATCH = "snapshot_mismatch"
    SNAPSHOT_STALE = "snapshot_stale"
    STALE_LINEAGE = "stale_lineage"
    LINEAGE_UNREADABLE = "lineage_unreadable"
    WRONG_STAGE = "wrong_stage"
    CONFLICTING_OPEN_OCCURRENCE = "conflicting_open_occurrence"
    PREREQUISITE_INCOMPLETE = "prerequisite_incomplete"
    GATE_INPUTS_INVALID = "gate_inputs_invalid"
    OCCURRENCE_REPLAY_CONFLICT = "occurrence_replay_conflict"
    OCCURRENCE_MISMATCH = "occurrence_mismatch"
    GATE_MISMATCH = "gate_mismatch"
    SEMANTIC_RESULT_CONFLICT = "semantic_result_conflict"
    SEMANTIC_RESULT_INVALID = "semantic_result_invalid"
    REPAIR_REQUIRES_SEMANTIC_JUDGMENT = "repair_requires_semantic_judgment"
    AUTHORITATIVE_STATE_UNREADABLE = "authoritative_state_unreadable"
    WORKFLOW_DEFINITION_MISMATCH = "workflow_definition_mismatch"
    PERSISTENCE_CONFLICT = "persistence_conflict"
    PERSISTENCE_UNAVAILABLE = "persistence_unavailable"


@dataclass(frozen=True, slots=True)
class OperationResult:
    ok: bool
    outcome: OutcomeCode | ErrorCode
    review_id: ReviewId | None = None
    lineage_token: LineageToken | None = None
    data: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.ok and isinstance(self.outcome, ErrorCode):
            raise ValueError("successful result cannot carry an ErrorCode")
        if not self.ok and isinstance(self.outcome, OutcomeCode):
            raise ValueError("failed result cannot carry an OutcomeCode")
