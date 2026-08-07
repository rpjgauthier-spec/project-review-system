#!/usr/bin/env python3
"""Validate deterministic invariants in a Markdown review-stage tracker.

This checks only tracker structure and state consistency. It does not judge
review quality, evidence accuracy, scope completeness, authorization, security,
report contents, or domain correctness.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

OPEN = {"Ready", "In Review", "Reopened"}
PERMITTED_TERMINAL = {"Complete", "Conditional"}
BLOCKING_TERMINAL = {"Failed"}
KNOWN = OPEN | PERMITTED_TERMINAL | BLOCKING_TERMINAL | {"Pending"}
PROGRAM = {"Draft", "Active", "Complete", "Failed"}
MODES = {"Diagnostic", "Proposed corrective", "Authorized corrective"}
INDEPENDENCE = {"Independent", "Same-agent self-review", "Mixed"}
SUSPENSION_MARKER = "awaiting revalidation"
ROW = re.compile(
    r"^\|\s*(?P<number>\d+)\s*\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*(?P<date>[^|]+?)\s*\|\s*(?P<report>[^|]+?)\s*\|\s*(?P<residual>[^|]*?)\s*\|",
    re.MULTILINE,
)
FIELD = re.compile(r"^- \*\*(?P<name>[^*]+):\*\*\s*(?P<value>.+?)\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"\[[^\]]+\]|YYYY-MM-DD|list exact allowed actions", re.IGNORECASE)


def _blank(value: str) -> bool:
    return value.strip() in {"", "—", "-"}


def _unresolved(value: str) -> bool:
    return _blank(value) or bool(PLACEHOLDER.search(value))


def validate(text: str) -> list[str]:
    errors: list[str] = []
    rows = [match.groupdict() for match in ROW.finditer(text)]
    if not rows:
        return ["No stage rows were found."]

    fields = {
        m.group("name").strip().lower(): m.group("value").strip()
        for m in FIELD.finditer(text)
    }

    counts = Counter(row["number"] for row in rows)
    for number, count in counts.items():
        if count > 1:
            errors.append(f"Stage number {number} appears {count} times.")

    numbers = [int(row["number"]) for row in rows]
    if numbers != sorted(numbers):
        errors.append("Stage rows are not ordered by stage number.")
    if numbers and numbers != list(range(numbers[0], numbers[-1] + 1)):
        errors.append("Stage numbers are not contiguous.")

    for row in rows:
        status = row["status"].strip()
        if status not in KNOWN:
            errors.append(f"Stage {row['number']} has unknown status {status!r}.")
        if status in PERMITTED_TERMINAL | BLOCKING_TERMINAL:
            if _blank(row["date"]):
                errors.append(f"Terminal stage {row['number']} has no date.")
            if _blank(row["report"]):
                errors.append(f"Terminal stage {row['number']} has no report path.")

    required_boundary_fields = {
        "review mode",
        "authorized write actions",
        "program status",
        "current stage",
        "current status",
        "accessible scope",
        "material exclusions or inaccessible surfaces",
        "reviewer independence",
        "last updated",
    }
    missing = sorted(name for name in required_boundary_fields if name not in fields)
    if missing:
        errors.append("Missing review-boundary fields: " + ", ".join(missing))

    for name in sorted(required_boundary_fields & fields.keys()):
        if _unresolved(fields[name]):
            errors.append(f"Field {name!r} contains an unresolved placeholder or blank value.")

    program_status = fields.get("program status", "")
    if program_status and program_status not in PROGRAM:
        errors.append(f"Unknown Program status {program_status!r}.")

    review_mode = fields.get("review mode", "")
    if review_mode and review_mode not in MODES:
        errors.append(f"Unknown Review mode {review_mode!r}.")

    independence = fields.get("reviewer independence", "")
    if independence and independence not in INDEPENDENCE:
        errors.append(f"Unknown Reviewer independence value {independence!r}.")

    open_rows = [row for row in rows if row["status"].strip() in OPEN]
    reopened_rows = [row for row in rows if row["status"].strip() == "Reopened"]
    failed_rows = [row for row in rows if row["status"].strip() in BLOCKING_TERMINAL]
    nonpermitted = [row for row in rows if row["status"].strip() not in PERMITTED_TERMINAL]

    if program_status == "Complete":
        if nonpermitted:
            errors.append("Program is Complete but one or more stages lack a permitted terminal status.")
    elif program_status == "Active":
        if len(open_rows) != 1:
            errors.append(
                f"Expected exactly one open stage while Program status is Active; found {len(open_rows)}."
            )
        if failed_rows:
            errors.append("Program is Active but one or more stages are Failed.")
    elif program_status == "Failed":
        if len(failed_rows) != 1:
            errors.append(
                f"Expected exactly one Failed stage while Program status is Failed; found {len(failed_rows)}."
            )
        if open_rows:
            errors.append("Program is Failed but an open stage remains.")

    current_stage = fields.get("current stage", "")
    current_status = fields.get("current status", "")
    controlling_rows = open_rows if program_status == "Active" else failed_rows if program_status == "Failed" else []
    if len(controlling_rows) == 1:
        row = controlling_rows[0]
        number = row["number"]
        status = row["status"].strip()
        if not re.search(rf"\b{re.escape(number)}\b", current_stage):
            errors.append(f"Current stage field does not identify controlling stage {number}.")
        if current_status != status:
            errors.append(
                f"Current status {current_status!r} does not match controlling stage status {status!r}."
            )
    elif program_status in {"Complete", "Draft"}:
        if current_stage.lower() != "none":
            errors.append(f"{program_status} program must set Current stage to None.")
        if current_status.lower() != "none":
            errors.append(f"{program_status} program must set Current status to None.")

    if reopened_rows:
        if len(reopened_rows) != 1:
            errors.append(f"Expected at most one Reopened stage; found {len(reopened_rows)}.")
        else:
            reopened_number = int(reopened_rows[0]["number"])
            for row in rows:
                number = int(row["number"])
                status = row["status"].strip()
                residual = row["residual"].strip().lower()
                if number > reopened_number:
                    if status in OPEN:
                        errors.append(
                            f"Later stage {number} is open while stage {reopened_number} is Reopened."
                        )
                    if status in PERMITTED_TERMINAL and SUSPENSION_MARKER not in residual:
                        errors.append(
                            f"Later terminal stage {number} must record Awaiting revalidation while stage {reopened_number} is Reopened."
                        )

    if review_mode == "Diagnostic":
        actions = fields.get("authorized write actions", "")
        if actions.lower() != "none":
            errors.append("Diagnostic mode must set Authorized write actions to None.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tracker", type=Path)
    args = parser.parse_args()

    try:
        text = args.tracker.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(str(exc))

    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "Review tracker state is structurally valid. "
        "This does not validate report contents, semantic correctness, evidence, authorization, coverage, or domain claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
