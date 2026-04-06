#!/usr/bin/env python3
"""Report skills whose next_review date has passed or is missing."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS = ROOT / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check skill review dates and report stale entries.")
    parser.add_argument("--today", default=str(date.today()), help="Override the comparison date in YYYY-MM-DD format.")
    parser.add_argument(
        "--skills-dir",
        default=str(DEFAULT_SKILLS),
        help="Override the skills directory to inspect.",
    )
    args = parser.parse_args()

    today = date.fromisoformat(args.today)
    skills_dir = Path(args.skills_dir).resolve()
    stale = 0
    missing = 0

    for skill in sorted(skills_dir.rglob("SKILL.md")):
        text = skill.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^next_review:\s+(\d{4}-\d{2}-\d{2})$", text, flags=re.M)
        rel = skill.relative_to(skills_dir)
        if not match:
            missing += 1
            print(f"MISSING {rel}")
            continue
        review_date = date.fromisoformat(match.group(1))
        if review_date < today:
            stale += 1
            print(f"STALE {rel} next_review={review_date}")

    print(f"SUMMARY stale={stale} missing={missing}")
    return 1 if stale or missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
