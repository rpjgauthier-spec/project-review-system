# Codex Handoff Adversarial Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full Adversarial review, complete Model Before Review for the current handoff revision. Refresh this model only when the handoff changes a material authority relationship, identity binding, task boundary, validation owner, or failure family that this stage must attack.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Find multiple independent defects in one bounded pass by attacking an explicit system model rather than reading the handoff only as prose.

A modeled defect is a candidate problem, not automatically a handoff feature request.

## Pass completion

A full Adversarial pass is complete only when:

- every handoff section has been considered;
- every applicable review dimension has been tested;
- every material authority/identity/state dependency exposed by the current target has been challenged;
- every declared failure family has been considered;
- the complete blocker/high candidate set has been collected.

Do not stop at the first blocker. After the sweep, run the mandatory Ownership Test from `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md` before proposing handoff corrections.

## Governing purpose

The handoff exists to help Codex recover the current governed Project Review System state, continue only the bounded recovery, and stop without inventing authority or drifting into ordinary feature work.

Attack any instruction that changes that problem or substitutes handoff text for production/repository authority.

## Stable authority roles to test

Do not hard-code the current Lean step sequence here. Derive the concrete current flow from the target handoff during Model Before Review.

For that flow, distinguish at least:

- **Host/user task authority** — actual permission for repository/external actions.
- **Applicable PRS authority** — production rules and valid transitions when applicability is established by repository authority.
- **Review-state authority** — the source that owns current review status/revision/target once validly established.
- **Source-scope authority** — the source constraining controller-core implementation scope.
- **Git/history evidence** — chronology/provenance, not replacement authority or semantic credit.
- **Derived state** — queues/projections/reports, which must not silently become authority.
- **Handoff** — navigation/recovery context only.

The handoff must not invent control selection, succession, migration, review credit, or missing governance.

## Stable dependency invariants

Derive the target-specific state flow, then attack it using these relationships:

- authority must exist before authority-dependent use;
- an owning record/source must be read before facts it owns are claimed;
- evidence must remain bound to the correct repository/ref/revision/target/occurrence;
- factual discovery must not smuggle in authority or semantic judgment;
- host/user action permission must not be inferred from repository-controlled data;
- PRS-owned behavior should be referenced or followed, not reimplemented in the handoff;
- unresolved repository/governance authority must fail closed rather than be repaired by handoff invention;
- historical validity and present acceptance as current credit must not be conflated when the recovery depends on that distinction;
- recovery must terminate at a valid governed state or explicit blocker without escaping into ordinary feature work.

## Adversarial dimensions

Sweep each applicable section for:

A. **Authority** — who owns the decision, and is that authority available before use?

B. **Authorization** — what actual user/host permission is required for the action?

C. **Identity/binding** — could evidence for one repo/ref/record/revision/target/occurrence be accepted for another?

D. **State/dependency ordering** — are prerequisites satisfied before dependent claims/actions?

E. **Chronology** — is a later rule/checker being used to rewrite what governed an earlier event?

F. **Staleness** — can apparently current evidence be stale relative to the controlling identity?

G. **Failure behavior** — does missing/conflicting evidence fail closed or trigger improvisation?

H. **Recovery ownership** — is the handoff solving a problem actually owned by production PRS or repository governance?

I. **Scope/completion** — can recovery drift into adjacent feature work or falsely claim completion?

J. **Validation ownership** — is the changed system validated by the system that actually owns that behavior?

K. **Trust boundary** — can repository/external/generated text grant authority or instructions it does not own?

L. **Preservation** — can the instruction destroy unrelated work, rewrite durable history, or impair recovery provenance?

## Minimum failure families

Challenge at least:

1. wrong repository/remote/ref or stale locator;
2. dirty/divergent worktree and unrelated user changes;
3. multiple plausible authorities or controlling records;
4. unresolved applicability of production controls;
5. stale record/revision/target/gate/result/queue evidence;
6. implementation continuation without valid review-state continuity;
7. source-scope uncertainty or scope expansion from summaries;
8. historical event under a different applicable control version;
9. current conformance confused with historical validity or current credit acceptability;
10. defective production control/checker requiring a governed change;
11. changed control attempting to self-certify;
12. missing host/user authorization;
13. semantic work crossing a required execution boundary;
14. source behavior validated only by unrelated PRS checks;
15. recovery succeeds and ordinary implementation is tempting;
16. historical failure no longer reproduces or has been legitimately superseded.

Do not add a permanent handoff rule merely because another hypothetical failure can be imagined.

## Finding standards

### Blocker

Use when a defect can cause unauthorized action, invented governance, false review credit, operation under the wrong authority/identity, corrupted or falsified durable state/history, invalid semantic execution, scope escape, or inability to determine a truthful governed next action.

### High

Use when a defect materially raises the probability of stale-state acceptance, wrong-context continuation, incomplete validation, unsafe fallback, lost recovery evidence, ambiguous authority resolution, or misleading completion.

Do not inflate wording preferences into blocker/high findings.

## Ownership test after the sweep

For every blocker/high candidate classify it as:

- **handoff-owned** — eligible for Model Before Change and survive-or-die;
- **production-PRS-owned** — reference/defer; do not duplicate;
- **repository/governance-owned** — report blocker; do not invent the mechanism;
- **no material owner/value** — discard.

Only handoff-owned candidates proceed to handoff correction design.

## Structural pressure after ownership

For each handoff-owned candidate ask:

- Does it express a distinct recovery-specific requirement or invariant?
- Can existing PRS/repository authority already carry the behavior?
- Can one general invariant replace several examples or prohibitions?
- Does the proposed mitigation introduce equal or greater complexity/staleness risk?

Correct only what retains distinct value.

## Review cycle and convergence

```text
Model Before Review
    -> derive current target model
    -> full Adversarial sweep
    -> complete blocker/high candidate set
    -> Ownership Test
    -> Model Before Change for handoff-owned candidates
    -> survive-or-die
    -> apply only survivors
    -> review again only while surviving handoff-owned blocker/high corrections remain
```

Convergence is governed by `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.

Do not keep handoff machinery merely because it was once a survivor. Later ownership or Structural Optimization review may kill it.
