#!/usr/bin/env python3
"""Validate Agent Skills against the Agent Skills specification.

Usage:
    validate_skill.py [PATH ...] [--strict] [--quiet]

PATH is a skill directory, a repository root containing skills/, or a
SKILL.md file. Defaults to the current directory. With several paths, the
union of discovered skills is validated once (duplicates removed).

Exits 0 when clean, 1 on any error. Warnings do not fail the run unless
--strict is given. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024
MAX_COMPATIBILITY_LEN = 500
MAX_FILE_BYTES = 256 * 1024
MAX_BODY_LINES = 500
MIN_DESCRIPTION_LEN = 20

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RESERVED_WORDS = ("anthropic", "claude")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^(?P<indent> *)(?P<key>[A-Za-z0-9_-]+):(?P<rest>.*)$")
PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+")
KNOWN_SUFFIXES = {".md", ".py", ".sh", ".json", ".txt", ".yaml", ".yml", ".tmpl", ".csv", ".toml"}
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX|placeholder|lorem ipsum)\b|example\.com", re.I)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "build", "dist"}


class Finding:
    __slots__ = ("level", "code", "message", "line")

    def __init__(self, level: str, code: str, message: str, line: int | None = None):
        self.level = level
        self.code = code
        self.message = message
        self.line = line

    def render(self, rel: Path) -> str:
        where = f"{rel}:{self.line}" if self.line else f"{rel}"
        return f"  {self.level:<7} {self.code}  {where}  {self.message}"


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(lines: list[str]) -> tuple[dict, int, list[Finding]]:
    """Parse the YAML subset a SKILL.md header uses.

    Supports top-level scalars, folded/literal block scalars, and one level of
    nested mapping (metadata). Returns the mapping, the number of physical
    lines consumed including both '---' fences, and parse findings.
    """
    findings: list[Finding] = []
    data: dict = {}

    if not lines or lines[0].strip() != "---":
        return data, 0, [Finding("error", "E002", "frontmatter missing: file must start with '---' on line 1", 1)]

    end = None
    for idx in range(1, len(lines)):
        raw = lines[idx]
        if raw.strip() == "---":
            end = idx
            break
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            findings.append(Finding("error", "E012", "tab used for indentation in frontmatter", idx + 1))

    if end is None:
        return data, 0, [Finding("error", "E002", "frontmatter unterminated: no closing '---' found")]

    current: str | None = None
    buffer: list[str] = []
    block_style: str | None = None
    i = 1
    while i < end:
        raw = lines[i]
        match = KEY_RE.match(raw.rstrip())
        if match and not match.group("indent"):
            if current and buffer:
                data[current] = finish_value(block_style, buffer)
            current, buffer, block_style = match.group("key"), [], None
            rest = match.group("rest").strip()
            if rest in {">", ">-", ">+", "|", "|-", "|+"}:
                block_style = rest
            elif rest:
                data[current] = strip_quotes(rest)
                current, buffer = None, []
            i += 1
            continue
        if match and match.group("indent"):
            if current == "metadata":
                key = match.group("key")
                value = strip_quotes(match.group("rest"))
                data.setdefault("metadata", {})[key] = value
                i += 1
                continue
            findings.append(Finding("error", "E013", f"unexpected nested key '{match.group('key')}'", i + 1))
            i += 1
            continue
        if raw.strip() and not raw.startswith(" "):
            findings.append(Finding("error", "E013", f"unparseable frontmatter line: {raw.strip()[:40]!r}", i + 1))
        if raw.strip():
            buffer.append(raw.strip())
        i += 1

    if current and buffer:
        data[current] = finish_value(block_style, buffer)

    return data, end + 1, findings


def finish_value(block_style: str | None, buffer: list[str]) -> str:
    if block_style and block_style.startswith("|"):
        return "\n".join(buffer)
    return " ".join(buffer).strip()


def parse_path(raw: str) -> str:
    return raw.split("#", 1)[0].split("?", 1)[0].strip()


def check_frontmatter(skill_dir: Path, data: dict, offset: int, findings: list[Finding]) -> None:
    if not data:
        return

    unexpected = [k for k in data if k not in ALLOWED_KEYS]
    if unexpected:
        findings.append(Finding("error", "E008", f"unknown top-level key(s): {', '.join(sorted(unexpected))}"))

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.append(Finding("error", "E003", "'name' is required and must be a non-empty string"))
        name = None
    else:
        if len(name) > MAX_NAME_LEN:
            findings.append(Finding("error", "E003", f"'name' is {len(name)} characters; maximum is {MAX_NAME_LEN}"))
        if not NAME_RE.match(name):
            findings.append(
                Finding(
                    "error",
                    "E003",
                    "'name' must be lowercase letters, digits, and single hyphens, with no leading, "
                    "trailing, or consecutive hyphen",
                )
            )
        if any(word in name.lower() for word in RESERVED_WORDS):
            findings.append(Finding("error", "E007", f"'name' contains a reserved word: {', '.join(RESERVED_WORDS)}"))
        if name != skill_dir.name:
            findings.append(Finding("error", "E004", f"'name' {name!r} does not match directory {skill_dir.name!r}"))
        if unicodedata.normalize("NFKC", name) != name:
            findings.append(Finding("warn", "W005", "'name' is not NFKC-normalized; use ASCII to stay portable"))

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        findings.append(Finding("error", "E005", "'description' is required and must be a non-empty string"))
    else:
        if len(description) > MAX_DESCRIPTION_LEN:
            findings.append(
                Finding("error", "E005", f"'description' is {len(description)} characters; maximum is {MAX_DESCRIPTION_LEN}")
            )
        elif len(description) < MIN_DESCRIPTION_LEN:
            findings.append(Finding("warn", "W001", f"'description' is very short ({len(description)} characters); include what and when"))
        if "<" in description or ">" in description:
            findings.append(Finding("error", "E006", "'description' must not contain angle brackets"))
        low = description.lower()
        if re.match(r"^(this skill|i will|you can|you will|we will)\b", low.strip()):
            findings.append(Finding("warn", "W003", "'description' should be third person, e.g. 'Validates ...'"))
        if not re.search(r"\buse when\b|\buse this when\b|\buse for\b|\bwhen the user\b|\bwhen working\b|\bwhen creating\b|\bwhen reviewing\b|\bwhen fixing\b|\btrigger", low):
            findings.append(Finding("warn", "W006", "'description' states what the skill does but no 'Use when' trigger condition"))

    compatibility = data.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > MAX_COMPATIBILITY_LEN:
        findings.append(
            Finding("error", "E009", f"'compatibility' is {len(compatibility)} characters; maximum is {MAX_COMPATIBILITY_LEN}")
        )

    allowed = data.get("allowed-tools")
    if isinstance(allowed, str) and ("<" in allowed or ">" in allowed):
        findings.append(Finding("error", "E006", "'allowed-tools' must not contain angle brackets"))

    metadata = data.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        findings.append(Finding("error", "E010", "'metadata' must be a mapping of string keys to string values"))


def check_body(text: str, offset: int, skill_dir: Path, findings: list[Finding]) -> None:
    lines = text.split("\n")
    body = lines[offset:]
    body_text = "\n".join(body).strip("\n")

    if not body_text:
        findings.append(Finding("error", "E011", "SKILL.md body is empty; add instructions after the frontmatter"))
        return

    if len(body) > MAX_BODY_LINES:
        findings.append(
            Finding("warn", "W002", f"body is {len(body)} lines; keep under {MAX_BODY_LINES} and move depth into references/")
        )

    in_fence = False
    visible: list[tuple[int, str]] = []
    for number, raw in enumerate(body, start=offset + 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            visible.append((number, raw))

    for number, raw in visible:
        for match in PLACEHOLDER_RE.finditer(raw):
            findings.append(Finding("warn", "W004", f"unresolved placeholder text {match.group(0)!r}", number))

    referenced: set[str] = set()
    for number, raw in visible:
        for match in MD_LINK_RE.finditer(raw):
            target = parse_path(match.group(1))
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            referenced.add((number, target))
        inside_code = re.findall(r"`([^`]+)`", raw)
        for token in inside_code:
            for candidate in PATH_TOKEN_RE.findall(token):
                if Path(candidate).suffix.lower() in KNOWN_SUFFIXES:
                    referenced.add((number, candidate))

    for number, target in sorted(referenced):
        if not target or target.startswith("/"):
            continue
        if not (skill_dir / target).exists():
            findings.append(Finding("error", "E014", f"referenced path does not exist: {target}", number))


def validate_skill(skill_md: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        raw_bytes = skill_md.read_bytes()
    except OSError as exc:
        return [Finding("error", "E001", f"unreadable: {exc}")]

    if len(raw_bytes) > MAX_FILE_BYTES:
        findings.append(Finding("error", "E010", f"file is {len(raw_bytes)} bytes; maximum is {MAX_FILE_BYTES}"))

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return findings + [Finding("error", "E001", "SKILL.md is not valid UTF-8")]

    if text.startswith("\ufeff"):
        findings.append(Finding("error", "E002", "file starts with a byte-order mark; frontmatter must begin at byte 0"))

    lines = text.replace("\r\n", "\n").split("\n")
    data, offset, parse_findings = parse_frontmatter(lines)
    findings.extend(parse_findings)
    check_frontmatter(skill_md.parent, data, offset, findings)
    check_body(text, offset, skill_md.parent, findings)

    return findings


def discover(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_file() and path.name == "SKILL.md":
            found.append(path)
        elif path.is_dir():
            direct = path / "SKILL.md"
            if direct.is_file():
                found.append(direct)
                continue
            for skill_md in sorted(path.rglob("SKILL.md")):
                if any(part in SKIP_DIRS for part in skill_md.parts):
                    continue
                found.append(skill_md)
    unique: list[Path] = []
    seen: set[Path] = set()
    for item in found:
        resolved = item.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(item)
    return unique


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills.")
    parser.add_argument("paths", nargs="*", default=["."], type=Path, help="skill dir, repo root, or SKILL.md file")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="print only findings and the summary line")
    args = parser.parse_args(argv)

    roots = [p for p in args.paths]
    for path in roots:
        if not path.exists():
            print(f"error: path does not exist: {path}", file=sys.stderr)
            return 2

    skills = discover(roots)
    if not skills:
        print("error: no SKILL.md files found", file=sys.stderr)
        return 2

    root = roots[0] if len(roots) == 1 else Path.cwd()
    total_errors = total_warnings = 0

    for skill_md in skills:
        findings = validate_skill(skill_md)
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warn"]
        total_errors += len(errors)
        total_warnings += len(warnings)

        if args.quiet and not findings:
            continue

        status = "FAIL" if errors else ("WARN" if warnings else "OK")
        rel = skill_md.relative_to(root) if skill_md.is_relative_to(root) else skill_md
        print(f"{status}  {rel}")
        for finding in errors + warnings:
            print(finding.render(rel))

    print(f"\n{len(skills)} skill(s) checked - {total_errors} error(s), {total_warnings} warning(s)")

    if total_errors or (args.strict and total_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
