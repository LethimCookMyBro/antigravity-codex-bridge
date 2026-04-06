#!/usr/bin/env python3
"""Validate skill metadata, shared references, and basic production requirements."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS = ROOT / "skills"
REQUIRED_META = [
    "skill",
    "version",
    "source",
    "last_updated",
    "reviewed_by",
    "next_review",
    "load_priority",
    "depends_on",
    "os_support",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    meta: dict[str, str] = {}
    for line in parts[0].splitlines()[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            meta[key.strip()] = value.strip()
    return meta


def check_references(skill_path: Path, text: str) -> list[str]:
    issues: list[str] = []
    for match in re.finditer(r"\((\.\./[^)#]+)(#[^)]+)?\)", text):
        rel_target = match.group(1)
        anchor = match.group(2)
        target = (skill_path.parent / rel_target).resolve()
        if not target.exists():
            issues.append(f"missing reference target: {rel_target}")
            continue
        if anchor:
            anchor_name = anchor[1:]
            target_text = target.read_text(encoding="utf-8", errors="replace")
            if f"## {anchor_name}" not in target_text and f"# {anchor_name}" not in target_text:
                issues.append(f"missing anchor {anchor} in {rel_target}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repo-local skill metadata and references.")
    parser.add_argument("--strict", action="store_true", help="Return nonzero when line-count targets are not met.")
    parser.add_argument(
        "--skills-dir",
        default=str(DEFAULT_SKILLS),
        help="Override the skills directory to validate.",
    )
    args = parser.parse_args()

    failures = 0
    line_warnings = 0
    skills_dir = Path(args.skills_dir).resolve()
    skills = sorted(skills_dir.rglob("SKILL.md"))

    for skill in skills:
        rel = skill.relative_to(skills_dir)
        text = skill.read_text(encoding="utf-8", errors="replace")
        meta = parse_frontmatter(text)

        missing = [field for field in REQUIRED_META if field not in meta]
        if missing:
            failures += 1
            print(f"FAIL {rel}: missing metadata {', '.join(missing)}")

        if not re.search(r"^version:\s+\d+\.\d+\.\d+$", text, flags=re.M):
            failures += 1
            print(f"FAIL {rel}: invalid semver")

        if not re.search(r"^last_updated:\s+\d{4}-\d{2}-\d{2}$", text, flags=re.M):
            failures += 1
            print(f"FAIL {rel}: invalid last_updated")

        if not re.search(r"^next_review:\s+\d{4}-\d{2}-\d{2}$", text, flags=re.M):
            failures += 1
            print(f"FAIL {rel}: invalid next_review")

        folder = skill.parent.name
        if meta.get("skill") != folder:
            failures += 1
            print(f"FAIL {rel}: skill name mismatch ({meta.get('skill')} != {folder})")

        if "## WHEN TO USE THIS SKILL" not in text and "## WHEN TO USE" not in text:
            failures += 1
            print(f"FAIL {rel}: missing WHEN TO USE section")

        if text.count("```bash") < 1:
            print(f"WARN {rel}: missing bash example block")

        refs = check_references(skill, text)
        for item in refs:
            failures += 1
            print(f"FAIL {rel}: {item}")

        line_count = text.count("\n") + 1
        if line_count < 400:
            line_warnings += 1
            print(f"WARN {rel}: {line_count} lines (<400)")

    total = len(skills)
    print(f"SUMMARY total_skills={total} failures={failures} line_warnings={line_warnings}")
    if failures:
        return 1
    if args.strict and line_warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
