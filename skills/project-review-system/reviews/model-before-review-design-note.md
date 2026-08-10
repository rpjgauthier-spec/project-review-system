# Model-Before-Review Reasoning — Living Design Note

## Status and authority

This is a living, non-authoritative design note for the Project Review System local-first refactor.

It records a review-method improvement discovered while iteratively adversarially reviewing a Codex recovery handoff. It does **not** change current Project Review System authority, review stages, execution controls, or production behavior by itself.

## Problem

Repeated full-document reviews still tended to discover only a few new defect classes per pass because the reviewer was reading the target primarily as prose. Important dimensions such as authority, identity binding, chronology, staleness, task completion, validation ownership, and failure recovery were often rediscovered only after later corrections made them salient.

This creates an avoidable pattern:

```text
review prose
  -> find salient defect
  -> correct
  -> later discover another latent model-level defect
```

Some iteration is unavoidable because corrections can create new defects. The avoidable part is failing to systematically inspect defect classes that were already present.

## General principle

Before a semantic review, construct or refresh the **minimum useful model of the thing being reviewed**, then review the target against that model rather than relying only on linear prose reading.

Conceptually:

```text
freeze purpose
    -> map authorities
    -> map identities/bindings
    -> map states/transitions
    -> extract invariants
    -> enumerate material failure paths
    -> select stage-specific review model
    -> sweep the full target
    -> report the complete bounded finding set
```

This is complementary to Model Before Change:

```text
before review     -> Model Before Review
before correction -> Model Before Change
```

## Intended effect

Model Before Review should increase the number of independent credible defects found in a single bounded pass by making the review surface explicit.

For example, an adversarial review of a recovery workflow may need to test:

- authority provenance;
- user/task authorization;
- repository/remote/ref identity;
- review-record/revision/target binding;
- chronology and historical control applicability;
- stale queue/gate/result evidence;
- failure and recovery paths;
- semantic execution boundaries;
- validation ownership;
- task-completion boundaries;
- preservation of unrelated user work and durable history.

The goal is not to maximize finding count mechanically. Low-value wording preferences should not be inflated into defects.

## Whole-sweep rule

A declared full semantic review should not stop diagnostic discovery merely because one blocker is found.

The reviewer should complete the bounded sweep across all applicable modeled dimensions and collect all blocker/high findings that can still be evaluated reliably.

A blocker may terminate the target workflow while not terminating the diagnostic review of the remaining interpretable target.

## Stage-specific models

The shared Model-Before-Review step should select a stage-specific review model when one exists.

For example, an Adversarial model can define:

- authority attacks;
- identity-confusion attacks;
- stale-state attacks;
- unsafe fallback/failure attacks;
- scope-escape attacks;
- validation-owner attacks;
- trust-boundary attacks;
- completion-path attacks.

Interdependency, Normalization, Structural Optimization, and End-to-end validation may eventually have their own domain-appropriate stage models.

Do not require identical review artifacts for every stage or domain.

## Adaptive depth

For a simple focused review, the useful model may be only a short list of purpose, constraints, and dependencies.

For governance/stateful/safety-sensitive review, explicit authority, state, identity, invariant, and failure-path models may be justified.

Do not turn Model Before Review into mandatory paperwork whose complexity exceeds the review target.

## Model freshness

If a correction changes an authority edge, identity binding, state transition, invariant, validation owner, task boundary, or material failure path, the applicable review model should be refreshed before the next semantic review.

A stale review model can hide exactly the secondary defects the method is intended to expose.

## Relationship to Structural Optimization

Model Before Review should broaden defect discovery. It should **not** authorize every proposed safeguard.

After findings:

1. apply Model Before Change to the proposed correction set;
2. structurally optimize / justify the proposed corrections;
3. implement only those that retain distinct risk-reduction value.

This separation prevents comprehensive adversarial review from rebuilding unnecessary governance.

## Handoff-maintenance dogfood

The immediate dogfood implementation uses three maintenance artifacts:

1. a maintenance guide containing the mandatory pre-review trigger;
2. a shared Model-Before-Review method;
3. a stage-specific Adversarial Review Model.

The recovery handoff itself does not contain this maintenance machinery, preserving the separation between runtime recovery instructions and handoff-maintenance method.

## Future PRS integration question

A future PRS implementation may make Model Before Review an adaptive pre-stage capability rather than a new semantic stage.

Potential controller responsibilities could include:

- selecting a stage-appropriate review representation;
- generating deterministic model fragments where possible;
- binding review models to exact target snapshots;
- detecting stale models after target changes;
- recording which model revision a semantic pass consumed;
- enforcing declared whole-sweep completion without claiming semantic correctness.

Any such implementation requires normal governed design/review/cutover. This note alone authorizes none of it.
