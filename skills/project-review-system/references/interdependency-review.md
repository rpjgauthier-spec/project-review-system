# Interdependency Review

## Mission

Verify that authorities, producers, consumers, statuses, handoffs, fallbacks, archives, review-state records, and update duties form a coherent system without broken or duplicate contracts.

## Bounded inspection

For each material output, identify:

- authoritative owner
- producer or update source
- direct consumers
- status vocabulary or schema
- trigger and timing
- propagation targets
- fallback when unavailable or invalid
- archive or retention behavior
- review mode and allowed write actions when the output can cause changes
- trust boundary when the output contains instructions or external content

Inspect only direct dependencies and material fallback or escalation targets. Do not follow unlimited reference chains.

## Review-program contract

For a staged review, trace this control path:

```text
review request
→ selected review mode and scope
→ one review-state authority
→ active stage lock
→ active module and shared control model
→ findings and authorized corrections
→ stage report
→ state-authority propagation
→ next stage or bounded completion
```

The tracker or equivalent state authority controls current stage and advancement. Reports are historical evidence. README files, summaries, and changelogs may describe the state but must not override it.

## Finding classes

- conflicting authority
- orphan producer
- consumer without producer
- broken propagation
- incompatible status mapping
- circular dependency
- duplicate ownership
- missing fallback
- fallback bypassing a gate
- archive losing evidence or restrictions
- update cascade disproportionate to value
- stale record treated as current
- handoff without completion condition
- report-tracker disagreement
- review-mode or write-permission mismatch
- untrusted data treated as controlling instruction
- validator-schema mismatch
- unresolved template placeholder treated as state

## Core tests

1. If a source fact changes, which records must change for the system to remain truthful?
2. Can the same fact be entered once and referenced elsewhere?
3. Does every controlling status have a defined producer and consumer?
4. Can a consumer act when its input is unknown, stale, contradictory, inaccessible, or still a template placeholder?
5. Does a fallback preserve the same authorization and safety boundaries?
6. Does closure preserve evidence, restrictions, and stable links?
7. Does a new cycle reassess current facts rather than inherit stale approval?
8. Can a deleted or renamed element silently break downstream behavior?
9. Do review reports, trackers, summaries, changelogs, and metadata agree on version and current state?
10. Does the validator enforce the tracker contract it claims to validate?
11. Does every stage load the shared trust, authorization, evidence, and completion model?
12. Can a report advance a stage without propagation to the state authority?

## Correction order

Prefer:

1. establish one owner for current state
2. clarify ownership
3. repair references, report paths, and status mappings
4. narrow propagation duties
5. merge duplicate producers while retaining distinct consumers
6. add a bounded fallback
7. preserve stable source paths and additive archives
8. align deterministic validation with the declared schema
9. escalate authority or protected-control changes

## Validation

Trace at least:

- normal request-to-verdict path
- diagnostic review without write permission
- authorized corrective write and report propagation path
- missing or invalid input path
- change propagation path
- stale write or partial failure path
- report-tracker disagreement path
- cancellation or closure path
- later resumption or recurrence path when applicable

A stage is `Complete` when material producer-consumer, authority, state-propagation, and validator contracts in the accessible scope are coherent and no blocking escalation remains. It is `Conditional` only when named external or user-controlled facts are required to resolve a bounded contract. It is `Failed` when a material broken dependency or unsafe propagation path remains.