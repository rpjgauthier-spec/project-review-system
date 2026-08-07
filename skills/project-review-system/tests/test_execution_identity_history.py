#!/usr/bin/env python3
"""Regression tests for execution identity uniqueness across review history."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = SKILL_ROOT / "scripts" / "check_execution_identity_history.py"

spec = importlib.util.spec_from_file_location("check_execution_identity_history", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def snapshot(revision: int, stage: str, pass_id: str, gate_sha: str, unit_id: str, boundary_id: str):
    return {
        "review_revision": revision,
        "results": {stage: "supported"},
        "execution_gates": {stage: {"gate_sha256": gate_sha}},
        "execution_completions": {
            stage: {
                "gate_sha256": gate_sha,
                "passes": [
                    {
                        "pass_id": pass_id,
                        "status": "complete",
                        "execution_unit_id": unit_id,
                        "boundary": {"kind": "declared-execution-unit", "id": boundary_id},
                    }
                ],
            }
        },
    }


def subdivided_snapshot(revision: int):
    gate_sha = f"gate-r{revision}"
    return {
        "review_revision": revision,
        "results": {"Adversarial": "supported"},
        "execution_gates": {"Adversarial": {"gate_sha256": gate_sha}},
        "execution_completions": {
            "Adversarial": {
                "gate_sha256": gate_sha,
                "passes": [
                    {
                        "pass_id": "authorization",
                        "status": "complete",
                        "execution_unit_id": f"unit-r{revision}-a",
                        "boundary": {"kind": "declared-execution-unit", "id": f"boundary-r{revision}-a"},
                    },
                    {
                        "pass_id": "trust-boundary",
                        "status": "complete",
                        "execution_unit_id": f"unit-r{revision}-b",
                        "boundary": {"kind": "isolated-context", "id": f"boundary-r{revision}-b"},
                    },
                ],
            }
        },
    }


class ExecutionIdentityHistoryTests(unittest.TestCase):
    def test_distinct_redo_identity_passes(self):
        snapshots = [
            ("c1", snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-r7", "boundary-r7")),
            ("c2", snapshot(8, "Adversarial", "stage-main", "gate-r8", "unit-r8", "boundary-r8")),
        ]
        checker.validate_identity_history_snapshots("current", snapshots)

    def test_redo_cannot_reuse_execution_unit_id(self):
        snapshots = [
            ("c1", snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-shared", "boundary-r7")),
            ("c2", snapshot(8, "Adversarial", "stage-main", "gate-r8", "unit-shared", "boundary-r8")),
        ]
        with self.assertRaisesRegex(ValueError, "reuses execution_unit_id"):
            checker.validate_identity_history_snapshots("current", snapshots)

    def test_redo_cannot_reuse_boundary_identity(self):
        snapshots = [
            ("c1", snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-r7", "boundary-shared")),
            ("c2", snapshot(8, "Adversarial", "stage-main", "gate-r8", "unit-r8", "boundary-shared")),
        ]
        with self.assertRaisesRegex(ValueError, "reuses execution boundary"):
            checker.validate_identity_history_snapshots("current", snapshots)

    def test_same_occurrence_can_persist_across_later_commits(self):
        value = snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-r7", "boundary-r7")
        checker.validate_identity_history_snapshots("current", [("c1", value), ("c2", value)])

    def test_subdivided_passes_each_have_distinct_occurrences(self):
        checker.validate_identity_history_snapshots("current", [("c1", subdivided_snapshot(7))])

    def test_subdivided_redo_cannot_reuse_prior_subpass_identity(self):
        first = subdivided_snapshot(7)
        second = subdivided_snapshot(8)
        second["execution_completions"]["Adversarial"]["passes"][1]["execution_unit_id"] = "unit-r7-b"
        with self.assertRaisesRegex(ValueError, "reuses execution_unit_id"):
            checker.validate_identity_history_snapshots("current", [("c1", first), ("c2", second)])

    def test_pr_history_includes_existing_base_snapshot(self):
        base_value = snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-r7", "boundary-r7")
        head_value = snapshot(8, "Adversarial", "stage-main", "gate-r8", "unit-r8", "boundary-r8")

        def fake_snapshot(record_id, ref):
            if ref == "base-sha":
                return base_value
            if ref == "commit-r8":
                return head_value
            return None

        with patch.object(checker, "snapshot_at_ref", side_effect=fake_snapshot), patch.object(
            checker.subprocess,
            "run",
            return_value=SimpleNamespace(stdout="commit-r8\n"),
        ):
            values = checker.load_pr_history("current", "base-sha", "head-sha")

        self.assertEqual([item[0] for item in values], ["base-sha", "commit-r8"])
        checker.validate_identity_history_snapshots("current", values)

    def test_pr_history_base_snapshot_blocks_cross_pr_reuse(self):
        base_value = snapshot(7, "Adversarial", "stage-main", "gate-r7", "unit-shared", "boundary-r7")
        head_value = snapshot(8, "Adversarial", "stage-main", "gate-r8", "unit-shared", "boundary-r8")

        def fake_snapshot(record_id, ref):
            if ref == "base-sha":
                return base_value
            if ref == "commit-r8":
                return head_value
            return None

        with patch.object(checker, "snapshot_at_ref", side_effect=fake_snapshot), patch.object(
            checker.subprocess,
            "run",
            return_value=SimpleNamespace(stdout="commit-r8\n"),
        ):
            values = checker.load_pr_history("current", "base-sha", "head-sha")

        with self.assertRaisesRegex(ValueError, "reuses execution_unit_id"):
            checker.validate_identity_history_snapshots("current", values)


if __name__ == "__main__":
    unittest.main()
