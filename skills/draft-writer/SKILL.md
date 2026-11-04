---
name: draft-writer
description: Writes a publishable first draft from a research brief, in the channel's calibrated voice, to a stated length and structure — output to drafts/<slug>.md with an explicit spec block. Use when a brief exists and the piece needs actual prose, when a draft keeps turning into notes, when writing needs to sound like the channel rather than like a generic assistant, or when a piece must be rewritten shorter.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---

# Draft writer

A first draft has one job: to be a real piece of writing that a reader could finish, whose argument is visible and whose seams are honest. It does not have to be perfect. It does have to be *itself* — not a summary of the brief, not a list of facts, not an essay about the essay.

## Process

### 1. Load three things

- `briefs/<slug>.md` — the spine, claims, quotes, and gaps
- `channel/channel.yaml` — length, cadence, voice knobs
- `channel/voice-guide.md` — adjectives, signature moves, banned list, and the **on-voice calibration sample**

If the brief is missing, say so and offer two paths: research first, or write from the idea with every unverified claim marked. If the voice guide is missing, write in plain, direct, first-person prose and flag it in `## Open questions` — do not silently invent a house style.

### 2. Write the spec block first

Before a single sentence of the piece:

```markdown
## Spec
- **Promise:** what the reader gets, in one sentence
- **Reader:** the specific person, from channel.yaml
- **Length:** 1,200 words (min 900 / max 1,400)
- **Shape:** the 3–5 beats, with rough word allocation
- **Takeaway:** the one thing to remember
- **Call to action:** what they do this week (or: none — essay)
- **Tone dial:** which two voice adjectives matter most here
- **Claims to land:** the 4–6 sourced claims this piece must use
```

The spec is the contract. If the draft and the spec disagree at the end, the draft is wrong, or the spec is — but you have to pick one and say which. A draft that quietly changes its promise is the most common failure in the whole pipeline.

### 3. Choose a shape, deliberately

Pick from `references/structures.md` — argument, mechanism teardown, post-mortem, field report, translation piece, or annotated example. Each has a different engine:

- **Argument** runs on a claim and a counterclaim.
- **Mechanism** runs on sequence; the reader wants step four.
- **Post-mortem** runs on suspense backwards: what we thought, what happened, why.
- **Field report** runs on observation and specificity, not conclusion.
- **Translation** runs on a gap between two vocabularies.

Choose by what the evidence supports, not by what's comfortable. If the brief has three interviews and no data, that's a field report or a translation piece, not a data-driven argument.

### 4. Draft to the spine, in one pass

Write the whole piece before polishing anything. Rules for the pass:

- **One paragraph per beat first.** Then expand each beat to its word allocation. This prevents the 400-word intro and the 90-word ending that every unplanned draft has.
- **Lead with the strongest concrete thing you have** — a number, a scene, a quote, a failure. Not context, not definitions, not "as we've seen."
- **Every claim from the brief carries its label into the prose.** A `sourced` claim gets its attribution naturally woven in ("a 2025 Utility Dive survey of 118 US IOUs found..."). An `opinion` gets framed as judgement ("my read is..."). A `needs-check` claim does not appear in the draft at all — move it to `## Open questions` and write the paragraph without it, or with a visible placeholder.
- **Quotes are verbatim** and attributed in the same sentence or the next one.
- **Use the counterargument** at full strength, in its own section or as a concession mid-argument. A weakened counterargument is worse than none — readers spot it and stop trusting the rest.
- **End on the most useful sentence.** Not a recap, not a call to subscribe.

### 5. Calibrate against the sample

Before finishing, put your opening two paragraphs next to the on-voice sample in `channel/voice-guide.md`. Check the measurable things:

- Mean sentence length within ~3 words of `voice.mean_sentence_words`
- Reading level within one grade of `voice.reading_level`
- Person consistent throughout
- Zero words from `banned_words`, zero banned openers
- Signature moves present — all of them, ideally more than once

If the draft reads like a competent generalist rather than this channel, the fix is almost always: fewer abstractions, more specifics, shorter sentences, one fewer hedge per claim.

### 6. Cut it before handing it over

Drafts arrive 15–25% too long. Cut now, not later:

1. Delete the first paragraph if it's throat-clearing. It usually is.
2. Delete every sentence that restates the previous one in different words.
3. Delete hedges that don't carry information ("I think," "it seems," "perhaps" where the claim is sourced).
4. Convert every paragraph over five sentences into two.
5. Remove the summary section at the end if the argument already landed.

Then count words. If you're still over `max_words`, cut a whole beat rather than shaving every sentence — a tighter argument beats a thinner one.

### 7. Write the file

`drafts/<slug>.md`:

```markdown
---
slug:
status: draft
words: 1180
needs_check: []
voiced: true
---

## Spec
...

# <working title>

<body>

## Open questions
- Anything you guessed at
- Any `needs-check` claim you wrote around
- Any structural decision the author should overrule
```

Report in three lines:

```
Draft: drafts/<slug>.md — 1,180 words, 5 beats, target 1,200
Shape: <structure name> | Voice: <2 adjectives> | Claims used: <n> sourced
Watch: <the weakest paragraph and why>
```

## Refuse when

- There's no brief and the user won't accept unverified claims being marked. Writing confidently about unverified facts is how channels lose readers.
- The requested length can't hold the argument. Say what the argument needs — "this is a 2,000-word piece or a 700-word one; at 1,200 it will be a list" — and let them choose.
- The user asks you to match another publication's voice closely. Write in the channel's voice and say which structural move you borrowed; pastiche of a living writer's style is a bad trade.

## References

- `references/structures.md` — six shapes, with the engine of each and when it fails
- `assets/draft-template.md` — the file skeleton including the spec block
- `shared/style-guide.md` — universal craft rules that override voice on matters of clarity
- `shared/handoff-contract.md` — what `line-editor` expects to receive
