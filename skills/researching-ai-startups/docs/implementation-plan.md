# Researching AI Startups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a portable English-language Agent Skill that supports AI startup company selection and source-driven single-company research without making employment recommendations.

**Architecture:** One orchestrating `SKILL.md` routes requests into two modes. Focused reference files hold the detailed research methods, templates define portable outputs, and a zero-dependency validator checks source metadata and private-environment leaks. Static repository tests verify package structure, trigger quality, plain-language requirements, templates, and validator behavior; agent scenarios verify behavioral changes before and after loading the skill.

**Tech Stack:** Markdown, JSON, Python 3 standard library, `unittest`, the repository’s `tools/skill_lint.py`, git.

---

## File Map

| Path | Responsibility |
|---|---|
| `skills/researching-ai-startups/evals/scenarios.md` | Stable RED/GREEN behavioral scenarios and expected failures |
| `skills/researching-ai-startups/evals/baseline.md` | Verbatim baseline observations from agents that do not receive the skill |
| `skills/researching-ai-startups/SKILL.md` | Small routing and execution contract for both research modes |
| `skills/researching-ai-startups/references/company-selection.md` | How to discover, compare, and prioritize companies for deeper research |
| `skills/researching-ai-startups/references/single-company-research.md` | Company overview, founders, product, business, culture, and careers workflow |
| `skills/researching-ai-startups/references/source-quality.md` | Source order, evidence labels, transcript provenance, and claim handling |
| `skills/researching-ai-startups/references/interview-notes.md` | Interview discovery, transcript handling, coverage, and note-series workflow |
| `skills/researching-ai-startups/references/output-formats.md` | Portable directory and output contracts, including optional HTML companions |
| `skills/researching-ai-startups/templates/company-selection.md` | Comparable company-selection report template |
| `skills/researching-ai-startups/templates/company-index.md` | Single-company research index template |
| `skills/researching-ai-startups/templates/source-metadata.json` | Machine-readable source metadata example |
| `skills/researching-ai-startups/templates/interview-note.md` | One-source-per-note research template |
| `skills/researching-ai-startups/scripts/validate_sources.py` | Standard-library validation of metadata and private assumptions |
| `tests/test_researching_ai_startups.py` | Repository-level integration tests for the self-contained skill package |
| `README.md` | Public discovery entry under Research & information |

## Task 1: Record Failing Behavioral Baselines

**Files:**
- Create: `skills/researching-ai-startups/evals/scenarios.md`
- Create: `skills/researching-ai-startups/evals/baseline.md`

**Execution note:** Run agents without exposing the proposed skill or its design document. Baseline output must reflect natural behavior rather than expectations copied from the spec.

**Test scenarios:**

- **Happy path:** Sierra, a well-documented enterprise AI company. Ask for product, founders, culture, careers, and useful interviews.
- **Sparse evidence:** A recent AI infrastructure startup with scattered official material. Ask for the same output and require unknowns to remain explicit.
- **Weak independent evidence:** A heavily promoted AI startup with strong founder marketing but limited customer proof. Ask for a company research collection.
- **Mode routing:** Ask for a landscape of agent infrastructure startups rather than a named company.

- [ ] **Step 1: Write the scenario file before running any baseline**

Create `skills/researching-ai-startups/evals/scenarios.md` with this structure:

```markdown
# Researching AI Startups Evaluation Scenarios

## Rules

Run each scenario in a fresh agent session. Do not provide the proposed skill, design spec, or expected-failure list. Record the model, date, prompt, files produced, and final response.

## S1 — Rich company evidence

Prompt: Research Sierra as a potential employer. Explain what it builds, who founded it, how its technology and culture work, what it is hiring for, and find the most useful founder or technical interviews. Organize the research into reusable notes. Do not decide whether I should join.

## S2 — Sparse company evidence

Prompt: Research a recently founded AI infrastructure startup with limited public material. Explain what is verified, what the company claims, what remains unknown, who founded it, and which interviews or talks are available. Organize the research into reusable notes. Do not invent missing facts.

## S3 — Marketing-heavy company

Prompt: Research a highly promoted AI startup whose independent customer evidence may be weak. Separate official claims, founder statements, independent evidence, and unresolved questions. Find useful interviews and organize the research into reusable notes. Do not make an employment recommendation.

## S4 — Company selection

Prompt: Map popular AI agent infrastructure startups. Explain what each company actually builds, identify founders and useful interviews, and recommend which companies deserve deeper research. Do not rank them only by funding or media attention.

## Evaluation dimensions

For each run mark PASS, PARTIAL, or FAIL for: correct mode; plain product explanation; founder identity; source URLs; transcript provenance; claim/evidence separation; explicit unknowns; one-source-per-note behavior; discovered versus completed coverage; no unsolicited employment verdict; no invented facts.
```

- [ ] **Step 2: Run at least two independent baseline agents in parallel**

Use fresh subagents with no access to `skills/researching-ai-startups/`. Give one agent S1 and S4; give the second S2 and S3. Require each to return its exact final answer, planned files, and reasoning summary.

Expected result: at least one material failure across the dimensions. If both agents already satisfy every requirement, stop and narrow the skill to the missing behavior rather than writing redundant instructions.

- [ ] **Step 3: Record baseline evidence verbatim**

Create `skills/researching-ai-startups/evals/baseline.md` with these exact sections:

```markdown
# Baseline Results Without the Skill

## Environment

## S1 — Rich company evidence

### Observed behavior

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|

## S2 — Sparse company evidence

### Observed behavior

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|

## S3 — Marketing-heavy company

### Observed behavior

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|

## S4 — Company selection

### Observed behavior

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|

## Failure patterns to address
```

Under `Environment`, record the actual ISO date, model names, and `Skill available: no`. Under each `Observed behavior`, paste the relevant output verbatim. Add one evaluation row per dimension from `scenarios.md`, using `PASS`, `PARTIAL`, or `FAIL` and a direct quote or concrete behavior. Under `Failure patterns to address`, list observed failures only.

- [ ] **Step 4: Verify the baseline files contain no placeholders**

Run:

```bash
rg -n 'TBD|TODO|<actual|<verbatim|<quote|PASS/PARTIAL' skills/researching-ai-startups/evals
```

Expected: no unresolved template markers in `baseline.md`. Template markers may remain only in fenced examples inside `scenarios.md`.

- [ ] **Step 5: Commit the RED evidence**

```bash
git add skills/researching-ai-startups/evals
git commit -m "test: record AI startup research baselines"
```

## Task 2: Add Static Contract Tests Before the Skill

**Files:**
- Create: `tests/test_researching_ai_startups.py`

**Test scenarios:**

- **Happy path:** complete package contains required English files and valid metadata template.
- **Edge cases:** no forbidden employment verdict, jargon heading, private path, or copyrighted transcript body.
- **Error paths:** validator rejects missing required metadata and private-environment strings.
- **Integration:** repository skill linter sees the new skill with zero errors and warnings.

- [ ] **Step 1: Write the failing package tests**

Create `tests/test_researching_ai_startups.py` with the following tests and helpers:

```python
import importlib.util
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
        for phrase in ["Company selection", "Single-company research", "Do not decide whether the user should join"]:
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
        data = json.loads((SKILL / "templates/source-metadata.json").read_text(encoding="utf-8"))
        required = {"id", "title", "speakers", "publisher", "published_at", "url", "media_type", "transcript"}
        self.assertTrue(required.issubset(data))
        self.assertTrue({"status", "provenance", "language", "word_count"}.issubset(data["transcript"]))

    def test_public_package_has_no_private_environment_assumptions(self):
        forbidden = ["/root/", "/Users/", "Tailscale", "MemoryKit", "Telegram", "100.108.", "jingchao"]
        hits = []
        for path in SKILL.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="ignore")
                hits.extend(f"{path.relative_to(SKILL)}: {token}" for token in forbidden if token in text)
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
/usr/bin/python3 -m unittest tests.test_researching_ai_startups -v
```

Expected: failures because `skills/researching-ai-startups/` does not exist.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_researching_ai_startups.py
git commit -m "test: define AI startup research skill contract"
```

## Task 3: Implement the Minimal Routing Skill and Research References

**Files:**
- Create: `skills/researching-ai-startups/SKILL.md`
- Create: `skills/researching-ai-startups/references/company-selection.md`
- Create: `skills/researching-ai-startups/references/single-company-research.md`
- Create: `skills/researching-ai-startups/references/source-quality.md`
- Create: `skills/researching-ai-startups/references/interview-notes.md`
- Create: `skills/researching-ai-startups/references/output-formats.md`

**Test scenarios:**

- **Happy path:** named company routes to single-company research; category request routes to company selection.
- **Edge cases:** ambiguous request starts with a small overview rather than launching uncontrolled research; transcript discovery is not counted as completed analysis.
- **Error paths:** missing facts remain unknown; inaccessible sources are not reconstructed from snippets.
- **Integration:** all detailed steps live in references and the main skill remains scannable.

- [ ] **Step 1: Write a concise `SKILL.md`**

Required frontmatter:

```yaml
---
name: researching-ai-startups
description: Use when researching AI startups, surveying a startup category, comparing AI companies, understanding what a startup builds, identifying founders, or collecting company podcasts, interviews, talks, YouTube videos, transcripts, culture evidence, and hiring signals.
---
```

The body must contain:

```markdown
# Researching AI Startups

## Core rule

Build an evidence-backed understanding of the company. Do not decide whether the user should join it.

## Choose a mode

| Request | Mode | Required reference |
|---|---|---|
| Category, market, or list of companies | Company selection | `references/company-selection.md` |
| Named company | Single-company research | `references/single-company-research.md` |

Always apply `references/source-quality.md`. For interviews, podcasts, talks, YouTube, or transcripts, also apply `references/interview-notes.md`. Before writing files, apply `references/output-formats.md` and honor the project’s requested output location and format.
```

Add a numbered happy path:

1. confirm the research question and existing files;
2. choose the mode;
3. make a coverage map before searching;
4. search primary sources first and contradictory evidence deliberately;
5. retrieve complete sources before interpreting them;
6. write only claims supported by the recorded source;
7. mark unknowns and discovered-but-unprocessed sources;
8. validate output against the requested format.

Explicit prohibitions:

- Do not issue `Join`, `Watch`, or `Pass` verdicts.
- Do not rank quality by funding or media attention.
- Do not treat founder claims as independent evidence.
- Do not treat customer logos as verified production use.
- Do not count a downloaded transcript as completed research.
- Do not download audio or video unless the user asks.
- Do not write from search snippets when the full source can be opened.

- [ ] **Step 2: Write `company-selection.md`**

Define:

- input: category, time frame, geography if relevant, company-count target;
- discovery buckets: known companies, newer entrants, technical infrastructure, application companies, counterexamples;
- required row fields from the design spec;
- research-priority factors: relevance, product clarity, technical distinctiveness, source quality, founder interviews, hiring relevance, independent evidence;
- an explicit note that priority means “worth deeper research,” not “good employer”;
- stop conditions: requested company count reached, source diversity achieved, and important gaps named.

Include the exact output table from `templates/company-selection.md` and a source list grouped by company.

- [ ] **Step 3: Write `single-company-research.md`**

Define six coverage areas:

1. company overview;
2. founders;
3. product and technology;
4. business model;
5. culture;
6. careers.

For each area specify questions, preferred sources, and common overclaims. Require a coverage table with `Not started`, `Sources found`, `Note complete`, and `Evidence gap` states.

- [ ] **Step 4: Write `source-quality.md`**

Define the source order and five evidence labels exactly as:

- Direct
- Attributed
- Independent
- Inferred
- Unverified

Require URL, title, publisher, speaker or author, date, access date, and what each source supports. Require contradiction search and recency checks. State that evidence labels describe support conditions, not truth.

- [ ] **Step 5: Write `interview-notes.md`**

Include:

- interview ranking by speaker relevance, depth, transcript completeness, new coverage, date, and technical or operating detail;
- default transcript and metadata policy;
- transcript provenance values: `official`, `platform-captions`, `publisher-transcript`, `third-party`, `generated`, `unavailable`;
- one important source per note;
- discovered source versus completed note distinction;
- raw transcript copyright boundary;
- parallel-worker rule: workers may write separate notes but may not concurrently edit the shared index;
- no audio/video download by default.

- [ ] **Step 6: Write `output-formats.md`**

Define portable logical outputs without hard-coded directories. Support:

- one report only;
- Markdown collection;
- Markdown plus optional sibling HTML;
- existing project conventions when provided.

Require raw sources to remain separate from edited notes. State that HTML is optional and must use the project’s renderer or HTML skill rather than embedding a private shell.

- [ ] **Step 7: Run contract and repo tests**

Run:

```bash
/usr/bin/python3 -m unittest tests.test_researching_ai_startups -v
/usr/bin/python3 tools/skill_lint.py skills
```

Expected at this stage: package-file tests still fail because templates and validator are not present; `SKILL.md` lint should pass without warnings.

- [ ] **Step 8: Commit the skill instructions**

```bash
git add skills/researching-ai-startups/SKILL.md skills/researching-ai-startups/references
git commit -m "feat: add AI startup research workflow"
```

## Task 4: Add Portable Output Templates

**Files:**
- Create: `skills/researching-ai-startups/templates/company-selection.md`
- Create: `skills/researching-ai-startups/templates/company-index.md`
- Create: `skills/researching-ai-startups/templates/source-metadata.json`
- Create: `skills/researching-ai-startups/templates/interview-note.md`

**Test scenarios:**

- **Happy path:** templates can represent a rich company and a sparse company without changing schema.
- **Edge cases:** unknown dates, unavailable transcripts, conflicting claims, and zero independent evidence are representable.
- **Error paths:** templates never instruct agents to invent fields or paste copyrighted transcripts.
- **Integration:** references link to the correct templates.

- [ ] **Step 1: Write `company-selection.md` template**

Use English headings and this table:

```markdown
# <Category> AI Startup Research

## Scope

- Research question:
- Time frame:
- Companies considered:
- Selection limits:

## Company comparison

| Company | Product | User and buyer | Founders | Technical advantage | Business progress | Hiring signals | Useful interviews | Evidence gaps |
|---|---|---|---|---|---|---|---|---|

## Research order

1. **<Company>** — worth deeper research because <evidence availability and relevance, not an employment judgment>.

## Sources

### <Company>

- <title> — <URL> — supports <claim>
```

- [ ] **Step 2: Write `company-index.md` template**

Include mandate, evidence policy, coverage table, completed notes, source backlog, current facts, contradictions, unknowns, and related files. The coverage table must use the four states defined in Task 3.

- [ ] **Step 3: Write valid `source-metadata.json`**

Use this concrete example:

```json
{
  "id": "publisher-2026-founder-interview",
  "title": "Example Founder Interview",
  "speakers": ["Founder Name"],
  "publisher": "Publisher Name",
  "published_at": "2026-01-15",
  "accessed_at": "2026-07-12",
  "url": "https://example.com/interview",
  "media_type": "video",
  "duration_seconds": 3600,
  "topics": ["product", "culture"],
  "evidence_types": ["Attributed"],
  "transcript": {
    "status": "available",
    "provenance": "platform-captions",
    "language": "en",
    "word_count": 8400,
    "local_path": "sources/transcripts/publisher-2026-founder-interview.txt"
  },
  "notes": ["interviews/publisher-2026-founder-interview.md"]
}
```

- [ ] **Step 4: Write `interview-note.md` template**

Include source metadata, provenance warning, “The whole source in N lines,” attributed claims, direct evidence, independent checks, analysis labeled as inference, contradictions, what this source adds, unanswered questions, and related notes. Do not include a raw-transcript body section.

- [ ] **Step 5: Run package tests**

Run:

```bash
/usr/bin/python3 -m unittest tests.test_researching_ai_startups -v
```

Expected: only validator-related tests or required-file checks for the missing script may fail.

- [ ] **Step 6: Commit templates**

```bash
git add skills/researching-ai-startups/templates
git commit -m "feat: add portable startup research templates"
```

## Task 5: Build the Zero-Dependency Source Validator

**Files:**
- Create: `skills/researching-ai-startups/scripts/validate_sources.py`
- Modify: `tests/test_researching_ai_startups.py`
- Create: `skills/researching-ai-startups/evals/fixtures/valid/sources.json`
- Create: `skills/researching-ai-startups/evals/fixtures/invalid/sources.json`

**Test scenarios:**

- **Happy path:** valid metadata returns exit code 0 and JSON summary.
- **Edge cases:** unavailable transcript may have zero words and no local path; optional duration may be absent.
- **Error paths:** missing URL, invalid transcript provenance, negative word count, and private local path return exit code 1.
- **Integration:** `--json` output is machine-readable and `--help` succeeds.

- [ ] **Step 1: Add failing validator tests**

Append tests that invoke:

```python
VALIDATOR = SKILL / "scripts" / "validate_sources.py"
FIXTURES = ROOT / "tests" / "fixtures" / "researching_ai_startups"


def run_validator(path, *extra):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path), *extra],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
```

Required assertions:

```python
def test_validator_accepts_valid_metadata(self):
    result = run_validator(FIXTURES / "valid" / "sources.json", "--json")
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertEqual(json.loads(result.stdout)["errors"], [])


def test_validator_rejects_invalid_metadata(self):
    result = run_validator(FIXTURES / "invalid" / "sources.json", "--json")
    self.assertEqual(result.returncode, 1)
    errors = json.loads(result.stdout)["errors"]
    self.assertTrue(any("url" in error for error in errors))
    self.assertTrue(any("provenance" in error for error in errors))
    self.assertTrue(any("private path" in error for error in errors))


def test_validator_help(self):
    result = subprocess.run([sys.executable, str(VALIDATOR), "--help"], text=True, stdout=subprocess.PIPE)
    self.assertEqual(result.returncode, 0)
    self.assertIn("source metadata", result.stdout.lower())
```

- [ ] **Step 2: Run validator tests and verify RED**

Run:

```bash
/usr/bin/python3 -m unittest tests.test_researching_ai_startups.ResearchingAIStartupsTests.test_validator_accepts_valid_metadata -v
```

Expected: FAIL because the validator and fixtures do not exist.

- [ ] **Step 3: Create valid and invalid fixtures**

The valid fixture should be a JSON array containing the template object. The invalid fixture should omit `url`, set transcript provenance to `unknown-source`, set word count to `-1`, and use `/root/private/transcript.txt` as `local_path`.

- [ ] **Step 4: Implement `validate_sources.py`**

Required behavior:

```text
usage: validate_sources.py SOURCE_JSON [--json]
```

The script must:

1. accept either one source object or a list;
2. require `id`, `title`, `speakers`, `publisher`, `published_at`, `url`, `media_type`, and `transcript`;
3. validate `url` as HTTP or HTTPS;
4. validate transcript status as `available` or `unavailable`;
5. validate provenance against `official`, `platform-captions`, `publisher-transcript`, `third-party`, `generated`, or `unavailable`;
6. require nonnegative integer `word_count`;
7. reject local paths containing `/root/`, `/Users/`, private IPv4 ranges, tokens, chat IDs, or project-specific names;
8. print human-readable results by default and `{"sources": N, "errors": [...]}` with `--json`;
9. exit 0 only when errors is empty.

Use only `argparse`, `ipaddress`, `json`, `pathlib`, `re`, `sys`, and `urllib.parse` from the standard library.

- [ ] **Step 5: Run validator and package tests**

Run:

```bash
/usr/bin/python3 -m unittest tests.test_researching_ai_startups -v
/usr/bin/python3 -m pytest tests/ -q
```

Expected: all tests pass.

- [ ] **Step 6: Commit validator and fixtures**

```bash
git add skills/researching-ai-startups/scripts tests/test_researching_ai_startups.py skills/researching-ai-startups/evals/fixtures
git commit -m "feat: validate startup research sources"
```

## Task 6: Run GREEN Behavioral Evaluations and Refine the Skill

**Files:**
- Create: `skills/researching-ai-startups/evals/with-skill.md`
- Modify only when an observed failure requires it: `skills/researching-ai-startups/SKILL.md`
- Modify only when an observed failure requires it: `skills/researching-ai-startups/references/*.md`

**Execution note:** Use the same scenario wording and comparable agent models from Task 1. Provide the complete skill package. Do not summarize the skill for the worker; make the worker load and follow it.

**Test scenarios:** S1–S4 from Task 1, scored on the same dimensions.

- [ ] **Step 1: Run the same scenarios with the skill**

Dispatch at least two fresh agents. Require exact output files or proposed file contents, source metadata, and a final response.

Expected:

- S1–S3 select single-company research.
- S4 selects company selection.
- No scenario issues an employment verdict.
- Claims and evidence types remain distinct.
- Sources without transcripts are marked unavailable.
- Discovered sources are not counted as completed notes.
- Unknowns remain explicit.

- [ ] **Step 2: Record GREEN results**

Create `skills/researching-ai-startups/evals/with-skill.md` using the same scoring table as `baseline.md`. Include before/after differences tied to observed evidence.

- [ ] **Step 3: Refactor only observed gaps**

If an agent fails, add the smallest instruction needed to close that failure. Rerun the failed scenario after each change. Do not add speculative rules unrelated to a test failure.

- [ ] **Step 4: Verify static tests after behavioral changes**

Run:

```bash
/usr/bin/python3 -m pytest tests/ -q
/usr/bin/python3 tools/skill_lint.py skills
```

Expected: all tests pass; linter reports zero errors and zero warnings.

- [ ] **Step 5: Commit behavioral evidence and refinements**

```bash
git add skills/researching-ai-startups/evals skills/researching-ai-startups
git commit -m "test: verify AI startup research behavior"
```

## Task 7: Publish, Install, and Verify Discovery

**Files:**
- Modify: `README.md`

**Test scenarios:**

- **Happy path:** public README exposes the skill under Research & information.
- **Edge cases:** install via symlink works from a fresh temporary skill directory.
- **Error paths:** portability scan finds no private environment strings.
- **Integration:** repository tests, linter, validator, and git checks all pass.

- [ ] **Step 1: Add the README entry**

Under **Research & information**, add:

```markdown
| [`researching-ai-startups`](skills/researching-ai-startups) | Research an AI startup category or one company: explain the product, identify founders, collect interviews and transcripts, separate claims from evidence, and organize reusable company notes. |
```

Keep the row entirely in English.

- [ ] **Step 2: Run the portability scan**

Run:

```bash
rg -n '/root/|/Users/|Tailscale|MemoryKit|Telegram|100\.[0-9]+\.|token|chat[_ -]?id|jingchao' skills/researching-ai-startups
```

Expected: no meaningful hits. Generic warnings about tokens or chat IDs are allowed only inside `validate_sources.py`; inspect rather than blindly accepting them.

- [ ] **Step 3: Run the full verification suite**

Run:

```bash
/usr/bin/python3 -m pytest tests/ -q
/usr/bin/python3 tools/skill_lint.py skills
/usr/bin/python3 skills/researching-ai-startups/scripts/validate_sources.py \
  skills/researching-ai-startups/evals/fixtures/valid/sources.json --json
git diff --check
```

Expected:

- all pytest tests pass;
- skill linter exits 0 with zero errors and warnings;
- validator prints an empty errors list;
- `git diff --check` exits 0.

- [ ] **Step 4: Verify installation and discovery path**

Run:

```bash
tmp=$(mktemp -d)
mkdir -p "$tmp/.claude/skills"
ln -s "$PWD/skills/researching-ai-startups" "$tmp/.claude/skills/researching-ai-startups"
test -f "$tmp/.claude/skills/researching-ai-startups/SKILL.md"
/usr/bin/python3 tools/skill_lint.py "$tmp/.claude/skills"
rm -rf "$tmp"
```

Expected: one discovered skill, zero errors, zero warnings.

- [ ] **Step 5: Commit the public documentation**

```bash
git add README.md
git commit -m "docs: publish AI startup research skill"
```

- [ ] **Step 6: Review branch history and scope**

Run:

```bash
git status --short
git log --oneline main..HEAD
git diff --stat main...HEAD
git diff --check main...HEAD
```

Expected: clean worktree; only the spec, plan, skill package, evals, fixtures, tests, and README changed.

- [ ] **Step 7: Merge and push after review**

Follow `finishing-a-development-branch`. Merge the feature branch into `main`, rerun the full verification suite on `main`, and push with the configured root git credentials:

```bash
HOME=/root GIT_CONFIG_GLOBAL=/root/.gitconfig git push origin main
```

Expected: GitHub remote contains the tested commit and the public README links to the new skill.
