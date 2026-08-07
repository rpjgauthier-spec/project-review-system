# Project Review System

An Agent Skills-compatible workflow for reviewing repository-based projects through evidence-led identity discovery, adversarial, interdependency, normalization, structural optimization, and end-to-end validation.

The review methods themselves are semantic and can reason about broader bodies of work. Git manifests, object identity, changed-file enforcement, pull requests, and GitHub Actions remain repository-specific evidence and enforcement mechanisms.

## Review model

Pre-review when material: **Identity Pass**

1. Adversarial
2. Interdependency
3. Normalization
4. Structural Optimization
5. End-to-end validation

The Identity Pass is not a sixth stage. It discovers materially distinct purposes or lifecycles from evidence before the five-stage review so later stages do not accidentally conflate unrelated or only partially shared bodies of work. Bounded revalidation is a change-triggered lifecycle mechanism, not a sixth stage. Use the smallest review depth that answers the request: focused review, bounded revalidation, or full program.

## Package layout

```text
project-review-system/
├── SKILL.md                 # Canonical operating instructions
├── README.md                # Orientation
├── INSTALL.md               # Distribution and activation
├── CHANGELOG.md             # Release history
├── changes/                 # Change-impact records
├── config/                  # Canonical revalidation mapping
├── references/              # Shared model, identity pass, and stage modules
├── templates/               # Trackers, reports, impact and coverage records, workflow
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
4. For broad/full-program work, run the Identity Pass when identity boundaries could materially change interpretation.
5. Identify one review-state authority when a durable staged program is justified.
6. Record review changes under `changes/` and regenerate `reviews/revalidation-queue.md`.
7. Run the required stage work, evaluations, and deterministic tests.
8. Complete only when identity interpretation where applicable, tracker state, reports, changed-file coverage, queue state, traces, and bounded claims agree.

Focused reviews normally do not need permanent trackers or stage reports. Changes made during review still require a change-impact record. A supported `behavior-neutral` record does not reopen a review stage.

## Identity Pass

Use `references/identity-pass.md` to discover whether the reviewed scope contains multiple materially distinct identities that affect interpretation.

The pass is deliberately non-leading and medium-independent:

- collect evidence before assigning labels;
- do not use user speculation, container names, repository names, or a fixed taxonomy as a checklist;
- distinguish explicit identities from reviewer inference;
- allow shared artifacts and overlap;
- leave insufficiently supported material uncertain or unassigned;
- do not treat multiple identities as a defect by themselves;
- do not recommend storage or repository restructuring merely because multiple identities exist.

The output is context for the five review stages, not a new authority source or an additional stage.

For Git repositories, repository-specific evidence mechanisms may support the pass. In an exhaustive repository review, identity conclusions remain subject to the pinned-manifest and full-object semantic-coverage boundary. Other environments need evidence appropriate to their own claimed scope.

## Abstraction boundary

Structural Optimization now explicitly asks whether behavior is unnecessarily coupled to a platform, storage medium, implementation, domain, artifact type, or vendor.

The intended separation is:

```text
invariant semantic behavior
        ↓
environment-specific evidence and enforcement where actually required
```

Do not generalize merely because reuse is imaginable, and do not preserve platform coupling merely because it appeared in an initial requirement or feature name. Use `evals/abstraction-boundary.md` when this distinction is material.

## Exhaustive semantic coverage

When a review claims exhaustive repository coverage, inventory and semantic-processing coverage must be proven separately from the reviewer's conclusions.

Pin the target repository to a commit and build a manifest:

```bash
python skills/project-review-system/scripts/build_review_manifest.py \
  --repo /path/to/target-repository \
  --ref HEAD \
  --output review-manifest.json
```

The manifest includes every tracked tree entry reachable from the pinned commit, including directories, blobs, and gitlinks. Each entry records its Git object identity and a required semantic method such as code, structured data, document, image, archive, binary, repository structure, or gitlink analysis.

During review, maintain a coverage ledger based on `templates/review-coverage.json`. A complete exhaustive repository claim requires every manifest entry to have `semantic_status: COMPLETE` and full declared range coverage. There is no `EXCLUDED` or irrelevant-file shortcut for an exhaustive claim.

Validate the ledger with:

```bash
python skills/project-review-system/scripts/check_review_coverage.py \
  --manifest review-manifest.json \
  --coverage review-coverage.json
```

A passing coverage check proves that every inventoried object has matching identity, semantic method, and complete line/byte/object-range processing records. It does **not** prove comprehension, semantic correctness, domain correctness, or reviewer independence.

Semantic search, sampled reading, snippets, summaries, or repository-wide search results cannot substitute for the exhaustive manifest-and-coverage path when an exhaustive repository claim is made.

## Deterministic validation

```bash
python skills/project-review-system/scripts/update_revalidation_queue.py
python skills/project-review-system/scripts/update_revalidation_queue.py --check
python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'
```

For pull requests, GitHub Actions also invokes `scripts/check_change_impact_coverage.py` with the base and head SHAs.

These controls validate declared structures and mappings only. They do not prove semantic correctness, truthful classification, evidence accuracy, authorization validity, security, domain correctness, or comprehension.

## Enforcement boundary

The workflow reports `validate-revalidation-controls` for every pull request and runs substantive checks when Project Review System files are affected. Branch protection or a ruleset must require that check and restrict direct pushes if failures are intended to block merging. Repository settings do not travel with copied files and may permit privileged bypasses.

## Assurance limits

Version `0.1.11` corrects an abstraction-boundary defect in Version 0.1.10: semantic identity discovery is now medium-independent, while Git-specific exhaustive evidence and enforcement remain repository-specific. Structural Optimization also gains a reusable accidental-environment-coupling check and regression evaluation.

Version `0.1.10` introduced the evidence-led Identity Pass but framed the semantic capability too narrowly around Git repositories. The non-leading discovery controls remain valid; the abstraction boundary is corrected in Version 0.1.11.

Version `0.1.9` adds deterministic exhaustive repository-object inventory and full-range semantic-processing coverage controls. Bounded same-agent revalidation covered all five review stages, the exhaustive-object-inventory, full-range-coverage, premature-completion, reopening-chain, semantic-coverage-boundary, and structural-validator evaluations, and a live protected pull-request run in which changed-file coverage and all 37 regression tests passed before the intentionally unresolved queue gate.

Version `0.1.8` completed staged same-agent revalidation and live GitHub Actions runtime validation in its source repository. The standalone public bootstrap subsequently passed 28 regression tests, changed-file coverage, and a clear revalidation-queue check, while also exposing and correcting a `.github` path-normalization portability defect.

This standalone public repository does not constitute independent review. Independent review, unrelated-project effectiveness testing, host-specific testing, and measured false-positive/false-negative performance remain outstanding.

The package does not replace qualified domain expertise.

## License

Apache License 2.0. The standalone repository includes the complete license text at the repository root.