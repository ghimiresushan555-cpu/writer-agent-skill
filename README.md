# writer-agent-skill

Six Agent Skills that run a writing channel end to end — from "who is this for" to "ship it and cut it up for social."

A writing channel is a repeating promise: the same reader, the same voice, a new piece on a schedule. Most writing tools help you produce *a document*. This pack helps you run *the channel*: it holds the strategy, scores ideas before you spend a week on one, forces research into citable claims, writes to a spec, edits with a real checklist, and packages the result for every surface it lands on.

## The pipeline

```
  channel-strategy          who it's for, the promise, the pillars, the voice
        │                   → channel/channel.yaml + channel/voice-guide.md
        ▼
    idea-engine             raw inputs → scored backlog
        │                   → ideas/<slug>.md
        ▼
   research-brief           claims, sources, counterpoints, narrative spine
        │                   → briefs/<slug>.md
        ▼
    draft-writer            writes the piece to spec, in voice
        │                   → drafts/<slug>.md
        ▼
     line-editor            cuts, tightens, fact-checks, logs every change
        │                   → drafts/<slug>.edited.md
        ▼
 publish-and-repurpose      titles, dek, SEO, subject lines, social cuts
                            → published/<slug>.md + checklist
```

Each stage reads what the previous stage wrote, so you can start anywhere (`draft-writer` works from a brief *or* from a bare idea with a warning) and re-enter the pipeline when something changes.

## What's inside

| Skill | Use it when | Writes |
| --- | --- | --- |
| [`channel-strategy`](skills/channel-strategy/SKILL.md) | Starting a channel, or it has drifted and you can't say who it's for | `channel/channel.yaml`, `channel/voice-guide.md` |
| [`idea-engine`](skills/idea-engine/SKILL.md) | The backlog is empty, or full of ideas you can't rank | `ideas/<slug>.md`, `ideas/backlog.csv` |
| [`research-brief`](skills/research-brief/SKILL.md) | An idea is approved and you need something true to write from | `briefs/<slug>.md` |
| [`draft-writer`](skills/draft-writer/SKILL.md) | You have a brief and need a first draft that isn't a pile of notes | `drafts/<slug>.md` |
| [`line-editor`](skills/line-editor/SKILL.md) | The draft is done and probably 20% too long | `drafts/<slug>.edited.md` |
| [`publish-and-repurpose`](skills/publish-and-repurpose/SKILL.md) | The piece is edited and needs to actually go out | `published/<slug>.md` |

Shared craft lives in [`shared/`](shared): the universal style guide, the voice-guide template the strategy skill fills in, fact-check standards, and the handoff contract that keeps the six skills agreeing about file names.

## Quickstart

**Claude Code** — copy the skills into your project:

```bash
git clone https://github.com/ghimiresushan555-cpu/writer-agent-skill.git
cd writer-agent-skill
make install            # copies skills/* into .claude/skills/
```

Then, in Claude Code:

```
> use channel-strategy to set up a channel for a weekly newsletter
  about climate tech for startup operators
```

The `shared/` docs (style guide, voice-guide template, fact-check standards, handoff contract) deliberately stay at the repo root, so run Claude Code from the checkout — every skill refers to them by repo-relative path.

**Claude apps / API** — zip a skill folder (the one containing `SKILL.md`) and upload it, or point your agent at the path. Each skill is self-contained; the `shared/` docs are referenced by relative path, so keep the repo layout intact.

## How the skills stay in agreement

Every skill starts by reading `channel/channel.yaml` if it exists and refusing to invent what it doesn't find. That file is the single source of truth for audience, promise, pillars, cadence, and voice knobs; if a skill needs something it isn't there, it asks or flags the gap instead of guessing. The [handoff contract](shared/handoff-contract.md) pins down file paths and the fields each stage hands to the next.

```yaml
# channel/channel.yaml (abridged — see channel.example.yaml)
audience:
  who: "operators at 10–200 person climate-tech startups"
  they_want: ["fewer dead ends", "language for selling to utilities"]
positioning:
  promise: "one useful thing you can do Monday, every Tuesday"
voice:
  person: "first-person plural"
  reading_level: 9
```

## Design principles

- **Spec before prose.** Every stage writes a machine-readable spec (length, structure, promise, claims) before it writes sentences. Drafts that miss a spec are rejected by `line-editor`.
- **Claims carry sources or they don't ship.** `research-brief` marks every load-bearing claim `sourced`, `needs-check`, or `opinion`. `line-editor` fails the draft if a `needs-check` claim is still standing.
- **Cuts are the edit.** The editor's job is deletion and specificity, not rewriting in its own voice. Every change is logged with a severity so the author can reject it.
- **The channel is the context, not the prompt.** Voice and audience live in a file, so six skills and six months of drafts all sound like one person.
- **Small skills, deep references.** `SKILL.md` stays scannable; the long checklists live in `references/` and get loaded only when needed.

## Validating

```bash
make check        # validates every SKILL.md + runs the test suite
```

The validator enforces the Agent Skills frontmatter contract (name matches folder, lowercase-hyphen, description ≤1024 chars and written in third person), checks that every `references/` link in a body resolves, and warns when a `SKILL.md` grows past a screen and should push detail into `references/`. CI runs it on every push.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New skills must compose with the existing six — if yours needs a new file in the pipeline, add it to the handoff contract first.

## License

MIT — see [LICENSE](LICENSE).
