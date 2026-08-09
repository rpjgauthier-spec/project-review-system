"""Backend-neutral persistence protocol."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from .domain import (
    CompletionEvidence,
    InitializationIntentId,
    InitializationRecord,
    LineageToken,
    OccurrenceId,
    PassOccurrence,
    ReviewId,
    StateSnapshot,
)


@dataclass(frozen=True, slots=True)
class AuthoritativeRecord:
    state: StateSnapshot
    immutable_history: tuple[object, ...] = ()
    def __post_init__(self) -> None:
        if not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot")
        if not isinstance(self.immutable_history, tuple): raise ValueError("immutable_history must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class InitializationCommit:
    review_id: ReviewId
    state: StateSnapshot
    initialization_intent_id: InitializationIntentId
    immutable_events: tuple[object, ...] = ()
    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.state, StateSnapshot): raise ValueError("state must be a StateSnapshot")
        if self.review_id != self.state.review_id: raise ValueError("review_id must match state.review_id")
        if not isinstance(self.initialization_intent_id, InitializationIntentId): raise ValueError("initialization_intent_id must be an InitializationIntentId")
        if not isinstance(self.immutable_events, tuple): raise ValueError("immutable_events must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class TransitionCommit:
    review_id: ReviewId
    next_state: StateSnapshot
    immutable_events: tuple[object, ...] = ()
    immutable_evidence: tuple[object, ...] = ()
    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId): raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.next_state, StateSnapshot): raise ValueError("next_state must be a StateSnapshot")
        if self.review_id != self.next_state.review_id: raise ValueError("review_id must match next_state.review_id")
        if not isinstance(self.immutable_events, tuple): raise ValueError("immutable_events must be an immutable tuple")
        if not isinstance(self.immutable_evidence, tuple): raise ValueError("immutable_evidence must be an immutable tuple")


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
