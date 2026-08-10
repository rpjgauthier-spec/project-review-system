# Codex Handoff Maintenance Guide

## Purpose

Use this guide when modifying the Codex recovery handoff for `rpjgauthier-spec/project-review-system`.

This guide governs **handoff maintenance only**. It is not Project Review System authority and is not part of the instructions Codex should follow while recovering the repository.

## Core rule

Additional invariant:

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
4. complete the entire declared modeled sweep before treating that review pass as complete.

For Adversarial review, the required stage-specific model is:

`CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`

This checkpoint is mandatory even when the immediate user instruction merely says to perform another review. The reviewer must not rely on being reminded.

## Mandatory model-before-change check

Before any nontrivial correction to the handoff:

1. State the handoff's governing intent.
2. Identify protected invariants affected by the finding.
3. Choose the minimum useful representation of the change:
   - authority map;
   - dependency map;
   - flow/state transition;
   - constraint list;
   - scenario matrix;
   - or no additional representation for a genuinely local fix.
4. Stress the proposed change against relevant:
   - normal cases;
   - edge cases;
   - failure cases;
   - authority/self-certification cases;
   - interruption/retry cases;
   - downstream dependency effects.
5. Identify the smallest coherent change surface.
6. Check that the change does not:
   - add a new source of authority;
   - make non-authoritative context mandatory for runtime recovery;
   - expand the Codex task into future PRS redesign;
   - mix handoff-maintenance instructions into the recovery instructions;
   - weaken user-work/history protections.
7. Apply the coherent correction.
8. Review the behavioral/model delta, not only the textual diff.

For a typo, wrong path, or similarly isolated mechanical fix, record briefly that no additional model is needed.

## Canonical supporting design references

Handoff-maintenance method artifacts:

- `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`


When available, consult the roadmap-side living design notes:

- `skills/project-review-system/reviews/adaptive-model-before-change-design-note.md`
- `skills/project-review-system/reviews/model-before-change-workflow-integration-design-note.md`
- `skills/project-review-system/reviews/review-method-evolution-design-note.md`

They are non-authoritative supporting context. Their unavailability must not prevent maintenance if this guide contains enough method to perform the check.

## Separation rule

The recovery handoff should contain only what Codex needs to recover the repository.

If a proposed addition mainly explains:

- how the handoff itself should be edited;
- how future PRS should work;
- a speculative architecture;
- a general review-method improvement;

put it in this maintenance guide or the roadmap-side design notes instead.

## Acceptance test for handoff edits

Before accepting an edit, ask:

- Does this help Codex identify current authority or next action?
- Does this reduce ambiguity?
- Does it preserve user work and durable history?
- Does it avoid creating new authority?
- Could Codex safely ignore future design notes and still recover the current repository?
- Is the handoff still substantially a navigation/recovery guide?

If the answer to the last two questions is no, the edit probably belongs elsewhere.
