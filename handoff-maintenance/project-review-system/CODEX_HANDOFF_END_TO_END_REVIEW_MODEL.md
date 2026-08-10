# Codex Handoff End-to-end Validation Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full End-to-end validation pass, complete Model Before Review for the current handoff revision and derive the concrete recovery journeys from the current target. Do not hard-code Lean's current prose sequence into this model.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Validate that the handoff works as an integrated recovery guide across complete journeys rather than only as locally correct sections.

The pass asks whether a fresh Codex session can move from initial discovery to the next truthful governed state, or to an explicit blocker, without losing authority, identity, authorization, evidence, recovery scope, or completion semantics along the way.

A failed journey is a candidate finding, not automatically a handoff feature request. Apply the mandatory Ownership Test before proposing any correction.

## Pass completion

A full End-to-end validation pass is complete only when:

- the current target-specific recovery flow has been derived from the handoff;
- every mandatory journey family below has been traced from entry to terminal condition;
- authority, identity, authorization, evidence, and scope bindings have been checked at every material transition;
- interruption/re-entry behavior has been considered where a journey can span executions;
- completion and blocker reporting have been traced to their consumers;
- the complete blocker/high candidate set has been collected;
- every blocker/high candidate has been Ownership-Tested.

Do not stop after one successful happy path or the first failure.

## Governing purpose

The handoff exists to help Codex recover the current governed Project Review System state, continue only the bounded recovery, and stop at the next valid governed state or a real blocker.

End-to-end validation must therefore test the integrated recovery behavior without turning the handoff into a duplicate PRS controller, validator, or state machine.

## Journey model

During Model Before Review, derive the current target-specific journey graph using the minimum useful form. For each journey identify:

- entry condition;
- repository/ref identity;
- governing authority source(s);
- required host/user authorization;
- review/change-state identity;
- relevant evidence and pointers;
- PRS-owned transitions delegated to production controls;
- recovery-specific decisions owned by the handoff;
- possible interruption/re-entry points;
- terminal success state;
- terminal blocker state;
- required material report output.

Do not treat this derived graph as new authority.

## Mandatory journey families

Trace at least the following when applicable to the current target.

### 1. Normal recovery

Start from the stated recovery locator, establish repository identity and applicable authority, recover the current governed state, reproduce or resolve the targeted failure, take the next permitted recovery action, validate through the owning mechanisms, and stop at the next valid governed state.

Check that no step depends on a fact not yet established and that no PRS-owned transition is silently implemented by the handoff.

### 2. Stale locator / continued implementation

The initial branch/ref is stale or implementation has continued elsewhere.

Trace whether the handoff prevents implementation continuity from being mistaken for review-state continuity, and whether unresolved continuity fails closed without inventing succession or migration rules.

### 3. Stale or conflicting review evidence

A queue, record, gate, result, report, or other apparently current artifact conflicts with the authoritative review/change state or target identity.

Trace whether stale evidence can be rejected without substituting derived state for authority and whether the next action remains determinable.

### 4. Historical failure no longer reproduces

The named historical failure has been fixed, superseded, or displaced by a different current failure.

Trace whether the handoff can establish the current governed disposition without forcing reproduction of an obsolete state or falsely declaring success merely because the old failure disappeared.

### 5. Historical-credit dispute

Past evidence was produced under an earlier applicable control version or disputed execution history.

Trace whether historical validity and current acceptability as review credit remain distinct through diagnosis, correction, validation, and reporting.

### 6. Authorized correction and revalidation

A handoff-owned or governed recovery defect is identified and both PRS governance and host/user task authorization permit correction.

Trace through correction, required revalidation/validation, durable state updates, and the resulting next governed state. The handoff must delegate PRS transition mechanics to production controls rather than encoding them itself.

### 7. Correction not authorized

A required change is identified but actual action authorization is absent or narrower than PRS governance permits.

Trace to a blocked recovery without unauthorized writes, false completion, or pressure on the user to provide deterministic facts the system can derive itself.

### 8. Defective or insufficient governing mechanism

The apparent recovery requires a transition, authority rule, succession rule, self-certification path, or history rewrite that current repository governance cannot truthfully represent.

Trace to an explicit blocker. The handoff must not manufacture the missing mechanism.

### 9. Interrupted recovery / fresh-session continuation

Recovery is interrupted after material discovery, diagnosis, correction, or validation evidence has been created.

Trace whether a later session can re-establish current authority and state from durable repository evidence rather than trusting conversational memory or stale local assumptions.

Do not require the handoff to invent persistence already owned by PRS/repository mechanisms.

### 10. Successful recovery / temptation to continue

The targeted recovery reaches the next valid governed state.

Trace whether Codex stops rather than drifting into ordinary feature implementation, speculative cleanup, method evolution, or unrelated repair.

## Cross-journey invariants

Across every journey, test that:

- repository/ref identity remains bound to the evidence being used;
- applicable authority is established before authority-dependent action;
- host/user action authorization remains distinct from PRS-governed permission/state;
- source-scope constraints remain in force until legitimately advanced;
- derived state never silently becomes authority;
- historical evidence remains chronology/provenance unless current governance accepts it as current credit;
- stale or conflicting evidence fails closed;
- corrections propagate through the validation/revalidation mechanisms owned by the affected system;
- required semantic execution boundaries are respected through PRS rather than reimplemented here;
- unrelated user work and durable history remain preserved;
- success and blocker outcomes produce enough material reporting for the next consumer;
- the handoff terminates at recovery completion/blocker instead of expanding scope.

## Integrated failure classes

Look specifically for:

1. a journey that cannot start without assuming its own authority;
2. a transition whose producer and consumer disagree about identity or state;
3. a fallback that silently broadens authority or scope;
4. a correction path that lacks downstream revalidation/validation propagation;
5. a blocked path mislabeled as successful completion;
6. successful local steps whose composition creates an invalid global path;
7. an interruption point from which truthful re-entry is impossible;
8. a historical/current distinction that collapses during later steps;
9. a pointer treated as proof or a report treated as authority;
10. an end state that leaves the next consumer unable to determine what happened or what boundary comes next;
11. a route that requires duplicated PRS machinery in the handoff to function;
12. a route that continues beyond bounded recovery after success.

## Finding standards

### Blocker

Use when an integrated journey can cause unauthorized action, invented governance, wrong-context recovery, false review credit, corrupted/falsified durable history, invalid semantic execution, unrecoverable interruption, scope escape, or inability to reach a truthful terminal state.

### High

Use when an integrated journey materially raises the probability of stale-state acceptance, broken propagation, wrong downstream validation, ambiguous recovery completion, lost re-entry context, or misleading reporting.

Do not inflate cosmetic sequencing preferences into blocker/high findings when the integrated behavior remains correct.

## Ownership test after the sweep

For every blocker/high candidate classify it as:

- **handoff-owned** — the handoff's integrated navigation/recovery behavior is defective;
- **production-PRS-owned** — PRS owns the missing transition, execution rule, revalidation, validation, or state behavior;
- **repository/governance-owned** — repository authority or governance lacks the required mechanism;
- **no material owner/value** — the proposed mitigation is redundant, speculative, or more burdensome than the risk.

Only handoff-owned candidates proceed to Model Before Change and survive-or-die.

## Structural pressure after ownership

For each handoff-owned candidate ask:

- Is the failure truly end-to-end, or already covered by an existing local invariant?
- Can the correction be expressed as one recovery-specific boundary instead of a new workflow?
- Would production PRS or repository governance still own the behavior if the handoff disappeared?
- Does the mitigation add state, authority, lifecycle, or maintenance burden disproportionate to the failure reduced?

Prefer the smallest correction that restores the journey without duplicating the systems being navigated.

## Convergence

The End-to-end maintenance stage converges when every mandatory applicable journey has been traced and no blocker/high handoff correction survives both Ownership Testing and Structural Optimization.

A remaining production-PRS or repository/governance blocker does not justify additional handoff machinery merely to produce a clean handoff result.
