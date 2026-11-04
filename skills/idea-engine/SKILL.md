---
name: idea-engine
description: Generates and scores article and newsletter ideas against a channel's audience, pillars, and evidence, then writes the winners to ideas/<slug>.md with a ranked ideas/backlog.csv. Use when the backlog is empty, when ideas exist but nobody can rank them, when every idea feels generic, or when a pillar has been neglected for weeks.
license: MIT
metadata:
  version: 1.0.0
  pack: writer-agent-skill
---

# Idea engine

An idea is not a topic. "Battery recycling" is a topic; it can produce ten interchangeable essays. An idea carries a **claim**, an **audience reason to care now**, and **evidence you uniquely have**. This skill produces the second kind and throws away the first.

## Process

### 1. Load the channel

Read `channel/channel.yaml`. If it's missing, stop and say: *"I need `channel/channel.yaml` — run `channel-strategy` first, or paste your audience and pillars and I'll work from those for this session."* Do not invent pillars.

Also read `ideas/backlog.csv` if it exists. Never re-propose something already in it; if you have a genuinely different angle on a used idea, mark it `derivative-of: <slug>`.

### 2. Gather raw material

Ask for, or accept, any of these — the more specific, the better ideas:

- first-hand experience (a launch, a failure, a customer call)
- a surprising number the user has seen
- a recurring question from customers or readers
- a strong reaction to something someone else published
- a task the user repeats manually

If the user has nothing, generate from the pillars plus the audience's stated struggles — but label those ideas `origin: generated` so nobody mistakes them for earned insight.

### 3. Generate wide, then narrow

Produce **12–20 candidates** before scoring anything. Use these prompt shapes, which reliably produce claims rather than topics:

- **The correction:** "Everyone says X. The operators I've watched do Y." 
- **The receipt:** "We spent $______ learning ______, so you don't have to."
- **The mechanism:** "Here is the actual sequence nobody writes down."
- **The threshold:** "This stops working past ______, and here's how you know."
- **The translation:** "Your CFO calls this ______. Engineering calls it ______. They're not talking about the same thing."
- **The post-mortem:** "It failed. Three reasons, one of which was avoidable."
- **The uncomfortable comparison:** "Compare these two numbers and the conventional wisdom collapses."

Reject on sight: "X vs Y," "the ultimate guide to," "N lessons from," "why X matters," anything whose promise is *completeness* rather than a claim.

### 4. Score

Score every candidate 1–5 on six axes (see `references/scoring.md`):

| Axis | Question |
| --- | --- |
| **Specificity** | Is there a claim a reader could disagree with? |
| **Audience fit** | Does it serve a pillar and a stated want? |
| **Evidence** | Do we have first-hand material, or only vibes? |
| **Timeliness** | Is there a reason to publish it within a month? |
| **Durability** | Will it still be worth reading in a year? |
| **Effort** | Inverted: 5 = cheap to research and write |

Weighted total: `specificity × 1.5 + audience × 1.5 + evidence × 2 + timeliness × 1 + durability × 1 + effort × 0.5`. Any idea scoring 1 or 2 on evidence or specificity is disqualified regardless of total — those are the two failure modes that produce pleasant, useless drafts.

### 5. Write the winners

For each of the top 3–5 (or however many the user asks for), write `ideas/<slug>.md`:

```markdown
---
slug: battery-recycling-margins
title: "The recycling credit nobody budgets for"
status: idea
pillar: "Margins and money"
score: 34.5
origin: first-hand | generated | reaction
created: 2026-11-04
evidence: strong | partial | none
supersedes: (optional)
---

## The promise
One sentence a reader would repeat to a colleague. Must contain a claim.

## Why this channel
Which pillar, which stated want it serves, and why now rather than in six months.

## Angle
The specific argument, in two or three sentences. State what it argues *against*.

## Evidence we already have
Bulleted, with sources where they exist. "Nothing yet" is an acceptable and useful answer.

## What we'd need to verify
The research assignment, handed straight to `research-brief`.

## The shape
A guessed structure — three to five section heads, good enough to sanity-check length.

## Failure mode
How this piece goes wrong: the version of it that gets written by a tired person and reads like every other take.
```

The **Failure mode** section is not optional. Naming the bad version is what keeps the good version alive through brief, draft, and edit.

### 6. Update the backlog

Append to `ideas/backlog.csv` (create from `assets/backlog.csv` if absent):

```
slug,title,pillar,score,evidence,status,origin,created,notes
```

`status` walks `idea → briefed → drafted → edited → published → killed`. Sort by score descending when reporting; keep the file in creation order and let tools sort.

### 7. Report

A ranked table of the top five with one-line reasons, plus:

- **Safest bet:** highest score with strong evidence
- **Best bet:** highest score overall, with what makes it risky
- **Kill list:** the candidates you discarded and the one-line reason (this teaches the user the filter)

## Refuse when

- There's no `channel.yaml` and the user won't supply audience/pillars. Ideas generated for "everyone" are the reason content calendars fill with sludge.
- The user asks for volume — "give me 50 ideas." Offer 15 scored instead and explain that unscored volume is the same as zero. If they insist, produce 30 with the top 10 scored.

## References

- `references/scoring.md` — every axis, with 1/3/5 anchors so two people score the same idea similarly
- `assets/backlog.csv` — the backlog schema
- `shared/handoff-contract.md` — what `research-brief` expects to receive
