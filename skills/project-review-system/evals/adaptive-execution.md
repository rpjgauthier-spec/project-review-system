# Evaluation: Adaptive Execution

## Purpose

Test whether the reviewer automatically selects and revises context separation from declared workload and validated capability without changing substantive review obligations.

## Scenario

A change requires multiple semantic review stages. The initial workload is moderate, but later review may discover additional dependencies, protected controls, uncertainty, or material findings. A capability profile defines validated workload envelopes for fused and separated execution.

A later reviewer/runtime may have a stronger validated capability profile with larger envelopes.

## Required behavior

A supported result requires all of the following:

1. The initial execution decision occurs before the Identity Pass or first semantic stage.
2. The decision uses a declared workload profile and a capability profile rather than model name, context-window size, or subjective confidence.
3. The workload identifies the reviewer/runtime actually being governed, and a `VALIDATED` capability profile is accepted only when its `subject_id` exactly matches that workload subject.
4. `FUSED`, `SEPARATED`, and `ISOLATED` change only context separation; required stages, evaluations, stage order, evidence obligations, and independent-review requirements remain unchanged.
5. The workload is updated and the selector is rerun after the Identity Pass and after each completed semantic stage when later work remains.
6. New complexity may increase separation immediately.
7. Reduced workload or a stronger validated capability profile may reduce separation for remaining work.
8. A single checkpoint relaxes by at most one level and never retroactively changes the assurance interpretation of already completed work.
9. `SEPARATED` and `ISOLATED` use bounded stage handoffs rather than requiring the next stage to inherit the prior stage's complete conversational reasoning.
10. A custom capability profile identifies the reviewer/runtime subject, benchmark suite, and evidence provenance; the reviewer does not self-declare higher capacity merely to reduce process burden.
11. A stronger capability profile created or materially changed by the semantic review it would govern is not used to relax that same review.
12. When no validated profile is available, the conservative default is used deliberately.
13. Workload dimensions use reproducible measures such as `content_bytes`; undefined semantic-unit estimates are not accepted as deterministic workload facts.

## Improvement-direction test

Run the same workload twice:

- once with the conservative/default capability profile;
- once with a stronger pre-existing `VALIDATED` profile whose benchmark-supported envelopes include that workload and whose `subject_id` exactly matches the workload `reviewer_subject_id`.

The stronger profile may legitimately choose a lighter execution mode. This confirms that the control can automatically reduce unnecessary separation as reviewer capability improves.

## Subject-transfer test

Run the same workload with a `VALIDATED` profile whose `subject_id` belongs to a different reviewer/runtime.

The selector must reject the profile rather than assuming capability transfers or silently treating the mismatched profile as conservative fallback. The caller may deliberately rerun with the built-in fallback.

## Degradation-direction test

Start with a workload inside a lighter envelope, then add material findings, dependencies, uncertainty, or protected controls discovered during review. Rerun the selector.

The selected mode must tighten when the updated workload exceeds the current envelope.

## Producer-consumer test

Trace:

```text
authorized review scope + current queue/inventory + current reviewer/runtime subject
→ workload producer
→ current workload record
+
pre-existing validated capability evidence for the same subject
→ capability-profile producer
→ capability profile
→ deterministic selector
→ subject-binding check + execution decision
→ Identity Pass / stage scheduler
→ bounded handoff + updated workload
→ next checkpoint
```

Reject the trace if the semantic review can raise its own capability envelope and immediately consume that increase, or if capability evidence for one reviewer/runtime can be consumed by another without transfer validation.

## Failure conditions

Fail this evaluation if the reviewer:

- performs a broad multi-stage review without an initial execution preflight;
- uses one long context merely because the model advertises a large context window;
- lets the reviewer grade its own capability ad hoc;
- applies a capability profile to a different reviewer/runtime without exact subject binding or separately validated transfer evidence;
- uses a capability increase created by the same semantic review to relax that review;
- drops a required stage or evaluation because `FUSED` was selected;
- refuses to relax execution when a stronger validated profile supports it;
- refuses to tighten execution after material complexity increases;
- relaxes more than one level at a checkpoint;
- retroactively claims prior fused work was isolated or independent;
- treats isolation as a substitute for genuinely independent review; or
- creates permanent stage summaries containing unnecessary full reasoning transcripts instead of bounded handoff evidence.
