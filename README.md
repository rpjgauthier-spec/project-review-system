# Project Review System

A repository-review framework for adversarial, interdependency, normalization, structural optimization, and end-to-end validation of multi-document project systems.

The canonical Agent Skills-compatible package lives at:

```text
skills/project-review-system/
```

The package supports three review depths:

- focused review
- bounded revalidation after change
- full five-stage review

GitHub enforcement is provided by `.github/workflows/project-review-system-revalidation.yml`. The workflow checks changed-file impact coverage, runs the regression suite, and requires the generated revalidation queue to be current and clear.

## Install

See [`skills/project-review-system/INSTALL.md`](skills/project-review-system/INSTALL.md).

## Status

Version `0.1.8` completed same-agent staged revalidation and live GitHub Actions runtime validation in the source repository. The final source validation ran 27 regression tests successfully and produced a clear revalidation queue. Independent review, cross-project effectiveness testing, and measured false-positive/false-negative performance remain outstanding.

This repository is the standalone public distribution target. Source-project historical review records are intentionally not copied into the runtime package.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
