# Codex Handoff Normalization Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full Normalization review, complete Model Before Review for the current handoff revision. Derive the current concept/representation families from the target handoff rather than hard-coding Lean-specific content here.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Find materially inconsistent representations of the same concept, state, authority, identity, boundary, or outcome while preserving differences that are actually justified by ownership, lifecycle, scope, or semantics.

Normalization is not simplification-by-force. Equivalent things should align; non-equivalent things must remain distinct.

A normalization finding is a candidate problem, not automatically a handoff edit.

## Pass completion

A full Normalization pass is complete only when:

- every handoff section has been considered;
- every material repeated concept or representation family has been identified;
- equivalent concepts have been compared across all occurrences;
- apparently different concepts have been checked before merging;
- justified distinctions have been recorded rather than flattened;
- the complete blocker/high candidate set has been collected;
- every candidate has passed through the Ownership Test before any handoff correction is proposed.

Do not stop at the first inconsistency.

## Governing purpose

The handoff exists to provide compact, accurate recovery navigation without becoming a duplicate PRS specification.

Normalization should therefore reduce ambiguity and contradictory representation while avoiding:

- copying canonical PRS vocabulary unnecessarily;
- inventing a new handoff vocabulary where repository authority already owns the term;
- collapsing distinct authority or state concepts merely because their names look similar;
- preserving multiple phrasings that materially imply different behavior.

## Representation families to derive

From the current target, identify repeated families such as:

- authority and authorization terms;
- repository/ref/locator/target identity terms;
- review-state, revision, status, and credit terms;
- source-scope and recovery-scope terms;
- current versus historical evidence terms;
- blocker, stop, completion, and success terms;
- semantic activity, execution boundary, and ordinary implementation terms;
- validation/checker/result terms;
- pointers versus proof/authority distinctions;
- user-work/history preservation language;
- autonomy versus permission language.

Do not assume these are all present or require change. Derive only what the target actually uses.

## Stable normalization invariants

Attack the target using these relationships:

- one material concept should not imply different behavior merely because wording changes;
- one term should not silently refer to multiple materially different concepts;
- distinct authority layers must not be normalized into one generic "authority" if ownership differs;
- current-state evidence and historical evidence must remain distinguishable when the recovery depends on that distinction;
- permission, governance, scope, status, and evidence must not be collapsed into one approval concept;
- a pointer must not be represented elsewhere as proof or authority;
- a locator must not become a governing ref through wording drift;
- blocked recovery must not be normalized into successful completion;
- user-facing wording and repository-owned canonical vocabulary should align where divergence changes behavior, but the handoff should not duplicate canonical definitions unnecessarily;
- stylistic variation alone is not a blocker/high problem.

## Normalization dimensions

Sweep each applicable section for:

A. **Term equivalence** — do different phrases mean the same thing, and if so do they imply the same behavior?

B. **Term overloading** — is one phrase used for materially different concepts?

C. **Authority vocabulary** — are PRS authority, host/user authorization, source-scope authority, and evidence roles kept distinct?

D. **Identity vocabulary** — are repository, ref, locator, artifact state, review revision, target state, and occurrence identities represented consistently?

E. **State vocabulary** — are current, historical, stale, blocked, complete, reopened, and superseded states used consistently?

F. **Evidence vocabulary** — are pointer, evidence, proof, validator result, review credit, and authority represented without semantic inflation?

G. **Scope vocabulary** — are implementation scope, recovery scope, review scope, and ordinary feature work distinguished where needed?

H. **Action vocabulary** — are inspect, diagnose, correct, validate, commit, push, advance, stop, and complete used in ways consistent with their authorization/governance requirements?

I. **Consumer consistency** — would a fresh Codex interpret repeated terms the same way across sections?

J. **Justified difference** — is an apparent inconsistency actually required by different ownership, lifecycle, chronology, or consumer needs?

## Minimum failure families

Challenge at least:

1. `authority` used generically where host/user and PRS ownership differ;
2. `current` used without a bound identity or chronology;
3. `review state` and implementation state treated as interchangeable;
4. `scope` used for multiple independent boundaries;
5. `permission`, `mode`, `allowed action`, or `governed transition` collapsed together;
6. `failure`, `blocker`, `stop`, and `completion` represented inconsistently;
7. historical evidence described as current credit in one section but only as evidence in another;
8. a recovery pointer presented elsewhere as an authoritative source;
9. equivalent stop or reporting conditions phrased so differently that they imply different behavior;
10. normalization that would erase a real distinction and create an authority/identity bug;
11. imported PRS vocabulary duplicated in the handoff without a distinct recovery need;
12. cosmetic wording variation mistaken for a material normalization defect.

## Finding standards

### Blocker

Use when inconsistent representation can cause action under the wrong authority, false review credit, wrong identity/state binding, unauthorized action, scope escape, fabricated completion, or inability to determine a truthful recovery state.

### High

Use when inconsistent representation materially raises the probability of contradictory interpretation, stale-state acceptance, wrong-context continuation, incomplete propagation, or misleading reporting.

Do not elevate stylistic preference, sentence rhythm, or harmless synonym variation.

## Ownership test after the sweep

For every blocker/high candidate classify it as:

- **handoff-owned** — the inconsistency exists in the handoff and materially affects recovery interpretation;
- **production-PRS-owned** — canonical vocabulary/semantics are owned by PRS; reference or defer rather than duplicate;
- **repository/governance-owned** — the inconsistency reflects unresolved upstream authority/state rather than handoff wording;
- **no material owner/value** — cosmetic, redundant, or lower value than the complexity of normalization.

Only handoff-owned candidates proceed to correction design.

## Structural pressure after ownership

For each handoff-owned candidate ask:

- Can one existing term/phrase carry all equivalent uses?
- Would alignment reduce ambiguity without importing a duplicate PRS glossary?
- Is the difference actually semantically necessary?
- Can the inconsistency be removed by deleting duplicate wording rather than adding explanation?
- Would the proposed normalization create a larger terminology surface than it removes?

Prefer deletion, alignment, or reference over new taxonomy.

## Review cycle and convergence

```text
Model Before Review
    -> derive representation families
    -> full Normalization sweep
    -> complete blocker/high candidate set
    -> Ownership Test
    -> Model Before Change for handoff-owned candidates
    -> survive-or-die
    -> apply only survivors
    -> review again only while surviving handoff-owned blocker/high corrections remain
```

Convergence is governed by `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.

Do not normalize for aesthetic uniformity. Normalize only where representation affects meaning, ownership, state, action, recovery, or a material consumer.
