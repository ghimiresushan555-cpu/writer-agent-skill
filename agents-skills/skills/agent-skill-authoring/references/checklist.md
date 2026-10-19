# Pre-Commit Skill Checklist

Work top to bottom. The first items are the ones that break loading; the rest
determine whether the skill is actually useful once loaded.

## Blocks publishing

- [ ] File is named exactly `SKILL.md`, case-sensitive, inside the skill directory.
- [ ] Frontmatter opens at byte 0 with `---` and closes with `---`.
- [ ] `name` present, 1-64 characters, `[a-z0-9-]` only, no leading, trailing,
      or consecutive hyphens.
- [ ] `name` equals the parent directory name.
- [ ] `name` and `description` contain no XML or HTML tags and no `<` or `>`.
- [ ] Neither `anthropic` nor `claude` appears in `name`.
- [ ] `description` present, non-empty, 1-1024 characters.
- [ ] `description` states both what the skill does and when to use it.
- [ ] `description` is third person.
- [ ] Only spec-defined top-level keys: `name`, `description`, `license`,
      `compatibility`, `metadata`, `allowed-tools`.
- [ ] YAML parses: watch for unquoted values starting with `[`, `{`, `*`, `&`,
      `!`, `%`, `@`, or `` ` ``, and for tabs used for indentation.
- [ ] Every relative path referenced in the body resolves to a file in the repo.
- [ ] No `TODO`, `TBD`, `FIXME`, `example.com`, or placeholder text left behind.
- [ ] `validate_skill.py` exits 0 on the skill directory.
- [ ] CI on the repository is green.

## Quality of instructions

- [ ] Body is under 500 lines and starts with scope in one or two sentences.
- [ ] Steps are numbered where order matters and imperative in voice.
- [ ] Each command shown is copy-pasteable as written, with arguments.
- [ ] Failure paths are stated: missing input, script error, unfixable check.
- [ ] Long reference material lives in `references/`, linked from the body with
      a sentence explaining when to open it.
- [ ] Mechanical work is a script, not prose the model re-implements each run.
- [ ] Scripts were executed at least once against real input, and their output
      matched what the body claims.
- [ ] No time-sensitive phrasing (`currently`, `as of this year`, `for now`).
- [ ] Anything that changes weekly lives outside the skill, fetched at runtime.

## Activation testing

- [ ] Three phrasings a real user would type all activate the skill.
- [ ] Two adjacent-but-wrong requests do not activate it.
- [ ] The skill still produces correct output when the agent cannot see the
      reference files (proves the body is self-sufficient for the common case).
- [ ] Nothing in the skill tells the agent to skip validation, verification, or
      a safety check to save time.

## If a skill never fires

In rough order of likelihood:

1. Description lacks the keywords the user actually types.
2. Description is too generic, so it competes with every other skill and loses.
3. Task genuinely belongs to a sibling skill; say so in the description and
   point at it.
4. The skill directory is outside the path the product scans.
5. The file failed to parse and was dropped silently at discovery time —
   confirm with the validator before rewriting prose.
