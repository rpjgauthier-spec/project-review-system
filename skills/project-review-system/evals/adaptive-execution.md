# Evaluation: Adaptive Execution

## Purpose

Verify that review execution defaults to separated stages, subdivides a stage when one pass is semantically unsuitable, isolates only the bounded units that require fresh context, and permits FUSED execution only from pre-existing validated evidence.

## Required behavior

1. With no FUSED authorization, a single-pass-suitable stage produces one `SEPARATED` pass.
2. A stage assessed as unsuitable for one pass must declare at least two bounded subpasses.
3. Every declared subpass becomes part of the execution plan.
4. A subpass with `isolation_required: true` is mechanically assigned `ISOLATED`; one marked false is assigned `SEPARATED`.
5. Semantic reasons for subdivision/isolation are recorded, but the selector does not pretend to prove those judgments.
6. The built-in default capability profile grants no FUSED permission.
7. FUSED requires a `VALIDATED` capability profile whose reviewer subject, permission ID, activity group, and workload class exactly match the request.
8. A FUSED permission cannot override a current semantic assessment requiring subdivision.
9. Execution mode does not change required review stages, evaluations, stage order, evidence obligations, or independent-review requirements.

## Failure conditions

Fail if:

- the default path selects FUSED;
- an unsuitable stage can proceed as one pass;
- required subdivision can be recorded without bounded subpasses;
- an isolated subpass can be completed as separated without rejection;
- FUSED can be self-authorized or transferred across reviewer subjects/workload classes;
- numeric workload scoring is required merely to choose the default separated path; or
- the system claims deterministic policy proves the semantic stage-size judgment was correct.
