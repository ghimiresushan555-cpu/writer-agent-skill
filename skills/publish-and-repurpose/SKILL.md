---
name: publish-and-repurpose
description: Packages an edited piece for publication — title options, dek, SEO metadata, subject lines, and native cuts for each distribution surface — plus a publish checklist, written to published/<slug>.md. Use when a piece is edited and blocked-free and needs to actually ship, when a good piece is being published once and forgotten, when headlines keep underperforming, or when one essay needs to become a newsletter, a post, and a thread without sounding copy-pasted.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---

# Publish and repurpose

Publishing is a set of decisions, not a button. Most pieces die from four unforced errors: a title that only makes sense after reading, a subject line with no reason to open, a social post that is just the link, and no checklist — so the canonical URL, the alt text, and the disclosure all get missed at 11pm.

## Process

### 1. Confirm it's shippable

Load `drafts/<slug>.edited.md`, `channel/channel.yaml`, and `channel/voice-guide.md`.

Refuse to continue if `blockers > 0`. Publication converts an error into a public correction.

Then gather the facts you'll need downstream: canonical URL, publication date and time, byline, word count, estimated read time (`words / 220`), disclosures, and the piece's one-sentence takeaway.

### 2. Write five titles, then choose

Titles do different jobs on different surfaces, so don't write one title and adapt it four times.

Produce five options, each in a distinct mode:

1. **The claim** — states the argument ("Pilot success criteria are the product")
2. **The number** — leads with the most surprising figure
3. **The tension** — names the conflict without resolving it
4. **The search** — how the reader would actually phrase it
5. **The refusal** — what the channel won't do ("We stopped running pilots. Here's what replaced them.")

Then score each: clarity (does it survive with no context?), specificity, honesty (does the piece deliver it?), and length (under ~60 characters for sharing). State the winner and why, and name the runner-up for A/B testing if it's close.

Rules: no colons unless the second half earns it, no "why X matters," no clickbait the piece doesn't pay off, and never a title whose meaning depends on the subtitle.

The **dek** is one sentence, 15–30 words, that gives the reason to read past the title — not a summary.

### 3. SEO without writing for robots

- **Primary search phrase:** what a reader would type, in their words. One per piece.
- **Meta description:** 140–160 characters, containing the phrase naturally and a reason to click.
- **Slug:** the canonical URL path, matching `ideas/` slug where possible.
- **Structure:** one H1, H2s that are questions or claims; the primary phrase appears in the H1, the first 100 words, and one H2.
- **Internal links:** two or three to earlier pieces, with descriptive anchor text.

Say plainly if the piece has no search intent — essays often don't, and pretending otherwise produces stuffed, worse prose. In that case: optimise for sharing and email, and say so.

### 4. Write the subject lines

For email surfaces, produce five, using different levers:

| Lever | Example shape |
| --- | --- |
| Curiosity with a stake | "The clause that killed our pilot" |
| Specific number | "We lost 2 of 11 customers raising prices 30%" |
| Direct benefit | "A procurement checklist you can use Monday" |
| The disagreement | "Most pilot advice is wrong, and here's the document that shows it" |
| Plain and personal | "Notes from two weeks on site" |

Keep under 45 characters where possible (mobile truncation), no emoji unless the voice guide allows it, no "Re:" fakery, no ALL CAPS. Pick one primary and one backup; note which segment each suits if there's more than one list.

Preview text (the 40–90 characters after the subject) is separate copy — write it, don't let the first line of the body do it by accident.

### 5. Build native cuts per surface

Read `surfaces` in `channel.yaml`. For each, write copy that stands alone — reformatted, not truncated.

- **LinkedIn:** 150–300 words. First two lines must work before the "see more" fold. One idea, one number, no link in the body if reach matters (put it in the comments and say so).
- **X/Twitter:** a single post under 280 characters that makes a claim, or a thread of 5–7 posts where each is a complete thought and the first is the whole argument compressed.
- **Newsletter excerpt:** 40–60 words plus the link and a one-line reason to click.
- **Blog:** canonical, with internal links and a date.
- **Image or quote card:** one sentence, lifted verbatim, attributed.

Each cut must be readable by someone who never sees the original. Never post the dek with the link attached — that's the copy-paste tell.

### 6. Ship checklist

Copy `assets/publish-checklist.md`. Every item gets a tick, or an explicit "not done, because ______." No silent skips.

The non-negotiables: claim verification confirmed, links resolve, canonical URL set, disclosure present, alt text written, subject line tested on a phone, and a scheduled slot in a window when the audience actually reads (check the channel's own open data before trusting general advice).

### 7. Write the file and report

`published/<slug>.md`, with the body as published, then `## Packaging` and `## Checklist`.

Report:

```
Published: published/<slug>.md — "<chosen title>"
Surfaces: newsletter, blog, linkedin, x — all native
Watch: <the surface most likely to underperform, and why>
Next: schedule the follow-up piece <slug>, because this one opens a question
```

Close the loop: suggest the next idea the piece created, and note the backlog row to update to `status: published`.

## Refuse when

- Blockers remain in the edited draft.
- The user asks for the same copy on every surface. Truncated cross-posting is the reason repurposing gets a bad name; make the case once, then do it their way if they insist — but label it in the report.
- There's no way to verify a claim and the user wants to publish anyway. Offer the softening edit, and if refused, record the decision in the checklist so the choice is documented.

## References

- `references/channel-formats.md` — per-surface constraints, lengths, and the native moves for each
- `assets/publish-checklist.md` — the ship checklist
- `shared/handoff-contract.md` — what the final file must contain
