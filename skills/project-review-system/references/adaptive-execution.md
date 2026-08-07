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
2. Record `reviewer_subject_id` for the reviewer/runtime actually being governed.
3. Record `activity` for the Identity Pass or exact semantic stage being gated.
4. Record `target_state_id` for the exact governed artifact state. The semantic controller treats this as an environment-provided opaque identifier; the environment-specific enforcement layer is responsible for verifying it.
5. Record the current `review_revision`. Increment it when a correction or reopening invalidates prior execution gates.
6. Use deterministic or directly observable values where available: artifact count, content bytes, remaining required stages, remaining required evaluations, known dependencies, protected controls, known unknowns, self-referential scope, and exhaustive-claim status.
7. Select a reviewer capability profile. If no externally validated profile is available, use `config/default-execution-capability.json`.
8. Run `scripts/select_execution_policy.py --gate` and retain the generated gate with the active review evidence.
9. Validate the gate with `scripts/check_execution_gate.py` before treating the semantic activity as validly opened.
10. Execute the Identity Pass or semantic stage under the selected mode.

Do not infer capability from model name, context-window size, provider marketing, subjective confidence, or a reviewer saying it can handle the work.

## Enforced execution gate

Adaptive execution is not satisfied by prose stating that a preflight occurred. A governed semantic-stage result is valid only when a verifiable execution gate exists for that exact stage, current review revision, and exact governed artifact state.

`select_execution_policy.py --gate` records:

- the workload snapshot;
- the opaque `target_state_id` supplied by the current environment;
- the capability profile consumed;
- the prior/current execution mode when applicable;
- the selector's decision;
- hashes binding the decision to its workload and capability inputs; and
- the semantic activity the gate authorizes.

`check_execution_gate.py` recomputes the selector decision, verifies the gate hash, verifies the exact activity, checks `review_revision`, and can compare the recorded `target_state_id` with the current environment-derived target state. A stage gate must also show that at least one semantic stage remained when it was opened.

For repository revalidation, `update_revalidation_queue.py` derives `target_state_id` as a SHA-256 identity over the current contents of every governed changed file, excluding the active change-impact record and generated queue because recording the gate/result would otherwise invalidate itself. A governed file that is intentionally deleted is represented explicitly as absent in the hash. The queue rejects a passing stage result when its gate was created against any different governed artifact state.

This means an implementation/doc/test/evaluation change after a gate is created automatically stales the gate even when `review_revision` was not incremented. `review_revision` remains a separate lifecycle marker for reopening and explicit review-generation changes; artifact-state binding is an independent automatic stale-review control.

Historical change records created before execution-gate enforcement may be explicitly grandfathered only through the closed legacy exemption list in `config/revalidation-map.json`. A current reviewer cannot self-declare an exemption in an individual change record.

The gate proves only that the recorded execution decision matches its declared workload/capability inputs and current environment-verified target state. It does not prove that workload facts, benchmark evidence, semantic findings, or reviewer independence are truthful.

## Producer-consumer contract

Keep the adaptive execution inputs and decision ownership explicit:

- **Workload producer:** the active review controller/reviewer derives the current workload from the authorized scope and evidence available at that checkpoint. It records `reviewer_subject_id`, the exact semantic `activity`, and the environment-provided `target_state_id`. In repository revalidation, remaining stage/evaluation counts come from unresolved queue work and artifact/content measures come from the current in-scope inventory, diff, manifest, or equivalent deterministic source.
- **Target-state producer:** the current environment derives a stable identity for the exact governed artifact state. The generic semantic controller does not prescribe Git, filesystem, vault, or other storage semantics.
- **Capability-profile producer:** a benchmark/evaluation process or other explicitly trusted capability authority outside the semantic review currently being governed. The current review may consume a pre-existing validated profile but may not raise its own capability limits and immediately use that increase to reduce separation.
- **Selector:** `scripts/select_execution_policy.py` deterministically consumes the workload and capability profile, verifies subject binding for validated profiles, and produces the execution decision plus envelope-failure evidence.
- **Gate validator:** `scripts/check_execution_gate.py` verifies that the stored decision still matches its declared inputs, activity, review revision, and—when supplied by the environment—the current target state.
- **Decision consumer:** the review scheduler/reviewer applies the selected mode to the Identity Pass and stage execution while preserving the original stage/evaluation obligations.
- **Handoff producer:** each completed `SEPARATED` or `ISOLATED` stage produces a bounded handoff for the next stage and updates workload facts that changed.
- **Advancement consumer:** the revalidation queue rejects a passing governed stage result that lacks a valid current execution gate.

If a stronger capability profile is created or materially changed during the same semantic review it would govern, do not use the increased limits for that review. Continue with the prior validated profile or conservative default. The new profile may govern later reviews only after its capability evidence has completed its own required validation path.

A `VALIDATED` capability profile is usable only when `capability.subject_id` exactly matches the workload `reviewer_subject_id`. Reject mismatch rather than assuming capability transfers across models, runtimes, configurations, tool environments, or materially different reviewer implementations. The built-in conservative fallback is intentionally generic and does not claim measured subject-specific capability.

Do not duplicate mutable workload facts across several authorities. Keep one current workload record or equivalent current decision input and update it at checkpoints.

## Capability profiles

A capability profile defines the largest workload envelope demonstrated for `FUSED` and `SEPARATED` execution. Anything outside the separated envelope selects `ISOLATED`.

A non-default profile must be marked `VALIDATED`, identify the reviewer/runtime `subject_id` to which the evidence applies, name the benchmark suite, identify benchmark evidence, and declare the supported envelope model. The deterministic selector validates these declared fields, exact subject binding, and the envelope schema; it does not prove that the benchmark itself was honest or sufficient.

Version 1 supports `envelope_model: rectangular-v1`. Under this model, every workload satisfying every declared limit is treated as inside the envelope. Therefore a benchmark producer that publishes a `VALIDATED` rectangular envelope is asserting support for the **combined envelope**, not merely that each dimension was tested separately in isolation. If the evidence supports only selected workload combinations rather than the full rectangle, do not encode those independent maxima as a rectangular validated profile.

The built-in `DEFAULT_CONSERVATIVE` status is reserved for `default-conservative-v1`. Its thresholds are conservative policy fallback values, not a measured reviewer-capability claim.

As reviewer capability improves, a newly validated profile may raise the fused or separated envelope. The same workload can then automatically select a lighter execution mode without changing review governance, provided the profile applies to the same reviewer/runtime subject.

Capability improvement may relax context separation, but it cannot waive an independent-review requirement whose purpose is conflict-of-interest or assurance independence rather than context capacity. A profile validated for one reviewer/runtime must not be silently transferred to another subject.

## Workload dimensions

The selector compares the workload independently against every envelope dimension rather than collapsing everything into a single opaque score.

Current dimensions are:

- `artifact_count`
- `content_bytes`
- `remaining_stage_count`
- `remaining_evaluation_count`
- `dependency_count`
- `protected_control_count`
- `unresolved_uncertainty_count`
- `material_findings_count`
- `unexpected_dependency_count`
- `self_referential`
- `exhaustive_claim`

`reviewer_subject_id`, `activity`, `target_state_id`, and `review_revision` are control-binding fields rather than workload-magnitude dimensions. They bind the decision to the reviewer/runtime, semantic activity, governed artifact state, and explicit revalidation generation.

`content_bytes` is the reproducible byte size of the in-scope content represented by the workload decision. Use the same counting boundary in the workload and the benchmark that produced a capability envelope. Do not replace it with an undefined semantic-unit estimate. When content is added to or removed from scope, update the byte count at the next checkpoint.

`remaining_stage_count` and `remaining_evaluation_count` describe work still required at the checkpoint, not the original total. They decrease only after valid completion and increase again if work is reopened or newly required. This allows the controller to relax later work automatically when the remaining workload genuinely shrinks.

These dimensions are policy inputs, not scientific measures of reasoning difficulty. Capability envelopes should be revised only from evaluation evidence, not tuned merely to obtain a preferred execution mode. The selector validates declared structure but cannot prove that workload counts or benchmark claims are truthful; that remains an evidence and authority boundary.

## Dynamic re-evaluation

Re-run the selector after:

- the Identity Pass;
- Adversarial review;
- Interdependency review;
- Normalization review;
- Structural Optimization review;
- any material scope expansion, governed-artifact change, unexpected dependency discovery, protected-control discovery, new unresolved uncertainty, reopening, or newly required evaluation.

Before a reopened semantic stage begins, create and validate a new gate at the current `review_revision` and current `target_state_id`. Never reuse a gate from an earlier artifact state.

Update the workload record with facts discovered so far before each rerun.

### Tightening

If the new workload exceeds the current mode's validated envelope, increase separation immediately. A decision may jump directly from `FUSED` to `ISOLATED`.

### Relaxation

If the remaining workload falls inside a lighter validated envelope, relaxation applies only to remaining work. Never retroactively treat already-completed combined work as separately reviewed.

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
- the reviewer/runtime changed and prior capability evidence is not transferable;
- a stronger profile was created or materially changed by the same semantic review it would govern.

Reject a validated profile whose `subject_id` does not match the workload `reviewer_subject_id`. Do not silently downgrade a mismatched validated profile into the conservative default; the caller must deliberately select the fallback so the evidence trail remains clear.

If workload data required for a reliable decision is unavailable, do not estimate it optimistically. Record the unknown and choose the more separated applicable mode.

## Completion boundary

Adaptive execution is correctly applied when:

- the initial policy decision occurred before the Identity Pass or first semantic stage;
- the decision used a declared workload and capability profile;
- every governed passing stage result has a valid execution gate for the exact activity, current artifact state, and current review revision;
- the workload identified the reviewer/runtime actually being governed;
- target-state identity was verified by the current environment rather than trusted solely because the reviewer wrote it;
- input producers and decision consumers were identifiable;
- validated capability evidence was bound to the same reviewer/runtime subject;
- the current review did not self-authorize a stronger capability envelope;
- a validated rectangular profile had evidence intended to support its combined envelope rather than only isolated dimension maxima;
- mode changes did not remove required stages or evaluations;
- material discoveries, valid completion, reopening, artifact changes, and newly required work updated the workload and triggered re-evaluation;
- stale gates are invalidated automatically by target-state mismatch even if `review_revision` was not manually changed;
- relaxation never retroactively upgraded prior assurance;
- independent-review requirements remained separate from context-capacity decisions; and
- the final review record identifies which execution mode was used for each semantic stage or fused group.
