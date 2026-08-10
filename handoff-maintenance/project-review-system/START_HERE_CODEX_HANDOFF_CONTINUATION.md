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

Adversarial, Interdependency, Normalization, Structural Optimization, and End-to-end validation have converged on current Lean v9 under the current maintenance models.

A full Stage Model Completeness Audit was performed across all five stage models, Model Before Review, and their cross-stage boundaries. It found seven HIGH maintenance-method candidates centered on false exhaustiveness: broad instructions such as testing every material dimension, relationship, family, or element did not always require a bounded target-derived coverage witness before a pass could claim completion.

The complete seven-candidate batch has now been Ownership-Tested and subjected to Structural Optimization / survive-or-die as one set. No stage model was edited during that culling pass.

### Cull result

All seven candidates are maintenance-method-owned, but they do **not** justify seven independent mechanisms.

The smallest surviving correction architecture is:

1. **Shared coverage-closure invariant — SURVIVE INTACT.** Every semantic stage must derive the minimum useful finite/bounded target-specific coverage inventory before claiming a full sweep, then explicitly close every material inventory unit or justified material combination. A prose assertion that “all dimensions were considered” is not sufficient when a bounded witness can be derived.

2. **Adversarial combinatorial gap — MERGE into shared closure with a stage-specific specialization.** Adversarial must derive the material attack classes/combinations exposed by the target rather than checking dimensions only in isolation. No separate tracker or permanent matrix is required.

3. **Interdependency reachability/precondition gap — MERGE into shared closure with a stage-specific specialization.** Interdependency closure must test material producer-state variants against consumer reachability and downstream obligations. The existing node tuple remains; no second dependency model is needed.

4. **Normalization context-matrix gap — MERGE into shared closure with a stage-specific specialization.** Representation-family closure must include materially meaning-changing contexts such as current/historical and success/blocker/unknown when present. No glossary or permanent context taxonomy is justified.

5. **Structural Optimization rare-consumer/removal gap — MERGE into shared closure with a stage-specific specialization.** Removal/compression closure must test all target-derived material consumer/terminal classes, including blocker, interruption, re-entry, and reporting consumers when applicable. No separate removal checklist is justified.

6. **End-to-end journey-terminal cross-product gap — MERGE into shared closure with a stage-specific specialization.** End-to-end must close all materially reachable journey × terminal/interruption combinations. This extends the existing journey and terminal-contract model; it does not justify another workflow representation.

7. **Cross-stage ownership-gap risk — SURVIVE BUT COMPRESS.** After the target-specific failure/defect classes are derived, the maintenance method needs one compact cross-stage closure check that every material class has at least one explicit owning detection lens. Overlap is allowed; ownerless classes are not. This belongs at the shared method/guide layer, not duplicated in every stage model.

### What died

- five independent new completeness mechanisms;
- permanent per-stage trackers;
- a universal Cartesian-product requirement across every possible state/dimension combination;
- new taxonomies where only target-derived material classes are needed;
- duplicated closure machinery inside every map.

The cull therefore reduces seven findings to **two shared method requirements** plus minimal stage-specific definitions of closure:

```text
shared target-derived coverage witness + explicit closure
        ↓
stage-specific definition of what material units/combinations must close
        ↓
shared cross-stage owner check for uncovered defect classes
```

This is the surviving method-correction set.

## Exact next action

Apply the surviving method corrections in bounded correction passes, without modifying Lean in the same pass.

Recommended correction order:

1. strengthen `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md` with the shared target-derived coverage-witness/closure invariant and the compact cross-stage owner check;
2. minimally specialize each of the five stage models so its completion rule states what target-derived units/combinations must close under that shared invariant;
3. update the maintenance guide/manifest only as needed to register the strengthened method;
4. after method corrections are durable, re-run the affected semantic reviews on Lean under the strengthened maps.

Do not create permanent matrices or trackers merely to prove completeness. Derived bounded inventories may exist only during the review execution unless they have a separate durable consumer.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
