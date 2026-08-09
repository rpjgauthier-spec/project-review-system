"""Backend-neutral persistence protocol.

The controller owns transition semantics. Backends only provide atomic durability,
compare-before-write, immutable evidence retention, and coherent reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .domain import InitializationIntentId, LineageToken, ReviewId, StateSnapshot


@dataclass(frozen=True, slots=True)
class AuthoritativeRecord:
    state: StateSnapshot
    immutable_history: tuple[object, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.state, StateSnapshot):
            raise ValueError("state must be a StateSnapshot")
        if not isinstance(self.immutable_history, tuple):
            raise ValueError("immutable_history must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class InitializationCommit:
    state: StateSnapshot
    initialization_intent_id: InitializationIntentId
    immutable_events: tuple[object, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.state, StateSnapshot):
            raise ValueError("state must be a StateSnapshot")
        if not isinstance(self.initialization_intent_id, InitializationIntentId):
            raise ValueError("initialization_intent_id must be an InitializationIntentId")
        if not isinstance(self.immutable_events, tuple):
            raise ValueError("immutable_events must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class TransitionCommit:
    review_id: ReviewId
    next_state: StateSnapshot
    immutable_events: tuple[object, ...] = ()
    immutable_evidence: tuple[object, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.review_id, ReviewId):
            raise ValueError("review_id must be a ReviewId")
        if not isinstance(self.next_state, StateSnapshot):
            raise ValueError("next_state must be a StateSnapshot")
        if self.review_id != self.next_state.review_id:
            raise ValueError("review_id must match next_state.review_id")
        if not isinstance(self.immutable_events, tuple):
            raise ValueError("immutable_events must be an immutable tuple")
        if not isinstance(self.immutable_evidence, tuple):
            raise ValueError("immutable_evidence must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class CreateResult:
    created: bool
    state: StateSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.created, bool):
            raise ValueError("created must be a bool")
        if not isinstance(self.state, StateSnapshot):
            raise ValueError("state must be a StateSnapshot")


@dataclass(frozen=True, slots=True)
class TransitionResult:
    committed: bool
    state: StateSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.committed, bool):
            raise ValueError("committed must be a bool")
        if not isinstance(self.state, StateSnapshot):
            raise ValueError("state must be a StateSnapshot")


@runtime_checkable
class PersistenceBackend(Protocol):
    def read(self, review_id: ReviewId) -> AuthoritativeRecord | None:
        """Return one coherent authoritative state plus immutable history, or None."""
        ...

    def create_if_absent(
        self,
        review_id: ReviewId,
        commit: InitializationCommit,
    ) -> CreateResult:
        """Atomically create one authoritative review if it does not exist."""
        ...

    def commit_transition(
        self,
        expected_lineage_token: LineageToken,
        commit: TransitionCommit,
    ) -> TransitionResult:
        """Atomically compare lineage and commit one controller-supplied transition."""
        ...
