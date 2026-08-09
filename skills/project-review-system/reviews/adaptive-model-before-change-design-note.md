# Adaptive Model-Before-Change Reasoning — Living Design Note

## Status and authority

This is a living, non-authoritative design note for the Project Review System local-first refactor.

It records a review-method improvement discovered during controller-core recovery work. It does **not** change the authority, lifecycle, protected controls, or current validated behavior of the Project Review System by itself. Any implementation that materially changes reviewed behavior must go through the normal governed change/reopening/cutover path.

This note is intentionally adjacent to `local-first-refactor-living-design-notes.md`: the existing living notes remain the broader design notebook, while this file keeps the model-before-change concept bounded and independently reviewable.

## Problem observed

Repeated review/correction cycles exposed a general failure pattern:

1. a semantic review finds a local defect;
2. the correction is made directly in prose/code;
3. another review discovers a secondary dependency or authority problem introduced by the correction;
4. the new problem is patched locally;
5. the cycle repeats.

The reviews were useful, but the correction process was too locally reactive. The reviewer was often changing the representation before explicitly modeling the system relationships that the change could affect.

The improvement should not be limited to reviewing the Project Review System itself. The underlying problem occurs whenever a change affects a system with meaningful dependencies, constraints, state, authority, interfaces, or failure modes.

## General principle

Before making a meaningful change, construct the **minimum useful model of the thing being changed**, identify the relevant constraints and dependencies, evaluate the proposed change against that model, then apply the coordinated change and delta-review the result.

Conceptually:

```text
understand target
    -> choose minimum useful representation
    -> extract constraints/invariants/dependencies
    -> stress proposed change
    -> compute change surface
    -> apply coordinated change
    -> verify
    -> delta review
```

This is a reasoning scaffold, not a requirement to create a fixed set of documents for every task.

## Adaptive depth

The system should scale the amount of modeling to the task rather than impose bureaucracy.

### Low complexity

Examples: typo, isolated wording correction, mechanically local refactor with no meaningful dependency change.

Preferred path:

```text
direct change -> simple verification
```

Do not generate elaborate models merely because the capability exists.

### Moderate complexity

Examples: interface adjustment, workflow change, bounded configuration change, document rule that affects several dependent sections.

Preferred path:

```text
lightweight dependency/constraint representation
    -> representative scenario checks
    -> coordinated change
    -> delta verification
```

### High complexity / stateful / governance-sensitive / safety-sensitive

Examples: authority changes, lifecycle changes, state-machine changes, persistence/recovery behavior, safety-critical engineering behavior, broad architectural refactors.

Preferred path may include explicit artifacts such as:

- authority/dependency map;
- state/transition or flow model;
- invariant/constraint set;
- scenario/failure matrix;
- change-impact map;
- staged semantic review and delta review.

Use only the artifacts that materially reduce uncertainty for the target.

## Domain-adaptive representations

The representation should fit the object under review.

### Code / software / system design

Potential models:

- architecture/component map;
- interfaces and ownership;
- dependency graph;
- state transitions;
- invariants;
- concurrency/retry behavior;
- failure/recovery scenarios.

### Documents / governance / policy

Potential models:

- authority and precedence map;
- term/definition dependencies;
- obligations and permissions;
- contradiction/dependency graph;
- lifecycle/state model;
- exception/failure cases.

### Mechanical design

Potential models:

- components and interfaces;
- loads/constraints;
- operating states;
- material/environment assumptions;
- failure modes;
- maintenance/recovery conditions.

### Workflows / operations

Potential models:

- actors;
- inputs/outputs;
- transitions;
- queues/bottlenecks;
- ownership;
- exception/retry paths.

### Data pipelines

Potential models:

- sources;
- transformations;
- schemas/contracts;
- ownership;
- dependency lineage;
- failure/retry behavior;
- freshness/consistency invariants.

### Plans / projects

Potential models:

- assumptions;
- dependencies;
- resources;
- milestones;
- gating decisions;
- contingencies;
- failure/rollback paths.

The Project Review System should not assume that a state machine is always the best representation. The representation is selected because it helps expose the target's real risk surface.

## Generic reasoning pattern

For a nontrivial change, the reviewer should conceptually answer:

1. **Understand the object**
   - What is being changed?
   - What are its important parts?
   - What depends on it?

2. **Extract constraints**
   - What must remain true?
   - What must not change?
   - What defines success or failure?

3. **Choose the minimum useful model**
   - State machine, dependency graph, authority map, flow, interface model, causal model, scenario matrix, or another representation appropriate to the domain.

4. **Stress the proposed change**
   - normal path;
   - edge cases;
   - failure paths;
   - interrupted/retry paths where applicable;
   - downstream effects;
   - authority/self-certification effects where applicable.

5. **Compute the change surface**
   - Which other components, documents, tests, invariants, workflows, or review credits are affected?
   - Which changes should be coordinated rather than applied one sentence/file at a time?

6. **Apply the coordinated change**
   - Change the smallest coherent set, not merely the first obvious local symptom.

7. **Verify and delta-review**
   - Verify the changed system against the relevant model/scenarios.
   - Review the behavioral/model delta for newly introduced problems, not just the textual diff.

## Correction discipline

For sufficiently complex changes, prefer:

```text
finding
  -> identify violated relationship/constraint
  -> update or construct minimum useful model
  -> determine affected surfaces
  -> make coordinated correction
  -> scenario/validator verification
  -> delta review
```

Avoid defaulting to:

```text
finding -> patch one sentence -> continue
```

The latter is still appropriate for genuinely local low-complexity changes.

## Supporting artifacts versus authority

Models produced for reasoning must not silently become a second source of truth.

Unless explicitly promoted through existing governance, a generated authority map, dependency graph, state diagram, invariant list, scenario matrix, or impact plan is **supporting analysis**, not authority.

The authoritative review/change state remains wherever the current Project Review System defines it.

If supporting analysis materially contributed to a durable semantic result, preserve enough provenance to reconstruct what was relied upon. Do not require permanent storage of every scratch representation.

## Relationship to deterministic and semantic work

The Project Review System should generate and verify these representations deterministically where the source material makes that possible.

Examples:

- dependency/import graph from code;
- schema relationships;
- explicit workflow transitions;
- Git/file change surface;
- known configuration dependencies;
- test ownership mappings.

Semantic review remains responsible for judgments that cannot be mechanically derived, such as:

- whether an architectural boundary is justified;
- whether a dependency is materially behavior-changing;
- whether a failure scenario exposes an unacceptable design;
- whether two domain concepts are meaningfully equivalent.

Deterministic derivation should reduce what the semantic reviewer must remember or reconstruct, not pretend to replace semantic judgment.

## Relationship to existing review stages

This capability should support the existing semantic stages rather than become a parallel review framework.

Possible uses:

- **Adversarial:** use constraints/scenarios to attack proposed changes systematically.
- **Interdependency:** use dependency/authority models to expose coupling, cycles, duplicate authorities, and propagation effects.
- **Normalization:** use concept/definition relationships to distinguish terminology differences from semantic differences.
- **Structural Optimization:** use component/dependency models to test whether boundaries/components can be removed or merged.
- **End-to-end validation:** use states/flows/scenarios to trace complete normal, failure, interruption, and recovery paths.

The exact model artifacts and depth should be selected per target and stage rather than hard-coded globally.

## Model-aware delta review

A delta review should consider more than changed text/files when a meaningful model exists.

The review should ask:

- Which modeled relationships changed?
- Which states/transitions became reachable or unreachable?
- Which invariants gained or lost enforcement?
- Which dependencies or authority edges changed?
- Which failure scenarios changed outcome?
- Did the correction create a new dead end, authority cycle, hidden dependency, or self-certification path?

This helps detect problems introduced by a correction even when the new prose/code appears locally coherent.

## Candidate deterministic controller responsibilities

A future controller may be able to:

- classify task complexity using deterministic evidence plus bounded semantic judgment;
- select from available representation types;
- generate mechanically derivable model fragments;
- bind model artifacts to exact target snapshots;
- record which model revision a semantic pass consumed;
- compute change surfaces from explicit dependencies;
- require scenario coverage for affected transitions/invariants;
- reject stale model artifacts when target state changes;
- preserve material model provenance without treating the model as authority;
- expose the minimum model/context needed to the reviewer.

The controller must not claim semantic completeness merely because a generated graph or state model exists.

## Context and cognitive-load objective

A major purpose is to make reviewer behavior more intelligent **without requiring the reviewer to keep the entire system implicitly in context**.

A good representation externalizes relevant structure so the reviewer can reason over a bounded explicit model rather than repeatedly reconstructing dependencies from prose/code.

This should complement the existing bounded-subpass/context-isolation direction:

- use models to reduce hidden dependency load;
- use subdivision when the useful model is still too large for one semantic pass;
- preserve handoffs between passes;
- do not use model generation as an excuse to fuse semantic stages or bypass execution-boundary rules.

## Implementation caution

Do not implement this capability merely by adding mandatory documents to every review.

That would turn a reasoning improvement into paperwork.

A useful implementation should answer:

> What is the smallest explicit representation that materially lowers the chance of an incoherent or locally reactive change for this particular task?

If the answer is “none beyond the existing target and tests,” perform the simple review path.

## Open design questions

- How should review complexity be classified without letting the classifier become semantic authority?
- Which model types should be first-class concepts versus ordinary supporting files/data?
- When can models be generated deterministically from code/configuration?
- When is semantic model construction required?
- How should model completeness or coverage be assessed without overclaiming?
- What changes to a target invalidate a previously generated model?
- How should model deltas feed change-impact/revalidation mapping?
- Which stages should consume which model types by default?
- When should a model be persisted versus treated as ephemeral scratch?
- How should the system avoid generating redundant models that increase reviewer context instead of reducing it?
- Can the controller select a representation based on observed failure modes from previous review revisions?
- How should domain-specific model plugins/adapters be represented without making core review semantics domain-specific?

## Relationship to the controller-core recovery discovery

The immediate discovery came from repeatedly improving a complex Codex recovery handoff. Interdependency fixes produced secondary governance effects that later delta-adversarial reviews exposed. A model-first correction discipline would likely have surfaced more of those effects before prose was modified.

That incident is evidence for exploring this capability, not proof that the proposed design is correct.

The current controller-core Slice 1 must **not** expand merely to implement this idea. The capability belongs in future Project Review System design/review work and should be governed there before implementation.
