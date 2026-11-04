# Contributing

Thanks for wanting to make this better. This pack has one organising idea: **a writing channel is a repeating promise, and every skill either protects that promise or erodes it.** Changes are judged against that.

## Before you open a PR

```bash
make check
```

That validates every `SKILL.md` and runs the test suite. CI runs the same thing on Python 3.9, 3.11, and 3.12.

## Adding a skill

1. **Check it doesn't already exist.** Six skills cover strategy → ideas → brief → draft → edit → publish. A seventh should cover a genuinely missing job (translation, series planning, reader research), not a sub-step of an existing one.
2. **Write the contract first.** Add your file paths and handoffs to [`shared/handoff-contract.md`](shared/handoff-contract.md) before writing prose. If you can't describe what you hand over in five bullets, the skill isn't ready.
3. **Follow the shape of the existing skills**: frontmatter → the bar → numbered process → output template → "Refuse when" → references. The "Refuse when" section is mandatory; a skill that never refuses will happily produce slop.
4. **Keep `SKILL.md` under ~200 lines.** Long checklists go in `references/`, templates in `assets/`. The validator warns you.

## Frontmatter rules

```yaml
---
name: kebab-case-matching-the-folder
description: Third person, what it does, then "Use when ..." with concrete triggers. Max 1024 chars.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---
```

- `name` must match the directory name exactly, lowercase, hyphenated.
- `description` must be written in the third person ("Writes...", not "You can use this to..."). It is a routing signal, not marketing copy — include the situations that should trigger the skill.
- Add `allowed-tools` only if the skill genuinely needs a restricted set.

## Voice of the docs

The skills teach craft, so they must demonstrate it: no "delve," no "seamless," no "empower." Prefer a specific example to an adjective. If a rule can't be checked by a reader, it isn't a rule.

## Style for examples

Examples should be small, complete, and slightly boring. A worked example that fits on two screens teaches the pipeline; a beautiful 2,000-word sample essay teaches nothing about how the files connect.

## Reporting problems

Open an issue with: which skill, what you asked for, what came out, and what you expected. If a skill produced something confidently wrong, that's the highest-priority kind of bug in this repo — the fix is usually a missing refusal clause.

## Licence

Contributions are MIT, matching [`LICENSE`](LICENSE).
