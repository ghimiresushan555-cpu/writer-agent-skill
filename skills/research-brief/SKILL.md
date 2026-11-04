---
name: research-brief
description: Turns an approved idea into a cited research brief — narrative spine, claims table with sourced/needs-check/opinion labels, counterargument, verbatim quotes, and named gaps — written to briefs/<slug>.md. Use when an idea is approved and needs evidence before drafting, when a draft keeps making claims nobody can verify, or when the writer needs to know exactly what is still unknown before writing a sentence.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
allowed-tools: WebSearch WebFetch Read Write
---

# Research brief

The brief is where a piece becomes true or stays vague forever. A draft written without one is a sequence of confident sentences whose provenance nobody can reconstruct — which is precisely the failure mode readers punish hardest.

The brief's job is **not** to be comprehensive. It is to make the small number of load-bearing claims checkable, and to name what's missing loudly enough that the draft can't bluff past it.

## Process

### 1. Load and scope

Read `ideas/<slug>.md` and `channel/channel.yaml`. If the idea has no `## The promise`, stop: there's nothing to research toward.

Write down, before searching:

- **The promise** — what the piece has to prove
- **The word target** from the channel's cadence
- **The claim budget** — roughly one sourced claim per 100–150 words. A 1,200-word piece carries about 8–10 real claims, not 40. Most over-researched briefs are the ones that never chose.

### 2. Separate what you have from what you need

Copy `## Evidence we already have` and classify each item: first-hand (usable as-is, labelled `sourced` with "author's own data" as the source), public (needs a citation and a date), or hearsay (needs verification or it becomes `opinion`).

Then list the gaps the promise requires. Gap-driven research beats topic-driven research by a wide margin; you're looking for the smallest set of facts that makes the argument land.

### 3. Research in precision order

Follow `references/source-standards.md`, but the sequence is: **primary data → primary documents → named people → reputable secondary reporting → reference works**. Stop at the first rank that answers the question.

For every claim you intend to make, capture immediately — not later:

- the claim, stated in one sentence
- the exact source, with title, publisher, date, and URL
- the specific figure or quote as it appears in the source
- a note on what the source *doesn't* say

Search behaviour that actually works:

- Search for the number, not the topic: `"pilot success criteria" utility procurement 2025` beats `utility procurement`.
- Go to the origin. If three articles cite the same stat, find the study; half the time it says something narrower.
- Ask what would falsify the claim, then search for that. This is the cheapest way to find the counterargument before a reader does.
- Record dead ends. "No public data on X" is a finding, and often a better paragraph than the stat you were chasing.

### 4. Build the claims table

Every claim gets exactly one label from `shared/fact-check-standards.md`: `sourced`, `needs-check`, or `opinion`.

| Claim | Label | Evidence | Source | Date | Notes |
| --- | --- | --- | --- | --- | --- |
| Utilities require 12–18 months from pilot to PO | sourced | 3 interviews + 1 survey | Utility Dive survey, p.4 | 2025-06 | survey covers US IOUs only |

Rules:

- **A `needs-check` claim is a to-do, not a finding.** Say what would resolve it and how expensive that is.
- **Cap `needs-check` at three.** More than three and the brief isn't done — either verify, soften to `opinion`, or cut the claim.
- **Every number needs unit, period, and baseline.** "Up 40%" is not a claim; "up 40% YoY, from 2.1% to 2.9% of revenue" is.
- **Opinion is fine.** Label it and phrase it as judgement. Analysis is the product; unlabelled analysis is the problem.

### 5. Find the counterargument

Write the strongest case against the piece's promise in 2–4 sentences, as if you were the smartest person who disagrees. Then choose one of three handling strategies and say which:

1. **Concede and limit** — "true, except in cases like X" (most common, most credible)
2. **Refute** — you have evidence the objection is wrong (rare; needs the strongest evidence in the piece)
3. **Hold both** — the tension is the piece (best for essays, worst for advice)

A brief with no counterargument produces a draft that reads like marketing.

### 6. Collect quotes, verbatim

For each quote: exact wording, speaker's full name, role, organisation, date, and whether it was on the record. If you cannot verify the wording, don't quote — paraphrase and attribute the idea.

Two quotes minimum for a reported piece, zero for an essay. Never invent, tidy, or merge quotes. Never attribute a paraphrase with quotation marks.

### 7. Write the narrative spine

Five beats, one line each, in the order the reader will meet them:

```
1. Opening image or number:   ...
2. The tension:               ...
3. The mechanism (the proof): ...
4. The counterargument:       ...
5. What the reader does:      ...
```

If a beat can't be filled, the piece isn't ready — say which beat is missing and what would fill it. This is the single most useful thing you can hand a writer.

### 8. Write the file and report

Write `briefs/<slug>.md` per the template below. In the chat, report:

```
Brief: briefs/<slug>.md — <sourced> sourced claims, <needs-check> open, <opinion> labelled opinion
Spine: <beat 3, the mechanism, in one line>
Risk: <the weakest link and what would fix it>
```

## File template

```markdown
---
slug:
status: briefed
word_target: 1200
needs_check_count: 2
researched: 2026-11-04
---

## The promise (from the idea)
## Narrative spine
## Claims
## Counterargument
## Quotes
## What we have first-hand
## What we don't know
## Sources consulted (including dead ends)
```

`## What we don't know` is mandatory and must never be empty. A brief asserting complete knowledge is either sloppy or dishonest, and the draft will inherit whichever it is.

## Refuse when

- The promise requires data that doesn't publicly exist and no interview is available. Say so, and offer the smaller true piece instead — "we couldn't find out X, here's what that tells you" is often a better article than the one planned.
- The user asks you to cite a source you couldn't open. Fabricated citations are the one unrecoverable failure in this pipeline.
- The user asks you to write the draft "while you're at it." Finishing the brief first is what makes the draft cheap.

## References

- `references/source-standards.md` — source ranking, verification checks, and the failure modes to hunt
- `shared/fact-check-standards.md` — the label definitions both this skill and `line-editor` enforce
- `shared/handoff-contract.md` — what `draft-writer` expects to receive
