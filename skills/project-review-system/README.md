# Project Review System

An Agent Skills-compatible workflow for reviewing repository-based projects through separated-by-default adaptive execution, evidence-led identity discovery, adversarial, interdependency, normalization, structural optimization, and end-to-end validation.

The review methods themselves are semantic and can reason about broader bodies of work. Adaptive Execution controls context separation. Git manifests, object identity, changed-file enforcement, pull requests, and GitHub Actions remain repository-specific evidence and enforcement mechanisms.

## Review model

Preflight before semantic review: **Adaptive Execution**

Pre-review when material: **Identity Pass**

1. Adversarial
2. Interdependency
3. Normalization
4. Structural Optimization
5. End-to-end validation

Adaptive Execution and the Identity Pass are not additional review stages. Bounded revalidation remains a change-triggered lifecycle mechanism. Use the smallest review depth that answers the request.

## Package layout

```text
project-review-system/
├── SKILL.md
├── README.md
├── INSTALL.md
├── CHANGELOG.md
├── changes/
├── config/
├── references/
├── templates/
├── evals/
├── reviews/
├── scripts/
└── tests/
```

The repository-activated GitHub workflow lives at `.github/workflows/project-review-system-revalidation.yml`. A distributable copy lives under `skills/project-review-system/templates/`. Repository rules and branch protection must be configured separately in every destination repository.

## Use

1. Read `SKILL.md` and `references/shared-control-model.md`.
2. Select review mode, scope, authorization, and smallest sufficient depth.
3. Before the Identity Pass or first semantic stage, create and validate an Adaptive Execution gate.
4. Default each semantic stage to `SEPARATED` execution.
5. Before each stage, assess whether one bounded pass is suitable. If not, declare bounded subpasses; mark any subpass that still requires a fresh context as `isolation_required`.
6. Run the deterministic selector. It converts the assessment into the required execution plan: ordinary passes remain `SEPARATED`; isolation-required subpasses become `ISOLATED`.
7. `FUSED` is permitted only by exact pre-existing externally `VALIDATED` capability permission for the same reviewer/runtime, activity group, and workload class.
8. Execute every planned pass and record execution completion.
9. Record a passing stage result only when its current artifact-bound gate and completion evidence match.
10. Regenerate the revalidation queue and run all required stages, evaluations, and deterministic tests.

## Adaptive Execution

The normal path is deliberately simple:

```text
stage requested
    ↓
SEPARATED by default
    ↓
one bounded pass suitable?
    ├─ yes → one SEPARATED pass
    └─ no  → bounded subpasses
                 ↓
           subpass needs fresh context?
                 ├─ no → SEPARATED
                 └─ yes → ISOLATED
```

FUSED is an evidence-backed optimization, not the default. The built-in capability profile grants no FUSED permissions.

The stage-size decision may use semantic judgment. The deterministic layer does not attempt to replace that judgment with arbitrary numeric workload scores. Instead it enforces the consequences of the recorded assessment.

A gate binds the reviewer/runtime, activity, review revision, target artifact state, workload class, semantic assessment, capability profile, deterministic execution plan, and hashes over the inputs and decision.

A passing governed stage result additionally requires an execution completion record. The completion must reference the current gate hash and target state and contain every planned pass, in order, with the exact required context mode and `status: complete`.

For repository revalidation, `update_revalidation_queue.py` rejects passing results with absent, stale, or mismatched gate/completion evidence. Artifact-state binding independently invalidates stale gates after governed files change.

These controls prove plan consistency and completion, not semantic correctness. They do not prove that the stage-size assessment was wise, that the reviewer actually had an independent mind, or that review findings are correct.

## Identity Pass

Use `references/identity-pass.md` to discover whether the reviewed scope contains multiple materially distinct identities that affect interpretation. Collect evidence before assigning labels, distinguish explicit from inferred identities, allow overlap and uncertainty, and do not treat multiple identities as a defect by themselves.

The output is context for the five review stages, not a new authority source or an additional stage.

## Abstraction boundary

Structural Optimization asks whether behavior is unnecessarily coupled to a platform, storage medium, implementation, domain, artifact type, or vendor.

```text
invariant semantic behavior
        ↓
environment-specific evidence and enforcement where actually required
```

Do not generalize merely because reuse is imaginable, and do not preserve platform coupling merely because it appeared in an initial implementation.

## Exhaustive semantic coverage

When a review claims exhaustive repository coverage, inventory and semantic-processing coverage must be proven separately from the reviewer's conclusions.

Pin the target repository and build a manifest:

```bash
python skills/project-review-system/scripts/build_review_manifest.py \
  --repo /path/to/target-repository \
  --ref HEAD \
  --output review-manifest.json
```

Maintain a coverage ledger using `templates/review-coverage.json` and validate it with:

```bash
python skills/project-review-system/scripts/check_review_coverage.py \
  --manifest review-manifest.json \
  --coverage review-coverage.json
```

A passing coverage check proves inventory identity and declared full-range processing records. It does not prove comprehension, semantic correctness, domain correctness, or reviewer independence.

## Deterministic validation

```bash
python skills/project-review-system/scripts/select_execution_policy.py \
  --workload review-workload.json \
  --gate \
  --output execution-gate.json

python skills/project-review-system/scripts/check_execution_gate.py \
  --gate execution-gate.json \
  --activity Adversarial \
  --review-revision 1 \
  --completion execution-completion.json

python skills/project-review-system/scripts/update_revalidation_queue.py
python skills/project-review-system/scripts/update_revalidation_queue.py --check
python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'
```

For pull requests, GitHub Actions also invokes `scripts/check_change_impact_coverage.py` with the base and head SHAs.

## Enforcement boundary

The workflow reports `validate-revalidation-controls` for every pull request and runs substantive checks when Project Review System files are affected. Branch protection or a ruleset must require that check and restrict direct pushes if failures are intended to block merging.

Repository enforcement can reject acceptance of a stage result that violates its recorded execution plan. It cannot literally prevent a reviewer from thinking about a stage in the wrong context before recording evidence.

## Assurance limits

Version `0.1.12` adds Adaptive Execution. Its current design is intentionally asymmetric:

- `SEPARATED` is the default;
- stage subdivision is triggered by bounded semantic assessment;
- `ISOLATED` is required only for subpasses declared too broad for ordinary separated execution;
- `FUSED` requires exact pre-existing external validation.

Same-agent isolated execution is not independent review. Independent review, unrelated-project effectiveness testing, host-specific testing, benchmark calibration, and measured false-positive/false-negative performance remain outstanding.

## License

Apache License 2.0. The standalone repository includes the complete license text at the repository root.
