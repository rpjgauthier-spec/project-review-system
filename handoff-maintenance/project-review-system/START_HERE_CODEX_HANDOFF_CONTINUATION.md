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

Only the current Lean handoff remains in the live maintenance directory. Superseded Lean revisions are retained by Git history, not as parallel canonical-looking files.

## Mandatory read order

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md` before any new Adversarial review.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md`.
6. After a semantic sweep, Ownership-Test every blocker/high candidate before proposing handoff corrections.
7. Before any nontrivial handoff-owned correction, perform Model Before Change.
8. Run Structural Optimization / survive-or-die before editing.

## Current status

A delta survive-or-die reweighed the accumulated handoff survivors under the Ownership Test and removed shadow PRS machinery. A subsequent full modeled Adversarial sweep of Lean v9 produced one handoff-owned survivor: Lean misstated the relationship between host/user task authority and actual action authorization.

That survivor passed Ownership Testing and Structural Optimization and has now been applied. Lean v9 now states that actual action authorization comes from the host/user task context and is separate from PRS-governed mode, scope, and transitions.

The prior cull also:

- removed superseded Lean v6, v7, and v8 from the live tree;
- delegated PRS-owned behavior to production `SKILL.md`;
- removed duplicated Adaptive Execution, generic PRS validation, module-loading, and most duplicated authority-model machinery;
- simplified the Adversarial scroll so it derives the target-specific flow during Model Before Review;
- preserved the Ownership Test, convergence rule, and live-artifact hygiene.

## Exact next action

Perform a fresh **full modeled Adversarial review of corrected Lean v9**.

Mandatory method:

1. Run Model Before Review for the corrected Lean v9 and derive the current recovery model from the target.
2. Use the Adversarial Review Model to sweep the entire document.
3. Do not stop at the first blocker.
4. Collect the complete blocker/high candidate set.
5. Ownership-Test every candidate.
6. Report separately:
   - handoff-owned candidates;
   - production-PRS-owned findings;
   - repository/governance-owned blockers;
   - discarded low-value/redundant candidates.
7. Do not edit Lean v9 in the same semantic pass.

If no blocker/high handoff correction survives Ownership Testing and Structural Optimization, the Adversarial maintenance cycle has converged.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
