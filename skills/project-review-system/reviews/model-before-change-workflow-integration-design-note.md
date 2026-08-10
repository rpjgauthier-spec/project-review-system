# Model-Before-Change Workflow Integration — Living Design Note

## Status and authority

This is a living, non-authoritative design note for the Project Review System local-first refactor.

It records how the adaptive model-before-change concept may be integrated into review/correction workflows without turning supporting analysis into a second authority system or mandatory paperwork. It does not change current validated Project Review System behavior by itself.

Related design notes:

- `adaptive-model-before-change-design-note.md`
- `review-method-evolution-design-note.md`

## Problem

A useful model-before-change discipline can fail in practice if it remains merely optional advice that the reviewer must remember.

The correction loop can otherwise revert to:

```text
semantic finding -> direct local patch -> new secondary defect -> another local patch
```

The workflow should make the model-before-change consultation discoverable and difficult to omit while still scaling its burden to the change.

## Candidate integration rule

For any nontrivial correction produced by a semantic review finding, the correction workflow should require a **pre-correction reasoning checkpoint** before edits are applied.

The checkpoint should:

1. identify the target and governing intent;
2. identify protected constraints/invariants affected by the finding;
3. choose the minimum useful representation/model for the change;
4. stress the proposed correction against relevant normal, edge, failure, interruption, authority, and downstream-dependency cases;
5. determine the smallest coherent change surface;
6. record whether supporting analysis must be persisted because a durable semantic result materially relies on it;
7. only then allow the correction to be applied;
8. require later delta review to consider the behavioral/model delta, not only the text/file diff.

## Adaptive burden

This must not become a fixed document-generation gate.

### Local/low-complexity correction

Examples: typo, wrong path, mechanically local wording correction.

A minimal checkpoint may simply record:

- change is local;
- no meaningful dependency/authority/state effect was identified;
- no additional model artifact is required.

### Moderate/high-complexity correction

Use the minimum useful explicit representation, such as:

- dependency/authority map;
- state/transition model;
- invariant/constraint list;
- scenario matrix;
- change-impact map.

The workflow should require more structure only when the risk surface warrants it.

## Where the requirement should live

The long-term Project Review System should make the checkpoint part of the governed correction lifecycle at the point between **semantic finding** and **authorized corrective edit**.

The exact implementation remains open. Possible mechanisms include:

- a controller state/transition requiring a pre-correction analysis receipt;
- a change-impact schema field identifying the model/checkpoint used;
- a correction-plan object generated from review findings;
- an adaptive controller decision that records `model_required: false` for genuinely local fixes;
- a stage-specific correction handoff that cannot advance until the checkpoint is satisfied.

The mechanism should be deterministic about whether required fields/evidence exist, while semantic judgment may still be needed to decide what model is sufficient.

## Anti-bureaucracy requirement

The checkpoint exists to improve reasoning quality, not to maximize artifacts.

A useful implementation must preserve this invariant:

> The cost and complexity of the reasoning scaffold should remain proportionate to the change risk and should be smaller than the ambiguity/risk it removes.

If the workflow starts producing elaborate model artifacts for trivial changes, Structural Optimization should treat that as unnecessary review machinery.

## Authority boundary

Supporting models/checkpoints do not become authority merely because the workflow requires consulting them.

Current governing requirements, review state, protected controls, and validated workflow definitions remain authoritative.

A model can explain or expose a conflict; it cannot silently redefine the target, requirements, stage semantics, or completion state.

## Purpose-preservation check

The checkpoint should explicitly ask whether the correction:

- preserves the original governing intent;
- changes protected scope/non-goals;
- expands authority;
- solves a different problem than the finding identified;
- converts a correction into a redesign.

A material intent/scope change should be surfaced and separately authorized rather than hidden inside a correction.

## Initial dogfood application

The Codex recovery handoff is a suitable first dogfood target.

Before applying nontrivial semantic-review corrections to that handoff, the editing workflow should explicitly consult `adaptive-model-before-change-design-note.md`, construct only the minimum supporting analysis needed, and apply the correction from that analysis.

This dogfood requirement belongs to the handoff-editing process and is not evidence that current production Project Review System already implements the future capability.

## Open design questions

- Which current PRS lifecycle object should eventually own the checkpoint?
- Should the checkpoint occur once per correction revision or once per material finding cluster?
- How should deterministic tooling detect a falsely trivialized `model_required: false` decision without pretending to make semantic judgments?
- Which supporting-analysis provenance should be retained for auditability?
- How should the checkpoint interact with revalidation mapping and revision increments?
- Should Intent Preservation become a core stage, an adaptive dimension, or a mandatory invariant checked at this checkpoint?
- When should Structural Optimization challenge the checkpoint machinery itself as disproportionate complexity?
