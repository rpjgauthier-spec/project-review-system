# START HERE — Codex Handoff Maintenance Continuation

## Purpose

Use this file to continue the current Project Review System Codex-handoff work in a fresh ChatGPT conversation without relying on prior chat history.

Repository: `rpjgauthier-spec/project-review-system`

This directory is for maintaining/reviewing the Codex recovery handoff. It is not Project Review System production authority.

## Current artifacts

All canonical maintenance artifacts are in this directory:

- Recovery handoff: `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v5.md`
- Maintenance guide: `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`
- Mandatory pre-review method: `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- Adversarial stage model: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

Repository-side non-authoritative design references:

- `skills/project-review-system/reviews/adaptive-model-before-change-design-note.md`
- `skills/project-review-system/reviews/model-before-change-workflow-integration-design-note.md`
- `skills/project-review-system/reviews/model-before-review-design-note.md`
- `skills/project-review-system/reviews/review-method-evolution-design-note.md`

## Mandatory read order

1. Read this file completely.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md` before any new Adversarial review.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v5.md`, the current review target.
6. Before applying any nontrivial correction, perform the Model-Before-Change method required by the maintenance guide.
7. Subject proposed corrections to Structural Optimization / survive-or-die review before editing the handoff.

## Current review-cycle status

The current handoff is **Lean v5**.

The most recent completed action was:

- a full Adversarial sweep produced blocker/high candidates;
- Structural Optimization / survive-or-die retained only the justified corrections;
- those survivors were applied to produce Lean v5.

Lean v5 now includes:

- explicit bounded task-completion boundary;
- startup ordering that reads/discovers authority before relying on it;
- governing ref/record/revision/target establishment before queue use;
- review-mode and host/user authorization separation;
- remote identity verification;
- governed-state continuity requirement before moving recovery to another ref;
- historical occurrence chronology plus applicable control-version chronology;
- current checker failure explicitly not treated as automatic proof of historical invalidity;
- current revision/target binding verification before trusting prior credit;
- source-owned validation when governed source files change;
- recovery stop conditions that forbid invented authority and scope escape.

## Exact next action

Perform a fresh **full Adversarial review of `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v5.md`** using Model Before Review and `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`.

Requirements for that pass:

1. refresh the purpose/authority/identity/state/invariant/failure model for Lean v5;
2. sweep the entire document;
3. do not stop at the first blocker;
4. collect all blocker/high findings in that bounded pass before reporting;
5. do not edit Lean v5 in the same pass.

After findings are reported:

1. run Model Before Change on the proposed correction set;
2. run Structural Optimization / survive-or-die on those proposed corrections;
3. apply only surviving corrections;
4. then repeat a full modeled Adversarial sweep.

## Important maintenance invariants

- The handoff may direct discovery of authority and identify missing authority; it may not manufacture missing authority.
- The recovery handoff must remain a navigation/recovery guide, not a second PRS.
- Recovery instructions, future PRS design, and handoff-maintenance workflow must stay separated.
- Before every semantic review: Model Before Review.
- Before every nontrivial correction: Model Before Change.
- Adversarial review should maximize credible defect discovery.
- Structural Optimization decides which proposed corrections deserve to survive.
- A full Adversarial sweep must continue through the whole declared model even after blocker findings, unless the target becomes uninterpretable.
- Do not rely on repository-controlled text for host/user authorization.
- Do not let current rules retroactively invalidate historical evidence without establishing applicability.
- Do not let code continuity imply governed review-state continuity.
- Do not continue ordinary feature implementation after the bounded recovery task is complete.

## Fresh-chat continuation prompt

Use:

> In `rpjgauthier-spec/project-review-system`, read `skills/project-review-system/reviews/handoff-maintenance/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action. Do not skip Model Before Review or the full Adversarial sweep.

## Update rule

Before handing off to a fresh chat, update this file if any of these change:

- current handoff filename/version;
- maintenance-guide method;
- Model-Before-Review method;
- stage-specific review model;
- current review stage;
- exact next action;
- newly durable supporting design records.

Do not leave this continuation manifest pointing at superseded files.
