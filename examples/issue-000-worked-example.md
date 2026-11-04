# Worked example: one issue through all six skills

A short, deliberately unglamorous walk through the pipeline. The channel is fictional; the file names, fields, and decisions are exactly what the skills produce.

---

## 0. The starting point

```
> Run channel-strategy. I want to start a weekly newsletter about climate
  hardware operations for startup operators.
```

## 1. `channel-strategy`

Three questions in, the answer that matters: *"What do they believe that you think is wrong?"*

> "That pilots fail because the technology isn't ready. They fail because nobody defined success before the pilot started."

That's the wedge. The skill writes two files.

`channel/channel.yaml` (abridged):

```yaml
audience:
  who: "operators at 10–200 person climate-tech startups, usually the second or third PM hire"
  they_want: ["to sell into utilities without a 12-month pilot"]
positioning:
  promise: "Every issue ends with one thing you can do this week, backed by someone who already tried it."
  point_of_view: "Climate hardware companies fail on commercial execution far more often than on engineering."
pillars:
  - name: "Procurement, decoded"
    promise: "The actual steps, documents, and people between a pilot and a PO."
    share: 0.4
voice:
  person: "first-person plural"
  reading_level: 9
  banned_words: ["leverage", "unlock", "journey", "ecosystem", "delve"]
```

`channel/voice-guide.md` gets the two calibration samples — the part that makes the other five skills useful:

> **On-voice:** "We ran a nine-month pilot with a utility that had no idea what 'done' meant. Neither did we. The contract said 'successful demonstration.' The procurement team thought that meant a signed PO. We thought it meant they liked the demo."
>
> **Off-voice:** "Pilots are a critical step in the climate tech journey, and aligning stakeholder expectations is key to unlocking success."

## 2. `idea-engine`

Twelve candidates, scored. The winner:

```
specificity 5 · audience 5 · evidence 5 · timeliness 4 · durability 5 · effort 4
total = 34.5 / 37.5
```

`ideas/pilot-exit-criteria.md`:

```markdown
---
slug: pilot-exit-criteria
pillar: "Procurement, decoded"
score: 34.5
origin: first-hand
evidence: strong
---

## The promise
The exit criteria in your pilot contract decide whether you get a purchase
order — and almost nobody writes them before the pilot starts.

## Angle
Argues against "prove the technology works." The technology isn't the thing
being evaluated; the procurement team is evaluating whether they can buy it.

## Evidence we already have
- Two utility pilot contracts with "successful demonstration" as the only criterion
- A utility buyer who said, on a call, that no PO exists without a budget line

## What we'd need to verify
- How common vague exit criteria are (no public data — say so)
- Whether a standard clause exists in any public procurement guideline

## Failure mode
Becomes a generic "align stakeholders early" listicle, with no contract language.
```

## 3. `research-brief`

The gap-driven part: there is genuinely no public data on pilot exit criteria. Instead of inventing a stat, the brief records the absence and builds on what exists.

```markdown
## Claims
| Claim | Label | Evidence | Source | Date |
| --- | --- | --- | --- | --- |
| Public utility procurement guidelines specify evaluation criteria for RFPs, not pilots | sourced | RFP template | Utility RFP template, §4.2 | 2024-09 |
| Two of two contracts we audited named no measurable exit criterion | sourced | Author's own contracts, anonymised | — | 2026-10 |
| Vague exit criteria are common across the sector | opinion | Two contracts is not a sample | — | — |

## Counterargument
Buyers deliberately keep exit criteria vague to preserve optionality. That's a
real position, and the piece has to answer it rather than assume incompetence.

## What we don't know
No public data on how often pilots convert to POs. The piece must say this
instead of quoting a sector-wide conversion rate.
```

Note the third row: an honest `opinion` where a weaker process would have produced a fake percentage.

## 4. `draft-writer`

Shape chosen: **mechanism teardown** — the evidence is one lived sequence, not a dataset.

```markdown
## Spec
- Promise: exit criteria decide the PO; write them first
- Length: 1,200 (min 900 / max 1,400)
- Shape: mechanism — outcome, three steps, failure mode, your version
- Takeaway: the clause to add before the pilot starts
- Tone dial: direct, unshowy
```

The opening, first attempt and second:

> ~~"In today's climate tech landscape, pilots are an essential step..."~~ (deleted: throat-clearing, and it contains a word from the banned list)
>
> "Our pilot contract said 'successful demonstration.' The utility read that as: they liked the demo. We read it as: they were going to buy something. Nine months later we found out which of us was right."

## 5. `line-editor`

Cut 1,310 → 1,090 words (−17%). Blockers found: two.

```
| # | Change | Reason | Severity |
| 1 | Deleted "87% of pilots fail" | No source, no methodology, unresolvable | blocker |
| 2 | Turns out the count was 2, so "across the sector" → "in the two we audited" | Overclaim | blocker |
| 3 | Cut ¶2 (context on hardware startups) | Reader already knows; opens faster at ¶3 | should-fix |
| 4 | "leverage" → "use" | Banned word | should-fix |
| 5 | Split the 44-word sentence in ¶7 | Breath test | optional |
```

The first blocker is the important one: a plausible, widely repeated statistic with no traceable origin. Deleting it makes the piece *stronger* — the two audited contracts are the evidence, and the piece now says so.

## 6. `publish-and-repurpose`

Five titles, scored; the winner is the claim, not the topic:

- ~~"Pilot Exit Criteria: A Complete Guide"~~ (completeness, no claim)
- **"The clause that decides whether your pilot becomes a PO"** ✓

Subject line: `The clause that decides your pilot` (34 characters, no emoji, no "Re:").

The LinkedIn cut is rewritten, not truncated — first two lines:

> "Our pilot contract said 'successful demonstration.'
>
> The utility thought that meant they liked the demo. We thought it meant they were going to buy."

Checklist item that got skipped, and recorded: *image card — "skipped: no screenshot-worthy line survived the edit; the contract clause is confidential."*

## What the example is meant to show

1. **The strategy does the work.** Every downstream decision traces to `point_of_view`.
2. **Refusals are the quality bar.** The brief refused a fake statistic; the editor refused to let the claim stand; the publisher refused to truncate for LinkedIn.
3. **The pipeline keeps the author's voice** because voice was specified once, in a file, before there was anything to argue about.
4. **Evidence beats volume.** One honest sequence, clearly described, outperforms a page of hedged sector claims.
