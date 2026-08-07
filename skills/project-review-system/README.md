# Project Review System

An Agent Skills-compatible workflow for reviewing repository-based projects through adversarial, interdependency, normalization, structural optimization, and end-to-end validation.

## Review model

1. Adversarial
2. Interdependency
3. Normalization
4. Structural Optimization
5. End-to-end validation

Bounded revalidation is a change-triggered lifecycle mechanism, not a sixth stage. Use the smallest review depth that answers the request: focused review, bounded revalidation, or full program.

## Package layout

```text
project-review-system/
├── SKILL.md                 # Canonical operating instructions
├── README.md                # Orientation
├── INSTALL.md               # Distribution and activation
├── CHANGELOG.md             # Release history
├── changes/                 # Change-impact records
├── config/                  # Canonical revalidation mapping
├── references/              # Shared model and stage modules
├── templates/               # Trackers, reports, impact record, workflow
├── evals/                   # Evaluation scenarios
├── reviews/                 # Current state and historical evidence
├── scripts/                 # Deterministic controls
└── tests/                   # Regression suites
```

The repository-activated GitHub workflow lives outside the skill directory:

```text
.github/workflows/project-review-system-revalidation.yml
```

The distributable copy is bundled at:

```text
skills/project-review-system/templates/project-review-system-revalidation.yml
```

See `INSTALL.md` for review-only and enforced-GitHub installation profiles. Repository rules and branch protection must be configured separately in every destination repository.

## Use

1. Read `SKILL.md` and `references/shared-control-model.md`.
2. Select the review mode and smallest sufficient depth.
3. Define accessible scope, exclusions, and allowed actions.
4. Identify one review-state authority when a durable staged program is justified.
5. Record review changes under `changes/` and regenerate `reviews/revalidation-queue.md`.
6. Run the required stage work, evaluations, and deterministic tests.
7. Complete only when tracker state, reports, changed-file coverage, queue state, traces, and bounded claims agree.

Focused reviews normally do not need permanent trackers or stage reports. Changes made during review still require a change-impact record. A supported `behavior-neutral` record does not reopen a review stage.

## Deterministic validation

```bash
python skills/project-review-system/scripts/update_revalidation_queue.py
python skills/project-review-system/scripts/update_revalidation_queue.py --check
python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'
```

For pull requests, GitHub Actions also invokes `scripts/check_change_impact_coverage.py` with the base and head SHAs.

These controls validate declared structures and mappings only. They do not prove semantic correctness, truthful classification, evidence accuracy, authorization validity, security, domain correctness, or complete coverage.

## Enforcement boundary

The workflow reports `validate-revalidation-controls` for every pull request and runs substantive checks when Project Review System files are affected. Branch protection or a ruleset must require that check and restrict direct pushes if failures are intended to block merging. Repository settings do not travel with copied files and may permit privileged bypasses.

## Assurance limits

Version `0.1.8` completed staged same-agent revalidation and live GitHub Actions runtime validation in its source repository. The validated source state passed 27 regression tests, changed-file coverage, and a clear revalidation-queue check. Deliberate live failure-path tests also confirmed rejection of an unrecorded watched change, a deleted impact record, a stale new-record claim, and a stale generated queue.

This standalone public repository preserves that validated package layout but does not constitute independent review. Independent review, unrelated-project testing, host-specific testing, and measured false-positive/false-negative performance remain outstanding.

The package does not replace qualified domain expertise.

## License

Apache License 2.0. The standalone repository includes the complete license text at the repository root.
