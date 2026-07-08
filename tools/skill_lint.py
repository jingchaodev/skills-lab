#!/usr/bin/env python3
"""Zero-dependency linter for Agent Skill directories."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

DESCRIPTION_WARN_CHARS = 1200
BODY_WARN_CHARS = 8000
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
QUOTED_PHRASE_RE = re.compile(r"[\"“”']([^\"“”']+)[\"“”']")
GENERIC_SINGLE_WORD_TRIGGERS = {
    "analyze",
    "build",
    "check",
    "debug",
    "design",
    "fetch",
    "fix",
    "plan",
    "read",
    "research",
    "review",
    "search",
    "test",
    "triage",
    "write",
}


@dataclass
class Finding:
    severity: str
    message: str


@dataclass
class SkillReport:
    directory: Path
    display_name: str
    metadata_name: str | None = None
    description: str = ""
    findings: List[Finding] = field(default_factory=list)

    def add(self, severity: str, message: str) -> None:
        self.findings.append(Finding(severity, message))


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str, List[str]]:
    errors: List[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["frontmatter must start with ---"]

    end_marker = text.find("\n---", 4)
    if end_marker == -1:
        return {}, "", ["frontmatter must end with ---"]

    fm_text = text[4:end_marker]
    body_start = end_marker + len("\n---")
    if body_start < len(text) and text[body_start] == "\r":
        body_start += 1
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
    body = text[body_start:]

    fields: Dict[str, str] = {}
    current_key: str | None = None
    for lineno, raw_line in enumerate(fm_text.splitlines(), start=2):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_key is None:
                errors.append(f"frontmatter line {lineno}: continuation without a key")
            else:
                fields[current_key] += " " + line.strip()
            continue
        if ":" not in line:
            errors.append(f"frontmatter line {lineno}: expected key: value")
            current_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            errors.append(f"frontmatter line {lineno}: empty key")
            current_key = None
            continue
        if (len(value) >= 2) and value[0] == value[-1] and value[0] in {'\"', "'"}:
            value = value[1:-1]
        fields[key] = value
        current_key = key

    return fields, body, errors


def iter_skill_dirs(skills_dir: Path) -> Iterable[Path]:
    if not skills_dir.exists():
        return []
    return sorted([p for p in skills_dir.iterdir() if p.is_dir()], key=lambda p: p.name)


def lint_one(skill_dir: Path) -> SkillReport:
    report = SkillReport(directory=skill_dir, display_name=skill_dir.name)
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        report.add("ERROR", "SKILL.md missing with exact casing")
        return report

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        report.add("ERROR", f"SKILL.md is not valid UTF-8: {exc}")
        return report
    except OSError as exc:
        report.add("ERROR", f"could not read SKILL.md: {exc}")
        return report

    fields, body, parse_errors = parse_frontmatter(text)
    for message in parse_errors:
        report.add("ERROR", message)

    name = fields.get("name", "")
    description = fields.get("description", "")
    report.metadata_name = name or None
    report.description = description

    for required in ("name", "description"):
        if not fields.get(required):
            report.add("ERROR", f"frontmatter missing required field: {required}")

    if name:
        if not KEBAB_RE.fullmatch(name):
            report.add("ERROR", "name must be kebab-case")
        if name != skill_dir.name:
            report.add("ERROR", f"name '{name}' must match directory name '{skill_dir.name}'")

    if len(description) > DESCRIPTION_WARN_CHARS:
        report.add("WARN", f"description is {len(description)} chars > {DESCRIPTION_WARN_CHARS}; context cost risk")
    if len(body) > BODY_WARN_CHARS:
        report.add("WARN", f"body is {len(body)} chars > {BODY_WARN_CHARS}; move material to references/")

    return report


def extract_quoted_phrases(description: str) -> List[str]:
    phrases: List[str] = []
    seen = set()
    for match in QUOTED_PHRASE_RE.finditer(description):
        phrase = " ".join(match.group(1).strip().lower().split())
        if not phrase or not any(ch.isalnum() for ch in phrase):
            continue
        if phrase not in seen:
            phrases.append(phrase)
            seen.add(phrase)
    return phrases


def add_cross_skill_findings(reports: List[SkillReport]) -> None:
    names: Dict[str, List[SkillReport]] = {}
    phrases: Dict[str, List[SkillReport]] = {}

    for report in reports:
        if report.metadata_name:
            names.setdefault(report.metadata_name, []).append(report)
        for phrase in extract_quoted_phrases(report.description):
            phrases.setdefault(phrase, []).append(report)
            if " " not in phrase and phrase in GENERIC_SINGLE_WORD_TRIGGERS:
                report.add("WARN", f"quoted trigger phrase '{phrase}' is a generic single-word trigger")

    for name, owning_reports in names.items():
        if len(owning_reports) > 1:
            dirs = ", ".join(sorted(r.directory.name for r in owning_reports))
            for report in owning_reports:
                report.add("ERROR", f"duplicate skill name '{name}' across dirs: {dirs}")

    for phrase, owning_reports in phrases.items():
        if len(owning_reports) > 1:
            for report in owning_reports:
                others = sorted(r.directory.name for r in owning_reports if r is not report)
                report.add("WARN", f"quoted trigger phrase '{phrase}' also appears in: {', '.join(others)}")


def print_reports(reports: List[SkillReport]) -> Tuple[int, int]:
    error_count = 0
    warn_count = 0
    for report in sorted(reports, key=lambda r: r.directory.name):
        if not report.findings:
            print(f"{report.directory.name}: OK")
            continue
        severity_order = {"ERROR": 0, "WARN": 1}
        for finding in sorted(report.findings, key=lambda f: (severity_order.get(f.severity, 9), f.message)):
            if finding.severity == "ERROR":
                error_count += 1
            elif finding.severity == "WARN":
                warn_count += 1
            print(f"{report.directory.name}: {finding.severity} {finding.message}")
    return error_count, warn_count


def lint(skills_dir: Path) -> Tuple[List[SkillReport], int, int]:
    if not skills_dir.exists():
        report = SkillReport(directory=skills_dir, display_name=skills_dir.name)
        report.add("ERROR", f"skills directory does not exist: {skills_dir}")
        return [report], 1, 0
    if not skills_dir.is_dir():
        report = SkillReport(directory=skills_dir, display_name=skills_dir.name)
        report.add("ERROR", f"skills path is not a directory: {skills_dir}")
        return [report], 1, 0

    reports = [lint_one(path) for path in iter_skill_dirs(skills_dir)]
    add_cross_skill_findings(reports)
    errors, warnings = print_reports(reports)
    return reports, errors, warnings


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint Agent Skill directories.")
    parser.add_argument("skills_dir", nargs="?", default="./skills", help="skills directory (default: ./skills)")
    args = parser.parse_args(argv)

    skills_dir = Path(args.skills_dir)
    reports, errors, warnings = lint(skills_dir)
    print(f"SUMMARY: {len(reports)} skills, {errors} ERROR, {warnings} WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
