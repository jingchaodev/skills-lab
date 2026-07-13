import json
import subprocess
import sys
import tempfile
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
            "never infer a private path from memory, profile context, or the current environment",
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
        files = [path for path in SKILL.rglob("*") if path.is_file()]
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

    def run_payload(self, payload):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8") as handle:
            json.dump(payload, handle)
            handle.flush()
            validator = SKILL / "scripts" / "validate_sources.py"
            return subprocess.run(
                [sys.executable, str(validator), handle.name, "--json"],
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

    def test_validator_rejects_empty_collection(self):
        result = self.run_payload([])
        self.assertEqual(result.returncode, 1)
        self.assertIn("at least one source", json.loads(result.stdout)["errors"][0])

    def test_validator_rejects_empty_values_bad_date_and_missing_language(self):
        payload = {
            "id": "",
            "title": "",
            "speakers": ["Founder"],
            "publisher": "",
            "published_at": "yesterday",
            "url": "https://example.com/interview",
            "media_type": "",
            "transcript": {"status": "available", "provenance": "official", "word_count": 10},
        }
        result = self.run_payload(payload)
        self.assertEqual(result.returncode, 1)
        errors = json.loads(result.stdout)["errors"]
        for field in ["id", "title", "publisher", "published_at", "media_type", "language"]:
            self.assertTrue(any(field in error for error in errors), field)

    def test_validator_accepts_available_transcript_with_unknown_word_count(self):
        payload = {
            "id": "source",
            "title": "Interview",
            "speakers": ["Founder"],
            "publisher": "Publisher",
            "published_at": "2026-01-15",
            "url": "https://example.com/interview",
            "media_type": "video",
            "transcript": {
                "status": "available",
                "provenance": "publisher-transcript",
                "language": "en",
                "word_count": None,
            },
        }
        result = self.run_payload(payload)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_validator_rejects_impossible_calendar_date(self):
        payload = {
            "id": "source",
            "title": "Interview",
            "speakers": ["Founder"],
            "publisher": "Publisher",
            "published_at": "2026-99-99",
            "url": "https://example.com/interview",
            "media_type": "video",
            "transcript": {
                "status": "unavailable",
                "provenance": "unavailable",
                "language": "en",
                "word_count": 0,
            },
        }
        result = self.run_payload(payload)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(
            any("published_at" in error and "calendar" in error for error in json.loads(result.stdout)["errors"])
        )

    def test_validator_rejects_status_url_and_canonical_url_inconsistencies(self):
        base = {
            "id": "source",
            "title": "Interview",
            "speakers": ["Founder"],
            "publisher": "Publisher",
            "published_at": "2026-01-15",
            "url": "https://example.com/interview",
            "media_type": "video",
            "transcript": {
                "status": "unavailable",
                "provenance": "unavailable",
                "language": "en",
                "word_count": 0,
            },
        }
        cases = [
            ("available zero word count", {**base, "transcript": {**base["transcript"], "status": "available", "provenance": "official", "word_count": 0}}, "word_count"),
            ("unavailable word count", {**base, "transcript": {**base["transcript"], "word_count": 99}}, "word_count"),
            ("nested private url", {**base, "related": {"media_url": "http://127.0.0.1/private"}}, "related.media_url"),
            ("credential url", {**base, "url": "https://user:secret@example.com/x"}, "credentials"),
            ("nested credential url", {**base, "media_url": "https://user:secret@example.com/x"}, "credentials"),
            ("search result url", {**base, "url": "https://www.youtube.com/results?search_query=x"}, "search-results"),
            ("short YouTube search result", {**base, "url": "https://youtu.be/results?search_query=x"}, "search-results"),
            ("Google search result", {**base, "url": "https://www.google.com/search?q=x"}, "search-results"),
            ("Bing search result", {**base, "url": "https://www.bing.com/search?q=x"}, "search-results"),
            ("DuckDuckGo search result", {**base, "url": "https://duckduckgo.com/?q=x"}, "search-results"),
            ("nested search result url", {**base, "episode_url": "https://www.youtube.com/results?search_query=x"}, "search-results"),
        ]
        for name, payload, marker in cases:
            with self.subTest(name=name):
                result = self.run_payload(payload)
                self.assertEqual(result.returncode, 1)
                self.assertTrue(any(marker in error for error in json.loads(result.stdout)["errors"]))

    def test_validator_rejects_private_url_and_nested_private_value(self):
        payload = {
            "id": "source",
            "title": "Interview",
            "speakers": ["Founder"],
            "publisher": "Publisher",
            "published_at": "2026-01-15",
            "url": "http://192.168.1.20/interview",
            "media_type": "video",
            "notes": [{"path": "/home/alice/private/notes.md"}],
            "transcript": {
                "status": "unavailable",
                "provenance": "unavailable",
                "language": "en",
                "word_count": 0,
            },
        }
        result = self.run_payload(payload)
        self.assertEqual(result.returncode, 1)
        errors = json.loads(result.stdout)["errors"]
        self.assertTrue(any("url" in error and "private" in error for error in errors))
        self.assertTrue(any("notes[0].path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
