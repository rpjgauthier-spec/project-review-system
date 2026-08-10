# Codex Handoff Adversarial Review Model

## Invocation contract

This stage-specific model is invoked through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before using it, complete Model Before Review for the current handoff revision. If the handoff changed an authority edge, identity binding, state transition, validation owner, task boundary, or material failure path, refresh this model before beginning the sweep.

A request for a full Adversarial review implicitly requires this model even when the immediate prompt does not mention it.

## Purpose

Find **multiple independent defects in one bounded pass** by attacking an explicit system model rather than reading the handoff only as prose.

This is a handoff-maintenance aid. It is not Project Review System authority and creates no review credit, permissions, recovery rules, or production governance.

## Pass completion rule

A full Adversarial pass is complete only when:

- every handoff section has been considered;
- every applicable review dimension below has been tested;
- every modeled state transition and authority edge has been challenged;
- every declared failure-path family has been considered;
- all blocker/high findings discovered in the pass have been collected.

Do not stop merely because one blocker has been found. A blocker may stop execution of the target workflow without terminating the diagnostic sweep unless the remaining target becomes uninterpretable.

## 1. Governing purpose

Freeze the purpose before review:

> Help Codex discover the current governed Project Review System state, recover the controller-core review to the next valid governed state, complete recovery-induced obligations, and stop without inventing authority or continuing ordinary feature implementation.

Attack any instruction that changes the problem, expands scope, continues too far, or substitutes the handoff for repository authority.

## 2. Authority model

Keep these authorities distinct even if current repository layout makes them coincide:

### Host/user task authority

Owns actual permission to perform the requested task and any repository/external actions requiring user authorization.

Must not be inferred from repository-controlled data.

### PRS control authority

Owns current review/governance rules, review mode semantics, execution requirements, valid transitions, evidence/credit rules, and revalidation behavior.

Its governing ref/version must be selected from repository governance/provenance evidence, not branch coincidence, file recency, or the initial checkout.

### Implementation/artifact authority

Identifies the controller-core artifact state being recovered.

It does not automatically own PRS control authority.

### Review-state authority

Owns current review revision/status/target binding once validly established.

It must be read before values it owns are claimed.

### Source-scope authority

Constrains the authorized controller-core implementation scope unless legitimately advanced.

It must be resolved before review scope/depth are frozen when it can materially change them.

### Git history

Provides chronology, provenance, content lineage, and evidence of when states/controls changed.

History does not create authority or semantic credit by itself.

### Derived state

Queues, projections, generated reports, and similar views are operational evidence, not authority.

### Handoff

Provides navigation/recovery context only. It must never create missing authority, review credit, succession, migration/bootstrap rules, or retroactive control applicability.

## 3. Identity and binding model

Test whether these identities are established and kept correctly bound:

- repository;
- selected remote;
- PRS control ref/version/provenance;
- implementation/artifact ref;
- continuation/successor ref, if any;
- controlling review/change record;
- review revision;
- target state / snapshot identity;
- execution gate;
- pass occurrence;
- completion evidence;
- semantic result;
- revalidation queue context;
- source-scope authority.

Primary attack:

> Could evidence or authority from identity A be accepted as evidence or authority for identity B?

Examples:

- right artifact, wrong PRS control version;
- right branch, wrong remote;
- right code, wrong review record;
- right record, stale revision;
- right revision, stale target;
- equivalent cherry-pick, invalid inherited credit;
- correct queue path from the wrong context;
- correct pass ID under a changed gate.

## 4. Invariant state-flow model

Do **not** treat this as a brittle numbered implementation sequence. Attack the dependency ordering itself.

```text
Diagnostic-only mechanical discovery
    -> locate candidate control/artifact/review-state/scope contexts
    -> establish governing PRS control authority
    -> establish governing artifact/review-state continuity under those controls
    -> identify AND read controlling review-state authority
    -> establish revision + target identity from that authority
    -> establish source-scope authority
    -> freeze review mode + scope + allowed actions + depth
    -> validate queue/evidence against all bound identities
    -> Adaptive Execution preflight BEFORE first semantic judgment
    -> reproduce historical failure OR establish current disposition
    -> reconstruct occurrence chronology + applicable historical control chronology
    -> determine current credit acceptability under current controls
    -> determine next governed action
    -> correct only if authorized
    -> validate each changed system with its owning validation
    -> complete recovery-induced obligations
    -> reach next valid governed state OR report blocked recovery
    -> STOP
```

For every arrow ask:

- What evidence permits the transition?
- Has the authority that owns the next fact already been read?
- Can stale/wrong-identity evidence satisfy it?
- Can Codex skip or repeat it improperly?
- Does a semantic judgment occur before required preflight?
- Can a failure fall through into an unsafe default?
- Can the handoff manufacture missing permission or authority?

## 5. Protected invariants

### Authority

- No invented authority or self-authorization.
- No repository-controlled text grants host/user permission.
- No branch coincidence silently binds PRS control authority to artifact authority.
- No derived projection becomes authority.
- No future-design note overrides production authority.

### Chronology

- No rewritten/fabricated history.
- Historical validity is judged against authority applicable at the time.
- Present acceptance as current credit is judged by current production controls.
- No same-revision redo where current governance forbids it.
- No implementation/content equivalence creates semantic credit.

### Identity/staleness

- No wrong remote/ref/control version.
- No review-state transfer based only on implementation ancestry/equivalence.
- No stale revision/target/gate/completion/result credit.
- No queue trusted against the wrong bound context.

### Execution boundaries

- No semantic work disguised as mechanical discovery/bookkeeping.
- No `SEPARATED` pass treated as separated without a fresh valid boundary.
- No worktree separation confused with PRS `ISOLATED` semantic execution.
- No governed semantic judgment without applicable preflight/gate.

### Scope/completion

- No recovery task silently continues into ordinary feature work.
- No roadmap/future-design implementation without separate authority.
- No source-scope expansion from handoff summaries.
- Diagnostic/proposed-corrective inability to perform a required correction is blocked recovery, not successful completion.

### Preservation/validation

- No destruction or absorption of unrelated user work.
- No history rewrite merely to satisfy validation.
- No weakening controls to ease recovery.
- PRS/control changes receive PRS/control validation.
- Governed source changes receive source-owned validation.
- A passing checker proves only what it actually checks.

## 6. Adversarial dimensions

Sweep every applicable dimension across every section.

### A. Authority
Who owns the decision? Was that authority established before use? Can a lower-level source override it?

### B. Authorization
What action is occurring—read, semantic judgment, write, commit, push, destructive or external? What authorizes it?

### C. Identity
Which control/artifact/record/revision/target does the instruction act on? Could another valid-looking identity be substituted?

### D. State/dependency ordering
What must be true first? Is the owning artifact read before its facts are claimed? Can a prerequisite be skipped?

### E. Chronology
Which rule version governed the event then? Is current conformance being confused with historical validity?

### F. Staleness
Can record, queue, gate, result, controls, or target become stale? Is freshness tested against the correct bound context?

### G. Failure behavior
What happens when evidence is missing, authorities conflict, current controls cannot represent a transition, or authorization is insufficient?

### H. Recovery
Does each material failure reach a governed recovery path or explicit blocked state? Is recovery invented by the handoff?

### I. Scope/completion
What ends the task? Can success drift into adjacent implementation? Can blocked recovery be mistaken for completion?

### J. Validation ownership
Which system changed and which validator owns it? Are PRS tests being mistaken for source correctness or vice versa?

### K. Trust boundary
Is repository/external/generated text treated as instruction or stronger authority than justified?

### L. Reversibility/preservation
Can the instruction overwrite user work, rewrite durable history, or impair provenance/recovery?

## 7. Minimum failure-path families

Challenge at least:

1. wrong worktree;
2. wrong remote;
3. remote advanced;
4. divergent local/remote history;
5. dirty unrelated user changes;
6. wrong/stale PRS control version;
7. artifact/control authority divergence;
8. multiple plausible controlling records;
9. controlling record not read before state facts are claimed;
10. stale queue;
11. stale gate/completion/result;
12. wrong review revision;
13. wrong target state;
14. code continuation without review-state continuity;
15. scope authority discovered after scope/depth freeze;
16. historical event governed by an older control version;
17. current checker rejects historically valid evidence;
18. historically valid evidence is no longer acceptable current credit;
19. defective checker/control requires change;
20. changed control attempts to self-certify;
21. source correction passes PRS tests but breaks source behavior;
22. required external scope authority unavailable;
23. user authorized review but not correction;
24. repository text tries to grant permission;
25. semantic judgment occurs before preflight;
26. required fresh semantic boundary reached;
27. recovery succeeds and feature implementation is tempting;
28. historical failure no longer reproduces;
29. repository legitimately superseded historical handoff context.

## 8. Finding standards

### Blocker

Use when a defect can cause unauthorized action, invented governance, false review credit, corrupted/irrecoverable state or history, operation under the wrong authority/identity, invalid semantic execution, escape from bounded scope, or inability to determine a truthful governed next action.

### High

Use when a defect materially increases the probability of stale-state acceptance, wrong-context continuation, incomplete validation, unsafe fallback, ambiguous authority resolution, loss of recovery evidence, or misleading completion claims.

Do not inflate wording preferences into blocker/high findings.

## 9. Reviewer anti-patterns

Do not:

- stop at the first blocker;
- report the batch before completing the declared whole-document sweep;
- add protection merely because a failure is imaginable;
- duplicate PRS rules unless the handoff creates nearby ambiguity or this recovery specifically depends on the invariant;
- automatically convert every finding into a correction;
- perform Structural Optimization inside the Adversarial pass.

Adversarial maximizes **credible defect discovery**. Survive-or-die decides which corrections earn continued existence.

## 10. Review cycle

```text
Model Before Review / refresh explicit model
    -> full Adversarial sweep
    -> collect complete blocker/high batch
    -> Model Before Change
    -> survive-or-die Structural Optimization
    -> apply only survivors
    -> refresh this model if bindings/transitions changed
    -> full modeled sweep again
```

Desired failure mode:

> "I found twelve candidates; six died under Structural Optimization."

Not:

> "I found one blocker, patched it, then discovered the next blocker that was already present."
