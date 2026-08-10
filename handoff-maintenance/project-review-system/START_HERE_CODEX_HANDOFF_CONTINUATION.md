# START HERE — Codex Handoff Maintenance Continuation

## Purpose

Use this file to continue the current Project Review System Codex-handoff maintenance work in a fresh ChatGPT conversation without relying on prior chat history.

Repository: `rpjgauthier-spec/project-review-system`

This directory maintains and reviews the Codex recovery handoff. It is not Project Review System production authority and is intentionally outside `skills/project-review-system/**` so routine handoff maintenance does not itself enter the PRS changed-file/revalidation surface.

## Current artifacts

- Recovery handoff: `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md`
- Maintenance guide: `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`
- Mandatory pre-review method: `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- Adversarial stage model: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`
- Interdependency stage model: `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`
- Normalization stage model: `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`
- Structural Optimization stage model: `CODEX_HANDOFF_STRUCTURAL_OPTIMIZATION_REVIEW_MODEL.md`
- End-to-end stage model: `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`
- Deferred stage-model meta-audit: `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md`

Only the current Lean handoff remains in the live maintenance directory. Superseded Lean revisions are retained by Git history, not as parallel canonical-looking files.

## Mandatory read order

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read the stage-specific model for the review being performed.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md`.
6. After a semantic sweep, Ownership-Test every blocker/high candidate before proposing handoff corrections.
7. Before any nontrivial handoff-owned correction, perform Model Before Change.
8. Run Structural Optimization / survive-or-die before editing.

## Current status

Adversarial, Interdependency, Normalization, and Structural Optimization have converged on current Lean v9, including required backward-impact delta checks.

The first End-to-end pass initially appeared to converge, but a skeptical re-hunt exposed a terminal-reporting defect: blocked journeys can terminate before some report facts are established or produced.

That miss exposed a methodological blind spot in the End-to-end model. The model has therefore been strengthened with **terminal-contract completeness**: for every success, blocker, and semantic-boundary terminal state, identify facts guaranteed to exist, facts that may remain unknown or not applicable, report obligations and their preconditions, and whether the next consumer can distinguish `not established` / `not applicable` from omission or fabrication.

The first local Lean correction made only the authority/report-state field tolerant of early blockers. Re-running under the strengthened model showed that field-specific exceptions were too narrow because other report facts may also legitimately not exist on early terminal paths.

The broader terminal-reporting candidate was explicitly Ownership-Tested and subjected to Structural Optimization / survive-or-die. It survived as one general invariant rather than a collection of per-field exceptions.

Lean v9 now states:

> Report each applicable material recovery fact truthfully. When a valid terminal path ends before a fact can be established or produced, report it as `not established` or `not applicable` rather than infer or fabricate it.

The previous local authority-field workaround was removed. No report schema, new state, or additional authority machinery was introduced.

A separate deferred `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md` now exists to review whether any of the five stage models contain similar hidden coverage gaps, false exhaustiveness, weak completion proof, missing state/path combinations, or unchecked obligation preconditions. This meta-audit is maintenance-only and must not be treated as production PRS authority.

## Exact next action

Perform a fresh **full modeled End-to-end validation of corrected Lean v9 under the strengthened End-to-end model** as a convergence hunt.

Mandatory method:

1. Run Model Before Review and derive the current complete recovery journey graph.
2. Read and use `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`, including terminal-contract completeness.
3. Trace every applicable mandatory journey family from entry through terminal state.
4. For every distinct success, blocker, and semantic-boundary terminal state, enumerate:
   - facts guaranteed to exist;
   - facts that may remain `not established` or `not applicable`;
   - report/output obligations;
   - preconditions for each obligation;
   - whether the next consumer can distinguish unknown/not-applicable from omission or fabrication.
5. Collect the complete blocker/high candidate set before reporting.
6. Ownership-Test every candidate.
7. Subject handoff-owned candidates to Structural Optimization / survive-or-die.
8. Do not edit Lean v9 in the same semantic pass.

If no blocker/high handoff correction survives Ownership Testing and Structural Optimization, the End-to-end maintenance stage has converged under the strengthened model.

After the five-stage sequence is settled, perform the deferred `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md` before treating the maintenance review method itself as exhausted or reusable.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
