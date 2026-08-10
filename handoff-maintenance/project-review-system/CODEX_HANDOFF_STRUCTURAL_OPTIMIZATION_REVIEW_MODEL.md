# Codex Handoff Structural Optimization Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full Structural Optimization review, complete Model Before Review for the current handoff revision and derive the concrete current handoff structure, ownership boundaries, consumers, dependencies, and failure protections from the target itself.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Reduce the handoff to the lowest-burden reliable structure that preserves recovery capability, authority boundaries, evidence integrity, safety, and truthful stopping behavior.

Structural Optimization is not prose shortening for its own sake. It asks whether every retained element earns its maintenance and interpretation cost.

## Pass completion

A full Structural Optimization pass is complete only when:

- every section and persistent instruction in the current handoff has been tested;
- every material repeated concept or prohibition has been considered for merge or delegation;
- every pointer, exception, special case, and report requirement has been tested for a current consumer;
- every handoff-owned protection has been checked against deletion, compression, or replacement by an existing authoritative mechanism;
- every material deletion/compression candidate has been tested against all target-derived consumer and terminal classes that could depend on it;
- the bounded structure/consumer inventory is explicitly closed under the shared coverage rule from `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`;
- the complete blocker/high structural candidate set has been collected;
- every candidate has passed the mandatory Ownership Test before being treated as a proposed handoff correction.

Do not stop after finding the first removable element.

## Structural coverage closure

For each material element or proposed deletion/compression, derive the current consumers and terminal/re-entry contexts that can depend on it. Include blocker, interruption, fresh-session re-entry, reporting, or success consumers only when the target makes them materially relevant.

A removal verdict is not closed merely because the happy path still works. Verify that deleting, merging, compressing, or delegating the element does not remove the only protection or information needed by any target-derived material consumer or terminal class.

Do not create a permanent removal matrix. Use the minimum bounded structure/consumer witness needed for the current review.

## Governing principle

> Justify your existence or die.

An element survives only if removing or materially compressing it would create a distinct recovery failure, ambiguity, authority violation, evidence loss, unsafe fallback, scope escape, or materially worse operator burden that is not already handled by the owning authoritative layer.

Historical survival is not evidence of present necessity.

## Unit of analysis

Derive the current target structure during Model Before Review. Test at least:

- sections;
- paragraphs and persistent rules;
- examples and enumerations;
- named files/issues/checkers/pointers;
- stop conditions;
- autonomy rules;
- report fields;
- duplicated concepts across sections;
- any handoff-maintenance concept that has leaked into runtime recovery text.

Do not hard-code Lean-specific content into this model.

## Survival tests

For every material handoff element ask:

A. **Distinct requirement** — Does it express a recovery-specific requirement not already carried elsewhere?

B. **Invariant** — Does it protect a material invariant whose loss would create a real failure mode?

C. **Consumer** — Is there a concrete current recovery consumer that needs this information?

D. **Ownership** — Is the behavior actually owned by the handoff rather than production PRS, repository governance, source authority, Git history, or host/user authorization?

E. **Failure reduction** — Does the element materially reduce a plausible failure rather than merely describe one?

F. **Compression** — Can a general invariant replace multiple examples, warnings, or prohibitions without losing needed precision?

G. **Mergeability** — Can it be merged into an adjacent rule without creating ambiguity or hidden coupling?

H. **Delegation** — Can the owning authoritative mechanism be referenced instead of reimplemented?

I. **Lifecycle** — Does it have a distinct lifecycle or update trigger that justifies separate representation?

J. **Maintenance burden** — Does keeping it create staleness, selection ambiguity, duplicated update duties, or review churn disproportionate to its value?

K. **Interpretation burden** — Does it force Codex to resolve distinctions that do not affect a governed recovery decision?

L. **Removal safety** — If deleted, is any capability, authority boundary, evidence protection, recovery path, or truthful stop behavior actually lost?

## Structural verdicts

Classify each tested element as one of:

- **SURVIVE INTACT** — distinct value and current representation is already near-minimal;
- **SURVIVE BUT COMPRESS** — distinct value remains but wording/representation can shrink;
- **MERGE** — value remains but a separate element is unnecessary;
- **DELEGATE** — authoritative layer already owns the behavior; retain at most a pointer/boundary if recovery needs it;
- **DELETE** — no distinct current value or burden exceeds benefit;
- **REPORT EXTERNAL GAP** — the need is real but owned by repository/governance/PRS, so the handoff must not manufacture the missing mechanism.

## Minimum structural failure families

Challenge at least:

1. duplicated PRS procedure inside the handoff;
2. duplicated authority models or control-selection logic;
3. repeated warnings that can be one invariant;
4. stale versioned artifacts retained without a current consumer;
5. pointers whose source no longer has a recovery-specific role;
6. examples mistaken for permanent requirements;
7. report fields with no downstream consumer;
8. stop conditions that overlap or can collapse safely;
9. autonomy clauses that merely restate host/PRS authority;
10. recovery-specific distinctions that have become generic PRS design;
11. maintenance instructions leaking into runtime handoff text;
12. generated views, trackers, checklists, or status surfaces lacking a distinct consumer;
13. extra roles or identities that do not change a decision or failure path;
14. parallel representations of the same state or invariant;
15. speculative protections whose machinery costs as much or more than the risk reduced;
16. removal of a genuinely necessary protection in the name of minimalism.

Structural Optimization must attack both **excess** and **over-pruning**.

## Anti-expansion rule

Do not add a permanent document, tracker, checklist, status field, role, review artifact, generated view, adapter, synchronization duty, or update obligation unless an existing mechanism cannot serve a material current consumer.

Do not create new machinery merely to make the structure appear systematic.

## Ownership test after the sweep

For every blocker/high structural candidate classify it as:

- **handoff-owned** — eligible for Model Before Change and correction;
- **production-PRS-owned** — reference/defer; do not duplicate;
- **repository/governance-owned** — report the gap; do not invent the mechanism;
- **no material owner/value** — discard.

A finding that something is redundant does not by itself authorize deletion if the element is owned by another layer or required by current authority.

## Correction pressure

For each handoff-owned survivor:

1. identify the minimum capability that must remain;
2. choose the smallest representation preserving that capability;
3. verify normal, edge, failure, interruption, authority, and downstream cases;
4. prefer deletion over abstraction when nothing consumes the abstraction;
5. prefer delegation over duplication;
6. prefer one invariant over many examples when equivalent;
7. preserve explicit distinctions only when they change behavior, ownership, authority, evidence, or failure handling.

## Relationship to the deferred cull-the-herd candidate

This stage supplies the **survive-or-die** pressure used by the maintenance workflow's deferred canonical-method candidate.

That broader pattern remains non-authoritative maintenance methodology. Do not infer from this model that production PRS has adopted it canonically.

## Review cycle and convergence

```text
Model Before Review
    -> derive bounded current structure and material consumer/terminal inventory
    -> close removal/compression candidates against those consumers
    -> full Structural Optimization sweep
    -> complete blocker/high structural candidate set
    -> Ownership Test
    -> Model Before Change for handoff-owned survivors
    -> apply the smallest coherent structural correction
    -> repeat only while surviving handoff-owned blocker/high corrections remain
```

Convergence is governed by `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.

The preferred terminal state is not the shortest possible handoff. It is the **smallest handoff that still reliably performs its recovery job**.
