# Model Before Review — Handoff Maintenance Method

## Purpose

Use this method before every semantic review of the Codex recovery handoff.

Its purpose is to prevent a reviewer from treating the handoff as prose alone. Before review begins, the reviewer must construct or refresh the minimum useful model of the handoff's purpose, authorities, identities, state transitions, invariants, dependencies, and failure paths, then use the applicable stage-specific review model to sweep the entire target.

This is a handoff-maintenance method. It is not Project Review System authority.

## Mandatory trigger

Before **every semantic review** of the Codex recovery handoff:

1. read this method;
2. freeze the handoff's current governing purpose and task boundary;
3. identify the current authority model;
4. identify the current identity/binding model;
5. identify the current state-flow/recovery model;
6. identify protected invariants;
7. identify material failure-path families;
8. select the applicable stage-specific review model;
9. update that model if the handoff revision changed any authority edge, identity, state transition, invariant, or failure path;
10. only then begin the semantic review.

Do not skip Model Before Review because the handoff revision appears small.

For a truly local mechanical correction that does not require semantic review, this method does not apply.

## Minimum review model

Before semantic review, establish at least:

### Purpose

What exact job must the handoff accomplish, and where must it stop?

### Authorities

Which source owns:

- host/user authorization;
- PRS review mode and governance;
- current review/change state;
- source-scope authority;
- chronology/provenance evidence;
- derived state;
- non-authoritative handoff context?

### Identities and bindings

Which identities must remain correctly bound?

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

What states/transitions does the handoff direct?

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

What must remain true despite review/correction?

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

What material failure families must be attacked?

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

## Stage-specific review models

Model Before Review does not itself perform the semantic stage.

It selects the appropriate stage-specific model.

### Adversarial

Mandatory stage model:

`CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

Use it to sweep the entire handoff across authority, authorization, identity, state, chronology, staleness, failure, recovery, scope, validation ownership, trust boundary, preservation, and completion.

The Adversarial reviewer must finish the declared whole-document sweep before reporting its complete blocker/high set, unless the target becomes uninterpretable.

### Other stages

Interdependency, Normalization, Structural Optimization, and End-to-end review may use stage-specific models as they are created.

Until a dedicated model exists, the reviewer must still perform this Model-Before-Review step and derive the minimum stage-appropriate representation rather than reverting to an unmodeled linear prose read.

## Update rule

If a correction changes any of the following:

- authority source or precedence;
- identity or binding relationship;
- state transition;
- completion boundary;
- failure/recovery path;
- validation ownership;
- trust boundary;
- semantic execution behavior;

then update the applicable review model before the next semantic review.

Do not allow the review model to become stale relative to the handoff.

## Relationship to Model Before Change

These methods protect different boundaries.

```text
before review
    -> MODEL BEFORE REVIEW
    -> semantic findings

before correction
    -> MODEL BEFORE CHANGE
    -> correction
```

Model Before Review asks:

> What explicit system model should the reviewer attack so it does not miss whole classes of defects?

Model Before Change asks:

> Given the findings, what relationships/invariants could the proposed correction disturb?

Both are mandatory for nontrivial handoff maintenance at their respective boundaries.

## Relationship to Structural Optimization

Model Before Review maximizes systematic coverage.

It does **not** decide that every plausible adversarial correction deserves implementation.

After Adversarial findings are produced:

1. perform Model Before Change on the proposed correction set;
2. subject the proposed corrections to Structural Optimization / survive-or-die review;
3. apply only corrections that retain distinct justified value.

This keeps broad defect discovery from rebuilding unnecessary governance.

## Completion evidence for a review pass

Before declaring a semantic review pass complete, be able to state:

- which handoff revision was reviewed;
- which stage-specific review model was used;
- whether the model was refreshed for the current revision;
- whether the whole declared sweep completed;
- which blocker/high findings were collected.

Do not claim a full modeled sweep if only part of the document or part of the declared model was tested.

## Anti-skip rule

If a future handoff-maintenance instruction says only:

> perform an adversarial/interdependency/normalization/structural/end-to-end review

that instruction implicitly expands to:

```text
read Model Before Review
    -> refresh/select applicable review model
    -> perform the full stage review
```

A reviewer must not treat the absence of an explicit reminder in the immediate prompt as permission to skip this method.
