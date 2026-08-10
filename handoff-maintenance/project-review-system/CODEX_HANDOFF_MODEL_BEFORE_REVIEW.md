# Model Before Review — Handoff Maintenance Method

## Purpose

Use this method before every semantic review of the Codex recovery handoff.

Its purpose is to prevent a reviewer from treating the handoff as prose alone. Before review begins, construct or refresh the minimum useful model of purpose, authorities, identities, state transitions, invariants, dependencies, failure paths, and the bounded target-derived coverage inventory that defines what the selected stage must actually exhaust.

This is a handoff-maintenance method. It is not Project Review System authority.

## Mandatory trigger

Before every semantic review of the Codex recovery handoff:

1. read this method;
2. freeze the current governing purpose and task boundary;
3. identify the authority model;
4. identify the identity/binding model;
5. identify the state-flow/recovery model;
6. identify protected invariants;
7. identify material failure-path families;
8. select the applicable stage-specific review model;
9. derive the minimum useful finite/bounded target-specific coverage inventory required by that stage, including only material combinations exposed by the target;
10. refresh the stage model if the handoff revision changed an authority edge, identity, state transition, invariant, validation owner, task boundary, material failure path, or the classes the stage must close;
11. only then begin semantic review.

Do not skip Model Before Review because a revision appears small.

For a truly local mechanical correction that does not require semantic review, this method does not apply.

## Minimum review model

### Purpose

What exact job must the handoff accomplish, and where must it stop?

### Authorities

Identify which source owns:

- host/user authorization;
- PRS review mode and governance;
- current review/change state;
- source-scope authority;
- chronology/provenance evidence;
- derived state;
- non-authoritative handoff context.

### Identities and bindings

At minimum consider:

- repository;
- remote;
- branch/ref;
- controlling review/change record;
- review revision;
- target state/snapshot;
- gate/pass/completion/result evidence;
- generated queue/projection context;
- source-scope authority.

### State flow

At minimum model:

```text
discover
    -> establish authority
    -> establish governing state
    -> reproduce/diagnose
    -> determine governed action
    -> correct if authorized
    -> validate
    -> recover
    -> complete obligations
    -> stop
```

### Invariants

Typical examples:

- no invented authority;
- no unauthorized writes;
- no fabricated history;
- no stale credit;
- no retroactive rule application without applicability evidence;
- no wrong-identity evidence reuse;
- no semantic-pass fusion;
- no recovery scope escape;
- no loss of unrelated user work.

### Failure paths

Examples:

- wrong remote/ref;
- dirty/divergent worktree;
- conflicting current-state evidence;
- stale gate/queue/result;
- historical control-version mismatch;
- defective control requiring governed change;
- source change validated by wrong test owner;
- missing authorization;
- required fresh semantic boundary;
- recovery success followed by unwanted feature continuation.

## Shared coverage-closure invariant

A full semantic review may not be claimed merely because every stage heading or broad dimension was considered.

Before the sweep, derive the smallest useful bounded inventory of the target-specific units, classes, or material combinations that the selected stage says must be exhausted. The stage-specific model defines what those units are.

During the sweep:

1. close every material inventory unit or justified material combination;
2. record or explain exclusions when a candidate class is not materially applicable;
3. do not require universal Cartesian products when most combinations have no material consumer or failure mode;
4. add a newly exposed material class to the active inventory rather than silently treating the original inventory as exhaustive;
5. do not declare the pass complete until every active inventory item is closed or the target becomes uninterpretable.

The coverage witness may be a compact list, matrix, graph annotation, or equivalent derived representation. It need not become a permanent artifact unless another durable consumer requires it.

A prose assertion that “all dimensions were tested” is not completion evidence when a bounded target-derived witness can be produced.

## Cross-stage detection ownership

When a multi-stage review sequence is being treated as methodologically complete, map each material defect/failure class exposed by Model Before Review to at least one explicit stage lens that owns its detection.

- overlap between stages is allowed;
- detection ownership does not transfer correction ownership;
- an ownerless material defect class is a maintenance-method coverage gap;
- do not create a new stage merely because two existing stages overlap or because a low-value hypothetical class can be imagined.

This is a compact method-coverage check, not a second semantic review workflow.

## Ownership test — mandatory before proposing a handoff correction

A modeled defect does **not** automatically justify a new handoff feature or rule.

For every blocker/high candidate, identify the owning layer before proposing correction:

1. **Handoff-owned** — the handoff is ambiguous, incorrectly ordered, misleading, or missing navigation needed for this recovery. Correct the handoff with the smallest coherent change.
2. **Production-PRS-owned** — current PRS already owns the behavior. Reference or defer to PRS; do not duplicate its mechanism in the handoff.
3. **Repository/governance-owned** — the required authority, succession rule, transition, or mechanism is genuinely absent or unresolved in the repository. Report the blocker; do not manufacture the missing mechanism in the handoff.
4. **No material owner/value** — the candidate is theoretical, redundant, or its mitigation adds equal or greater complexity/risk. Discard it.

A missing relationship discovered by the model is evidence that something must be resolved; it is **not** evidence that the handoff owns the resolution.

Before a correction survives, ask:

> If this behavior disappeared from the handoff, which authoritative layer should still own it?

If the answer is production PRS or repository governance, the handoff should point, defer, or stop—not implement a substitute.

## Stage-specific review models

Model Before Review does not itself perform a semantic stage.

### Adversarial

Mandatory stage model:

`CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

Use it to sweep the entire handoff across authority, authorization, identity, state, chronology, staleness, failure, recovery, scope, validation ownership, trust boundary, preservation, and completion.

The Adversarial reviewer must finish the declared whole-document sweep and close its target-derived coverage inventory before reporting its complete blocker/high set unless the target becomes uninterpretable.

### Other stages

Use the dedicated stage-specific models for Interdependency, Normalization, Structural Optimization, and End-to-end validation.

Each stage model must define the target-derived units/classes or material combinations that constitute closure under the shared coverage invariant. If a dedicated model is unavailable, still perform this Model-Before-Review step and derive the minimum stage-appropriate representation rather than reverting to an unmodeled linear prose read.

## Update rule

If a correction changes authority source/precedence, identity/binding, state transition, completion boundary, failure/recovery path, validation ownership, trust boundary, semantic execution behavior, or the material classes required for stage closure, refresh the applicable review model before the next semantic review.

## Relationship to Model Before Change

```text
before review
    -> MODEL BEFORE REVIEW
    -> semantic findings
    -> OWNERSHIP TEST

before correction
    -> MODEL BEFORE CHANGE
    -> Structural Optimization / survive-or-die
    -> correction
```

Model Before Review asks what explicit system model and bounded coverage set should be attacked.

The Ownership Test asks which layer owns the discovered defect.

Model Before Change asks what relationships/invariants a surviving proposed correction could disturb.

## Relationship to Structural Optimization

Model Before Review maximizes systematic coverage. It does not decide that every plausible correction deserves implementation.

After findings:

1. run the Ownership Test;
2. perform Model Before Change only for surviving handoff-owned correction proposals;
3. subject them to Structural Optimization / survive-or-die;
4. apply only corrections retaining distinct justified value.

This prevents broad defect discovery from rebuilding unnecessary governance inside the handoff.

## Completion evidence for a review pass

Before declaring a semantic review complete, be able to state:

- handoff revision reviewed;
- stage-specific model used;
- whether the model was refreshed;
- target-derived coverage inventory used;
- whether every active inventory item/material combination was closed or explicitly excluded as non-material;
- whether the whole declared sweep completed;
- complete blocker/high candidate set.

When claiming completion of the multi-stage maintenance sequence, also verify that every material defect/failure class exposed by the shared model has at least one explicit owning detection lens.

Do not claim a full modeled sweep if only part of the target/model or only representative coverage classes were tested.

## Anti-skip rule

A future instruction to perform a semantic review implicitly expands to:

```text
read Model Before Review
    -> refresh/select applicable model
    -> derive bounded target-specific coverage inventory
    -> perform full stage review and close the inventory
    -> ownership-test resulting blocker/high candidates before proposing handoff changes
```
