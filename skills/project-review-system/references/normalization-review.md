# Normalization Review

## Mission

Make equivalent concepts use equivalent representation, terminology, granularity, and treatment while preserving differences justified by risk, authority, consumer needs, or lifecycle state.

Load `shared-control-model.md` first. Its review modes, program statuses, stage statuses, verdicts, dispositions, evidence labels, and independence labels are canonical for this package.

Normalization is not forced uniformity. It must not erase a meaningful distinction discovered by adversarial or interdependency review.

## Questions

1. Do equivalent statuses use the same meaning and transition rules?
2. Are program status, stage status, report verdict, finding disposition, and project authorization kept distinct?
3. Are similar records held at comparable levels of detail?
4. Are evidence labels, dates, IDs, headings, and completion criteria consistent where their functions are equivalent?
5. Are synonymous terms creating ambiguity or duplicate categories?
6. Are unlike concepts sharing one term or status?
7. Is one object over-specified or under-specified relative to comparable objects without a justified reason?
8. Do templates distinguish required, conditional, optional, and historical fields?
9. Are differences explained by authority, risk, consumer, lifecycle, review mode, or independence needs?
10. Do code constants, templates, reports, examples, and prose use the same canonical vocabulary?

## Finding classes

- inconsistent terminology
- status-semantic drift
- program-stage-verdict conflation
- disposition-status conflation
- unjustified granularity difference
- equivalent records using incompatible structures
- duplicate category names
- one term covering unlike concepts
- inconsistent evidence treatment
- inconsistent completion criteria
- template-code vocabulary mismatch
- superficial uniformity that would erase a legitimate distinction

## Dispositions

- `Normalize` when equivalent elements should align.
- `Retain with justification` when a difference is legitimate.
- `Escalate` when normalization would alter authority, authorization, protected controls, or a dependency contract.

## Correction order

Prefer:

1. identify the canonical vocabulary owner
2. define the shared concept once
3. select the clearest existing representation
4. update equivalent instances and deterministic consumers
5. preserve explicit exceptions with reasons
6. repair direct consumers and mappings
7. perform bounded interdependency and adversarial revalidation when behavior changes

## Validation

Test that:

- equivalent cases now produce equivalent interpretation
- program, stage, verdict, disposition, authorization, and independence concepts remain distinct
- legitimate exceptions remain distinguishable
- no status transition or authorization meaning changed silently
- code constants and templates accept the same values
- no direct consumer was broken
- normalization did not add a universal template where a small shared vocabulary would suffice

A stage is `Complete` when material unjustified inconsistency in scope is corrected and legitimate differences are recorded rather than flattened.