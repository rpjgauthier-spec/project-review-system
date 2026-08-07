# Adaptive Review Execution

## Purpose

Control context load without changing the five semantic review stages, their order, required evaluations, evidence obligations, or independent-review requirements.

Adaptive Execution is a control layer, not a sixth stage.

## Default policy

**SEPARATED is the default execution mode.** Each semantic stage receives its own bounded working pass and produces a bounded handoff before the next stage.

Do not dynamically fuse stages merely because the current reviewer believes it can handle them. FUSED execution is an optimization that requires explicit pre-existing externally validated permission for the same reviewer/runtime, exact activity group, and declared workload class.

## Stage-size assessment

Before each semantic stage, perform a bounded assessment of whether that stage is suitable for one working pass. This assessment may use semantic judgment and deterministic evidence together.

Record:

- `single_pass_suitable`: `true` or `false`;
- concise evidence-backed reasons;
- when false, at least two bounded subpasses;
- for each subpass, its stable `pass_id`, scope, whether a fresh context is required, and the reason.

Do not invent numeric precision for semantic complexity merely to feed a selector. Artifact counts, content sizes, remaining work, or other deterministic facts may inform the judgment when useful, but they are evidence rather than mandatory workload-score dimensions.

## Deterministic execution policy

Given the recorded assessment, the execution plan is mechanical:

1. If no valid FUSED authorization exists and `single_pass_suitable` is true, run one `SEPARATED` pass.
2. If `single_pass_suitable` is false, the stage must be `SUBDIVIDED` into the declared bounded subpasses.
3. Each subpass with `isolation_required: false` runs `SEPARATED`.
4. Each subpass with `isolation_required: true` runs `ISOLATED` in a fresh context or equivalent isolated execution.
5. FUSED is permitted only when an externally `VALIDATED` capability profile contains an exact permission matching reviewer subject, activity group, and workload class. FUSED cannot override an assessment that says the stage requires subdivision.

The selector therefore does not decide whether semantic complexity is high. It enforces the consequences of the recorded semantic assessment.

## Execution gate and completion

Before a governed semantic stage begins, create an execution gate. The gate binds:

- reviewer/runtime subject;
- exact activity;
- `review_revision`;
- current `target_state_id`;
- workload class;
- stage-size assessment;
- capability profile;
- resulting deterministic execution plan; and
- hashes over the declared inputs and decision.

A passing stage result also requires an execution completion record. Completion must reference the current gate hash and target state and list every planned pass in order with the exact required context mode and `status: complete`.

For repository revalidation, `update_revalidation_queue.py` rejects a passing stage result when:

- the gate is absent, stale, tampered, or for another stage;
- the gate does not match the current `review_revision` or governed artifact state;
- execution completion is absent;
- a required subpass is missing or extra;
- a pass used a different context mode than the plan required;
- any required pass is incomplete; or
- materialized scratch work has not been recorded as cleaned up.

This makes the **consequence** of the semantic stage-size judgment deterministically enforceable. It does not prove that the judgment itself was correct.

## Ephemeral subpass workspace

Subpass scratch material is **ephemeral by default**. Do not create durable subpass files merely because a stage was subdivided.

When working material must be materialized, prefer an environment-provided temporary workspace outside the tracked project or repository. The normal lifecycle is:

1. create or use the temporary workspace;
2. perform the bounded pass or passes;
3. write only the durable gate, completion record, bounded handoff, findings, or evidence that has an identified consumer;
4. verify that required durable evidence exists; and
5. delete the temporary workspace and its remaining contents before accepting the stage as complete.

An execution completion record must declare:

- `scratch_materialized`: whether a temporary workspace or scratch files were materialized;
- `scratch_cleanup_status`: `complete` when materialized scratch has been deleted, otherwise `not_applicable`; and
- `retained_subpass_artifacts`: any intentionally durable subpass artifacts, each with an identified artifact, downstream consumer, and retention reason.

A durable subpass artifact is permitted only when it has an identified downstream consumer or is required as evidence. Convenience, debugging history, or the mere existence of a subpass is not sufficient reason for permanent retention.

The execution host or orchestrator performs actual deletion. Deterministic validation can reject completion unless cleanup is recorded appropriately and retained artifacts have consumers, but a repository validator cannot prove deletion of an external temporary directory it cannot inspect. Environments that can inspect their own temporary workspace should verify its removal directly before recording cleanup as complete.

## Artifact-state binding

Environment-specific enforcement verifies `target_state_id` against the actual governed artifacts. In this repository, the state is derived from path-bound Git blob identities for the changed governed files, excluding the active change-impact record and generated queue so recording review evidence does not invalidate itself.

A governed artifact change after gate creation makes the old gate stale even if `review_revision` was not manually incremented.

`review_revision` remains a separate lifecycle/reopening marker and should still increment when a correction invalidates prior review conclusions.

## FUSED permission

The built-in capability profile grants no FUSED permissions.

A custom capability profile may grant FUSED only when it is `VALIDATED` and identifies:

- the reviewer/runtime `subject_id`;
- benchmark suite and evidence;
- a stable permission ID;
- the exact activity group;
- a stable workload class; and
- evidence specifically supporting that fused activity group and workload class.

The permission must pre-exist the review it governs. The current review may not create stronger capability evidence and immediately consume it to reduce its own separation.

## Bounded handoffs

A SEPARATED or ISOLATED pass externalizes only what later work needs:

- material findings and dispositions;
- affected authorities and consumers;
- unresolved conditions;
- evidence locations;
- corrections applied or proposed; and
- conclusions later passes must preserve or challenge.

Do not require later passes to inherit the full reasoning transcript.

## Assurance boundary

Adaptive Execution controls context separation. It does not prove:

- that the semantic stage-size assessment was correct;
- semantic correctness of stage findings;
- truthful reviewer identity;
- benchmark validity;
- reviewer independence;
- actual deletion of an external scratch workspace the validator cannot inspect; or
- domain correctness.

It does provide deterministic enforcement that a recorded plan was bound to the current artifact state and that a passing result cannot be accepted unless all required passes were completed in the required context modes and required cleanup evidence is present.
