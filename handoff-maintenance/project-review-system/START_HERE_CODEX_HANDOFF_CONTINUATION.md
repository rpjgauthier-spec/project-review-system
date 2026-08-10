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

The five-stage Lean review sequence previously converged under the pre-audit maps. A later Stage Model Completeness Audit found a false-exhaustiveness weakness in the maintenance method: broad instructions to test every material dimension, relationship, family, or element did not always require a bounded target-derived coverage witness proving what had actually been exhausted.

The seven HIGH audit candidates were culled into one shared coverage-closure invariant, minimal stage-specific closure definitions, and one compact cross-stage detection-owner check.

### Shared method strengthening

`CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md` now requires:

- a minimum finite/bounded target-derived coverage inventory before a full review claim;
- only materially justified combinations rather than universal Cartesian products;
- explicit closure or justified exclusion of every active inventory unit/material combination;
- newly exposed material classes to be added to the active inventory;
- a compact review-execution coverage witness rather than permanent tracking machinery;
- a cross-stage check that every material defect/failure class has at least one explicit owning detection lens.

Shared-method commit:

`8b00d5ef7b7c1190c029bd754e54d4ad2660c1b8`

### Strengthened stage maps now durable

All five maps have now been minimally specialized under the shared closure invariant:

- **Adversarial** — derives and closes materially relevant attack classes/cross-dimension combinations rather than isolated dimension checkoffs only. Commit: `55481e006b8ff4b8de1da2195c7cc813329f1c24`.
- **Interdependency** — closes target-derived producer-state variants against consumer reachability, prerequisites, downstream obligations, and fallback behavior. Commit: `d27656cbad6389944be0301fc90bf2ba3cdc8553`.
- **Normalization** — closes each material representation family across occurrences and materially meaning-changing chronology/state/terminal contexts. Commit: `701847c555a154974b26722b89d0e3b6082d2cfa`.
- **Structural Optimization** — closes deletion/compression decisions against all target-derived material consumers and terminal/re-entry contexts, not only the happy path. Commit: `03fdbb0a0cbc9f570654dc7bb59f7145bd0aacc9`.
- **End-to-end** — closes all materially reachable journey × terminal/interruption combinations in addition to terminal-contract completeness. Commit: `fbd3cab25b131122d63f435a1149b55facef7e46`.

No Lean edit and no semantic Lean review occurred while strengthening these maps.

## Exact next action

Begin fresh Lean v9 re-evaluation under the strengthened maps in separated semantic passes.

Start with a fresh **full modeled Adversarial review** using the strengthened Model Before Review and strengthened Adversarial map.

Mandatory boundary:

1. derive the bounded target-specific Adversarial coverage witness;
2. complete and close the full Adversarial sweep;
3. collect the complete blocker/high candidate set;
4. Ownership-Test every candidate;
5. subject handoff-owned candidates to Structural Optimization / survive-or-die;
6. report the complete result;
7. **do not edit Lean in the same semantic pass**;
8. **do not begin Interdependency in the same pass**.

After any surviving correction is separately applied and Adversarial converges, continue through Interdependency, Normalization, Structural Optimization, and End-to-end as separate execution boundaries, including backward-impact/delta reviews when a later correction can invalidate an earlier converged lens.

Do not modify production PRS during this handoff re-evaluation. Production method evolution remains a separate later task.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
