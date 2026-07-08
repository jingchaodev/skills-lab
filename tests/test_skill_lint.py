import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "tools" / "skill_lint.py"
FIXTURES = ROOT / "tests" / "fixtures"


class SkillLintTests(unittest.TestCase):
    maxDiff = None

    def run_lint(self, skills_dir):
        return subprocess.run(
            [sys.executable, str(LINTER), str(skills_dir)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_clean_fixture_passes_with_summary(self):
        result = self.run_lint(FIXTURES / "clean_skills")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUMMARY: 2 skills, 0 ERROR, 0 WARN", result.stdout)
        self.assertIn("clean-one: OK", result.stdout)
        self.assertIn("clean-two: OK", result.stdout)

    def test_planted_violations_report_errors_warnings_and_exit_1(self):
        result = self.run_lint(FIXTURES / "bad_skills")
        self.assertEqual(result.returncode, 1)
        out = result.stdout
        self.assertIn("ERROR", out)
        self.assertIn("WARN", out)
        self.assertIn("missing-skill-md", out)
        self.assertIn("SKILL.md missing with exact casing", out)
        self.assertIn("bad-name: ERROR name must be kebab-case", out)
        self.assertIn("bad-name: ERROR name 'bad_name' must match directory name 'bad-name'", out)
        self.assertIn("wrong-frontmatter: ERROR frontmatter must start with ---", out)
        self.assertIn("no-description: ERROR frontmatter missing required field: description", out)
        self.assertIn("long-description: WARN description is", out)
        self.assertIn("huge-body: WARN body is", out)
        self.assertIn("dupe-a: ERROR duplicate skill name 'same-name'", out)
        self.assertIn("dupe-b: ERROR duplicate skill name 'same-name'", out)
        self.assertIn("trigger-one: WARN quoted trigger phrase 'panic button' also appears in: trigger-two", out)
        self.assertIn("trigger-two: WARN quoted trigger phrase 'panic button' also appears in: trigger-one", out)
        self.assertIn("generic-trigger: WARN quoted trigger phrase 'review' is a generic single-word trigger", out)

    def test_default_skills_dir_is_relative_to_cwd(self):
        result = subprocess.run(
            [sys.executable, str(LINTER)],
            cwd=FIXTURES / "default_cwd",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUMMARY: 1 skills, 0 ERROR, 0 WARN", result.stdout)


if __name__ == "__main__":
    unittest.main()
