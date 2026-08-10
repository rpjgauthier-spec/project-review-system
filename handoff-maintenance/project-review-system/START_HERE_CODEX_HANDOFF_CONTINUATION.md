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
4. Read the applicable strengthened stage model.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md` when the review targets Lean.
6. Derive the bounded target-specific coverage witness required by Model Before Review and the stage model.
7. Complete and close the declared semantic sweep before reporting.
8. Ownership-Test blocker/high candidates before proposing corrections.
9. Before any nontrivial owned correction, perform Model Before Change and Structural Optimization / survive-or-die.

## Current status

The maintenance method and all five stage maps have been strengthened with bounded target-derived coverage closure.

Fresh Lean v9 re-evaluation under those maps completed these separated stages on handoff blob `0d5a3b926d78c7512322b477ea1b7babfa51773a`:

- Adversarial: converged, zero blocker/high handoff-owned survivors.
- Interdependency: converged, zero blocker/high handoff-owned survivors.
- Normalization: converged, zero blocker/high handoff-owned survivors.
- Structural Optimization: converged, zero blocker/high handoff-owned survivors.

End-to-end had not yet begun.

A user-raised discoverability check then found that the local-first roadmap and living design notes were not deterministically reachable from Lean alone. Repository inspection established their current known navigation location on branch `review-local-first-refactor-roadmap`:

- `skills/project-review-system/reviews/local-first-refactor-roadmap.md`
- `skills/project-review-system/reviews/local-first-refactor-living-design-notes.md`

Issue #11 consumes the frozen Issue #10 execution contract but does not itself name those two files. The roadmap states that it is a reviewed/disposable design artifact; the living notes explicitly state that they are non-authoritative refinements and do not override the reviewed roadmap/current validated PRS.

Lean was therefore minimally corrected to add these two navigation pointers while explicitly requiring current repository location/applicability to be verified before use and preserving their non-authoritative relationship to repository/PRS authority.

Lean pointer-correction commit:

`5b6fa7839534508c6dca97e72e8350d37751b000`

Current Lean blob after correction:

`db4e5295b91b5566bbba108d11d0b46300074a55`

No semantic re-review was fused into the pointer-correction pass.

Because this correction changes Lean's navigation/authority surface after Adversarial, Interdependency, Normalization, and Structural Optimization had converged, those prior results require bounded backward-impact/delta revalidation before End-to-end begins.

## Exact next action

Perform a **delta Adversarial review only** of the roadmap/living-notes pointer correction on current Lean v9.

Delta scope:

- branch/path pointer staleness and identity binding;
- roadmap/living-notes authority characterization;
- whether navigation context can be mistaken for source-scope or PRS authority;
- whether the pointer could broaden recovery scope improperly;
- trust/chronology implications of reading artifacts from a non-current branch.

Mandatory boundary:

1. derive and close the bounded Adversarial delta inventory;
2. collect and Ownership-Test any blocker/high candidates;
3. do not edit Lean in the same semantic pass;
4. do not begin Interdependency in the same pass.

If Adversarial delta converges, continue with separate delta Interdependency, Normalization, and Structural Optimization passes as materially required. Only after the correction is revalidated through affected earlier lenses should full strengthened End-to-end validation begin.

Do not modify production PRS during this handoff re-evaluation. Production method evolution remains a separate later task.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
