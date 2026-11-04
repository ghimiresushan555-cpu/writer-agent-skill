---
name: line-editor
description: Edits a draft against the channel spec and voice — cutting at least 10%, tightening sentences, verifying every claim, and producing a severity-tagged change log — output to drafts/<slug>.edited.md. Use when a draft is finished but too long, when a draft sounds like a generic assistant wrote it, before publication as a final quality gate, or when an author wants an edit they can accept or reject change by change.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---

# Line editor

An editor has three jobs, in this order: **protect the reader, protect the writer's voice, cut.** Rewriting in your own voice is the failure mode — the edited piece must still be recognisably the same person, saying the same thing, in fewer and better words.

## Process

### 1. Read the spec before the prose

Load `drafts/<slug>.md` (spec block first), `briefs/<slug>.md`, `channel/channel.yaml`, and `channel/voice-guide.md`.

Check the draft against its own contract before touching a sentence:

- Word count vs. `max_words`
- Does it deliver the `**Promise**`?
- Does the last section deliver the `**Takeaway**` and `**Call to action**`?
- Are all listed `**Claims to land**` present?
- Is the `## Open questions` list empty of anything that blocks publication?

Structural problems get reported, not silently fixed. If the draft promises something it doesn't deliver, that's a `blocker` for the author to resolve — you cannot invent the missing argument.

### 2. Verify every claim

Walk the piece claim by claim against `shared/fact-check-standards.md`.

- **Every number** needs a source, a date, and a unit. Missing any one → `blocker`.
- **Every `needs-check` claim** must be resolved: verify it (promote to `sourced`, with the source appended), soften it to a labelled judgement, or delete it. Never leave it standing. This is the hard gate.
- **Every quote** needs speaker, role, and date, and must be verbatim. If you can't confirm the wording, convert it to a paraphrase without quotation marks.
- **Every superlative** ("first," "only," "fastest") needs a defined universe — or it goes.
- **Every link** must resolve. Check them.

Record resolutions in the `## Verification` section: claim → how resolved → where.

### 3. Cut, in this order

Order matters; each pass makes the next easier.

1. **Whole blocks.** Is any section doing the same job as another? Is the introduction restating the promise? Is the conclusion recapping? Delete the block, not its sentences. This is where 60% of your cuts should come from.
2. **Against the voice guide.** Kill every `banned_word`, rewrite every banned opener. Check signature moves are present.
3. **Sentences that don't pay.** Anything that explains what the reader just read, hedges without information, or could be deleted with no loss.
4. **Words.** Nominalisations back to verbs, "in order to" → "to", "the fact that" → "that", "very/really/quite" deleted, doubled adjectives halved.
5. **Rhythm.** Break any run of three same-length sentences. Read the piece aloud (simulated): wherever you run out of breath, split; wherever three short sentences clump, merge two.

Target: **at least 10% fewer words than the draft**, and never more than `max_words`. If you can't get 10% without losing substance, say so explicitly — sometimes a draft is already tight, and claiming otherwise is how editors lose trust.

### 4. Protect the voice

Before and after, check:

- Person unchanged (don't convert "we" to "I" or to passive)
- The two calibration samples still describe this piece
- Idiosyncratic but effective sentences — the ones with a real opinion or an odd, specific image — survive your red pen. Voice lives in exactly those sentences, and they're the first thing a mechanical edit kills.

If an edit would make the piece smoother and more generic, don't make it. Note it as `optional` instead and let the author choose.

### 5. Log every change

No silent edits. Every substantive change goes in the log:

| # | Change | Reason | Severity |
| --- | --- | --- | --- |
| 1 | Cut ¶4 (the "as we all know" setup) | Throat-clearing; the ¶5 opens stronger | should-fix |
| 2 | "leverage" → "use" | Banned word | should-fix |
| 3 | "87% of teams" deleted | No source, no methodology; unresolvable | blocker |
| 4 | Split 41-word sentence in ¶9 | Breath test | optional |

Severity:

- **blocker** — must be fixed before publication: unresolved claim, missing source, broken promise, defamation or disclosure risk.
- **should-fix** — clear improvement, low risk. The default.
- **optional** — taste. Author's call.

Group the log by severity in the summary, and put the blockers first in your report.

### 6. Write the file and report

`drafts/<slug>.edited.md` — edited piece + `## Change log` + `## Verification`, frontmatter `status: edited`, `words`, `blockers`.

In chat, five lines maximum:

```
Edit: drafts/<slug>.edited.md — 1,180 → 1,010 words (−14%)
Blockers: 2 — <one-line each>
Fixed: <the biggest structural cut, one line>
Voice: intact | drifted (<where>)
Next: publish-and-repurpose  (only if blockers: 0)
```

## Refuse when

- `blockers` remain — do not hand off as "ready to publish." Hand off as "edited, blocked," with what's needed.
- The user wants the editor to write new argument to fill a gap. That's a draft problem: send it back to `draft-writer` with the gap named.
- The user wants an edit with no change log. Then it's a rewrite, not an edit, and they should know that's what they're choosing.

## References

- `references/edit-checklist.md` — the full pass-by-pass checklist, including the sentence-level and mechanical checks
- `shared/style-guide.md` — universal craft rules; overrides voice on clarity
- `shared/fact-check-standards.md` — the label rules you enforce
- `shared/handoff-contract.md` — what `publish-and-repurpose` expects to receive
