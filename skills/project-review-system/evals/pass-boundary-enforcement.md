# Evaluation: Pass-Boundary Enforcement

## Purpose

Verify that an Adaptive Execution pass cannot be represented as merely another checklist item inside one undifferentiated semantic execution. Each completed execution-plan pass must have a distinct declared execution occurrence, must externalize a bounded handoff that the next pass explicitly consumes, and in repository execution must leave ordered durable evidence rather than being backfilled together after the fact.

The evaluation covers ordinary one-pass stages, subdivided stages, ISOLATED subpasses, reopened/redo executions, partial/intermediate completion states, and evidence carried across pull-request or base-state boundaries.

## Required behavior

1. Every completed execution-plan pass has a nonempty `execution_unit_id`.
2. Every completed pass records a boundary kind and boundary ID.
3. Execution-unit identifiers and boundary identities are unique across distinct execution occurrences of the same change record, including reopened/redo revisions and occurrences first recorded in a prior/base state.
4. Once an execution occurrence first receives durable completion evidence, its recorded pass evidence—including execution-unit identity, boundary identity, inbound handoff, and outbound handoff—cannot be mutated while retaining the same occurrence identity.
5. A pass produces a bounded handoff containing findings, evidence references when applicable, unresolved conditions when applicable, and its exact downstream consumer.
6. The handoff is hashed canonically and the recorded hash must match its contents.
7. Except for the first completed pass in the current ordered chain, each pass records the exact previous handoff hash as `inbound_handoff_sha256`.
8. A later required stage cannot begin or receive passing credit while an earlier required stage remains unpassed.
9. An `ISOLATED` pass requires an `isolated-context` boundary declaration; a non-isolated pass may not claim that boundary kind.
10. The final completed pass hands off to `review-completion`.
11. In repository execution, the current gate must already exist in a prior durable change-record state before a pass first receives completion evidence.
12. Two distinct passes may not first receive completion evidence in the same change-record commit.
13. Before a later pass first completes, the exact previous pass handoff must already exist in the prior durable change-record state.
14. A subdivided stage may record completed passes before stage credit only as an exact ordered prefix of the gate's execution plan.
15. Each subdivided subpass must first complete in its own later durable state; the enclosing stage must not receive a passing result until every planned pass is complete.
16. Any recorded completed pass, including a partial subdivided prefix before stage credit, must remain bound to a current gate for the current `review_revision` and current governed `target_state_id`.
17. Historical uniqueness validation for a pull request includes relevant pre-existing/base-state evidence so reopening in a later pull request cannot reuse an earlier execution-unit or boundary identity.
18. The historical exemption set is closed; the active change record cannot self-authorize an exemption from pass-boundary enforcement.
19. In a chat host where one assistant message is the selected SEPARATED execution unit, perform only one semantic pass per assistant message and put its bounded findings/handoff in that message or a durable artifact read by the next pass before it begins.

## Failure conditions

Fail if:

- two distinct execution occurrences reuse the same execution-unit or boundary identity, including across reopened revisions or a prior/base state;
- completed pass evidence can be rewritten while retaining the same occurrence identity;
- a later pass does not consume the previous pass handoff;
- handoff contents can change without invalidating their hash;
- stage credit skips an earlier required stage;
- an ISOLATED pass is recorded without an isolation boundary;
- a pass completes before its current gate existed in a prior durable change-record state;
- two passes first complete together in one change-record commit;
- the exact prior handoff was not durably present before the next pass completed;
- a subdivided completion is not an ordered prefix of its execution plan;
- a subdivided stage receives passing credit before its full plan is complete;
- a partial/intermediate pass completion is accepted under a stale gate, stale review revision, or stale governed artifact state;
- reopening in a later pull request can reuse an execution identity because base-state history was omitted;
- the active record can add itself to an enforcement exemption;
- multiple semantic stages are executed in one undifferentiated assistant message while being recorded as separate passes; or
- the repository claims that its deterministic checker proves a host message/context boundary when the host supplied no independently meaningful boundary ID.

## Required scenarios

Exercise at least:

- a normal one-pass stage;
- a two-subpass stage whose subpasses complete in separate durable states before stage credit;
- rejection when two subpasses first complete in the same durable state;
- rejection of a non-prefix or premature subdivided completion;
- rejection of execution-unit reuse by a reopened/redo occurrence;
- rejection of boundary-identity reuse by a reopened/redo occurrence;
- rejection of identity reuse from a pre-existing/base-state occurrence in a later pull request;
- rejection of post-completion mutation of execution identity or handoff evidence;
- rejection of a stale partial-subpass gate or completion target state;
- rejection of a broken or tampered handoff chain;
- ISOLATED boundary enforcement; and
- the assurance-limit case where no independently meaningful host message/context identifier exists.

## Assurance boundary

The deterministic controls can prove consistency of the recorded execution identities, handoff chain, plan-prefix shape, current artifact binding, historical uniqueness/immutability, and—inside Git repository execution—the durable chronology of gate-before-completion and one-first-completion-commit-per-pass. They cannot independently prove that a ChatGPT message boundary or fresh context actually occurred unless the execution host exposes a trustworthy boundary identifier. Where no such identifier exists, the boundary identity remains an attestation; Git chronology and immutable handoff evidence limit backfilling and replay but do not convert that attestation into host-level proof.
