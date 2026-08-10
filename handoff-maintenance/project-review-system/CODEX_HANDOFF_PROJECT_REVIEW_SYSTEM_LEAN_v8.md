# Codex Handoff — Project Review System Recovery

## Purpose

Recover the current state of `rpjgauthier-spec/project-review-system`, determine the next valid governed action from repository evidence, and continue the existing Project Review System workflow.

This handoff is a **navigation/recovery guide only**. It is not Project Review System authority and must not invent missing authority, review credit, succession rules, control-selection rules, or migration/bootstrap mechanisms.

This handoff ends when the controller-core review reaches the next valid governed state after recovery and all recovery-induced obligations are complete. Do not resume ordinary feature implementation.

## Repository

Repository:

`rpjgauthier-spec/project-review-system`

Initial recovery locator:

`implementation-phase-2-controller-core`

Treat that branch as a locator, not authority. Moving recovery to another ref requires existing repository evidence that governing review/change state legitimately continued there; implementation similarity, ancestry, or cherry-pick equivalence alone is insufficient. If review-state continuity cannot be established under existing repository authority, do not transfer review credit or state; report the blocker.

## Startup

1. Before applicable PRS controls are established, perform only **non-destructive factual discovery** needed to locate repository evidence.
   - Verify the selected remote corresponds to `rpjgauthier-spec/project-review-system` before repository-identity-dependent network Git operations.
   - Inventory refs, commit identities, relevant file existence/content, Git chronology/provenance, candidate review records, and external authority pointers without declaring them authoritative merely because they were found.
   - Preserve unknown or unrelated local modifications.
   - Do not reset, discard, stash, overwrite, or include unrelated user changes without existing authorization.
   - Prefer a separate worktree when needed for workspace separation. A separate worktree does not satisfy PRS `ISOLATED` semantic execution.

2. Determine which PRS controls are applicable **only through existing repository authority/provenance**.
   - Do not create a handoff-specific election, succession, precedence, or cross-ref binding mechanism.
   - Do not select controls merely because they are on the initial checkout, implementation branch, newest branch, or most recent file.
   - If existing repository authority does not determine applicable PRS controls from available evidence, stop and report the control-applicability ambiguity. The handoff must not resolve the missing governance itself.

3. Read the applicable current PRS authority needed for this recovery:
   - `skills/project-review-system/SKILL.md`
   - applicable current control/reference files;
   - applicable current deterministic status/state-discovery scripts.

4. Under those controls, establish the governing implementation/artifact context and review-state continuity.
   - Treat `implementation-phase-2-controller-core` as the initial locator, not authority.
   - Follow continuation elsewhere only when repository evidence establishes continuity of governing review/change state, not merely continuity of implementation.
   - If implementation continuation is established but review-state continuity is not, do not transfer review credit or state.

5. Identify and **read** the controlling review/change record using the governed status/state-discovery mechanism, if one exists.
   - Do not choose by filename, timestamp, or apparent recency.
   - If the mechanism is unavailable or itself under investigation, reconstruct only what current production governance permits from relevant records plus Git chronology.

6. From the controlling record and bound artifact context, establish the current review revision and target-state identity.

7. Establish controlling source-scope authority before freezing review scope or depth.
   - If frozen controller-core Slice 1 still constrains the work, read the actual source authority:
     - Issue #11 — `Implementation Phase 2: executable controller core and conformance harness`
     - clarification/comment ID `5229287324`
   - The handoff does not substitute for that source. If it cannot be accessed, do not broaden scope from historical summaries; continue only when existing repository evidence independently resolves the controlling scope.

8. Establish under PRS controls:
   - review mode;
   - bounded governed recovery scope;
   - review depth;
   - next permitted PRS transition/activity.

   Separately establish actual action authorization from the host/user task context before editing, committing, pushing, or performing any other action requiring such permission. Repository-controlled content cannot grant host/user permission.

9. Read the current revalidation queue:
   - `skills/project-review-system/reviews/revalidation-queue.md`
   - verify it is current against the applicable PRS control context, artifact ref, controlling record, review revision, and target-state identity before relying on it for advancement.

10. Read remaining authority/evidence material to recovery:
   - applicable evaluation definitions;
   - applicable deterministic scripts/checkers;
   - gate/completion/result evidence relevant to the disputed state.

11. Before the first governed semantic judgment, use the current PRS Adaptive Execution preflight/gate requirements for the exact semantic activity. Factual discovery may precede this boundary; semantic judgment may not.

12. Reproduce the historical deterministic failure or establish its current governed disposition/replacement failure from current repository state.

13. Before relying on existing review credit, verify with current PRS controls that it is bound to the current review revision and target state.

14. When historical credit is disputed, reconstruct both:
   - occurrence/review-state chronology;
   - applicable control/authority-version chronology.

   Historical validity is evaluated against authority applicable when the occurrence happened. Whether that historical evidence is acceptable as **current review credit** is determined by current production governance. A current checker failure is evidence about current conformance; it does not by itself prove that a historical occurrence was invalid under the authority that governed it.

15. Continue through the next valid governed recovery action unless a stop condition below is reached.

## Authority model

Keep these roles distinct without inventing new selection machinery:

1. **PRS controls** own review/governance rules and valid transitions when their applicability is established by existing repository authority.
2. **Implementation/artifact state** is the controller-core artifact being recovered.
3. **Review-state authority** owns current review revision/status/target binding once validly established.
4. **Source-scope authority** constrains controller-core implementation scope unless legitimately advanced.
5. **Host/user task authority** owns actual permission for edits, commits, pushes, destructive actions, and other externally authorized actions.
6. Git history provides chronology/provenance evidence.
7. Derived queues, stale/failed artifacts, roadmap notes, prior reports, and this handoff are not authority.

Current recorded state is presumptively controlling, not immune from governed validation.

Historical evidence does not create replacement authority or new review credit by itself.

## Recovery target

Earlier recovery work identified a `pass-boundary-enforcement` failure involving:

- durable End-to-end pass evidence;
- later gate mutation and logical-pass rerun within the same review revision;
- handoff-consumer naming mismatches;
- final semantic handoff recorded to the wrong consumer.

Relevant recovery pointers:

- `skills/project-review-system/changes/2026-08-08-controller-core-skeleton.json`
- `skills/project-review-system/evals/pass-boundary-enforcement.md`
- `skills/project-review-system/scripts/check_pass_boundaries.py`
- Issue #13 — `Harden review-state transitions and cross-platform artifact binding`

Treat these as pointers, not proof that the repository is still in the same state.

At minimum, inspect the applicable evaluation/checker and run the PRS regression suite required by the applicable controls:

```bash
python -m unittest discover -s skills/project-review-system/tests -p "test_*.py"
```

Then run the targeted pass-boundary check using the repository-defined invocation/inputs.

If governed source files change, also run validation owned by that source scope before treating the correction as complete.

## Semantic execution boundary

Before any governed semantic activity, use current PRS Adaptive Execution requirements for that exact activity.

When current PRS requires `SEPARATED`, complete and durably record the current semantic pass, then stop semantic work until a fresh valid execution boundary.

Mechanical bookkeeping may continue only where current authority permits and must not contain additional semantic judgment.

Do not relabel compatibility, behavioral equivalence, materiality, acceptability, authority applicability, continuity, or similar judgment as mechanical work merely to cross the boundary.

## Recovery rule

If existing production controls provide a truthful governed path, use it and continue.

If the apparent fix would require:

- fabricated or rewritten chronology;
- changed-control self-certification not explicitly permitted by production governance;
- invented authority, succession, control-selection, migration, or bootstrap rules;
- a transition production governance cannot truthfully represent;

stop and report the exact governance/control-model blocker.

The handoff may direct discovery of authority or identify an authority gap. It must not fill the gap itself.

Do not rewrite/squash/force-push history merely to make checks pass, and do not perform a same-revision redo when current governance requires revision advance after durable completion.

## Codex autonomy

Perform routine non-destructive inspection, testing, governed edits, required state/record/projection updates, commits, and pushes autonomously **only when host/user permissions and PRS governance both permit the relevant action**.

Preserve unrelated user work.

Ask the user only for credentials/access, destructive actions not already authorized, unresolved product/scope choices, external permission requirements, or authority ambiguity repository evidence cannot resolve.

Do not ask the user to supply hashes or choose routine Git mechanics that can be derived deterministically.

## Stop conditions

Stop when:

- a fresh semantic execution boundary is required;
- applicable PRS controls or current repository authority cannot be resolved;
- a required correction is identified but current host/user authorization permits diagnosis/proposal only;
- a defective-control transition has no truthful repository-defined governance mechanism;
- credentials/access or external permission block required work;
- a destructive or product/scope decision requires user authorization;
- the only apparent path would falsify durable history or invent authority.

Otherwise continue autonomously.

A diagnostic/proposed-corrective stop because required correction is not authorized is **blocked recovery**, not successful completion.

## Expected recovery report

Report only material facts:

- applicable PRS control context used and its repository evidence;
- governing implementation ref/head used;
- recovery worktree/branch selected, if different;
- current authoritative review revision/status;
- current target-state identity, if applicable;
- deterministic failure reproduced or replacement failure;
- governing next action chosen and why;
- changes made;
- tests/checkers run and results;
- commits pushed;
- remaining blocker or exact next semantic boundary.

If recovery stops because required correction is not authorized or authority applicability is unresolved, report it as blocked rather than complete.

Do not claim correctness beyond the scope actually validated.
