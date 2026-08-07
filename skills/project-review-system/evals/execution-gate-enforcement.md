# Evaluation: Execution Gate Enforcement

## Purpose

Verify that Adaptive Execution is an enforced stage-result/advancement gate rather than a reminder the reviewer may skip.

## Required behavior

A supported result requires all of the following:

1. A governed semantic stage cannot have a passing result accepted without an execution gate for that exact stage.
2. The gate embeds the workload and capability inputs used by the selector and the selector decision can be deterministically recomputed.
3. Tampered or stale gate hashes fail.
4. A validated capability profile remains subject-bound to the reviewer/runtime identified by the workload.
5. `review_revision` invalidates gates created before a correction or reopening that requires ordered revalidation.
6. A stage gate records at least one remaining stage so already-complete work cannot be relabeled as a fresh gated pass.
7. Historical records that predate gate enforcement may be explicitly grandfathered by the canonical mapping; the exemption list is closed and deterministic rather than reviewer-selected per change.
8. Identity Pass may use the same gate format even though it is not one of the five semantic stages.
9. Execution-gate validation does not claim the workload facts or semantic review result are truthful; it proves only that the recorded execution decision matches its declared inputs and current review revision.

## Failure conditions

Fail if:

- a passing stage result is accepted with no gate;
- a gate for another stage is reused;
- a pre-reopening gate remains valid after `review_revision` changes;
- a reviewer can self-select a legacy exemption;
- a modified decision still passes without recomputation;
- gate enforcement changes which semantic stages or evaluations are required; or
- the system claims the gate proves semantic correctness or reviewer independence.
