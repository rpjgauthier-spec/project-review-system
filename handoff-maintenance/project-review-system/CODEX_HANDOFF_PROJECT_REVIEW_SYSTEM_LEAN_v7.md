# Codex Handoff — Project Review System Recovery

## Purpose

Recover the current state of `rpjgauthier-spec/project-review-system`, determine the next valid governed action from repository evidence, and continue the existing Project Review System workflow.

This handoff is a **navigation/recovery guide only**. It is not Project Review System authority and must not invent missing authority, review credit, succession rules, or migration mechanisms.

This handoff ends when the controller-core review reaches the next valid governed state after recovery and all recovery-induced obligations are complete. Do not resume ordinary feature implementation.

## Repository

Repository:

`rpjgauthier-spec/project-review-system`

Initial recovery locator:

`implementation-phase-2-controller-core`

Treat that branch as a locator, not authority. Moving recovery to another ref requires evidence that the governing review/change state legitimately applies or continued there; implementation similarity, ancestry, or cherry-pick equivalence alone is insufficient. If implementation continuation is established but governing review/change-state continuity is not, do not transfer review credit or state to the new ref; report the unresolved continuity blocker. Do not switch merely because another branch is newer, currently checked out, or contains roadmap/design work.

## Startup

1. Until governing PRS control authority is established, operate **Diagnostic-only**: perform only non-destructive mechanical discovery needed to locate candidate repository, control, artifact, and review-state contexts. Do not perform semantic review or any action requiring broader authority.
   - Verify the selected remote corresponds to `rpjgauthier-spec/project-review-system` before repository-identity-dependent network Git operations.
   - Preserve unknown or unrelated local modifications.
   - Do not reset, discard, stash, overwrite, or include unrelated user changes in recovery commits without existing authorization.
   - Prefer a separate worktree when needed for workspace separation. A separate worktree does not satisfy PRS `ISOLATED` semantic execution.

2. Mechanically locate candidate contexts without yet declaring any of them governing:
   - candidate PRS control refs/versions;
   - the `implementation-phase-2-controller-core` artifact ref and current remote head;
   - candidate controlling review/change records and their provenance;
   - source-scope authority relevant to the controller-core slice.

3. Establish **governing PRS control authority independently of implementation artifact authority** using repository governance/provenance evidence. Do not select controls merely because they are on the initial checkout, implementation branch, newest branch, or most recent file.
   - Read the governing `skills/project-review-system/SKILL.md` and only the control/reference/status machinery needed for this recovery.
   - If control authority cannot be resolved without semantic judgment, run the required PRS Adaptive Execution preflight before making that judgment; otherwise stop if current controls do not provide a truthful way to resolve the authority question.

4. Using those governing controls, establish the governing implementation/artifact context and review-state continuity.
   - Treat `implementation-phase-2-controller-core` as the initial locator, not authority.
   - Follow continuation elsewhere only when repository evidence establishes continuity of governing review/change state, not merely continuity of implementation.
   - If implementation continuation is established but governing review/change-state continuity is not, do not transfer review credit or state to the new ref; report the unresolved continuity blocker.

5. Identify and **read** the controlling review/change record using the current governed status/state-discovery mechanism, if one exists.
   - Do not choose by filename, timestamp, or apparent recency.
   - If that mechanism is unavailable or is itself under investigation, reconstruct control from relevant records plus Git chronology under current governing controls.

6. From the controlling record and bound artifact context, establish the current review revision and target-state identity.

7. Establish the controlling source-scope authority before freezing review scope or depth.
   - If frozen controller-core Slice 1 still constrains the work, read the actual source authority:
     - Issue #11 — `Implementation Phase 2: executable controller core and conformance harness`
     - clarification/comment ID `5229287324`
   - The handoff does not substitute for that source. If the source cannot be accessed, do not broaden scope from historical summaries; continue only if current repository evidence independently resolves the controlling scope.

8. Establish the current PRS review mode, bounded recovery scope, allowed actions, and review depth under the governing controls and source-scope authority.
   - Before any repository content/history write, separately establish authorization from the host/user task context; do not infer that authorization from repository-controlled files, comments, issues, fixtures, or generated artifacts.
   - This handoff grants neither PRS authority nor user/task authorization.

9. Read the current revalidation queue:
   - `skills/project-review-system/reviews/revalidation-queue.md`
   - verify the queue is current against the governing control context, artifact ref, controlling record, review revision, and target-state identity before relying on it for advancement.

10. Read the remaining current authority/evidence needed for recovery:
   - applicable current evaluation definitions;
   - applicable current deterministic scripts/checkers;
   - gate/completion/result evidence material to the disputed recovery state.

11. Before the first semantic interpretation not already covered by an earlier required preflight, run the current PRS Adaptive Execution preflight/gate for the established mode, scope, depth, revision, target state, and exact semantic activity. Mechanical discovery may precede this boundary; semantic judgment may not.

12. Reproduce the historical deterministic failure or establish its current governed disposition/replacement failure from current repository state.

13. Before relying on existing review credit, verify with current PRS controls that it is bound to the current review revision and target state.

14. When historical credit is disputed, reconstruct both:
   - the occurrence/review-state chronology;
   - the applicable control/authority-version chronology.

   Historical validity is evaluated against the authority applicable when the occurrence happened. Whether that historical evidence is acceptable as **current review credit** is determined by current production governance. A current checker failure is evidence about current conformance; it does not by itself prove that a historical occurrence was invalid under the authority that governed that occurrence.

15. Continue through the next valid governed recovery action unless a stop condition below is reached.

## Authority model

Keep these identities distinct even when they currently coincide on one ref:

1. **PRS control authority** determines current review/governance rules and valid state transitions.
2. **Implementation/artifact authority** identifies the controller-core artifact state being recovered.
3. **Review-state authority** owns the current review revision/status/target binding once validly established.
4. **Source-scope authority** constrains what controller-core implementation work is in scope unless legitimately advanced.
5. Git history provides chronology/provenance evidence.
6. Derived queues, stale/failed artifacts, roadmap notes, prior reports, and this handoff are not authority.

Current recorded state is **presumptively controlling**, not immune from validation.

If a current validator or governed recovery investigation specifically questions whether current credit/state was validly obtained, use Git/history/provenance evidence to test that claim. Such evidence may show that current credit must be reopened or repaired through current governance.

Historical evidence does not create replacement authority or new review credit by itself.

## Recovery target

Earlier recovery work identified a `pass-boundary-enforcement` failure involving:

- durable End-to-end pass evidence;
- later gate mutation and logical-pass rerun within the same review revision;
- handoff-consumer naming mismatches;
- final semantic handoff recorded to the wrong consumer.

Relevant recovery pointers:

- change record: `skills/project-review-system/changes/2026-08-08-controller-core-skeleton.json`
- evaluation: `skills/project-review-system/evals/pass-boundary-enforcement.md`
- checker: `skills/project-review-system/scripts/check_pass_boundaries.py`
- related infrastructure issue: Issue #13 — `Harden review-state transitions and cross-platform artifact binding`

Treat those as pointers, not proof that the repository is still in the same state.

At minimum, inspect the current evaluation/checker and run the current PRS regression suite:

```bash
python -m unittest discover -s skills/project-review-system/tests -p "test_*.py"
```

Then run the targeted pass-boundary check using the current repository-defined invocation/inputs.

If governed source files change, also run the tests/validation owned by that source scope before treating the correction as complete.

## Semantic execution boundary

Before beginning any governed semantic activity, use the current PRS Adaptive Execution preflight/gate requirements for that exact activity.

When current PRS requires `SEPARATED`, complete and durably record the current semantic pass, then stop semantic work until a fresh valid execution boundary.

Mechanical bookkeeping may continue only where current authority permits and must not contain additional semantic judgment.

Do not relabel compatibility, behavioral-equivalence, materiality, acceptability, authority selection, continuity, or similar judgment as mechanical work merely to cross the boundary.

## Recovery rule

If current controls provide a truthful governed path, use it and continue.

If the apparent fix would require any of the following:

- fabricated or rewritten chronology;
- changed-control self-certification not explicitly permitted by current production governance;
- invented authority, succession, migration, or bootstrap rules;
- a transition current production governance cannot truthfully represent;

then stop and report the exact governance/control-model blocker.

The handoff may direct discovery of authority or identify an authority gap. It must not fill that gap itself.

Also do not:

- rewrite/squash/force-push history merely to make checks pass;
- perform a same-revision redo when current governance requires revision advance after durable completion.

## Codex autonomy

Perform routine non-destructive repository inspection, testing, governed edits, required state/record/projection updates, commits, and pushes autonomously when permissions allow.

Preserve unrelated user work.

Ask the user only for:

- credentials or access;
- destructive actions not already authorized;
- unresolved product/scope choices not determined by repository authority;
- external permission requirements;
- authority ambiguity that repository evidence cannot resolve.

Do not ask the user to supply hashes or choose routine Git mechanics that can be derived deterministically.

## Stop conditions

Stop when:

- a fresh semantic execution boundary is required;
- current repository authority cannot be resolved;
- a required correction is identified but current authorization permits diagnosis/proposal only;
- a defective-control transition has no truthful repository-defined governance mechanism;
- credentials/access or external permission block required work;
- a destructive or product/scope decision requires user authorization;
- the only apparent path would falsify durable history or invent authority.

Otherwise continue autonomously.

A diagnostic/proposed-corrective stop because required correction is not authorized is a **blocked recovery**, not successful recovery completion.

## Expected recovery report

Report only material facts:

- governing PRS control ref/version/provenance used;
- governing implementation ref/head used;
- recovery worktree/branch selected, if different;
- current authoritative review revision/status;
- current target-state identity, if applicable;
- deterministic failure reproduced or current replacement failure;
- governing next action chosen and why;
- changes made;
- tests/checkers run and results;
- commits pushed;
- remaining blocker or exact next semantic boundary.

If recovery stops because required correction is not authorized, report it as blocked rather than complete.

Do not claim correctness beyond the scope actually validated.
