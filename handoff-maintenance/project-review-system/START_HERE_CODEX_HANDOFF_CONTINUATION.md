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

The first full modeled Interdependency review found two handoff-owned HIGH dependency defects that survived Ownership Testing and Structural Optimization:

1. source-scope authority was consulted only after governed recovery scope had effectively been established;
2. the historical-validity distinction consumed the authority applicable at the disputed occurrence without identifying a producer for that historical authority.

Those two survivors were corrected minimally. A second full modeled Interdependency review then found one remaining handoff-owned HIGH dependency defect: Lean asked Codex to determine Slice-1 applicability from “current source authority” without first establishing which source-scope authority was current.

That survivor has now been applied minimally. Lean v9 now requires this chain:

```text
existing repository authority
    -> identify current source-scope authority
    -> determine whether frozen Slice 1 still applies
    -> finalize governed recovery scope
```

If Slice 1 remains controlling, Issue #11 and clarification/comment `5229287324` are read as controlling source material. No source-authority election, succession, migration, revalidation, or state machinery was added.

The historical-authority provenance correction remains in place: disputed historical authority is established from durable repository chronology/provenance under current governance, with a truthful limitation reported if it cannot be established.

The complete five-stage maintenance model set exists. The deferred `cull the herd` pattern remains a maintenance-method candidate only and is not production PRS authority.

## Exact next action

Perform another fresh **full modeled Interdependency review of corrected Lean v9** as a convergence hunt.

Mandatory method:

1. Run Model Before Review for the corrected Lean v9 and derive the current recovery dependency graph.
2. Read and use `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`.
3. Sweep the entire document; do not stop at the first broken edge.
4. Collect the complete blocker/high candidate set.
5. Ownership-Test every candidate.
6. Subject handoff-owned candidates to Structural Optimization / survive-or-die.
7. Report separately:
   - handoff-owned survivors;
   - production-PRS-owned findings;
   - repository/governance-owned blockers;
   - discarded low-value/redundant candidates.
8. Do not edit Lean v9 in the same semantic pass.

If no blocker/high handoff correction survives Ownership Testing and Structural Optimization, the Interdependency maintenance cycle has converged and the next stage is Normalization.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
