# Changelog

## 0.1.8 — 2026-08-06

Changed-file and pull-request enforcement release.

### Added

- deterministic changed-file coverage checker
- regression tests for changed-file coverage
- GitHub Actions pull-request workflow
- mandatory impact record for the enforcement change itself

### Changed

- every watched pull-request file must be covered by an impact record changed in the same diff
- impact records must list themselves
- stale file claims are rejected for newly added impact records while existing records may retain historical file coverage during later result/status updates
- pull-request enforcement runs the full regression suite before the queue-clear gate
- branch protection is explicitly required to convert failed checks into merge blocking

### Final validation update — 2026-08-07

- Adversarial, Interdependency, Normalization, Structural Optimization, and End-to-end revalidation completed in the source repository
- live GitHub Actions validation passed changed-file coverage, 27 regression tests, and a current/clear generated queue
- deliberate failure-path runs confirmed rejection of an unrecorded watched change, a deleted impact record, a stale new-record claim, and a stale generated queue
- same-agent limitation remains; independent and cross-project validation remain outstanding

## 0.1.7 — 2026-08-06

Automatic revalidation queue release.

### Added

- structured JSON change-impact records
- canonical change-class-to-stage mapping
- generated revalidation queue and source hash
- queue-generator regression tests
- `--check` advancement gate

### Changed

- every review change requires an impact record
- mapped stage and evaluation requirements are generated rather than remembered manually
- stale or unresolved queues block advancement

### Revalidation status

- Release entered bounded revalidation immediately; no full-program completion claim was made

## 0.1.6 — 2026-08-06

Structural Optimization rename and reopening-control release.

### Added

- normative reopening algorithm
- backward-impact gate
- stage suspension and resumption rules
- expanded Structural Optimization guidance
- reopening regression scenarios

### Changed

- `Minimalist Review` became `Structural Optimization Review`
- the current module path became `references/structural-optimization-review.md`
- historical Minimalist reports retained their original terminology and paths
- the prior Version 0.1.5 completion claim was suspended pending bounded revalidation

## 0.1.5 — 2026-08-06

End-to-end validation release.

### Added

- stage-specific `references/end-to-end-validation.md`
- representative normal, failure, withdrawal, recurrence, focused-review, behavioral-change, unauthorized-action, and incomplete-access traces
- tracker-validator regression suite with three valid and five invalid lifecycle cases
- explicit structural-validation expectations and reopening rules

### Changed

- full-program completion now requires selected end-to-end traces and applicable deterministic checks
- package README documents the validation module and regression-test command
- final bounded claim includes successful selected end-to-end paths

### Validation status

- Same-agent end-to-end validation completed for the visible package scope
- All eight validator regression cases produced expected results
- No prior stage required reopening
- Independent, cross-project, host-specific, and measured-accuracy validation remain outstanding

## 0.1.4 — 2026-08-06

Bounded minimalist correction release.

### Added

- explicit Focused review, Bounded revalidation, and Full program depth selection
- minimalist tests for excessive review depth and unnecessary permanent artifacts
- focused-review completion rule

### Changed

- the full staged sequence is no longer implied for every narrow request
- permanent trackers and reports are required only when a durable staged record has a distinct consumer
- required inputs are limited to those material to the selected review depth
- evaluation scenarios are selected by changed behavior rather than run indiscriminately
- authoritative facts should be referenced instead of copied into multiple records
- minimalist dispositions now point to the shared control model as the vocabulary authority
- README maturity and package layout updated through Version 0.1.4

### Review status

- Bounded minimalist self-review of Version 0.1.3 completed
- Material over-processing and duplicate-authority defects corrected
- Same-agent review; end-to-end and independent validation remain outstanding

## 0.1.3 — 2026-08-06

Bounded normalization correction release.

### Added

- canonical definitions for review modes, program statuses, stage statuses, verdicts, dispositions, evidence labels, and independence labels in the shared control model
- explicit distinction between open, permitted-terminal, and blocking-terminal stage states

### Changed

- `Failed` no longer counts as an open stage
- validator now requires Program status `Failed` to own exactly one failed stage with no open stage
- templates, skill instructions, and validator semantics use the canonical vocabulary
- minimalist module references the shared control model for canonical dispositions

### Review status

- Bounded normalization self-review of Version 0.1.2 completed
- Material vocabulary and state-semantic drift corrected
- Same-agent review; cross-project vocabulary portability remains untested

## 0.1.2 — 2026-08-06

Bounded interdependency correction release.

### Added

- one package-level self-review tracker as the current review-state authority
- explicit review-program producer-consumer control path
- report-tracker disagreement and unresolved-template evaluation scenarios
- validator checks for resolved boundary fields, current-stage/current-status agreement, contiguous stages, review mode, program status, independence value, and Diagnostic write restrictions

### Changed

- every stage now loads the shared control model before its stage-specific module
- stage reports are explicitly historical evidence and cannot advance the program without tracker propagation
- tracker template now requires concrete values instead of unresolved option strings
- completion requires agreement between the state authority and stage reports
- interdependency module now covers review modes, trust boundaries, validator contracts, and review-state propagation

### Review status

- Bounded interdependency self-review of Version 0.1.1 completed
- Material state-authority and validator-contract defects corrected
- Same-agent review; independent and cross-project validation remain outstanding

## 0.1.1 — 2026-08-06

Adversarial hardening release.

### Added

- explicit Diagnostic, Proposed corrective, and Authorized corrective modes
- untrusted repository-content and instruction-injection boundary
- accessible-scope, exclusion, and incomplete-access requirements
- reviewer-independence disclosure and independent-review requirement for stronger assurance claims
- sensitive-data, host-permission, concurrency, stale-write, partial-failure, and irreversible-side-effect checks
- eight additional adversarial evaluation scenarios
- review-boundary fields in tracker and report templates
- stronger deterministic tracker validation and explicit semantic-validation disclaimer

### Changed

- bounded completion claim now includes accessible scope, available evidence, and reviewer independence
- adversarial module now covers the reviewer, host tools, and repository content as threat surfaces
- protected controls now include repository writes, secrets, host permissions, and external side effects
- README maturity and public-release guidance now distinguish same-agent review from independent validation

### Review status

- Full adversarial self-review completed against Version 0.1.0
- Material defects corrected
- This was a same-agent corrective review, not independent public-release validation

## 0.1.0 — 2026-08-06

Initial extracted prototype.

### Added

- Agent Skills-compatible `SKILL.md`
- adversarial review module
- interdependency review module
- normalization review module
- minimalist review module
- shared authority, evidence, protection, and escalation model
- stage tracker and report templates
- twelve scenario-based evaluation cases
- deterministic Markdown tracker-state validator
- installation, maturity, and licensing guidance

### Known limitations

- Derived primarily from one repository and not yet cross-project validated
- No automated semantic dependency extraction
- No measured false-positive or false-negative rate
- No multi-agent independence protocol
- No standalone release packaging or full root license file yet
