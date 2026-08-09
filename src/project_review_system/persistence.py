"""Backend-neutral persistence protocol.

The controller owns transition semantics. Backends only provide atomic durability,
compare-before-write, immutable evidence retention, and coherent reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence, runtime_checkable

from .domain import InitializationIntentId, LineageToken, ReviewId, StateSnapshot


@dataclass(frozen=True, slots=True)
class InitializationCommit:
    state: StateSnapshot
    initialization_intent_id: InitializationIntentId
    immutable_events: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class TransitionCommit:
    review_id: ReviewId
    next_state: StateSnapshot
    immutable_events: tuple[object, ...] = ()
    immutable_evidence: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class CreateResult:
    created: bool
    state: StateSnapshot


@dataclass(frozen=True, slots=True)
class TransitionResult:
    committed: bool
    state: StateSnapshot


@runtime_checkable
class PersistenceBackend(Protocol):
    def read(self, review_id: ReviewId) -> StateSnapshot | None:
        """Return one coherent authoritative state, or None when absent."""
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

    def read_immutable_history(self, review_id: ReviewId) -> Sequence[object]:
        """Return immutable durable events/evidence for retry and integrity checks."""
        ...
