# Adaptive Review Execution

## Purpose

Choose how much semantic review work may safely share one working context without changing which review stages, evaluations, evidence obligations, or independent-review requirements apply.

Run the initial execution preflight **before the Identity Pass**. Re-evaluate the decision after the Identity Pass and after each completed review stage because newly discovered complexity can change the safe execution mode.

This control addresses context load and cross-stage interference. It does not create a sixth review stage, replace the Identity Pass, alter stage order, waive required evaluations, or substitute for independent review.

## Execution modes

- **`FUSED`** — two or more required semantic activities may share one bounded working context when the workload is inside a validated fused-capability envelope.
- **`SEPARATED`** — each review stage receives its own explicit semantic pass and writes a bounded handoff before the next stage. The same overall session may continue if context remains reliable.
- **`ISOLATED`** — each review stage runs in a fresh context or equivalent isolated execution, using repository/workspace evidence and bounded prior-stage handoffs rather than the prior stage's full conversational reasoning.

Execution mode changes only context separation. All required stages and evaluations still run.

## Initial preflight

Before the Identity Pass or first semantic stage:

1. Build a workload record using `templates/review-workload.json`.
2. Use deterministic or directly observable values where available: artifact count, semantic units, required stages, required evaluations, known dependencies, protected controls, known unknowns, self-referential scope, and exhaustive-claim status.
3. Select a reviewer capability profile. If no externally validated profile is available, use `config/default-execution-capability.json`.
4. Run `scripts/select_execution_policy.py`.
5. Record the selected mode and decision evidence in the active review record or bounded working notes.
6. Execute the Identity Pass, when applicable, under that mode.

Do not infer capability from model name, context-window size, provider marketing, subjective confidence, or a reviewer saying it can handle the work.

## Capability profiles

A capability profile defines the largest workload envelope demonstrated for `FUSED` and `SEPARATED` execution. Anything outside the separated envelope selects `ISOLATED`.

A non-default profile must be marked `VALIDATED` and identify benchmark evidence. The deterministic selector validates the profile schema and uses its declared envelopes; it does not prove that the benchmark itself was honest or sufficient.

As reviewer capability improves, a newly validated profile may raise the fused or separated envelope. The same workload can then automatically select a lighter execution mode without changing review governance.

Capability improvement may relax context separation, but it cannot waive an independent-review requirement whose purpose is conflict-of-interest or assurance independence rather than context capacity.

## Workload dimensions

The selector compares the workload independently against every envelope dimension rather than collapsing everything into a single opaque score.

Current dimensions are:

- `artifact_count`
- `semantic_units`
- `required_stage_count`
- `required_evaluation_count`
- `dependency_count`
- `protected_control_count`
- `unresolved_uncertainty_count`
- `material_findings_count`
- `unexpected_dependency_count`
- `self_referential`
- `exhaustive_claim`

These dimensions are policy inputs, not scientific measures of reasoning difficulty. Capability envelopes should be revised only from evaluation evidence, not tuned merely to obtain a preferred execution mode.

## Dynamic re-evaluation

Re-run the selector after:

- the Identity Pass;
- Adversarial review;
- Interdependency review;
- Normalization review;
- Structural Optimization review;
- any material scope expansion, unexpected dependency discovery, protected-control discovery, or new unresolved uncertainty.

Update the workload record with facts discovered so far before each rerun.

### Tightening

If the new workload exceeds the current mode's validated envelope, increase separation immediately. A decision may jump directly from `FUSED` to `ISOLATED`.

### Relaxation

If the workload falls inside a lighter validated envelope, relaxation applies only to remaining work. Never retroactively treat already-completed combined work as separately reviewed.

To reduce mode oscillation, a single checkpoint may relax by at most one level:

```text
ISOLATED -> SEPARATED -> FUSED
```

A later checkpoint may relax again if the workload still qualifies.

## Bounded stage handoff

When using `SEPARATED` or `ISOLATED`, each completed stage should externalize only the material information the next stage needs:

- findings and dispositions;
- affected authorities and consumers;
- unresolved conditions;
- evidence locations;
- corrections applied or proposed;
- changes to workload dimensions;
- conclusions that later stages must preserve or challenge.

Do not require later stages to inherit the previous stage's full reasoning transcript. Repository/workspace artifacts and bounded stage handoffs are the durable memory surface.

## Fallback behavior

Use the conservative default capability profile when:

- no validated capability profile exists;
- benchmark provenance is unavailable;
- the supplied profile is malformed or expired under local policy;
- the reviewer/runtime changed and prior capability evidence is not transferable.

If workload data required for a reliable decision is unavailable, do not estimate it optimistically. Record the unknown and choose the more separated applicable mode.

## Completion boundary

Adaptive execution is correctly applied when:

- the initial policy decision occurred before the Identity Pass or first semantic stage;
- the decision used a declared workload and capability profile;
- mode changes did not remove required stages or evaluations;
- material discoveries triggered workload updates and re-evaluation;
- relaxation never retroactively upgraded prior assurance;
- independent-review requirements remained separate from context-capacity decisions; and
- the final review record identifies which execution mode was used for each semantic stage or fused group.
