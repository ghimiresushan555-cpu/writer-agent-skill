# Contributing

## Before you open a pull request

1. Scaffold with the bundled generator so the shape is right from the start:

   ```bash
   python3 skills/agent-skill-authoring/scripts/new_skill.py my-skill --dir skills/
   ```

2. Validate, including strict mode, and fix every warning:

   ```bash
   python3 skills/agent-skill-authoring/scripts/validate_skill.py skills/ --strict
   ```

3. Run any script you added at least once against real input. A script that has
   never executed should not be merged.

4. Add the skill to the table in `README.md`.

## Bar for a new skill

- **Reusable.** It encodes a procedure you have run more than once, not a
  one-off preference.
- **Bounded.** The `description` says what it does *and* when to use it, and
  names what it does not cover.
- **Self-sufficient body.** The common case works without opening `references/`.
- **Under 500 lines** in `SKILL.md`. Depth goes into `references/`.
- **Deterministic work is scripted.** If a step is mechanical, ship the script
  instead of describing it.

## Style

- Third person in `description`, imperative in the body.
- No time-sensitive phrasing, no marketing copy, no changelog inside a skill.
- English names, kebab-case directories, `name` matching the directory.
- Every relative path in a body must resolve inside the skill directory.

## Layout

One skill per directory under `skills/`. Keep helper files inside their own
skill so the directory can be copied into another project intact. Do not add a
file named `SKILL.md` anywhere except as a skill entry point — templates use a
`.tmpl` suffix for that reason.
