#!/usr/bin/env python3
"""Validate Agent Skills in this repo.

Checks the SKILL.md contract (frontmatter, name/directory agreement, description
length and person), that referenced files actually exist, and that a skill body
has not grown so large it should push detail into references/.

No third-party dependencies: a tiny frontmatter reader stands in for PyYAML so
`make check` works on a clean machine.

Usage:
    python3 scripts/validate_skills.py [--skills-dir skills] [--quiet]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"(?:\.\./)*(?:(?:references|assets|scripts)/[\w./-]*|[a-z0-9-]+/SKILL\.md)")
SHARED_RE = re.compile(r"`(shared/[\w./-]+)`|\((shared/[\w./-]+\.md)\)")
PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|XXX|lorem ipsum)\b", re.IGNORECASE)
SECOND_PERSON_RE = re.compile(r"\byou\b|\byour\b", re.IGNORECASE)

MAX_DESCRIPTION = 1024
MIN_DESCRIPTION = 40
MAX_BODY_LINES = 200
MIN_BODY_CHARS = 100


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def split_frontmatter(text: str) -> tuple[dict[str, str], str, str | None]:
    """Return (frontmatter dict, body, error). Handles top-level scalars only."""
    if not text.startswith("---"):
        return {}, text, "file does not start with a '---' frontmatter block"
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, "frontmatter block is not closed with '---'"

    raw = text[3:end].strip("\n")
    body = text[end + 4 :]

    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():  # nested value, e.g. under `metadata:`
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data, body, None


def validate_skill(skill_dir: Path, repo_root: Path) -> Result:
    res = Result()
    skill_md = skill_dir / "SKILL.md"
    label = skill_dir.name

    if not skill_md.is_file():
        res.errors.append(f"{label}: missing SKILL.md")
        return res

    text = skill_md.read_text(encoding="utf-8")
    meta, body, fm_error = split_frontmatter(text)
    if fm_error:
        res.errors.append(f"{label}: {fm_error}")
        return res

    name = meta.get("name", "")
    description = meta.get("description", "")

    # --- name -------------------------------------------------------------
    if not name:
        res.errors.append(f"{label}: frontmatter is missing 'name'")
    else:
        if name != label:
            res.errors.append(f"{label}: name '{name}' does not match directory '{label}'")
        if not NAME_RE.match(name):
            res.errors.append(f"{label}: name '{name}' must be lowercase-hyphenated")
        if len(name) > 64:
            res.errors.append(f"{label}: name is {len(name)} chars (max 64)")

    # --- description ------------------------------------------------------
    if not description:
        res.errors.append(f"{label}: frontmatter is missing 'description'")
    else:
        if len(description) > MAX_DESCRIPTION:
            res.errors.append(
                f"{label}: description is {len(description)} chars (max {MAX_DESCRIPTION})"
            )
        if len(description) < MIN_DESCRIPTION:
            res.errors.append(
                f"{label}: description is {len(description)} chars — too short to route on"
            )
        if SECOND_PERSON_RE.search(description):
            res.warnings.append(
                f"{label}: description uses second person — write it in third person"
            )
        if not re.search(r"\buse (it |this )?when\b", description, re.IGNORECASE):
            res.warnings.append(
                f"{label}: description has no 'Use when ...' trigger clause — routing will suffer"
            )

    if not meta.get("license"):
        res.warnings.append(f"{label}: no 'license' in frontmatter")

    # --- body -------------------------------------------------------------
    if len(body.strip()) < MIN_BODY_CHARS:
        res.errors.append(
            f"{label}: body is nearly empty ({len(body.strip())} chars, min {MIN_BODY_CHARS})"
        )

    line_count = len(body.splitlines())
    if line_count > MAX_BODY_LINES:
        res.warnings.append(
            f"{label}: SKILL.md body is {line_count} lines (> {MAX_BODY_LINES}) — "
            "move detail into references/"
        )

    for match in PLACEHOLDER_RE.finditer(text):
        line_no = text[: match.start()].count("\n") + 1
        res.warnings.append(f"{label}: placeholder '{match.group(0)}' at line {line_no}")

    # --- referenced files exist ------------------------------------------
    for ref in sorted(set(REF_RE.findall(body))):
        ref = ref.rstrip(".,;:)").strip()
        if not ref or ref.startswith("http"):
            continue
        if not (skill_dir / ref).exists():
            res.errors.append(f"{label}: references missing file '{ref}'")

    for match in SHARED_RE.finditer(body):
        ref = (match.group(1) or match.group(2) or "").rstrip(".,;:)")
        if ref and not (repo_root / ref).exists():
            res.errors.append(f"{label}: references missing shared file '{ref}'")

    return res


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills in this repo.")
    parser.add_argument("--skills-dir", default="skills", help="directory of skill folders")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    skills_dir = (repo_root / args.skills_dir).resolve()

    if not skills_dir.is_dir():
        print(f"✗ skills directory not found: {skills_dir}", file=sys.stderr)
        return 2

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not skill_dirs:
        print(f"✗ no skills found in {skills_dir}", file=sys.stderr)
        return 2

    total_errors = 0
    total_warnings = 0

    for skill_dir in skill_dirs:
        res = validate_skill(skill_dir, repo_root)
        total_errors += len(res.errors)
        total_warnings += len(res.warnings)
        status = "✓" if res.ok else "✗"
        if not args.quiet or res.errors:
            print(f"{status} {skill_dir.name}")
        for err in res.errors:
            print(f"    ✗ {err}")
        for warn in res.warnings:
            print(f"    ! {warn}")

    print()
    print(f"{len(skill_dirs)} skills · {total_errors} errors · {total_warnings} warnings")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
