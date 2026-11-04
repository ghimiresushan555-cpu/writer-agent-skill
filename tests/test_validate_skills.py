"""Tests for scripts/validate_skills.py — run with `make test`."""

from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_skills import split_frontmatter, validate_skill  # noqa: E402

DESCRIPTION = (
    "Writes a thing for a channel and outputs it to a file. Use when a channel "
    "needs a thing written and nobody wants to write it."
)

BODY = """
# A skill

Some genuinely useful instructions about the craft of writing things.

## References

- `references/notes.md`
"""


class FrontmatterTests(unittest.TestCase):
    def test_parses_top_level_scalars(self):
        text = textwrap.dedent(
            """\
            ---
            name: my-skill
            description: "Quoted value"
            metadata:
              version: 1.0.0
              nested: ignored
            license: MIT
            ---

            body here
            """
        )
        meta, body, error = split_frontmatter(text)
        self.assertIsNone(error)
        self.assertEqual(meta["name"], "my-skill")
        self.assertEqual(meta["description"], "Quoted value")
        self.assertEqual(meta["license"], "MIT")
        self.assertNotIn("version", meta)
        self.assertIn("body here", body)

    def test_missing_frontmatter_is_an_error(self):
        _, _, error = split_frontmatter("# no frontmatter")
        self.assertIsNotNone(error)

    def test_unclosed_frontmatter_is_an_error(self):
        _, _, error = split_frontmatter("---\nname: x\n")
        self.assertIsNotNone(error)


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make_skill(self, name="my-skill", description=DESCRIPTION, body=BODY, with_ref=True):
        skill_dir = self.root / "skills" / name
        (skill_dir / "references").mkdir(parents=True, exist_ok=True)
        if with_ref:
            (skill_dir / "references" / "notes.md").write_text("notes\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\nlicense: MIT\n---\n{body}",
            encoding="utf-8",
        )
        return skill_dir

    def test_valid_skill_passes(self):
        skill_dir = self.make_skill()
        res = validate_skill(skill_dir, self.root)
        self.assertEqual(res.errors, [])

    def test_name_must_match_directory(self):
        skill_dir = self.make_skill(name="my-skill")
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            text.replace("name: my-skill", "name: other-skill"), encoding="utf-8"
        )
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("does not match directory" in e for e in res.errors))

    def test_bad_name_format(self):
        skill_dir = self.make_skill(name="My_Skill")
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("lowercase-hyphenated" in e for e in res.errors))

    def test_long_description(self):
        skill_dir = self.make_skill(description="x" * 1100)
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("max 1024" in e for e in res.errors))

    def test_second_person_description_warns(self):
        desc = "Writes a thing to a file. Use when you need a thing written nicely."
        skill_dir = self.make_skill(description=desc)
        res = validate_skill(skill_dir, self.root)
        self.assertEqual(res.errors, [])
        self.assertTrue(any("second person" in w for w in res.warnings))

    def test_missing_use_when_warns(self):
        desc = "Writes a thing to a file for a channel that needs a thing written."
        skill_dir = self.make_skill(description=desc)
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("Use when" in w for w in res.warnings))

    def test_missing_referenced_file_is_an_error(self):
        body = BODY + "\n- `references/absent.md`\n"
        skill_dir = self.make_skill(body=body)
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("absent.md" in e for e in res.errors))

    def test_missing_shared_file_is_an_error(self):
        body = BODY + "\nSee `shared/nope.md` for details.\n"
        skill_dir = self.make_skill(body=body)
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("shared/nope.md" in e for e in res.errors))

    def test_placeholder_warns(self):
        skill_dir = self.make_skill(body=BODY + "\nTODO: finish this section.\n")
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("placeholder" in w for w in res.warnings))

    def test_empty_body_is_an_error(self):
        skill_dir = self.make_skill(body="\n\n")
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("nearly empty" in e for e in res.errors))

    def test_missing_skill_md(self):
        skill_dir = self.root / "skills" / "empty-skill"
        skill_dir.mkdir(parents=True)
        res = validate_skill(skill_dir, self.root)
        self.assertTrue(any("missing SKILL.md" in e for e in res.errors))


class RepoSkillsTests(unittest.TestCase):
    """The skills actually in this repo must pass their own validator."""

    def test_every_shipped_skill_is_valid(self):
        repo_root = Path(__file__).resolve().parent.parent
        skills_dir = repo_root / "skills"
        skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
        self.assertGreaterEqual(len(skill_dirs), 6)

        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                res = validate_skill(skill_dir, repo_root)
                self.assertEqual(res.errors, [], msg=f"{skill_dir.name}: {res.errors}")

    def test_handoff_contract_paths_exist(self):
        repo_root = Path(__file__).resolve().parent.parent
        for relative in [
            "channel.example.yaml",
            "shared/voice-guide-template.md",
            "shared/style-guide.md",
            "shared/fact-check-standards.md",
            "shared/handoff-contract.md",
        ]:
            with self.subTest(path=relative):
                self.assertTrue((repo_root / relative).is_file())


if __name__ == "__main__":
    unittest.main()
