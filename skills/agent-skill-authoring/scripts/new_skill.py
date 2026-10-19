#!/usr/bin/env python3
"""Scaffold a spec-shaped Agent Skill directory.

Usage:
    new_skill.py <skill-name> [--dir skills/] [--title "Human Title"]
                 [--description "..."] [--force]

Creates <dir>/<skill-name>/ with SKILL.md, references/, scripts/, and assets/.
The name must already satisfy the specification, since the directory name and
the frontmatter name are checked for agreement by validate_skill.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME_LEN = 64

TEMPLATE = """---
name: {name}
description: {description}
license: MIT
compatibility: {compatibility}
metadata:
  version: "0.1.0"
---

# {title}

One or two sentences stating what this skill covers and the boundary of its
scope. Agents read this after deciding the skill is relevant, so it should
answer "is this the right skill for my task" quickly.

## Workflow

1. First step the agent takes, written as an instruction to carry out.
2. Second step, including the command to run where one exists.
3. Third step, naming what to inspect before continuing.
4. Confirm the result: what to check, and what to report back.

## Conventions

- Imperative voice, numbered steps where order matters.
- Show every command exactly as it should be run, with arguments.
- State what to do when an input is missing or a step fails.

## References

- `references/notes.md` holds the long-form detail this body omits. Open it
  when the task needs specifics rather than the procedure above.
- Delete any section of this file you do not need. Unused headings cost tokens
  on every activation.
"""

CHECKLIST = """# Skill Notes

Long-form material that the SKILL.md body should not carry on every
activation. Link this file from the body with one sentence saying when to open
it.

## Details

- Replace this file with real reference material, or delete it along with the
  link in SKILL.md.
"""

GITIGNORE = """__pycache__/
*.pyc
.venv/
"""


def title_from_name(name: str) -> str:
    return " ".join(part.upper() if part.isdigit() else part.capitalize() for part in name.split("-"))


def default_description(name: str) -> str:
    words = name.replace("-", " ")
    return (
        f"Performs {words} work: describes the concrete operations here. "
        f"Use when the user asks to {words}, or mentions the file types, "
        "tools, or error messages this skill handles. Replace this sentence "
        "with the real capability list before publishing."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new Agent Skill.")
    parser.add_argument("name", help="skill name, e.g. pdf-forms")
    parser.add_argument("--dir", default="skills", type=Path, help="directory that holds skills (default: skills)")
    parser.add_argument("--title", help="human-readable heading (default: derived from name)")
    parser.add_argument("--description", help="frontmatter description")
    parser.add_argument("--compatibility", default="No special requirements; document any here.")
    parser.add_argument("--force", action="store_true", help="overwrite an existing skill directory")
    args = parser.parse_args(argv)

    name = args.name
    problems = []
    if len(name) > MAX_NAME_LEN:
        problems.append(f"name is {len(name)} characters; maximum is {MAX_NAME_LEN}")
    if not NAME_RE.match(name):
        problems.append("name must be lowercase letters, digits, and single hyphens")
    if re.search(r"\b(anthropic|claude)\b", name, re.I):
        problems.append("name must not use a reserved word")
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 2

    target = args.dir / name
    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"error: {target} already exists and is not empty (use --force to overwrite)", file=sys.stderr)
        return 2

    (target / "references").mkdir(parents=True, exist_ok=True)
    (target / "scripts").mkdir(parents=True, exist_ok=True)
    (target / "assets").mkdir(parents=True, exist_ok=True)

    skill_md = target / "SKILL.md"
    skill_md.write_text(
        TEMPLATE.format(
            name=name,
            title=args.title or title_from_name(name),
            description=args.description or default_description(name),
            compatibility=args.compatibility,
        ),
        encoding="utf-8",
    )
    (target / "references" / "notes.md").write_text(CHECKLIST, encoding="utf-8")
    (target / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    print(f"created {target}")
    print("  next steps:")
    try:
        shown = skill_md.relative_to(Path.cwd())
    except ValueError:
        shown = skill_md
    ref = shown.parent / "references" / "notes.md"
    print(f"  1. rewrite the description in {shown} for what users actually type")
    print("  2. replace the workflow steps with the real procedure")
    print(f"  3. fill in or delete {ref} and the link to it")
    print("  4. add scripts for mechanical steps, then validate:")
    print(f"     python3 skills/agent-skill-authoring/scripts/validate_skill.py {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
