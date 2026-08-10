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

A full Stage Model Completeness Audit has now been performed across all five stage models, Model Before Review, and their cross-stage boundaries. No stage model was edited during that audit.

The audit found a shared false-exhaustiveness mechanism: several models require the reviewer to test "every material" dimension, relationship, family, or element, but do not always require a bounded target-derived inventory that proves what the complete set is before declaring it exhausted. This permits a competent reviewer to satisfy the prose checklist while unknowingly omitting a non-obvious class.

The complete blocker/high maintenance-method candidate set is:

1. **Shared coverage-closure gap — HIGH.** Model Before Review and stage completion rules lack a general bounded coverage witness. A full review can be asserted without first enumerating the target-derived units/classes that constitute the declared sweep and proving each was closed. Candidate strengthening: require the minimum useful target-derived coverage inventory/matrix appropriate to the stage, with explicit closure before a full-pass claim.

2. **Adversarial combinatorial gap — HIGH.** Authority, authorization, identity, chronology, staleness, failure, trust, preservation, and scope are listed as dimensions, but the model does not force materially relevant combinations such as present/absent/ambiguous/conflicting authority crossed with action/evidence/terminal use. Candidate strengthening: derive finite attack classes from the target and require coverage of material cross-dimension combinations rather than isolated dimension checkoffs.

3. **Interdependency reachability/precondition gap — HIGH.** The node tuple is strong, but the model does not explicitly require each consumer to be tested for reachability under producer present, missing, stale, conflicting, or changed states, nor require obligation preconditions to close for terminal/output consumers. Candidate strengthening: for each material node/edge, test producer-state variants against consumer reachability and downstream obligations.

4. **Normalization context-matrix gap — HIGH.** The model derives representation families and all occurrences, but does not force comparison across materially distinct chronology/path/terminal contexts. A harmless synonym or term can become behaviorally different only on one failure path. Candidate strengthening: compare each material representation family across occurrences plus the contexts that can change meaning, especially current/historical and success/blocker/unknown states.

5. **Structural Optimization rare-consumer/removal gap — HIGH.** Removal safety asks whether capability is lost, but does not explicitly require testing deletion/compression against success, blocker, interruption, re-entry, and reporting consumers. A rule can appear redundant on the happy path while being the only protection on a rare terminal path. Candidate strengthening: test each material removal/compression candidate against all target-derived consumer/terminal classes before verdict.

6. **End-to-end journey-terminal cross-product gap — HIGH.** Terminal-contract completeness is now strong, but the model still permits journey families and terminal classes to be enumerated separately without explicitly proving all materially reachable journey × terminal combinations and interruption points were traced. Candidate strengthening: require a bounded reachability matrix crossing applicable journey families with materially distinct terminal/interruption classes.

7. **Cross-stage ownership-gap risk — HIGH.** A defect can hide between stages when each assumes another stage owns the class. Candidate strengthening: after stage-specific inventories are derived, require a compact cross-stage coverage check that every material defect/failure class exposed by Model Before Review has at least one explicit owning detection lens; overlap is acceptable, ownerless classes are not.

All seven candidates are maintenance-method-owned. They do not imply production PRS changes and do not justify Lean edits by themselves.

The common root candidate is the shared coverage-closure gap; several stage-specific candidates may compress into that general mechanism plus small stage-specific decompositions. They must now be Ownership-Tested and subjected to Structural Optimization / survive-or-die before any map is strengthened.

## Exact next action

Perform **Ownership Test + Structural Optimization / survive-or-die on the complete seven-candidate Stage Model Completeness Audit set**.

Mandatory method:

1. Treat the seven candidates as one collected batch; do not edit any model yet.
2. Test whether the shared coverage-closure candidate can subsume any stage-specific candidate without losing a distinct failure class.
3. For each candidate determine:
   - distinct requirement/invariant;
   - concrete review consumer;
   - maintenance-method ownership;
   - failure reduction;
   - mergeability with the shared closure mechanism;
   - added execution/maintenance burden;
   - removal safety.
4. Classify each as SURVIVE INTACT, SURVIVE BUT COMPRESS, MERGE, DELEGATE, DELETE, or REPORT EXTERNAL GAP.
5. Preserve only the smallest correction set that makes omissions mechanically harder rather than merely making the scrolls longer.
6. Do not edit stage models in the same culling pass.

After the cull, apply surviving method corrections in later bounded correction passes, then re-run affected review scopes on Lean as required.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
