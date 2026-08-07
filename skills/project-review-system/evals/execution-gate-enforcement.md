# Evaluation: Execution Gate Enforcement

## Purpose

Verify that Adaptive Execution is enforced at the stage-result/advancement boundary rather than remaining advisory.

## Required behavior

A passing governed stage result requires all of the following:

1. A current execution gate for the exact stage.
2. A gate bound to the current `review_revision` and governed artifact `target_state_id`.
3. A deterministically recomputable decision and valid gate hash.
4. An execution completion record referencing that exact gate hash and target state.
5. Completion of every planned pass in plan order.
6. Exact agreement between each planned pass and completed `context_mode`.
7. No omitted or extra subpasses.
8. A stage assessed as unsuitable for one pass cannot bypass its declared subdivision.
9. A subpass declared `isolation_required` cannot be credited as complete when recorded as `SEPARATED`.
10. Historical records may be exempt only through the canonical closed allowlist.

## Failure conditions

Fail if:

- a passing result is accepted with no gate;
- a passing result is accepted with no execution completion;
- an old artifact-state or review-revision gate remains valid;
- a reviewer can omit a required subpass;
- a reviewer can record the wrong context mode and still pass;
- a modified gate or completion can pass without hash/plan agreement;
- a current record can self-declare a legacy exemption; or
- deterministic enforcement is described as proof that the semantic subdivision judgment or review conclusion was correct.

## Assurance boundary

The deterministic controls prove consistency between the recorded assessment, execution plan, artifact state, and completion evidence. They do not prove the semantic assessment was wise, that a fresh context was genuinely independent, or that the semantic findings were correct.
