# Handoff contract

The six skills are only useful together if they agree on where things live and what each stage promises the next. This file is that agreement. If you add a skill, add it here first.

## File layout

All paths are relative to whatever directory the channel lives in (the repo root, by default).

```
channel/
  channel.yaml          # written by channel-strategy; read by everyone
  voice-guide.md        # written by channel-strategy; read by draft-writer, line-editor
ideas/
  backlog.csv           # appended by idea-engine; read by everyone choosing what's next
  <slug>.md             # one idea per file, written by idea-engine
briefs/
  <slug>.md             # written by research-brief; read by draft-writer, line-editor
drafts/
  <slug>.md             # written by draft-writer
  <slug>.edited.md      # written by line-editor
published/
  <slug>.md             # written by publish-and-repurpose
```

**Slug rules:** lowercase, hyphenated, 2–6 words, no dates (`battery-recycling-margins`, not `2026-11-04-battery`). The slug is the join key across all five stages — never silently rename it. If a piece changes direction enough to need a new name, write a new idea file and link the old one under `supersedes:`.

**Never overwrite an input.** Each stage writes a new file or a new field. `line-editor` reads `drafts/<slug>.md` and writes `drafts/<slug>.edited.md`; the author's draft survives.

## What each stage must hand over

### channel-strategy → everyone

`channel/channel.yaml` with, at minimum: `audience.who`, `audience.they_want`, `positioning.promise`, `pillars[]`, `cadence.target_words`, `voice.person`, `voice.reading_level`.
`channel/voice-guide.md` with the five adjectives, rhythm knobs, signature moves, banned list, and two calibration samples.

### idea-engine → research-brief

`ideas/<slug>.md` containing:
- `## The promise` — one sentence a reader would repeat to a friend
- `## Why this channel` — which pillar it serves and why this audience cares now
- `## Angle` — the specific argument, not the topic
- `## Evidence we already have` — anything first-hand; empty is a red flag
- `## What we'd need to verify` — the research assignment
- Frontmatter: `status`, `pillar`, `score` (see `skills/idea-engine/references/scoring.md`)

### research-brief → draft-writer

`briefs/<slug>.md` containing:
- `## Narrative spine` — the argument in five beats, one line each
- `## Claims` — a table: claim | label | evidence | source | date
- `## Counterargument` — the strongest case against, and how the piece handles it
- `## Quotes` — verbatim, attributed, with role and date
- `## What we don't know` — named gaps, so the draft doesn't bluff
- Frontmatter: `status: briefed`, `word_target`, `needs_check_count`

### draft-writer → line-editor

`drafts/<slug>.md` containing:
- `## Spec` block at the top: promise, length, structure, takeaway, call to action
- The piece itself, in voice, with a working title
- `## Open questions` — anything the writer had to guess at
- Frontmatter: `status: draft`, `words`, `needs_check[]` (claims still unlabelled)

### line-editor → publish-and-repurpose

`drafts/<slug>.edited.md` containing:
- The edited piece
- `## Change log` — table of change | reason | severity (`blocker` / `should-fix` / `optional`), with line references
- `## Verification` — how every `needs-check` claim was resolved, or the blocker that remains
- Frontmatter: `status: edited`, `words`, `blockers: 0`

### publish-and-repurpose → the world

`published/<slug>.md` containing:
- Final title, dek, byline, canonical URL placeholder
- The body as published
- `## Packaging`: 5 title options with the chosen one, subject lines, meta description, social copy per surface
- `## Checklist`: completed, with the specific items that were *not* done and why
- Frontmatter: `status: published`, `published_at`, `url`

## Blocking rules

A stage may refuse to proceed, and should say why in one line. Refuse when:

- The required input file is missing and the user hasn't authorised working without it.
- `channel.yaml` is missing the fields the stage depends on.
- A `needs-check` claim survives into a draft (reader-facing risk).
- The draft misses the spec by more than 20% on length, or omits the promised takeaway.

Refusing is a valid output. Guessing is not.
