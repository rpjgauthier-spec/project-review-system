# START HERE — Codex Handoff Maintenance Continuation

## Purpose

Use this file to continue the current Project Review System Codex-handoff maintenance work in a fresh ChatGPT conversation without relying on prior chat history.

Repository: `rpjgauthier-spec/project-review-system`

This directory is for maintaining and reviewing the Codex recovery handoff. It is not Project Review System production authority and is intentionally outside `skills/project-review-system/**` so routine handoff maintenance does not itself enter the PRS changed-file/revalidation surface.

## Current artifacts

- Recovery handoff: `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v6.md`
- Maintenance guide: `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`
- Mandatory pre-review method: `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- Adversarial stage model: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

Repository-side non-authoritative design references remain under `skills/project-review-system/reviews/` and must not be treated as production authority unless current PRS governance promotes them.

## Mandatory read order

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md` before any new Adversarial review.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v6.md`.
6. Before any nontrivial correction, perform Model Before Change.
7. Run Structural Optimization / survive-or-die on proposed corrections before editing.

## Current status

Lean v6 is the current review target. It incorporates the latest survive-or-die survivors:

- Diagnostic-only bootstrap before governing PRS controls are established;
- production PRS controls must be bound to the legitimate recovery context before semantic reliance;
- worktree `isolation` wording replaced with workspace separation and explicitly distinguished from PRS `ISOLATED`;
- Adaptive Execution preflight placed at the mechanical-to-semantic transition;
- historical validity separated from present acceptance as current review credit;
- maintenance artifacts moved outside `skills/project-review-system/**`.

## Exact next action

Perform a fresh **full Adversarial review of Lean v6**.

Mandatory method:

1. Run Model Before Review for Lean v6.
2. Refresh the purpose/authority/identity/state/invariant/failure model.
3. Use the Adversarial Review Model.
4. Sweep the entire document.
5. Do not stop at the first blocker.
6. Collect all blocker/high findings before reporting.
7. Do not edit Lean v6 in the same pass.

After findings:

1. Model Before Change on proposed corrections.
2. Survive-or-die / Structural Optimization.
3. Apply only survivors.
4. Repeat the full modeled Adversarial sweep.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model versions, review stage, or exact next action changes.
