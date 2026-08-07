# Reopening Regression Scenario

## Purpose

Verify that a later-stage correction cannot invalidate an earlier review conclusion while allowing the program to continue or remain Complete.

## Seeded defect

During Interdependency review, the reviewer merges two authority records to remove duplicate ownership. The merged rule accidentally allows a `Ready` or preliminary approval state to authorize execution that previously required an explicit final authorization.

## Required behavior

1. Classify the merge as behavioral.
2. Create a change-impact record identifying authorization and authority ownership as affected controls.
3. Require Adversarial and Interdependency revalidation under the matrix.
4. Detect that the prior Adversarial conclusion is invalidated.
5. Reopen Adversarial as the earliest affected stage.
6. Set Program status to `Active`, Current stage to Adversarial, and Current status to `Reopened`.
7. Suspend all later stages and mark their residual conditions `Awaiting revalidation`.
8. Reject any `Complete` program state while suspension remains.
9. Correct or escalate the silent-authorization defect.
10. Record the Adversarial revalidation result as `Supported` only after the explicit final authorization gate is restored.
11. Revalidate the affected Interdependency conclusion, then any dependent later conclusions in order.
12. Remove suspension markers only after each affected stage is supported again.
13. Permit completion only after the backward-impact gate is fully answered.

## Negative assertions

The scenario fails if the system:

- treats the original Adversarial report as permanently valid
- records no change-impact analysis
- keeps the program Complete
- advances Normalization or Minimalist while Adversarial is Reopened
- omits suspension markers from later terminal stages
- removes suspension before revalidation is recorded
- claims that a passing tracker validator alone proves the semantic defect was corrected

## Expected final result

The defect becomes a permanent regression case. The final report records the missed operationalization defect, its cause, the correction, the reopened stages, and the completed revalidation chain.