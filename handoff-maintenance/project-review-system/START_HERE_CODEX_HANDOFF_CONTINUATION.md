# START HERE — Codex Handoff Maintenance Continuation

## Purpose

Use this file to continue the current Project Review System Codex-handoff maintenance work in a fresh ChatGPT conversation without relying on prior chat history.

Repository: `rpjgauthier-spec/project-review-system`

This directory maintains and reviews the Codex recovery handoff. It is not Project Review System production authority and is intentionally outside `skills/project-review-system/**` so routine handoff maintenance does not itself enter the PRS changed-file/revalidation surface.

## Current artifacts

- Recovery handoff: `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v8.md`
- Maintenance guide: `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`
- Mandatory pre-review method: `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- Adversarial stage model: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

Repository-side non-authoritative design references remain under `skills/project-review-system/reviews/` and must not be treated as production authority unless current PRS governance promotes them.

## Mandatory read order

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md` before any new Adversarial review.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v8.md`.
6. After a semantic sweep, ownership-test blocker/high candidates before proposing handoff corrections.
7. Before any nontrivial handoff-owned correction, perform Model Before Change.
8. Run Structural Optimization / survive-or-die before editing.

## Current status

Lean v8 is the current review target.

The latest correction deliberately **removed machinery** rather than adding more governance:

- bootstrap is now non-destructive factual discovery, not a handoff-assigned PRS `Diagnostic` mode;
- the handoff-created cross-ref PRS control-election/binding subsystem was removed;
- applicable PRS controls must come from existing repository authority/provenance, otherwise recovery stops on unresolved applicability;
- factual discovery is limited to inventory/provenance rather than authority/relevance judgment;
- PRS-governed mode/scope/depth/transition is separated from host/user action authorization;
- Model Before Review now contains a mandatory Ownership Test;
- the Adversarial model was reframed so modeled defects are candidates, not automatic handoff features;
- the Maintenance Guide now defines convergence and an anti-churn condition.

## Exact next action

Perform a fresh **full Adversarial review of Lean v8** using the reframed model.

Mandatory method:

1. Run Model Before Review for Lean v8.
2. Refresh the purpose/authority/identity/state/invariant/failure model.
3. Use the refreshed Adversarial Review Model.
4. Sweep the entire document; do not stop at the first blocker.
5. Collect the complete blocker/high candidate set.
6. Run the Ownership Test on every candidate.
7. Report separately:
   - handoff-owned candidates;
   - production-PRS-owned findings;
   - repository/governance-owned blockers;
   - discarded low-value/redundant candidates.
8. Do not edit Lean v8 in the same semantic pass.

After findings, only surviving **handoff-owned** correction proposals proceed to Model Before Change and survive-or-die.

## Convergence

Handoff maintenance converges when a complete modeled semantic review produces no blocker/high handoff correction that survives both Ownership Testing and Structural Optimization.

External PRS/repository blockers may remain without forcing new handoff machinery; report them at the owning layer.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
