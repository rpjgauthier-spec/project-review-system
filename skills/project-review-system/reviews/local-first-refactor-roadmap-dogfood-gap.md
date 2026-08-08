# Dogfooding governance gap — follow-up requirement

## Purpose

Record the process defect discovered while using the current Project Review System to review the roadmap for improving the Project Review System.

## Observed failure

The review correctly applied the five semantic stages, but initially credited those stages without also establishing the current system's required deterministic review machinery: Adaptive Execution gates/completions, current change-impact/revalidation state, and durable pass-credit chronology.

The term **dogfooding** therefore needs a mechanically checkable meaning when the Project Review System is used to review itself or its own roadmap. Following only the semantic stages is not sufficient when the current operating mode claims governed Project Review System execution.

## Improvement requirement

Future implementation/design work must evaluate a **dogfood declaration integrity** control with these goals:

1. When a review is declared to be dogfooding the Project Review System, the system should determine which currently applicable Project Review System controls govern that review before the first semantic stage receives credit.
2. The user/reviewer should receive one clear preflight showing the required semantic stages, execution gates, change-impact/revalidation obligations, evidence/chronology requirements, and any explicitly inapplicable controls.
3. A stage must not receive governed dogfood credit if required mechanical preconditions were never opened. Missing preconditions must fail before or at attempted completion rather than being discovered only at final End-to-end validation.
4. The system must not retroactively fabricate gates, boundaries, completions, or chronology for already-performed work. Recovery must reopen the earliest affected stage and preserve the earlier work only as uncredited prior analysis.
5. The control should avoid circularity: the current validated system governs migration to its replacement until the replacement has itself been validly reviewed and accepted.
6. The implementation should distinguish **semantic-method-only use** from **governed dogfooding**, so a user can intentionally use only the five review lenses without accidentally claiming the stronger governed assurance.
7. This should be implemented with the lowest-burden reliable mechanism, preferably as preflight/state-engine enforcement rather than another permanent manual checklist.

## Intended consumer

Structural/implementation planning for the local-first refactor and later End-to-end validation of the replacement workflow engine.

## Status

Recorded for later implementation. This note does not retroactively credit the earlier ungated passes; the active review chain remains reopened at Adversarial.
