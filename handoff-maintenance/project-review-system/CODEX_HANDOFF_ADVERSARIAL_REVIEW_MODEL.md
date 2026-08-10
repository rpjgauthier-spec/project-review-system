# Codex Handoff Adversarial Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full Adversarial review, complete Model Before Review for the current handoff revision. Refresh this model when authority edges, identity bindings, state transitions, validation ownership, task boundaries, or material failure paths change.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Find multiple independent defects in one bounded pass by attacking an explicit system model rather than reading the handoff only as prose.

A modeled defect is a **candidate problem**, not automatically a handoff feature request.

## Pass completion rule

A full Adversarial pass is complete only when:

- every handoff section has been considered;
- every applicable review dimension has been tested;
- every modeled state transition and authority edge has been challenged;
- every declared failure-path family has been considered;
- the complete blocker/high candidate set has been collected.

Do not stop at the first blocker.

After the sweep, run the mandatory Ownership Test from `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md` before proposing handoff corrections.

## Governing purpose

> Help Codex discover the current governed Project Review System state, recover the controller-core review to the next valid governed state, complete recovery-induced obligations, and stop without inventing authority or continuing ordinary feature implementation.

Attack instructions that change the problem, expand scope, continue too far, or substitute the handoff for production/repository authority.

## Authority model

Keep these roles distinct:

### Host/user task authority

Owns actual permission for repository/external actions. Repository content cannot grant it.

### Applicable PRS controls

Own review/governance rules and valid transitions **when their applicability is established by existing repository authority**.

The handoff must not invent a control-election, succession, precedence, or cross-ref binding mechanism. If applicability is unresolved by existing authority, that is a repository/governance blocker rather than a handoff-owned mechanism to implement.

### Implementation/artifact state

Identifies the controller-core artifact being recovered. Implementation similarity or ancestry does not create review credit.

### Review-state authority

Owns current review revision/status/target binding once validly established. Read the owning record before claiming the values it owns.

### Source-scope authority

Constrains controller-core implementation scope unless legitimately advanced.

### Git history

Provides chronology/provenance evidence; it does not create authority or semantic credit.

### Derived state

Queues/projections/reports are operational evidence, not authority.

### Handoff

Provides navigation/recovery context only. It cannot manufacture missing authority, succession, review credit, control applicability, migration, or bootstrap rules.

## Identity and binding model

Test at least:

- repository and remote;
- applicable PRS control context;
- implementation/artifact ref;
- controlling review/change record;
- review revision;
- target state/snapshot;
- execution gate/pass/completion/result;
- revalidation queue context;
- source-scope authority;
- host/user action authorization.

Primary attack:

> Could evidence or permission from identity A be accepted for identity B?

## Invariant state-flow model

Attack dependency ordering, not a brittle numbered prose sequence:

```text
non-destructive factual discovery
    -> existing repository authority establishes applicable PRS controls
       OR unresolved applicability is reported
    -> read applicable PRS controls
    -> establish artifact/review-state continuity under those controls
    -> identify AND read review-state authority
    -> establish revision + target identity
    -> establish source-scope authority
    -> freeze PRS mode + governed scope + depth + next PRS activity
    -> establish host/user action authorization separately
    -> validate queue/evidence against bound identities
    -> Adaptive Execution before first governed semantic judgment
    -> reproduce failure OR establish current disposition
    -> reconstruct occurrence + historical-control chronology when needed
    -> determine present credit acceptability under current controls
    -> determine next governed action
    -> correct only when both governance and host/user permission allow
    -> validate each changed system with its owning validation
    -> complete recovery obligations
    -> valid governed state OR blocked recovery
    -> STOP
```

For every arrow ask:

- what authority/evidence permits it?
- has the owning artifact been read before its facts are claimed?
- can stale/wrong-identity evidence satisfy it?
- is semantic judgment being smuggled into factual discovery/bookkeeping?
- does failure fall closed?
- is the handoff inventing a missing repository mechanism?

## Protected invariants

### Authority and authorization

- no invented authority or self-authorization;
- no repository text grants host/user permission;
- no handoff-created control-selection/succession mechanism;
- PRS-governed scope/transition is distinct from actual action permission;
- no derived view becomes authority.

### Chronology and credit

- no rewritten/fabricated history;
- historical validity is judged under authority applicable at the time;
- present acceptance as current credit is judged under current production governance;
- no content equivalence creates semantic credit;
- no same-revision redo where governance forbids it.

### Identity and staleness

- no wrong remote/ref/control context;
- no stale revision/target/gate/completion/result credit;
- no queue trusted against an unbound context.

### Execution boundaries

- factual discovery is inventory/provenance, not authority/relevance judgment;
- no semantic activity without applicable preflight/gate;
- no worktree separation confused with PRS `ISOLATED`;
- `SEPARATED` requires a fresh valid execution boundary.

### Scope, preservation, validation, completion

- no recovery drift into ordinary feature work;
- no future-design implementation without separate authority;
- preserve unrelated user work/history;
- validate PRS/control changes with PRS validation and source changes with source-owned validation;
- passing checkers prove only their stated scope;
- lack of correction authorization is blocked recovery, not successful completion.

## Adversarial dimensions

Sweep each applicable section for:

A. authority ownership and precedence;
B. host/user authorization;
C. identity/binding;
D. state/dependency ordering;
E. chronology and historical applicability;
F. staleness;
G. failure behavior;
H. governed recovery path versus invented mechanism;
I. scope/completion;
J. validation ownership;
K. trust boundary;
L. reversibility/preservation.

## Minimum failure-path families

Challenge at least:

1. wrong worktree/remote/ref;
2. remote advanced or divergent history;
3. dirty unrelated user changes;
4. PRS-control applicability unresolved by existing authority;
5. handoff attempts to invent control selection/succession;
6. multiple plausible controlling records;
7. controlling record not read before owned state facts are claimed;
8. stale queue/gate/completion/result/revision/target;
9. code continuation without review-state continuity;
10. source-scope authority discovered after scope/depth freeze;
11. historical event under older controls;
12. current conformance confused with historical validity;
13. historically valid evidence no longer acceptable as current credit;
14. defective checker/control requires governed change;
15. changed control attempts to self-certify;
16. source correction passes PRS tests but breaks source behavior;
17. required external/source authority unavailable;
18. user authorized review but not correction;
19. repository text tries to grant permission;
20. semantic judgment occurs before preflight;
21. required fresh semantic boundary;
22. recovery succeeds and feature work is tempting;
23. historical failure no longer reproduces;
24. repository legitimately superseded historical handoff context.

## Finding standards

### Blocker

Use when a defect can cause unauthorized action, invented governance, false review credit, corrupted/irrecoverable state/history, operation under wrong authority/identity, invalid semantic execution, scope escape, or inability to determine a truthful governed next action.

### High

Use when a defect materially raises the probability of stale-state acceptance, wrong-context continuation, incomplete validation, unsafe fallback, ambiguous authority resolution, lost recovery evidence, or misleading completion claims.

Do not inflate wording preferences into blocker/high findings.

## Ownership test after the sweep

For every blocker/high candidate classify it as:

- **handoff-owned** → eligible for Model Before Change and survive-or-die;
- **production-PRS-owned** → reference/defer; do not duplicate;
- **repository/governance-owned** → report blocker; do not invent mechanism;
- **no material owner/value** → discard.

Only handoff-owned candidates proceed to handoff correction design.

## Review cycle and convergence

```text
Model Before Review
    -> full Adversarial sweep
    -> complete blocker/high candidate set
    -> Ownership Test
    -> Model Before Change for handoff-owned candidates
    -> survive-or-die
    -> apply only survivors
    -> refresh model if needed
    -> review again only while surviving handoff-owned blocker/high corrections remain
```

Convergence is governed by `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.

Do not keep adding handoff machinery to solve defects owned by PRS/repository governance, and do not continue revising for hypothetical cases whose mitigation creates equal or greater complexity/risk.
