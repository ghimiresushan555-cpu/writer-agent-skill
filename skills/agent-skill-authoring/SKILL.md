---
name: agent-skill-authoring
description: Scaffolds new Agent Skills and validates existing SKILL.md files against the Agent Skills specification. Use when creating a skill, adding or editing SKILL.md frontmatter, reviewing a skill for spec violations, fixing invalid name or description fields, or wiring skill validation into CI.
license: MIT
compatibility: Requires Python 3.9 or newer. No third-party packages needed; the bundled scripts use only the standard library.
metadata:
  version: "1.0.0"
  author: agents-skills maintainers
allowed-tools: Read Write Edit Bash(python3)
---

# Agent Skill Authoring

Create and validate Agent Skills that load reliably. A skill is a directory
containing a `SKILL.md` file with YAML frontmatter plus optional `scripts/`,
`references/`, and `assets/` folders. Agents read only `name` and
`description` until a task matches, then load the body, then load bundled
files on demand. Everything below serves that three-stage disclosure.

## Workflow

1. **Scaffold the directory.** Run `scripts/new_skill.py <skill-name> --dir skills/`
   to create a spec-shaped skeleton with valid frontmatter already filled in.
   Naming a skill is the decision with the longest tail, so settle it before
   writing prose.
2. **Write the `description` first, before the body.** The description is the
   only text the agent sees when deciding whether to load the skill. A body
   you love with a weak description never activates.
3. **Write the body as a procedure**, not an essay. Numbered steps, imperative
   verbs, one section per stage of the task, and an explicit "what to check
   before reporting done" step.
4. **Push depth into `references/`.** Keep the body under 500 lines. Anything
   the agent needs only occasionally — a full field-by-field spec table, an
   exhaustive checklist, a long example — belongs in a reference file that the
   body links to with one sentence saying when to open it.
5. **Put determinism in `scripts/`.** If a step is mechanical (validate,
   convert, count, reformat), ship a script and instruct the agent to run it
   rather than perform the task by reading and rewriting. Scripts are correct
   and cost no tokens; prose instructions drift.
6. **Validate.** Run `scripts/validate_skill.py skills/<skill-name>` and fix
   every error. Repeated failures usually mean a name or description problem,
   not a formatting one.
7. **Test activation.** Ask the agent a question the description should match
   and a near-miss it should not. A skill that fires on everything is a skill
   with no boundaries.

## Writing the description

Write in third person, and pair **what it does** with **when to use it**.

Good:

```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and
  merges multiple PDFs. Use when working with PDF documents or when the user
  mentions PDFs, forms, or document extraction.
```

Poor, in three different ways:

```yaml
description: Helps with PDFs.                  # no trigger keywords, too vague
description: I will help you with documents.   # first person, hurts discovery
description: Any document or text task at all. # fires on unrelated requests
```

Practical rules:

- Lead with a third-person verb (`Extracts`, `Validates`, `Generates`), not
  `This skill...` or `Use this to...`.
- Include the literal words users type: file extensions, product names, error
  message fragments, verbs from the request.
- Name the adjacent tasks this skill does *not* cover, so the agent routes
  past it correctly instead of forcing a match.
- Never put `<` or `>` in frontmatter values; angle brackets in text injected
  into a system prompt invite instruction injection and are rejected by
  validators.
- Keep it under 1024 characters. Past that the file is refused outright.

## Naming

`name` must match its parent directory exactly, character for character:

| Check | Rule |
| --- | --- |
| Length | 1 to 64 characters |
| Alphabet | lowercase `a-z`, digits `0-9`, single hyphens |
| Hyphens | no leading, trailing, or consecutive (`--`) hyphens |
| Reserved | no `anthropic` or `claude` |
| Tags | no XML or HTML tags anywhere in the value |

Use a gerund or noun phrase that names the domain, not the tool: `pdf-forms`
over `handle-pdfs-now`. Never rename a published skill casually — agents,
docs, and CI may reference the directory by name.

## Body conventions

- Start with one or two sentences stating scope, then go straight to steps.
- Prefer `1. 2. 3.` for sequences with a real order; use bullets only for
  genuinely unordered sets.
- One code block per command, shown exactly as it should be run, including
  arguments and expected exit status.
- Address the agent as the actor ("run", "read", "confirm"), not the user.
- State failure handling inline: what to do when the input is missing, the
  script errors, or a validation check cannot pass.
- Avoid time-sensitive text (`as of 2026`, `currently`, `for now`) — it rots
  silently inside a skill that agents trust.

## Bundled resources

Keep the tree flat. Reference files link from the body and each other at most
one hop deep; deeply nested links go unread.

```
skills/<name>/
├── SKILL.md          # entry point, always loaded on activation
├── references/       # long-form detail, read only when needed
├── scripts/          # executable helpers the agent runs
└── assets/           # templates and files copied into output, not read
```

Link with paths relative to the skill root (`references/checklist.md`), so the
skill survives being copied into another project. Files that must not be
treated as a skill themselves should not be named `SKILL.md` — that is why the
bundled template is `assets/SKILL.md.tmpl`.

## Validation

Run the bundled validator before every commit and in CI:

```bash
python3 skills/agent-skill-authoring/scripts/validate_skill.py skills/
```

It exits `0` when every skill is clean and `1` with a file-and-rule report
otherwise. It checks frontmatter shape, name and directory agreement,
description limits, body size, unresolved placeholders, and that every
relative link in the body resolves to a real file.

See `references/frontmatter-spec.md` for the complete field-by-field
reference, including the optional `license`, `compatibility`, `metadata`, and
`allowed-tools` keys, and `references/checklist.md` for the pre-commit review
list.
