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

The corrected Lean v9 completed a full modeled Adversarial cycle with no surviving blocker/high handoff correction. A delta Adversarial review of the later Interdependency survivors also found no blocker/high handoff correction, so the Adversarial conclusion remains preserved.

The Interdependency cycle converged after three successive hunts. Its accepted corrections now provide these minimal recovery-specific edges:

```text
existing repository authority
    -> identify current source-scope authority
    -> determine whether frozen Slice 1 still applies
    -> finalize governed recovery scope
```

and:

```text
durable repository chronology/provenance
    -> establish authority applicable to disputed historical occurrence
    -> assess historical validity
    -> separately assess current-credit acceptability
```

The final source-scope producer correction was retroactively subjected to explicit Structural Optimization / survive-or-die and survived. No source-authority election, succession, migration, revalidation, or state machinery was added.

The first full modeled Normalization review found one handoff-owned HIGH candidate: `target` was overloaded between the current PRS review-state identity (`current revision/target`) and the heading describing the historical pass-boundary problem (`Recovery target`). After Ownership Testing and explicit Structural Optimization, only a one-line rename survived.

That correction has been applied: `## Recovery target` is now `## Historical recovery problem`. No glossary, new taxonomy, or other normalization machinery was added.

The complete five-stage maintenance model set exists. The deferred `cull the herd` pattern remains a maintenance-method candidate only and is not production PRS authority.

## Exact next action

Perform a fresh **full modeled Normalization review of corrected Lean v9** as a convergence hunt.

Mandatory method:

1. Run Model Before Review for corrected Lean v9 and derive the current concept/representation families.
2. Read and use `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`.
3. Sweep the entire document; do not stop at the first inconsistency.
4. Collect the complete blocker/high candidate set.
5. Ownership-Test every candidate.
6. Subject handoff-owned candidates to Structural Optimization / survive-or-die.
7. Report separately:
   - handoff-owned survivors;
   - production-PRS-owned findings;
   - repository/governance-owned blockers;
   - discarded cosmetic/redundant candidates.
8. Do not edit Lean v9 in the same semantic pass.

If no blocker/high handoff correction survives Ownership Testing and Structural Optimization, the Normalization maintenance cycle has converged. Before moving to Structural Optimization, perform any required delta review of the Normalization survivor(s) against earlier converged stages if the change materially affects those lenses.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
