# Codex Handoff Maintenance Guide

## Purpose

Use this guide when modifying the Codex recovery handoff for `rpjgauthier-spec/project-review-system`.

This guide governs **handoff maintenance only**. It is not Project Review System authority and is not part of the instructions Codex should follow while recovering the repository.

## Core rule

> The handoff may direct discovery of authority and recognize that current authority is insufficient; it must never manufacture the missing authority, succession rule, review credit, or migration mechanism.

Keep the recovery handoff single-purpose:

> Help Codex discover current repository authority, reproduce the current failure, determine the next valid governed action, and continue safely.

Do not turn the handoff into:

- a second reviewer;
- a future PRS design document;
- a handoff-editing workflow;
- a substitute for current repository authority.

## Mandatory pre-review checkpoint

Before every semantic review of the Codex recovery handoff:

1. read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`;
2. refresh the minimum purpose/authority/identity/state/invariant/failure model for the current handoff revision;
3. select and read the applicable stage-specific review model;
4. complete the entire declared modeled sweep before treating the pass as complete;
5. ownership-test blocker/high candidates before treating them as proposed handoff corrections.

Stage-specific models:

- Adversarial: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`
- Interdependency: `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`
- Normalization: `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`
- Structural Optimization: `CODEX_HANDOFF_STRUCTURAL_OPTIMIZATION_REVIEW_MODEL.md`
- End-to-end validation: `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`

This checkpoint is mandatory even when the immediate instruction merely says to perform another review.

## Mandatory model-before-change check

Before any nontrivial **handoff-owned** correction:

1. state the handoff's governing intent;
2. identify protected invariants affected by the finding;
3. choose the minimum useful representation of the change: authority map, dependency map, flow/state transition, constraint list, scenario matrix, or no extra representation for a genuinely local fix;
4. stress the proposed change against relevant normal, edge, failure, authority/self-certification, interruption/retry, and downstream cases;
5. identify the smallest coherent change surface;
6. check that the change does not add authority, make non-authoritative context mandatory for runtime recovery, expand into future PRS redesign, mix maintenance instructions into runtime recovery, or weaken user-work/history protections;
7. apply the coherent correction;
8. review the behavioral/model delta, not only the textual diff.

For a typo, wrong path, or similarly isolated mechanical fix, briefly record that no additional model is needed.

## Ownership boundary

Use the mandatory Ownership Test in `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

In particular:

- fix handoff-owned ambiguity/order/navigation defects in the handoff;
- reference rather than duplicate production-PRS behavior;
- report unresolved repository/governance authority rather than inventing it;
- discard theoretical/redundant mitigations whose machinery costs as much or more than the risk reduced.

Finding a missing relationship does not transfer ownership of that relationship to the handoff.

## Deferred canonical-method candidate

The maintenance workflow has produced a promising general review pattern informally described as **cull the herd**:

```text
broad modeled finding generation
    -> Ownership Test
    -> Structural Optimization / survive-or-die
    -> only surviving owned corrections proceed
```

This pattern may later deserve evaluation for canonical Project Review System use because it separates exhaustive defect discovery from correction ownership and aggressively suppresses redundant or mis-owned machinery.

For now it is **deferred**. Do not treat it as production PRS authority, do not modify production PRS merely to adopt it, and do not let evaluation of the candidate interrupt the current handoff-maintenance stage sequence. Revisit it only as a separate method-evolution task after the current handoff review work reaches its appropriate stopping point.

## Deferred stage-model completeness audit

The five maintenance stage models themselves require a later completeness review before this maintenance method is treated as exhausted or evaluated for broader reuse.

Use `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md` for that review.

This audit was added after a skeptical End-to-end re-hunt exposed a terminal-report contract defect that the original broad End-to-end coverage language had allowed a reviewer to miss. Its purpose is to test whether each stage merely names broad dimensions or actually forces enough bounded decomposition to support a claim that material subcases were exhausted.

Do **not** run this meta-review in the middle of an active stage correction loop. Run it after the current five-stage handoff review sequence reaches its appropriate stopping point and before claiming that the maintenance review method itself is complete enough for reuse or canonical-method evaluation.

If the audit finds a stage-model completeness gap, collect the complete five-stage audit first, Ownership-Test and structurally cull the method findings, then update only the surviving maintenance models. Re-run affected semantic stages afterward as required by the resulting model delta.

## Canonical supporting design references

Handoff-maintenance method artifacts:

- `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`
- `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`
- `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`
- `CODEX_HANDOFF_STRUCTURAL_OPTIMIZATION_REVIEW_MODEL.md`
- `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`
- `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md`

When available, consult the roadmap-side living design notes:

- `skills/project-review-system/reviews/adaptive-model-before-change-design-note.md`
- `skills/project-review-system/reviews/model-before-change-workflow-integration-design-note.md`
- `skills/project-review-system/reviews/review-method-evolution-design-note.md`

They are non-authoritative supporting context. Their unavailability must not prevent maintenance if this guide contains enough method to perform the check.

## Separation rule

The recovery handoff should contain only what Codex needs to recover the repository.

If a proposed addition mainly explains how the handoff should be edited, how future PRS should work, a speculative architecture, or a general review-method improvement, put it in maintenance/design material instead.

## Live-artifact hygiene

Keep only the current recovery handoff version in the live maintenance directory unless an older copy has a distinct current consumer that Git history cannot serve.

Git history is the archive for superseded handoff revisions. Do not retain obsolete canonical-looking Lean files merely for version history; stale live copies increase selection ambiguity without adding recovery capability.

The current continuation manifest must name exactly one live recovery handoff target.

## Convergence rule

Handoff maintenance is **not** an instruction to revise forever.

Maintenance converges when a complete modeled semantic review produces no blocker/high **handoff correction** that survives both:

1. the Ownership Test; and
2. Structural Optimization / survive-or-die.

A blocker/high owned by production PRS or unresolved repository/governance authority does not require another handoff feature. Reference or report it at the owning layer.

Do not continue revising solely to handle lower-value hypothetical cases when the proposed handoff machinery would introduce equal or greater complexity, ambiguity, authority surface, or failure risk.

A clean full review followed by an Ownership Test in which every candidate is delegated/reported/discarded is a valid convergence outcome even if external PRS/repository blockers remain.

## Acceptance test for handoff edits

Before accepting an edit, ask:

- Does this help Codex identify current authority or next action?
- Does this reduce ambiguity?
- Does it preserve user work and durable history?
- Does it avoid creating new authority?
- Is this behavior actually owned by the handoff?
- Could Codex safely ignore future design notes and still recover the current repository?
- Is the handoff still substantially a navigation/recovery guide?

If ownership is elsewhere, or the answer to the last two questions is no, the edit probably does not belong in the handoff.
