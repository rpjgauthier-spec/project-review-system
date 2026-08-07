# Installation and Packaging

The Project Review System has two installation layers:

1. **Skill package** — `skills/project-review-system/`
2. **Repository enforcement** — `.github/workflows/project-review-system-revalidation.yml` plus repository rules

The skill package can be used without GitHub Actions. GitHub enforcement is optional, but it is required when pull requests must be blocked automatically for missing or unresolved revalidation work.

## Installation profiles

### Review-only profile

Copy the complete directory:

```text
skills/project-review-system/
```

This includes the review instructions, stage modules, templates, mapping, scripts, tests, and bundled workflow template. It supports manual and local deterministic review workflows.

The contents of `reviews/` and `changes/` in this source repository include self-review evidence and active development state. Downstream projects should retain the directories but may start them with only the files needed for their own review program. Historical source-repository reports are not runtime dependencies.

### Enforced GitHub profile

Copy the complete skill directory, then copy:

```text
skills/project-review-system/templates/project-review-system-revalidation.yml
```

to:

```text
.github/workflows/project-review-system-revalidation.yml
```

The active workflow and bundled template must remain byte-for-byte identical. The packaging regression test checks this in the source repository.

Then configure the repository so the workflow is enforceable:

1. Enable GitHub Actions.
2. Open a pull request that causes `validate-revalidation-controls` to run.
3. Protect the target branch or create a ruleset.
4. Require pull requests before merging.
5. Require the `validate-revalidation-controls` status check.
6. Restrict direct pushes and force pushes.
7. Limit bypass permissions to explicitly approved roles.

Repository rules do not travel automatically when the package is copied, cloned into a new repository, or forked. Each destination repository must configure its own enforcement settings.

## Required versus development artifacts

### Runtime and review behavior

Retain:

- `SKILL.md`
- `references/`
- `config/revalidation-map.json`
- `templates/`
- `scripts/`
- `evals/`

### Deterministic verification

Retain when local or CI validation is expected:

- `tests/`

### Project state and evidence

Create or retain as needed by the destination project:

- `changes/`
- `reviews/revalidation-queue.md`
- a current tracker under `reviews/`
- stage and revalidation reports under `reviews/`

Historical reports from this source repository document development and self-review. They do not control downstream state and need not be distributed as part of a clean reusable installation.

## Validation

Run:

```bash
python skills/project-review-system/scripts/update_revalidation_queue.py
python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'
```

For an enforced GitHub installation, also open a pull request and confirm that the `validate-revalidation-controls` job runs. A local test pass does not prove that repository rules are configured or that GitHub Actions will block merging.
