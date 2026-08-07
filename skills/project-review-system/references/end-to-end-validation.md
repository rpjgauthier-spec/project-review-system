# End-to-End Validation

## Mission

Verify that the reviewed system can move from intake to a bounded conclusion through representative normal and failure paths without bypassing authority, losing restrictions, stalling indefinitely, or requiring unnecessary permanent work.

This stage validates the combined behavior of prior reviews. It does not replace domain testing, formal verification, independent review, or external evidence. It verifies integrated paths and recorded revalidation outcomes; it does not redesign prior stage modules or own the canonical revalidation mapping.

## Required traces

Select the traces material to the reviewed system:

1. **Normal path** — valid inputs move through the correct authorities, gates, consumers, and closure state.
2. **Missing-input path** — unknown or inaccessible information remains explicit and does not silently authorize action.
3. **Contradictory-input path** — conflicts route to the controlling authority or escalation rule.
4. **Unauthorized-action path** — review, readiness, or tool capability cannot bypass the required authorization gate.
5. **Withdrawal or cancellation path** — permissions, restrictions, and downstream consumers update without reopening unrelated work.
6. **Failure path** — an impossible, prohibited, unacceptable, or expired condition terminates rather than remaining in indefinite planning.
7. **Closure and recurrence path** — evidence and restrictions remain available, while a new cycle reassesses current facts instead of inheriting stale approval.
8. **Focused-review path** — a narrow request terminates without creating a full review program or unused permanent artifacts.
9. **Behavioral-change path** — every behavioral correction has a change-impact record and bounded revalidation.
10. **Earlier-stage reopening path** — a later-stage correction invalidates an earlier conclusion, reopens the earliest affected stage, suspends later stages, and prevents completion until ordered revalidation finishes.
11. **Incomplete-access path** — the final claim remains bounded to accessible scope and names unreviewed surfaces.

## Structural validation

When a deterministic validator exists:

- run it against the current state authority
- run positive fixtures representing valid `Draft`, `Active`, `Complete`, `Failed`, and `Reopened` states when supported
- run negative fixtures for mismatched status, unresolved placeholders, invalid permissions, nonterminal completion, missing suspension markers, multiple open stages, and other protected invariants
- record expected and actual results

A passing structural validator is supporting evidence only. It does not prove report accuracy, semantic dependency completeness, safe host behavior, or domain correctness.

## Completion tests

Before a full-program `Complete` verdict, verify:

- every required stage has a permitted terminal verdict and dated report
- the current review-state authority agrees with report verdicts and paths
- no open, failed, pending, suspended, invalidated, or unresolved stage conclusion remains
- every behavioral correction has a completed change-impact record
- every required bounded revalidation is recorded as `supported`
- residual conditions are external limitations rather than unresolved in-scope defects
- earlier corrections remain mutually compatible
- no correction introduced a new silent authorization, broken dependency, semantic inconsistency, or unnecessary recurring obligation
- the final claim states scope, exclusions, evidence limits, and reviewer independence

## Reopening validation

Test the exact transition:

```text
later-stage behavioral correction
→ identify affected prior conclusions
→ reopen earliest invalidated or unresolved stage
→ set it as the sole open stage
→ mark later terminal stages Awaiting revalidation
→ correct or escalate
→ revalidate affected later stages in order
→ remove suspension markers
→ permit completion
```

Reject completion if any transition, impact record, suspension marker, or revalidation result is missing.

## Verdicts

- `Complete` — selected traces pass, structural checks behave as expected, all impact records and revalidations are complete, and no material in-scope defect or blocking escalation remains.
- `Conditional` — the internal path is coherent, but named external or inaccessible conditions limit the conclusion.
- `Failed` — a material path bypasses controls, cannot terminate safely, contradicts the state authority, or leaves a blocking defect unresolved.
