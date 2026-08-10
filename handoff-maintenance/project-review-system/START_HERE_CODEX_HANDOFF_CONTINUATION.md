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

The corrected Lean v9 completed a fresh full modeled Adversarial review with no blocker/high handoff correction surviving Ownership Testing and Structural Optimization. The Adversarial maintenance cycle has converged.

The maintenance method now includes a dedicated Interdependency Review Model. It derives the current dependency graph from Lean rather than storing a duplicate target flow, and tests producer/consumer edges, authority-to-action relationships, evidence bindings, propagation duties, handoffs, fallbacks, circularity, orphaning, and completion propagation. Findings remain subject to the same Ownership Test before they can become handoff changes.

The prior culls remain in force:

- PRS-owned behavior is delegated to production `SKILL.md` rather than reimplemented in Lean;
- obsolete Lean revisions live only in Git history;
- the handoff remains recovery-specific navigation rather than a shadow PRS;
- modeled findings do not imply handoff ownership;
- maintenance converges when no blocker/high handoff correction survives Ownership Testing and Structural Optimization.

## Exact next action

Perform a fresh **full modeled Interdependency review of Lean v9**.

Mandatory method:

1. Run Model Before Review for Lean v9 and derive the current recovery dependency graph.
2. Read and use `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`.
3. Sweep the entire document; do not stop at the first broken edge.
4. Collect the complete blocker/high candidate set.
5. Ownership-Test every candidate.
6. Report separately:
   - handoff-owned candidates;
   - production-PRS-owned findings;
   - repository/governance-owned blockers;
   - discarded low-value/redundant candidates.
7. Do not edit Lean v9 in the same semantic pass.

If no blocker/high handoff correction survives Ownership Testing and Structural Optimization, the Interdependency maintenance cycle has converged.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
