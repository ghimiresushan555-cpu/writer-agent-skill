# Scoring ideas

Score 1–5. Use the anchor descriptions — a score without an anchor is a mood.

## Specificity (weight 1.5)

Does the idea make a claim someone could disagree with?

| 1 | 3 | 5 |
| --- | --- | --- |
| A topic. "Procurement." Nothing could fail it. | A narrow topic with an implied argument. "Why procurement kills pilots." | A claim with a named opponent. "Procurement doesn't kill pilots — weak success criteria do, and here's the document that proves it." |

Disqualifier: 1–2.

## Audience fit (weight 1.5)

| 1 | 3 | 5 |
| --- | --- | --- |
| Serves no pillar, or serves a pillar but no stated reader want. | Serves a pillar; the reader would read it if it appeared. | Serves a pillar *and* a listed `they_want` or `they_struggle_with`; the reader would search for it. |

## Evidence (weight 2 — the heaviest axis)

| 1 | 3 | 5 |
| --- | --- | --- |
| We'd be summarizing other people's published work. | We have a little first-hand material plus public sources to build on. | We have data, a named experience, or access that nobody else writing on this has. |

Disqualifier: 1–2. The most common reason a piece is boring is that the author had nothing the reader couldn't google.

## Timeliness (weight 1)

| 1 | 3 | 5 |
| --- | --- | --- |
| Evergreen with no hook; could run any year, so it runs never. | A soft occasion: a recent conversation, a slowly building trend. | A hard hook inside the next four weeks: a rule change, a dataset drop, a launch, a public failure. |

## Durability (weight 1)

| 1 | 3 | 5 |
| --- | --- | --- |
| Dead in a week — reaction to a single news event. | Good for six months; a useful explanation of a current situation. | Still cited in two years; a mechanism, a method, or a post-mortem. |

Timeliness and durability pull against each other deliberately. The best ideas score 4+ on both by pairing a durable mechanism with a current hook.

## Effort (weight 0.5, inverted)

| 1 | 3 | 5 |
| --- | --- | --- |
| Needs original research, multiple interviews, or data we'd have to build. | Two or three verification calls, one existing dataset. | We could write it today from what's already on hand. |

Low effort is a tiebreaker, not a strategy. A backlog of only 5s here becomes a stream of thin posts.

## Weights and total

```
total = specificity×1.5 + audience×1.5 + evidence×2 + timeliness + durability + effort×0.5
```

Maximum 37.5. In practice:

- **30+** — write it next.
- **22–29** — keep in the backlog; it becomes writable when the missing evidence arrives.
- **below 22** — kill it, or rework it until the failing axis improves.

## Rehabilitating a low score

Before killing, try one move per weak axis:

- **Specificity 2** → Add the opponent. Who is this arguing with?
- **Evidence 2** → Change the piece: instead of claiming the general truth, report the one case you actually have.
- **Timeliness 2** → Find the hook, or accept it's an evergreen and schedule it in a slow month.
- **Effort 2** → Cut the scope to the smallest claim that still helps: one section of the intended essay.

If two axes stay at 2, kill it and write the reason in the backlog's `notes`. A killed idea with a reason is an asset; a zombie idea is a tax on every future planning session.
