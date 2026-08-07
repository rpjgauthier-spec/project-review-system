#!/usr/bin/env python3
"""Regression tests for validate_review_state.py."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_review_state.py"
SPEC = importlib.util.spec_from_file_location("validate_review_state", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate = MODULE.validate


def tracker(
    *,
    program: str,
    current_stage: str,
    current_status: str,
    rows: str,
    mode: str = "Authorized corrective",
    actions: str = "Modify review package",
) -> str:
    return f"""# Tracker

- **Review mode:** {mode}
- **Authorized write actions:** {actions}
- **Program status:** {program}
- **Current stage:** {current_stage}
- **Current status:** {current_status}
- **Accessible scope:** Review package
- **Material exclusions or inaccessible surfaces:** None
- **Reviewer independence:** Same-agent self-review
- **Last updated:** 2026-08-06

| Stage | Review | Status | Date | Report | Residual condition |
|---:|---|---|---|---|---|
{rows}
"""


class ValidatorRegressionTests(unittest.TestCase):
    def assert_valid(self, text: str) -> None:
        self.assertEqual(validate(text), [])

    def assert_invalid(self, text: str, expected: str) -> None:
        errors = validate(text)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_active(self) -> None:
        self.assert_valid(
            tracker(
                program="Active",
                current_stage="2 — Interdependency",
                current_status="In Review",
                rows="""| 1 | Adversarial | Complete | 2026-08-06 | a.md | — |
| 2 | Interdependency | In Review | — | b.md | — |
| 3 | Normalization | Pending | — | c.md | — |""",
            )
        )

    def test_valid_complete(self) -> None:
        self.assert_valid(
            tracker(
                program="Complete",
                current_stage="None",
                current_status="None",
                rows="""| 1 | Adversarial | Complete | 2026-08-06 | a.md | — |
| 2 | Interdependency | Conditional | 2026-08-06 | b.md | External access |""",
            )
        )

    def test_valid_failed(self) -> None:
        self.assert_valid(
            tracker(
                program="Failed",
                current_stage="2 — Interdependency",
                current_status="Failed",
                rows="""| 1 | Adversarial | Complete | 2026-08-06 | a.md | — |
| 2 | Interdependency | Failed | 2026-08-06 | b.md | Blocking defect |""",
            )
        )

    def test_valid_reopened_with_suspended_later_stages(self) -> None:
        self.assert_valid(
            tracker(
                program="Active",
                current_stage="1 — Adversarial",
                current_status="Reopened",
                rows="""| 1 | Adversarial | Reopened | — | a2.md | Revalidating authorization boundary |
| 2 | Interdependency | Complete | 2026-08-06 | b.md | Awaiting revalidation after stage 1 |
| 3 | Normalization | Complete | 2026-08-06 | c.md | Awaiting revalidation after stage 1 |""",
            )
        )

    def test_reopened_requires_suspension_marker(self) -> None:
        self.assert_invalid(
            tracker(
                program="Active",
                current_stage="1 — Adversarial",
                current_status="Reopened",
                rows="""| 1 | Adversarial | Reopened | — | a2.md | Revalidating authorization boundary |
| 2 | Interdependency | Complete | 2026-08-06 | b.md | Prior result retained |""",
            ),
            "must record Awaiting revalidation",
        )

    def test_reopened_blocks_later_open_stage(self) -> None:
        self.assert_invalid(
            tracker(
                program="Active",
                current_stage="1 — Adversarial",
                current_status="Reopened",
                rows="""| 1 | Adversarial | Reopened | — | a2.md | Revalidating authorization boundary |
| 2 | Interdependency | Ready | — | b.md | Awaiting revalidation |""",
            ),
            "Expected exactly one open stage",
        )

    def test_diagnostic_requires_no_writes(self) -> None:
        self.assert_invalid(
            tracker(
                program="Active",
                current_stage="1 — Adversarial",
                current_status="Ready",
                rows="| 1 | Adversarial | Ready | — | a.md | — |",
                mode="Diagnostic",
                actions="Commit changes",
            ),
            "Diagnostic mode must set Authorized write actions to None",
        )

    def test_complete_rejects_pending_stage(self) -> None:
        self.assert_invalid(
            tracker(
                program="Complete",
                current_stage="None",
                current_status="None",
                rows="""| 1 | Adversarial | Complete | 2026-08-06 | a.md | — |
| 2 | Interdependency | Pending | — | b.md | — |""",
            ),
            "Program is Complete but one or more stages lack a permitted terminal status",
        )

    def test_current_status_must_match_stage(self) -> None:
        self.assert_invalid(
            tracker(
                program="Active",
                current_stage="1 — Adversarial",
                current_status="Ready",
                rows="| 1 | Adversarial | In Review | — | a.md | — |",
            ),
            "does not match controlling stage status",
        )

    def test_placeholder_rejected(self) -> None:
        text = tracker(
            program="Active",
            current_stage="1 — Adversarial",
            current_status="Ready",
            rows="| 1 | Adversarial | Ready | — | a.md | — |",
        ).replace("Review package", "[bounded scope]")
        self.assert_invalid(text, "unresolved placeholder")

    def test_noncontiguous_stages_rejected(self) -> None:
        self.assert_invalid(
            tracker(
                program="Active",
                current_stage="3 — Normalization",
                current_status="Ready",
                rows="""| 1 | Adversarial | Complete | 2026-08-06 | a.md | — |
| 3 | Normalization | Ready | — | c.md | — |""",
            ),
            "Stage numbers are not contiguous",
        )


if __name__ == "__main__":
    unittest.main()
