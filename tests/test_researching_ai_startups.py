import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "researching-ai-startups"
LINTER = ROOT / "tools" / "skill_lint.py"


class ResearchingAIStartupsTests(unittest.TestCase):
    def test_required_package_files_exist(self):
        expected = [
            "SKILL.md",
            "docs/design.md",
            "docs/implementation-plan.md",
            "evals/scenarios.md",
            "evals/baseline.md",
            "references/company-selection.md",
            "references/single-company-research.md",
            "references/source-quality.md",
            "references/interview-notes.md",
            "references/output-formats.md",
            "templates/company-selection.md",
            "templates/company-index.md",
            "templates/source-metadata.json",
            "templates/interview-note.md",
            "scripts/validate_sources.py",
        ]
        missing = [path for path in expected if not (SKILL / path).is_file()]
        self.assertEqual(missing, [])

    def test_skill_contract_uses_plain_language_and_two_modes(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for phrase in [
            "Company selection",
            "Single-company research",
            "Do not decide whether the user should join",
        ]:
            self.assertIn(phrase, text)
        for jargon in ["Company dossier", "Technical wedge", "Artifact set"]:
            self.assertNotIn(jargon, text)

    def test_skill_routes_to_required_references(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in [
            "references/company-selection.md",
            "references/single-company-research.md",
            "references/source-quality.md",
            "references/interview-notes.md",
            "references/output-formats.md",
        ]:
            self.assertIn(path, text)

    def test_metadata_template_is_valid_and_complete(self):
        data = json.loads(
            (SKILL / "templates" / "source-metadata.json").read_text(encoding="utf-8")
        )
        required = {
            "id",
            "title",
            "speakers",
            "publisher",
            "published_at",
            "url",
            "media_type",
            "transcript",
        }
        self.assertTrue(required.issubset(data))
        self.assertTrue(
            {"status", "provenance", "language", "word_count"}.issubset(
                data["transcript"]
            )
        )

    def test_operational_files_have_no_private_environment_assumptions(self):
        forbidden = [
            "/root/",
            "/Users/",
            "Tailscale",
            "MemoryKit",
            "Telegram",
            "100.108.",
            "jingchao",
        ]
        roots = [SKILL / "SKILL.md", SKILL / "references", SKILL / "templates", SKILL / "scripts"]
        files = [roots[0]]
        for directory in roots[1:]:
            if directory.exists():
                files.extend(path for path in directory.rglob("*") if path.is_file())
        hits = []
        for path in files:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            hits.extend(
                f"{path.relative_to(SKILL)}: {token}"
                for token in forbidden
                if token in text
            )
        self.assertEqual(hits, [])

    def test_repository_linter_accepts_skill(self):
        result = subprocess.run(
            [sys.executable, str(LINTER), str(ROOT / "skills")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("researching-ai-startups: OK", result.stdout)

    def run_validator(self, fixture, *extra):
        validator = SKILL / "scripts" / "validate_sources.py"
        return subprocess.run(
            [sys.executable, str(validator), str(SKILL / "evals" / "fixtures" / fixture), *extra],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_validator_accepts_valid_metadata(self):
        result = self.run_validator("valid-sources.json", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["sources"], 1)
        self.assertEqual(payload["errors"], [])

    def test_validator_rejects_invalid_metadata(self):
        result = self.run_validator("invalid-sources.json", "--json")
        self.assertEqual(result.returncode, 1)
        errors = json.loads(result.stdout)["errors"]
        self.assertTrue(any("url" in error for error in errors))
        self.assertTrue(any("provenance" in error for error in errors))
        self.assertTrue(any("word_count" in error for error in errors))
        self.assertTrue(any("private path" in error for error in errors))

    def test_validator_accepts_unavailable_transcript(self):
        result = self.run_validator("unavailable-transcript.json", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["errors"], [])

    def test_validator_help(self):
        validator = SKILL / "scripts" / "validate_sources.py"
        result = subprocess.run(
            [sys.executable, str(validator), "--help"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("source metadata", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
