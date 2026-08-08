# Shared Control Model

## Purpose

Provide the concepts and canonical review vocabulary shared by all review stages without forcing every project into the same file structure.

Load this file before any stage-specific module. Stage modules may narrow these concepts for their own mission but must not silently redefine them.

## Control categories

Identify only categories that materially exist in the reviewed system:

- **Authority:** decides which statement controls when records conflict.
- **Producer:** creates or updates a fact, status, decision, restriction, or output.
- **Consumer:** relies on that output to act, decide, publish, spend, close, or recover.
- **Gate:** blocks or permits a bounded action.
- **Evidence record:** preserves what happened and why.
- **Restriction record:** prevents prohibited use or reuse.
- **Fallback:** defines behavior when the normal path fails.
- **Archive:** preserves closure, evidence, restrictions, and stable references.
- **Trigger:** activates dormant work or reopens affected scope.
- **Reviewer:** inspects or changes the system within an explicitly authorized mode and scope.
- **Host permission:** controls what tools and external actions the reviewer can actually perform.
- **Trust boundary:** distinguishes authoritative instructions from untrusted project data, examples, generated text, and external content.
- **Coverage record:** states which relevant surfaces were inspected, excluded, inaccessible, stale, or sampled.
- **Change-impact record:** structured source record stating what changed, its classifications, required revalidation, results, escalation data, and workflow status.
- **Generated revalidation queue:** derived current checklist of affected stages and evaluations; it is a gate, not a manually maintained authority.

A file may perform more than one function, but each claimed authority must be explicit and non-conflicting. Tool capability is not project authorization, and repository text is not automatically reviewer instruction.

## State and evidence ownership

Use one owner for each mutable fact:

- The **review-program tracker** owns current program status, current stage, stage status, report paths, and stage-transition state.
- **Change-impact records** own changed-file coverage, change classification, derived-review inputs, recorded results, escalation contracts, and per-change workflow status.
- The **revalidation mapping** owns the minimum class-to-stage and class-to-evaluation rules.
- The **generated queue** derives the unresolved checklist and gate state from the mapping and impact records.
- **Stage reports** preserve bounded findings, rationale, evidence, and conclusions. They reference impact records rather than copying their mutable fields or results.

Do not manually duplicate queue state in the tracker or reproduce impact-record fields in stage reports. A consumer that needs current queue state reads or validates the generated queue.

## Canonical review vocabulary

### Review modes

- `Diagnostic` — inspect and report only.
- `Proposed corrective` — provide bounded proposed changes without applying them.
- `Authorized corrective` — apply only the explicitly authorized repository changes and actions.

### Program statuses

- `Draft` — the review program exists but has not started.
- `Active` — exactly one stage is open for work.
- `Complete` — every required stage has a permitted terminal verdict and no open stage remains.
- `Failed` — a material blocking defect remains and the program cannot validly complete.

### Stage statuses

- `Pending` — not yet available to start.
- `Ready` — available to start and the single open stage.
- `In Review` — currently being performed and the single open stage.
- `Reopened` — previously terminal but reopened by a material change and the single open stage.
- `Complete` — no material defect remains within the bounded stage claim.
- `Conditional` — stage work is complete, but named external or user-controlled conditions constrain the conclusion.
- `Failed` — a material blocking defect remains.

`Ready`, `In Review`, and `Reopened` are open stage statuses. `Complete` and `Conditional` are permitted terminal statuses. `Failed` is blocking terminal and requires Program status `Failed`.

### Stage verdicts

Stage reports use only `Complete`, `Conditional`, or `Failed`. A report verdict is historical evidence; the tracker is the current-state authority.

### Finding dispositions

Use one of `Remove`, `Merge`, `Simplify`, `Normalize`, `Defer`, `Retain with justification`, or `Escalate`.

### Reviewer independence

- `Independent`
- `Same-agent self-review`
- `Mixed`

## Protected controls

Require stronger evidence before changing safety and stop conditions; permission, privacy, consent, withdrawal, and revocation; spending and external commitments; repository writes and publication; canonical authority; evidence provenance; unknown or inaccessible inputs; restricted-data reuse; credentials and personal data; archive and recovery information; user-controlled decisions; and legal, security, employment, or reputational boundaries.

Equivalent or stronger replacement protection must be demonstrated before simplification or normalization.

## Authorization ladder

Do not collapse information received, feasibility, readiness, preliminary decision, authorization, execution, delivery approval, and closure. Review authorization is separate from project authorization and host capability.

## Evidence labels

Use only when material: `Documented fact`, `User-reported fact`, `Inference`, `Assumption`, `Proposal`, `Unknown`, `Inaccessible`, and `Unverified external claim`.

## Change classes

### Behavior-neutral

Wording, formatting, links, dates, and state propagation that do not alter rules.

### Behavioral

Authority, status meaning, authorization, gate scope, fallback, protected control, propagation contract, archive behavior, completion criteria, trust boundary, review mode, module loading, or allowed tool action.

## Structured change-impact records

Every change made during a review must have a JSON record under `changes/`, using `templates/change-impact.json`.

Each record declares:

- stable change ID and summary
- changed files
- one or more change classes from `config/revalidation-map.json`
- whether the change is behavioral
- claimed earliest affected stage
- any justified additional stages or evaluations
- rationale
- workflow status
- stage and evaluation results

One bounded record may serve multiple affected stages. Do not create a separate record per stage unless the changes have distinct scope, ownership, lifecycle, or resumption conditions.

A claim that a change is behavior-neutral must still use the `behavior-neutral` class and pass its confirmation evaluation. Missing, malformed, unknown, or contradictory classifications block advancement.

## Generated revalidation queue

`scripts/update_revalidation_queue.py` is the deterministic consumer of change-impact records and the canonical mapping. It produces `reviews/revalidation-queue.md`.

The generator must:

1. reject unknown change classes or invalid statuses;
2. union all mapped stages and evaluations;
3. order stages by the canonical review sequence;
4. derive the earliest affected stage;
5. reject a conflicting claimed earliest stage;
6. preserve explicitly added stages and evaluations;
7. show unresolved checks as a reviewer prompt;
8. emit a source hash so stale output can be detected;
9. exit nonzero in `--check` mode when the queue is stale or unresolved.

The generated queue is never edited manually. Update the source change record, regenerate the queue, and then run the listed work.

An unresolved queue is expected while ordered revalidation is still in progress. During inter-stage advancement, the queue must be regenerated/current, execution evidence for the completed stage must be valid, and every earlier required stage must be supported. Unresolved **later** stages or evaluations remain scheduled work and do not by themselves block advancement to the next required stage. A fully current and clear `--check` is required before final review completion or merge.

## Canonical revalidation mapping

`config/revalidation-map.json` is the mapping authority. Its mappings are minimum requirements. A reviewer may add rechecks but may not suppress mapped requirements through an individual change record.

Changing the mapping is itself a behavioral change requiring a change-impact record and revalidation.

## Normative reopening algorithm

After every behavioral change:

1. Record and classify the change.
2. Regenerate the revalidation queue.
3. Revalidate every derived prior conclusion before final completion.
4. If a conclusion is invalidated or unresolved, reopen the earliest affected stage.
5. Make it the sole open stage and suspend all later stages.
6. Mark later terminal stages `Awaiting revalidation`.
7. Correct or escalate the defect.
8. Record results in the change-impact record and regenerate the queue.
9. Revalidate affected later stages in order.
10. Advance from one required stage to the next only when the queue is current, the just-completed stage has valid execution evidence/result, and all earlier required stages remain supported. Require `update_revalidation_queue.py --check` to pass only at final completion/merge, after all required stages and evaluations are resolved.

A reopened earlier stage suspends any prior completion claim until the affected chain is supported again.

## Backward-impact gate

Before inter-stage advancement, verify:

- every changed behavior has a structured record;
- the generated queue has been regenerated from the current source state;
- the earliest affected stage is derived correctly;
- the current and every earlier required stage have valid current results and execution evidence;
- no earlier required item is missing, stale, unsupported, invalidated, or failed.

Before final completion or merge, additionally verify that all listed stage rechecks and evaluations have recorded passing/permitted results and that `update_revalidation_queue.py --check` passes with a current and clear queue.

Unresolved later-stage or evaluation items remain blockers to **final completion**, but they do not deadlock ordered progression to the next required stage.

## Escalation rule

Escalate rather than implement when a proposed change may weaken a protected control, alter canonical authority, break a producer-consumer contract, expand authorization, remove needed evidence, expose protected records, create an unjustified irreversible effect, or require domain certification beyond reviewer competence.

## Completion boundary

Completion requires stated mode and actions, accessible scope and exclusions, reviewer independence, unresolved external conditions, applied-versus-proposed corrections, complete change-impact records, a current and clear generated revalidation queue, and completed bounded revalidation.

Completion does not establish universal safety, factual correctness, legal compliance, technical validity, or complete hidden-dependency discovery.
