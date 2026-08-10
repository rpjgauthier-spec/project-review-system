# Codex Handoff Stage Model Completeness Audit

## Status

**Deferred maintenance audit.**

Do not treat this document as Project Review System authority and do not interrupt an active semantic-stage correction loop merely to execute it.

Run this audit after the current handoff's five-stage review sequence reaches its appropriate stopping point, and before claiming that the maintenance review method itself is complete enough for reuse or canonical-method evaluation.

## Purpose

Challenge whether the five handoff-maintenance stage models are actually complete enough to support the claim that a full modeled sweep leaves no material stone unturned.

This audit exists because the End-to-end stage initially appeared to converge, but a skeptical re-hunt exposed a hidden terminal-report contract defect. The lesson is not that End-to-end needs endless examples; it is that broad review dimensions can create false confidence when they are not decomposed into mechanically checkable obligations.

The audit therefore reviews the **review models**, not Lean itself.

## Scope

Audit these maintenance stage models:

- `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`
- `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`
- `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`
- `CODEX_HANDOFF_STRUCTURAL_OPTIMIZATION_REVIEW_MODEL.md`
- `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`

Also inspect `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md` and `CODEX_HANDOFF_MAINTENANCE_GUIDE.md` where their method affects coverage across stages.

Do not redesign production PRS as part of this audit.

## Core question

For each stage ask:

> Does the model merely name broad dimensions, or does it force the reviewer to enumerate the material subcases needed to know those dimensions were actually exhausted?

A model is not complete merely because every important word appears somewhere in it.

## Required audit dimensions

### A. Coverage decomposition

For every broad stage dimension, determine whether the model provides a finite or deriveable decomposition that prevents a reviewer from mentally checking the dimension as "covered" after inspecting only the obvious case.

Look for broad phrases such as:

- validate reporting;
- check authority;
- test dependencies;
- normalize state;
- preserve completion semantics;
- test every consumer;
- inspect failure behavior.

For each, ask what concrete subcases must be enumerated before the dimension is truthfully complete.

### B. State/path completeness

Where a stage reasons over states, paths, identities, actors, producers/consumers, or terminal classes, require explicit enumeration of the material classes rather than a single representative path.

Check especially:

- success vs blocker vs execution-boundary terminals;
- early vs late failure;
- known vs unknown vs not-applicable facts;
- current vs historical identities;
- present vs absent authorization;
- producer present vs stale vs conflicting vs missing;
- action taken vs not taken;
- artifact/result exists vs legitimately does not exist.

Do not add categories that have no material consumer.

### C. Obligation-precondition closure

For every required action, validation, output, report field, transition, or conclusion in a model, ask:

1. What facts must exist for this obligation to be satisfied?
2. Which paths guarantee those facts?
3. Which valid paths can terminate before those facts exist?
4. Does the model require a truthful representation of `not established`, `not applicable`, or equivalent absence where necessary?
5. Could the reviewer otherwise fabricate, omit, or silently assume a prerequisite?

This dimension generalizes the End-to-end terminal-report miss.

### D. Producer-consumer symmetry

Where a model checks producers, also check consumers; where it checks consumers, also check whether each consumer's prerequisites are guaranteed on every path that reaches it.

Attack one-sided checks such as:

- producer exists, but consumer can be reached before production;
- consumer exists, but producer's identity/lifecycle differs;
- output is required, but its source fact may legitimately be absent;
- deletion/compression is proposed, but a non-obvious downstream consumer exists.

### E. Negative-space coverage

Ask what the model does **not** force the reviewer to inspect.

For each stage, attempt to construct a material defect that:

- satisfies every explicit checklist bullet superficially;
- still violates the stage's governing purpose;
- could plausibly be missed by a competent reviewer following the model literally.

If such a defect exists, determine the smallest general test that would expose the class rather than adding one example-specific prohibition.

### F. Cross-stage boundary gaps

Check whether defects can hide between stages because each assumes another stage owns the issue.

Examples of boundaries to challenge:

- Adversarial vs Interdependency: authority defect or missing edge?
- Interdependency vs End-to-end: locally connected graph but invalid full journey?
- Normalization vs Adversarial: terminology drift that changes authority meaning?
- Structural Optimization vs Interdependency: deletion that breaks a non-obvious consumer?
- End-to-end vs Structural Optimization: globally valid path that requires redundant machinery?

Every material defect class should have at least one clear owning review lens, even if multiple stages can detect it.

### G. Completion-proof quality

For each stage's completion rule, ask what evidence demonstrates that the full modeled sweep occurred.

Reject completion criteria that can be satisfied by prose assertion alone when the stage's structure permits a more explicit bounded enumeration.

The goal is not to create heavy trackers. Prefer compact derived matrices, enumerated classes, or explicit closure checks that exist only for the review execution when needed.

### H. Anti-checklist theater

Challenge whether the model encourages superficial compliance:

- repeating the stage headings without constructing the target-specific model;
- declaring all dimensions tested without showing the derived classes;
- treating "considered" as equivalent to "exhausted";
- using one happy path plus one failure path as proxy for all materially distinct cases;
- assuming a broad invariant automatically proves all obligations downstream.

Strengthen only where a deterministic or bounded decomposition materially improves defect detection.

### I. False-exhaustiveness pressure

For each stage, explicitly ask:

> What would make us believe we left no stone unturned while still leaving one unturned?

Record the mechanism of false confidence, not merely the hypothetical missed defect.

Examples include:

- category too broad;
- hidden Cartesian product between states and obligations;
- terminal classes collapsed together;
- absence/null/not-applicable states ignored;
- downstream consumer checked only on success;
- examples mistaken for exhaustive families;
- stage ownership assumed rather than tested.

### J. Minimal strengthening

If a coverage gap is found, strengthen the smallest appropriate maintenance model.

Prefer, in order:

1. a general invariant;
2. a finite derived enumeration requirement;
3. a compact matrix/check closure;
4. one additional failure family only when the class cannot be expressed more generally.

Do not respond to a missed defect by endlessly accumulating examples.

## Stage-specific questions

### Adversarial

- Are authority, identity, trust, authorization, chronology, preservation, and scope attacks decomposed enough to expose combinations rather than isolated dimensions?
- Does the model test both the presence of invalid authority and the absence/ambiguity of required authority?
- Can a locally defensible instruction create an unsafe composition that Adversarial incorrectly delegates to End-to-end?

### Interdependency

- Are producer, consumer, binding, propagation, fallback, and owner checked as a complete tuple for every material node?
- Does every consumer's reachability get tested under producer absence/staleness/change?
- Are terminal/output consumers included rather than only operational dependencies?

### Normalization

- Does the model enumerate representation families from the target sufficiently to catch same-word/different-concept and different-word/same-concept cases?
- Does it test terms across terminal states and chronology, not only within adjacent prose?
- Can a "harmless synonym" become materially different only on one failure path?

### Structural Optimization

- Is every retained element checked against all material consumers, including rare blocker/re-entry/report consumers?
- Is removal safety tested across success, blocker, interruption, and future-session re-entry rather than the happy path only?
- Can apparently redundant wording be the only protection at a distinct decision point?

### End-to-end

- Are journey families crossed with materially distinct terminal classes?
- Are terminal obligations checked against the facts guaranteed to exist on each terminal path?
- Are early blockers, partial progress, interruption after each material phase, and `not established`/`not applicable` outputs explicitly covered?
- Does a valid local path remain valid when composed with reporting and re-entry obligations?

## Audit output

For each stage report:

- coverage mechanism that is already sufficient;
- concrete completeness gap, if any;
- mechanism of false confidence that allowed the gap;
- smallest general strengthening candidate;
- ownership classification;
- whether the strengthening survives Structural Optimization / survive-or-die.

Then report any cross-stage gaps separately.

Do not edit stage models during the same semantic audit pass. Apply surviving method corrections only after the complete five-stage audit has been collected and culled.

## Convergence

This audit converges when a complete review of all five stage models and their boundaries yields no blocker/high maintenance-method correction that survives Ownership Testing and Structural Optimization.

A stronger model should make omissions mechanically harder, not merely make the scroll longer.
