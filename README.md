# agents-skills

A collection of Agent Skills for AI coding agents. Each skill is a directory
under [`skills/`](skills/) containing a `SKILL.md` file — YAML frontmatter that
tells an agent what the skill does and when to load it, plus a body of
instructions and any bundled `scripts/`, `references/`, and `assets/`.

Skills follow the open [Agent Skills specification](https://agentskills.io/specification),
so the same directory works across products that implement it.

## Skills in this repository

| Skill | What it does |
| --- | --- |
| [`agent-skill-authoring`](skills/agent-skill-authoring/SKILL.md) | Scaffolds new skills and validates `SKILL.md` files against the specification |

## Install

Copy a skill directory into the skills path your agent reads. For a single
project, that is usually `.claude/skills/`, `./.agents/skills/`, or whatever
directory your tool documents; for a personal default, your home-level skills
directory.

```bash
git clone https://github.com/YOUR_NAME/agents-skills.git /tmp/agents-skills
mkdir -p .claude/skills
cp -r /tmp/agents-skills/skills/agent-skill-authoring .claude/skills/
```

Keep the whole directory: the `scripts/` and `references/` files are part of the
skill, and the body links to them by relative path.

## Validate

```bash
python3 skills/agent-skill-authoring/scripts/validate_skill.py skills/
```

Exits `0` when every skill is clean, `1` with a rule-by-rule report otherwise.
Add `--strict` to fail on warnings too. The check runs on every push and pull
request in [CI](.github/workflows/validate.yml).

## Add a skill

```bash
python3 skills/agent-skill-authoring/scripts/new_skill.py my-skill --dir skills/
```

Then edit `skills/my-skill/SKILL.md`, write the `description` before the body,
and validate. See [CONTRIBUTING.md](CONTRIBUTING.md) for the review bar.

## Layout

```
skills/<skill-name>/
├── SKILL.md          # frontmatter + instructions, loaded on activation
├── references/       # long-form detail, read only when the body points there
├── scripts/          # executable helpers the agent runs
└── assets/           # templates and files copied into output, not read
```

## License

MIT — see [LICENSE](LICENSE).
