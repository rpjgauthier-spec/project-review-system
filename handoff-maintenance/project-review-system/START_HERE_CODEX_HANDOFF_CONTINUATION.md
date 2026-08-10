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

Adversarial, Interdependency, Normalization, and Structural Optimization have converged on current Lean v9, including required backward-impact delta checks.

The first End-to-end pass initially appeared to converge, but a skeptical re-hunt exposed a terminal-reporting defect: blocked journeys can terminate before an authoritative review state is established while the report contract asked for that state. The candidate survived Ownership Testing and Structural Optimization, and Lean v9 was minimally corrected to permit reporting which governing repository/ref or authoritative review state could not be established.

That miss revealed a methodological blind spot: the End-to-end model traced journeys to terminal states but did not deterministically test whether each terminal state's output/report obligations were satisfiable from facts guaranteed to exist on that path.

The End-to-end model has therefore been strengthened with **terminal-contract completeness**. Every terminal class must now identify guaranteed facts, facts that may remain unknown/not applicable, report obligations, their preconditions, and whether the next consumer can distinguish unknown/not-established/not-applicable from omission or fabrication.

A fresh End-to-end re-run under that strengthened model found a broader remaining HIGH candidate: the report contract still lists other facts that may legitimately not exist on an early blocked path, including failure/current-disposition, governed action taken, validation performed, and commits. The local authority-field correction therefore may be insufficient; a general truthful terminal-reporting rule may be the smaller and more complete representation.

No additional Lean correction has been applied for this broader candidate yet.

## Exact next action

Perform **Ownership Test + Structural Optimization / survive-or-die** on the broader End-to-end terminal-reporting candidate only.

Candidate to test:

> The Expected recovery report should generally require each applicable material item to be reported truthfully, explicitly allowing `not established` / `not applicable` when a valid terminal path can end before that fact exists, rather than solving the problem field-by-field.

If it survives:

1. perform Model Before Change;
2. replace the local reporting workaround with the smallest general terminal-report rule that covers all report fields without adding a schema or new state machinery;
3. commit only that correction;
4. run a fresh full End-to-end validation under the strengthened model in a separate semantic pass.

Do not perform another Lean edit before this candidate is explicitly weighed.

## Fresh-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, or exact next action changes.
