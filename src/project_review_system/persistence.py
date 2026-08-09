"""Backend-neutral persistence protocol."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from .domain import (
    AuditEventId,
    CompletionEvidence,
    InitializationIntentId,
    InitializationRecord,
    LineageToken,
    OccurrenceId,
    PassOccurrence,
    ReviewId,
    SemanticResult,
    StateSnapshot,
)


ImmutableHistoryItem = str | AuditEventId | PassOccurrence | SemanticResult | CompletionEvidence | InitializationRecord
_IMMUTABLE_HISTORY_TYPES = (str, AuditEventId, PassOccurrence, SemanticResult, CompletionEvidence, InitializationRecord)
_REVIEW_BOUND_HISTORY_TYPES = (PassOccurrence, InitializationRecord)


def _validate_immutable_items(name: str, value: object, review_id: ReviewId) -> None:
    if not isinstance(value, tuple):
        raise ValueError(f"{name} must be an immutable tuple")
    if not all(isinstance(item, _IMMUTABLE_HISTORY_TYPES) for item in value):
        raise ValueError(f"{name} must contain only immutable typed history/evidence values")
    if any(
        isinstance(item, _REVIEW_BOUND_HISTORY_TYPES) and item.review_id != review_id
        for item in value
    ):
        raise ValueError(f"{name} review-bearing items must match the authoritative review_id")


@dataclass(frozen=True, slots=True)
class AuthoritativeRecord:
    state: StateSnapshot
    immutable_history: tuple[ImmutableHistoryItem, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot")
        _validate_immutable_items("immutable_history", self.immutable_history, self.state.review_id)


@dataclass(frozen=True, slots=True)
class InitializationCommit:
    review_id: ReviewId
    state: StateSnapshot
    initialization_intent_id: InitializationIntentId
    immutable_events: tuple[ImmutableHistoryItem, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot")
        if self.review_id != self.state.review_id: raise ValueError("review_id must match state.review_id")
        if not isinstance(self.initialization_intent_id, InitializationIntentId): raise ValueError("initialization_intent_id must be an InitializationIntentId")
        _validate_immutable_items("immutable_events", self.immutable_events, self.review_id)


@dataclass(frozen=True, slots=True)
class TransitionCommit:
    review_id: ReviewId
    next_state: StateSnapshot
    immutable_events: tuple[ImmutableHistoryItem, ...] = ()
    immutable_evidence: tuple[ImmutableHistoryItem, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.next_state, StateSnapshot): raise ValueError("next_state must be a StateSnapshot")
        if self.review_id != self.next_state.review_id: raise ValueError("review_id must match next_state.review_id")
        _validate_immutable_items("immutable_events", self.immutable_events, self.review_id)
        _validate_immutable_items("immutable_evidence", self.immutable_evidence, self.review_id)


class PersistenceOutcome(str, Enum):
    CREATED = "created"
    ALREADY_EXISTS = "already_exists"
    COMMITTED = "committed"
    ALREADY_APPLIED = "already_applied"
    CONFLICT = "conflict"
    UNAVAILABLE = "unavailable"
    OUTCOME_UNKNOWN = "outcome_unknown"


@dataclass(frozen=True, slots=True)
class CreateResult:
    outcome: PersistenceOutcome
    state: StateSnapshot | None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, PersistenceOutcome): raise ValueError("outcome must be a PersistenceOutcome")
        if self.outcome not in {PersistenceOutcome.CREATED, PersistenceOutcome.ALREADY_EXISTS, PersistenceOutcome.UNAVAILABLE, PersistenceOutcome.OUTCOME_UNKNOWN}: raise ValueError("invalid create outcome")
        if self.state is not None and not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot or None")
        if self.outcome in {PersistenceOutcome.CREATED, PersistenceOutcome.ALREADY_EXISTS} and self.state is None: raise ValueError("durable create outcome requires state")


@dataclass(frozen=True, slots=True)
class TransitionResult:
    outcome: PersistenceOutcome
    state: StateSnapshot | None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, PersistenceOutcome): raise ValueError("outcome must be a PersistenceOutcome")
        if self.outcome not in {PersistenceOutcome.COMMITTED, PersistenceOutcome.ALREADY_APPLIED, PersistenceOutcome.CONFLICT, PersistenceOutcome.UNAVAILABLE, PersistenceOutcome.OUTCOME_UNKNOWN}: raise ValueError("invalid transition outcome")
        if self.state is not None and not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot or None")
        if self.outcome in {PersistenceOutcome.COMMITTED, PersistenceOutcome.ALREADY_APPLIED, PersistenceOutcome.CONFLICT} and self.state is None: raise ValueError("known transition outcome requires authoritative state")


@runtime_checkable
class PersistenceBackend(Protocol):
    def read(self, review_id: ReviewId) -> AuthoritativeRecord | None: ...
    def create_if_absent(self, review_id: ReviewId, commit: InitializationCommit) -> CreateResult: ...
    def commit_transition(self, review_id: ReviewId, expected_lineage_token: LineageToken, commit: TransitionCommit) -> TransitionResult: ...
    def read_occurrence(self, occurrence_id: OccurrenceId) -> PassOccurrence | None: ...
    def read_completion(self, occurrence_id: OccurrenceId) -> CompletionEvidence | None: ...
    def read_initialization(self, review_id: ReviewId) -> InitializationRecord | None: ...


__all__ = [
    "ImmutableHistoryItem", "AuthoritativeRecord", "InitializationCommit", "TransitionCommit",
    "PersistenceOutcome", "CreateResult", "TransitionResult", "PersistenceBackend",
]
