# Review Stage — [Name]

## Date

YYYY-MM-DD

## Verdict

Complete / Conditional / Failed

## Review mode and authorization

- **Mode:** Diagnostic / Proposed corrective / Authorized corrective
- **Allowed write or external actions:**
- **Actions actually performed:**

## Scope, access, and exclusions

State the bounded scope, inventory or search method, direct dependencies inspected, accessible surfaces, inaccessible surfaces, stale or sampled content, and material exclusions.

## Reviewer independence

State whether the review was independent, same-agent self-review, or mixed. Do not claim independent validation when the reviewer created or corrected the reviewed system.

## Current outcome and active triggers

Describe the project state relevant to this stage. Distinguish active, conditional, dormant, and historical behavior.

## Files and dependencies inspected

List only material authorities, producers, consumers, fallbacks, archives, trust boundaries, host permissions, and escalation targets.

## Material findings

| Finding | Type | Disposition | Correction or justification |
|---|---|---|---|
| | | | |

Do not list every retained sentence or ordinary field.

## Protected controls

For any disputed protected control, state:

- original protection
- retained or replacement protection
- tested failure case

Do not reproduce secrets, personal data, exploit details, or restricted evidence. Use the minimum redacted reference needed for traceability.

## Change-impact references

List the path or stable ID of every change-impact record created or updated by this stage. The structured record owns changed files, classifications, derived requirements, results, escalation data, and workflow status.

Do not copy the record's field values or evaluation results into this report. State explicitly when the stage made no change requiring a record.

## Backward-impact outcome

Record only:

- whether the generated queue was regenerated after this stage's changes;
- whether an earlier stage was reopened;
- the next permitted stage or blocking condition.

The change-impact records and generated queue own the detailed revalidation requirements and completion state. The tracker owns the current stage transition.

## Validation

Record relevant normal, missing-input, contradictory-input, malicious-instruction, unauthorized-action, incomplete-access, partial-write, closure, withdrawal, recurrence, reopening, suspension, and navigation traces.

Separate deterministic structural checks from semantic conclusions and domain-expert validation.

## Escalations

Reference the controlling change-impact record containing the blocked scope, controlling review, and resumption condition. Omit this section when none exist.

## Residual conditions

List external, inaccessible, domain-expert, or user-controlled facts that remain unresolved without treating them as review defects.

## Verdict and next action

State the bounded conclusion, coverage limit, independence limit, whether corrections were proposed or applied, completed revalidation, any reopened stage, and the next permitted action.