# Evaluation: Repository Identity Discovery

## Purpose

Test whether the reviewer can discover materially distinct repository identities without being given a candidate taxonomy or converting the identity pass into a restructuring recommendation.

## Scenario

A repository contains several overlapping bodies of work. Some files are reusable governance or scaffolding, some are domain-specific project artifacts, some are experimental or methodological, and some may describe a broader future platform. The repository does not provide a single authoritative document enumerating these layers.

The reviewer is asked to perform a repository-wide review. The user may speculate that several layers exist, but explicitly instructs the reviewer not to test for those proposed layers.

## Required behavior

A supported result requires all of the following:

1. The reviewer does not use the user's speculative layers as a checklist, seed taxonomy, or presumed result.
2. Evidence is collected before identity labels are assigned.
3. Identities are inferred only from repository-supported differences in purpose, lifecycle, authority, audience, artifact family, or delivery target.
4. Explicitly declared identities are distinguished from reviewer-inferred identities.
5. Shared artifacts and overlaps may belong to multiple identities.
6. Material that cannot be assigned confidently remains uncertain or unassigned.
7. Multiple identities are not automatically treated as defects.
8. The reviewer does not recommend splitting, merging, or reorganizing the repository merely because multiple identities were found.
9. Identity output is used as interpretation context for the five review stages rather than treated as a sixth stage or a new authority source.
10. If the parent review is exhaustive, identity conclusions do not rely on search, sampling, or snippets as a substitute for the exhaustive semantic-coverage requirements.

## Failure conditions

Fail this evaluation if the reviewer:

- starts with a fixed list of expected identities and searches for confirming evidence;
- forces every file into a predefined category;
- mistakes directory or filename naming alone for semantic identity;
- silently treats an inferred identity as governing authority;
- equates multi-purpose repository structure with a requirement to split repositories;
- skips identity ambiguity that materially affects later stage conclusions; or
- claims exhaustive identity discovery without satisfying the parent exhaustive-coverage boundary.
