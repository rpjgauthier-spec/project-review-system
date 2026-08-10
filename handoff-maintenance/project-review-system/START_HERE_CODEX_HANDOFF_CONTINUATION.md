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

## Mandatory read order for future handoff maintenance

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

**Lean v9 is converged and ready for use as the Codex recovery handoff.**

The maintenance method and all five stage maps were strengthened with bounded target-derived coverage closure. Lean v9 was then re-evaluated through separated semantic stages.

Initial strengthened-stage results:

- Adversarial: converged, zero blocker/high handoff-owned survivors.
- Interdependency: converged, zero blocker/high handoff-owned survivors.
- Normalization: converged, zero blocker/high handoff-owned survivors.
- Structural Optimization: converged, zero blocker/high handoff-owned survivors.

A later discoverability check found that the local-first roadmap and living design notes were not deterministically reachable from Lean alone. Repository inspection established their current known navigation location on branch `review-local-first-refactor-roadmap`:

- `skills/project-review-system/reviews/local-first-refactor-roadmap.md`
- `skills/project-review-system/reviews/local-first-refactor-living-design-notes.md`

Lean was minimally corrected to add those navigation pointers while requiring current location/applicability to be verified and preserving their non-authoritative relationship to repository/PRS authority.

Lean pointer-correction commit:

`5b6fa7839534508c6dca97e72e8350d37751b000`

Current Lean blob:

`db4e5295b91b5566bbba108d11d0b46300074a55`

The correction was then revalidated through the affected earlier lenses as separate execution boundaries:

- Delta Adversarial: converged, zero blocker/high handoff-owned survivors.
- Delta Interdependency: converged, zero blocker/high handoff-owned survivors.
- Delta Normalization: converged, zero blocker/high handoff-owned survivors.
- Delta Structural Optimization: converged, zero blocker/high handoff-owned survivors; the navigation block survived intact.

Full strengthened End-to-end validation then traced all materially reachable recovery journeys, interruption/re-entry classes, terminal contracts, and journey × terminal combinations, including the roadmap/living-notes discovery path.

End-to-end result:

- zero blockers;
- zero HIGH handoff-owned survivors;
- reachable journey × terminal/interruption inventory closed;
- terminal-report contracts closed;
- no Lean correction required.

Therefore the current Lean v9 handoff has converged under all five strengthened stage maps.

## Exact next action

**Deploy the handoff in a fresh Codex recovery run.**

Give Codex the current Lean handoff as its recovery/navigation task and let it recover the actual current repository/PRS state. Do not preselect the implementation action beyond what Lean and current repository authority permit.

Codex should:

1. read `handoff-maintenance/project-review-system/CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md`;
2. recover repository identity, applicable repository authority, current PRS controls/state, and source-scope authority from durable repository evidence;
3. use the roadmap/living-design-note pointers only as applicable upstream design context, never as replacement authority;
4. continue only the governed controller-core recovery permitted by current PRS state and host/user authorization;
5. stop at the next valid governed state, required fresh semantic execution boundary, or real blocker;
6. report only facts actually established on the reached path.

Do not perform additional handoff semantic review unless the handoff itself is changed or execution exposes a new handoff-owned defect.

Do not modify production PRS merely because maintenance methodology suggests an improvement; production method evolution remains a separate task.

## Codex launch prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md` and execute that recovery handoff against the repository's actual current state. Follow current repository and Project Review System authority, continue only the bounded governed recovery, and stop exactly where the handoff requires.

## Fresh maintenance-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, convergence state, or exact next action changes.
