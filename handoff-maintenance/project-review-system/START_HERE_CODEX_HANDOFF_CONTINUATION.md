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
- Stage-model meta-audit: `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md`

Only the current Lean handoff remains in the live maintenance directory. Superseded Lean revisions are retained by Git history, not as parallel canonical-looking files.

## Mandatory read order

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read the applicable stage/model or meta-audit file for the work being performed.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md` when the review targets Lean.
6. After a semantic sweep, Ownership-Test every blocker/high candidate before proposing corrections.
7. Before any nontrivial owned correction, perform Model Before Change.
8. Run Structural Optimization / survive-or-die before editing.

## Current status

Adversarial, Interdependency, Normalization, Structural Optimization, and End-to-end validation have converged on current Lean v9, including required backward-impact delta checks.

The first End-to-end pass initially appeared to converge, but a skeptical re-hunt exposed a terminal-reporting defect: blocked journeys can terminate before some report facts are established or produced.

That miss exposed a methodological blind spot in the End-to-end model. The model was strengthened with **terminal-contract completeness**: for every success, blocker, and semantic-boundary terminal state, identify facts guaranteed to exist, facts that may remain unknown or not applicable, report obligations and their preconditions, and whether the next consumer can distinguish `not established` / `not applicable` from omission or fabrication.

Lean v9 now states:

> Report each applicable material recovery fact truthfully. When a valid terminal path ends before a fact can be established or produced, report it as `not established` or `not applicable` rather than infer or fabricate it.

A fresh full End-to-end convergence hunt under the strengthened model re-traced every mandatory journey and terminal class. No blocker/high handoff correction survived Ownership Testing and Structural Optimization. Sparse terminal paths—including authority ambiguity, authorization blockers, fresh semantic-boundary stops, and interruption after partial progress—can now satisfy the report contract without fabricating unavailable facts.

The five-stage Lean review sequence is therefore settled under the current maintenance models.

A separate `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md` exists because the End-to-end miss demonstrated that a stage model can appear exhaustive while broad dimensions still hide mechanically untested subcases. This meta-audit reviews the five maintenance stage models and their cross-stage boundaries; it is maintenance-only and is not production PRS authority.

## Exact next action

Perform the full **Stage Model Completeness Audit** defined by `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md`.

Mandatory method:

1. Read the audit scroll plus all five stage models, `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`, and `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
2. Audit all five stage models before proposing any method correction; do not stop at the first gap.
3. For each stage, test coverage decomposition, state/path completeness, obligation-precondition closure, producer-consumer symmetry, negative-space coverage, completion-proof quality, and false-exhaustiveness pressure.
4. Test cross-stage boundary gaps separately.
5. Collect the complete blocker/high maintenance-method candidate set.
6. Ownership-Test every candidate.
7. Subject maintenance-owned candidates to Structural Optimization / survive-or-die.
8. Report the complete surviving correction set without editing stage models in the same semantic audit pass.

The core question is:

> What would make us believe we left no stone unturned while still leaving one unturned?

After the complete audit and cull, apply surviving method corrections only in later bounded correction passes, then re-run affected review scopes as required.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
