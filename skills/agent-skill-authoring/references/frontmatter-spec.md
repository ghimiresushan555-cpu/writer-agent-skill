# SKILL.md Frontmatter Reference

`SKILL.md` is YAML frontmatter delimited by `---` lines, followed by a
Markdown body. The frontmatter block must begin at the first byte of the file:
no leading blank line, no BOM, no comment before the opening `---`.

## Field summary

| Field | Required | Constraints | Purpose |
| --- | --- | --- | --- |
| `name` | Yes | 1-64 chars, `a-z0-9-`, no leading/trailing/consecutive hyphens, must equal the parent directory name | Unique identifier used to load and reference the skill |
| `description` | Yes | 1-1024 chars, non-empty, no angle brackets | The trigger text the agent matches a task against |
| `license` | No | Short string; SPDX id preferred (`MIT`, `Apache-2.0`) or a path to a bundled license file | Usage rights |
| `compatibility` | No | 1-500 chars | Environment requirements: intended product, packages, network access |
| `metadata` | No | Map of string keys to string values, commonly `version` and `author` | Arbitrary extra metadata |
| `allowed-tools` | No | Space-separated list of pre-approved tools, experimental | Pre-approves tool access to reduce permission prompts |

Unknown top-level keys should be avoided; some parsers warn or ignore them, and
one product may reject what another accepts.

## `name`

```yaml
name: pdf-processing     # valid
name: data-analysis      # valid
name: code-review        # valid
name: PDF-Processing     # invalid: uppercase
name: -pdf               # invalid: leading hyphen
name: pdf--processing    # invalid: consecutive hyphens
```

The value must match the directory that contains `SKILL.md`. A skill at
`skills/pdf-forms/SKILL.md` therefore needs `name: pdf-forms`. Comparison is
made on the NFKC-normalized form of both strings, so visually identical names
using different Unicode are accepted while real differences are not.

Names that collide across installed skills make activation ambiguous. Prefix
with the domain when a generic name is already taken.

## `description`

Two clauses, in this order: third-person statement of capability, then a
`Use when` clause naming trigger conditions.

```yaml
description: >-
  Validates SKILL.md files against the Agent Skills specification and reports
  rule-level errors. Use when creating or reviewing a skill, when a skill fails
  to load, or when adding skill validation to continuous integration.
```

Folded (`>-`) and literal (`|`) block scalars are both fine for long values and
keep the YAML readable. Line folding inside a block scalar collapses newlines
into single spaces when the value is parsed.

Words the agent needs are the words from the user's request. A description that
reads as a category label ("PDF stuff") fails; one that enumerates operations
("extract text and tables, fill forms, merge, split, rotate") succeeds.

Never include `anthropic` or `claude` in `name`, and avoid them in
`description` as well; reserved-word checks reject the file.

## `compatibility`

State only what genuinely constrains execution, since this text is consumed
before the skill runs.

```yaml
compatibility: Requires Python 3.9+, network access for model calls, and the
  pdftotext binary on PATH.
```

## `metadata`

Free-form string map. Quote values that could otherwise parse as numbers,
booleans, or dates.

```yaml
metadata:
  version: "1.0.0"
  author: example-org
```

## `allowed-tools`

Experimental, and ignored by products that do not implement it. It lists tools
the skill may use without an approval prompt.

```yaml
allowed-tools: Read Grep Bash(python3)
```

Omit it unless reducing permission prompts matters for the skill; an
over-broad list grants access the skill never uses.

## Size limits

| Limit | Value | Consequence |
| --- | --- | --- |
| Whole file | 256 KB | File rejected outright |
| SKILL.md body | under 500 lines | Loads, but bloated context slows every activation |
| Instructions at activation | under 5000 tokens recommended | Move detail into `references/` |
| Per-skill advertised metadata | roughly 100 tokens | Long descriptions crowd out sibling skills |

## Complete minimal example

```markdown
---
name: csv-cleaner
description: Normalizes delimiter, encoding, and header row of CSV exports and
  flags ragged rows before analysis. Use when a CSV will not parse, when
  columns land in the wrong fields, or when the user mentions delimiter,
  encoding, or messy export files.
license: MIT
compatibility: Requires Python 3.9 or newer; standard library only.
metadata:
  version: "1.0.0"
---

# CSV Cleaner

## Workflow

1. Detect delimiter with `scripts/detect.py path/to/file.csv`.
2. Confirm the header row is row 1; if not, record the offset.
3. Normalize encoding and line endings with `scripts/normalize.py`.
4. Report row counts before and after, plus every ragged row index.
```
