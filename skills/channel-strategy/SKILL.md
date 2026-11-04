---
name: channel-strategy
description: Designs or revises the strategy for a writing channel — audience, positioning promise, content pillars, cadence, and voice — and writes it to channel/channel.yaml plus channel/voice-guide.md. Use when starting a newsletter, blog, or publication, when a channel has drifted and nobody can say who it's for, when issues feel interchangeable with everyone else's, or before running any other skill in this pack for the first time.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---

# Channel strategy

The other five skills in this pack read two files: `channel/channel.yaml` and `channel/voice-guide.md`. This skill is the only one allowed to write them. Everything downstream inherits the decisions made here, so a vague strategy becomes six months of vague drafts.

## The bar

A finished strategy passes one test: **a stranger could read `channel.yaml` and reject a bad idea without asking you a question.** If they'd have to ask "but who's it for really?", the strategy isn't done.

## Process

### 1. Read what exists

Look for `channel/channel.yaml`, `channel/voice-guide.md`, and anything in `drafts/` or `published/`.

- **Exists and the user wants a revision:** treat the current files as the baseline. Ask what's wrong before proposing changes — the diagnosis is the work.
- **Exists and the user wants a fresh start:** move the old files to `channel/archive/channel-<YYYY-MM-DD>.yaml` rather than deleting. Nothing is less useful than a strategy you can't compare against.
- **Doesn't exist:** start at step 2.

### 2. Interview, don't audit

Ask in small batches — never a wall of twelve questions. Use `references/interview.md`. The five that matter most, in order:

1. **Who is the one reader?** Not a segment. A job title at a company size, or a named person you're picturing.
2. **What do they already believe that you think is wrong?** This is the channel's reason to exist. If the answer is "nothing," the channel is entertainment and should be planned as such.
3. **What have you got that nobody else has?** Data, scars, access, a specific method. If the answer is "good writing," stop and say so.
4. **What does a reader do differently after an issue?** If the answer is "feel informed," push back once.
5. **How often can you actually ship, on your worst week?** Cadence is a promise, not an ambition.

Ask one at a time when the answers are load-bearing; batch only the easy ones. If the user says "just pick something," pick, but label every guess with `# assumed:` in the YAML so it can be corrected later.

### 3. Find the wedge

Before writing files, state the channel in one line and check it against the competition:

> **This channel is for ______ who want ______, and it's different because ______.**

Then run the three tests:

- **Replaceable test.** Swap in a competitor's name. Does the sentence still hold? Then there's no wedge.
- **Ten-issue test.** Can you name ten issues that fit? If not, the pillar is a one-off essay, not a pillar.
- **Boredom test.** Will you still care in issue 40? A channel dies of author boredom before reader boredom.

If any test fails, go back to the interview — don't paper over it in the YAML.

### 4. Choose pillars by subtraction

Three to four pillars, each with a one-line promise and a target share of issues (shares should sum to ~1.0). Pillars answer "what is this channel *about*," not "what topics might come up."

Good pillar: **"Procurement, decoded — the actual steps, documents, and people between a pilot and a PO."**
Bad pillar: **"Industry trends."** (Nothing can fail it, so nothing can be planned against it.)

Assign every pillar an exit condition: the number of issues after which you'll review whether it's working.

### 5. Set cadence you can survive

Work backwards from the publish day, and use the *worst* week, not the best. Record `lead_time_days` honestly. Then pick the format that fits the constraint rather than stretching the constraint to fit the format — a 600-word field note that ships beats a 2,000-word essay that doesn't.

### 6. Write the voice guide

Copy `shared/voice-guide-template.md` and fill it in **with two real calibration samples**: a paragraph that is exactly on-voice, and a paragraph that is exactly off-voice, both on the same subject. These samples do more work than the adjectives — downstream skills pattern-match against them.

Pull the banned list from the user's own drafts where possible: read three things they've written, and name the tics to kill.

### 7. Write the files

```bash
mkdir -p channel
# write channel/channel.yaml from channel.example.yaml, then channel/voice-guide.md
```

Validate before handing back:

- [ ] `audience.who` names a specific person, not a demographic
- [ ] `positioning.point_of_view` is falsifiable — someone could disagree
- [ ] Every pillar has a promise a stranger could use to reject an off-topic idea
- [ ] `cadence.target_words` sits between `min_words` and `max_words`
- [ ] `voice.banned_words` has at least five specific entries
- [ ] The voice guide has both calibration samples, on the same subject
- [ ] Any guess is marked `# assumed:` in the YAML

### 8. Report

End with three lines, not a summary essay:

```
Strategy: <the one-line wedge>
Pillars: <n>, sharing <x/y/z>
Watch out: <the single most likely way this drifts>
```

Then offer the next step: `idea-engine` to fill the backlog, or a revision pass once they read it.

## Refuse when

- The user wants a strategy for a channel they won't write. Say what the YAML can't fix: the voice guide needs their prose to calibrate against, and the first three issues are the strategy.
- The user asks for an SEO-driven content plan with no point of view. You can produce it — but say plainly that this pack optimises for a repeatable promise, and a keyword plan will fight every downstream skill.

## References

- `references/interview.md` — the full question bank, in the order that gets useful answers
- `shared/voice-guide-template.md` — the fill-in-the-blanks voice guide
- `channel.example.yaml` — the schema, with realistic values
- `shared/handoff-contract.md` — what downstream skills expect to find
