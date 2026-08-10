# Codex Handoff — Project Review System Recovery

## Purpose

Recover the current governed state of `rpjgauthier-spec/project-review-system`, determine the next valid recovery action from repository evidence, continue only that recovery, and stop when the next valid governed state or a real blocker is reached.

This handoff is navigation/recovery context only. It is not Project Review System (PRS) authority and must not invent authority, review credit, succession, control-selection, migration, or bootstrap rules.

## Starting point

Repository: `rpjgauthier-spec/project-review-system`

Initial recovery locator: `implementation-phase-2-controller-core`

Treat the locator as a place to begin discovery, not as authority. Implementation similarity, ancestry, or cherry-pick equivalence does not by itself transfer review state or review credit.

Before applicable repository authority is established, perform only non-destructive factual discovery. Verify repository/remote identity and preserve unrelated user work. A separate worktree may provide workspace separation but is not evidence of PRS semantic isolation.

## Governing controls and state

Read `skills/project-review-system/SKILL.md` from the PRS control context whose applicability is established by existing repository authority, then follow that authority for PRS behavior, required references, review-state discovery, execution controls, revalidation, validation, and advancement.

Do not recreate those mechanisms in this handoff.

If existing repository evidence does not determine which PRS controls or review state apply, stop and report the ambiguity rather than manufacturing a selection or succession rule.

Use current PRS mechanisms to establish the authoritative review/change state, current revision/target, and next permitted PRS activity. Establish actual action authorization from the host/user task context separately from PRS-governed mode, scope, and transitions.

Before finalizing governed recovery scope, identify the current source-scope authority through existing repository authority, then determine from that source whether the frozen controller-core Slice 1 boundary still applies. If it does, read the controlling source material, including when still applicable:

- Issue #11 — `Implementation Phase 2: executable controller core and conformance harness`
- clarification/comment ID `5229287324`

Do not broaden scope from historical summaries when controlling source authority cannot be established.

## Historical recovery problem

Earlier recovery identified a `pass-boundary-enforcement` failure involving:

- durable End-to-end pass evidence;
- later gate mutation and logical-pass rerun within the same review revision;
- handoff-consumer naming mismatches;
- final semantic handoff recorded to the wrong consumer.

Recovery pointers:

- `skills/project-review-system/changes/2026-08-08-controller-core-skeleton.json`
- `skills/project-review-system/evals/pass-boundary-enforcement.md`
- `skills/project-review-system/scripts/check_pass_boundaries.py`
- Issue #13 — `Harden review-state transitions and cross-platform artifact binding`

These are pointers, not proof that the repository is still in that historical state.

Reproduce the historical deterministic failure or establish its current governed disposition/replacement failure using current repository state and current PRS-required validation. Run the targeted pass-boundary checker using its repository-defined invocation/inputs.

When historical review credit is disputed, establish the authority applicable to the disputed occurrence from durable repository chronology/provenance under current governance; if it cannot be established truthfully, report that limitation rather than infer it. Then distinguish:

- whether the occurrence was valid under the authority applicable when it occurred; and
- whether current production governance accepts that evidence as current review credit.

A current checker failure is evidence about current conformance; it does not by itself rewrite the authority that governed a historical occurrence. Historical evidence likewise does not create replacement authority or new review credit.

## Recovery boundary

Follow current PRS controls for semantic execution boundaries, revalidation, corrections, and validation. Do not duplicate or override those rules here.

Use a truthful governed recovery path when one exists. Stop rather than:

- inventing missing authority or a transition mechanism;
- falsifying or rewriting durable chronology;
- weakening controls merely to make recovery pass.

Continue routine recovery autonomously when both PRS governance and host/user authorization permit it. Ask the user only when access, authorization, or a genuine unresolved decision requires user input.

Stop when any of the following applies:

1. PRS requires a fresh semantic execution boundary;
2. required authority or authorization cannot be established;
3. credentials/access or a genuine user decision is required;
4. the only apparent path would invent authority or falsify durable history.

A blocked recovery is not successful completion.

## Expected recovery report

Report only material recovery facts:

- governing repository/ref and authoritative review state used, or which of them could not be established;
- failure reproduced or current replacement disposition;
- governed next action taken;
- material changes and validation performed;
- commits pushed, if any;
- remaining blocker or exact next semantic boundary.

Do not claim correctness beyond what was actually validated.
