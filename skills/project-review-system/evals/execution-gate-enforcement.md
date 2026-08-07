# Evaluation: Execution Gate Enforcement

## Purpose

Verify that Adaptive Execution is an enforced stage-result/advancement gate rather than a reminder the reviewer may skip, and that stale semantic review evidence is invalidated automatically when the governed artifact state changes.

## Required behavior

A supported result requires all of the following:

1. A governed semantic stage cannot have a passing result accepted without an execution gate for that exact stage.
2. The gate embeds the workload and capability inputs used by the selector and the selector decision can be deterministically recomputed.
3. Tampered or stale gate hashes fail.
4. A validated capability profile remains subject-bound to the reviewer/runtime identified by the workload.
5. The workload carries a medium-independent `target_state_id` that identifies the exact governed artifact state.
6. Environment-specific enforcement verifies `target_state_id` against the actual current artifact state rather than trusting the reviewer to supply it correctly.
7. In repository revalidation, the current target-state identity is derived deterministically from governed changed-file contents; the active change record and generated queue are excluded so recording gate/results does not self-invalidate.
8. A change to any governed implementation, documentation, test, or evaluation file after gate creation makes the old gate invalid automatically even if `review_revision` is not manually incremented.
9. `review_revision` remains an independent lifecycle/reopening marker and still invalidates gates created before an explicitly reopened review generation.
10. A stage gate records at least one remaining stage so already-complete work cannot be relabeled as a fresh gated pass.
11. Historical records that predate gate enforcement may be explicitly grandfathered by the canonical mapping; the exemption list is closed and deterministic rather than reviewer-selected per change.
12. Identity Pass may use the same gate format even though it is not one of the five semantic stages.
13. Execution-gate validation does not claim the workload facts or semantic review result are truthful; it proves only that the recorded execution decision matches its declared inputs and the environment-verified target state.

## Artifact-state invalidation test

Create a valid gate for a governed artifact set. Then change one governed artifact without changing `review_revision`.

Expected result:

```text
recorded target_state_id != current environment-derived target_state_id
→ gate rejected
→ passing stage result rejected
→ fresh preflight/gate required
```

Also verify that editing only the active change-impact record or regenerated queue does not change the governed target-state identity.

## Failure conditions

Fail if:

- a passing stage result is accepted with no gate;
- a gate for another stage is reused;
- a pre-reopening gate remains valid after `review_revision` changes;
- a gate remains valid after a governed artifact changes;
- the system trusts a reviewer-written target-state identifier without environment verification where such verification is available;
- recording the gate/result itself causes unavoidable self-invalidation;
- a reviewer can self-select a legacy exemption;
- a modified decision still passes without recomputation;
- gate enforcement changes which semantic stages or evaluations are required; or
- the system claims the gate proves semantic correctness or reviewer independence.
