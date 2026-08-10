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

Adversarial, Interdependency, Normalization, Structural Optimization, and End-to-end validation have converged on current Lean v9 under the pre-audit maintenance maps.

A full Stage Model Completeness Audit found seven HIGH maintenance-method candidates centered on false exhaustiveness. The seven-candidate batch was Ownership-Tested and culled into two shared requirements plus minimal stage-specific closure definitions:

```text
shared target-derived coverage witness + explicit closure
        ↓
stage-specific definition of what material units/combinations must close
        ↓
shared cross-stage owner check for uncovered defect classes
```

The first bounded correction pass has now been applied to `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

### Shared method strengthening now durable

Model Before Review now requires every semantic stage to:

1. derive the minimum useful finite/bounded target-specific coverage inventory before review;
2. include only materially justified combinations rather than universal Cartesian products;
3. close every active inventory unit/material combination or explicitly exclude it as non-material;
4. add newly exposed material classes to the active inventory rather than silently treating the initial inventory as exhaustive;
5. retain a compact coverage witness only for the review execution unless another durable consumer exists;
6. avoid claiming a full sweep from prose assertion alone when a bounded witness can be produced.

It also now contains the compressed cross-stage detection-owner check: when the multi-stage sequence is treated as complete, every material defect/failure class exposed by Model Before Review must have at least one explicit owning detection lens. Overlap is allowed; ownerless material classes are maintenance-method gaps.

Shared-method commit:

`8b00d5ef7b7c1190c029bd754e54d4ad2660c1b8`

No Lean edit and no new semantic Lean review occurred in that correction pass.

## Exact next action

Apply the second bounded method-correction pass: **minimally specialize the five stage models under the shared coverage-closure invariant**.

Required specializations:

1. **Adversarial** — closure must derive and exhaust materially relevant attack classes/combinations exposed by the target; isolated dimension checkoffs are insufficient when a material combination changes the failure mode.
2. **Interdependency** — closure must test material producer-state variants (present/missing/stale/conflicting/changed as applicable) against consumer reachability and downstream obligations.
3. **Normalization** — closure must compare each material representation family across occurrences plus meaning-changing contexts exposed by the target, especially chronology and success/blocker/unknown contexts when material.
4. **Structural Optimization** — closure for deletion/compression/merge/delegation candidates must test all target-derived material consumer/terminal classes, including blocker/interruption/re-entry/report consumers when applicable.
5. **End-to-end** — closure must trace all materially reachable journey × terminal/interruption combinations, building on the existing terminal-contract completeness rule.

Constraints:

- modify only the five maintenance stage-model files plus the continuation/guide bookkeeping needed to register the correction;
- do not edit Lean v9 in the same pass;
- do not create permanent matrices, trackers, or new stage taxonomies;
- do not run the strengthened semantic reviews on Lean in the same correction pass.

After all five maps are durably strengthened, update the maintenance guide/manifest if needed and begin fresh Lean re-evaluation under the strengthened maps in separate semantic passes.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
