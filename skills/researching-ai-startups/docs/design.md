# Researching AI Startups Skill Design

**Date:** 2026-07-12
**Status:** Approved concept; implementation pending
**Target repository:** `jingchaodev/skills-lab`
**Proposed skill name:** `researching-ai-startups`

## 1. Purpose

Create a portable Agent Skill for researching AI startups as potential employers. The skill should help a user understand:

- what a company actually builds;
- who uses and buys the product;
- who founded the company and why;
- how the product, technology, business model, and culture work;
- what the company is hiring for;
- which founder interviews, podcasts, talks, and YouTube videos are worth reading or watching;
- what is known, claimed, inferred, or still unclear.

The skill organizes facts and source material. It does not decide whether the user should join the company.

## 2. Design Principles

1. **Use plain language.** Prefer concrete words such as “company research,” “source list,” and “founder interviews.” Avoid unnecessary terms such as “dossier,” “wedge,” and “artifact set.”
2. **Start from first principles.** Explain the user, problem, product, constraints, and causal mechanism before repeating a company’s positioning.
3. **Separate claims from evidence.** A company statement, customer proof, independent reporting, and analyst inference are not equivalent.
4. **Prefer primary sources.** Product documentation, technical writing, founder interviews, customer evidence, and career pages come before summaries and listicles.
5. **Research coverage is earned.** Finding or downloading a transcript does not mean the source has been analyzed.
6. **Keep the public skill portable.** Do not assume a user, host, private network, note system, repository, directory layout, or HTML renderer.
7. **Do not make the career decision.** Present facts, tensions, missing evidence, and hiring signals without issuing `Join`, `Watch`, or `Pass` verdicts.

## 3. User Entry Points

The skill supports two modes.

### 3.1 Company Selection

Use when the user provides a category, theme, or broad question, for example:

- “Research popular AI agent infrastructure startups.”
- “Which AI coding startups should I understand?”
- “Map the current AI application infrastructure startup landscape.”

The output is a comparable list of companies and a recommended research order. “Recommended” means the company has enough relevance and evidence to justify deeper research; it does not mean the company is a good employer.

### 3.2 Single-Company Research

Use when the user names a company or selects one from the company-selection output.

The output is a source-driven company research collection covering the company overview, founders, product and technology, business model, culture, careers, and important interviews.

## 4. Company Selection Output

Each company row should contain, when evidence is available:

| Field | Meaning |
|---|---|
| Company | Name and official website |
| Category | The market or technical category |
| Product | What the company sells, in plain language |
| User and buyer | Who uses it and who pays |
| Founders | Names and relevant background |
| Founded and funding | Dates and financing, with sources |
| Technical advantage | What may be technically hard or differentiated |
| Business model | How the company appears to make money |
| Business progress | Customers, revenue, usage, or other verified signals |
| Hiring signals | Roles and capabilities the company is building |
| Founder interviews | High-value podcasts, talks, and videos |
| Evidence gaps | Important facts that remain unclear |

The research order should consider:

1. relevance to the requested category;
2. product clarity;
3. technical distinctiveness;
4. source quality and availability;
5. founder interview availability;
6. hiring relevance;
7. independent evidence.

Funding size and media attention must not be treated as proof of product quality.

## 5. Single-Company Research Output

The skill should produce a logical collection equivalent to:

```text
<company>/
├── index.md
├── company-overview.md
├── founders.md
├── product-and-technology.md
├── business-model.md
├── culture.md
├── careers.md
├── sources/
│   ├── sources.json
│   ├── metadata/
│   └── transcripts/
└── html/
```

This is a suggested structure, not a hard-coded path. The user or project may define a different destination and may omit HTML.

### 5.1 Company Overview

Answer:

- What problem does the company solve?
- Who experiences the problem?
- Who pays for the solution?
- What old workflow or product does it replace or improve?
- Why is the product possible or important now?
- What does the company directly claim?
- What can be observed or independently verified?
- What remains unknown?

### 5.2 Founders

Cover:

- founder names and roles;
- relevant education and work history;
- prior history working together;
- why they chose the problem;
- division of product, engineering, research, and sales responsibility;
- repeated principles in public statements;
- relevant past failures, disputes, or contradictions when credibly sourced.

The goal is not a celebrity biography. It is to understand how founder history may shape the company.

### 5.3 Product and Technology

Explain:

- the product workflow from the user’s point of view;
- the important system components;
- what the company builds versus buys;
- where AI models, data, evaluation, infrastructure, and human review fit;
- the main technical constraints;
- claimed differentiation and competing alternatives;
- evidence that the product works in production.

### 5.4 Business Model

Cover:

- buyer and sales motion;
- pricing model when public;
- deployment and integration burden;
- customer concentration or platform dependence;
- verified business progress;
- the difference between announced partnerships and real product use.

### 5.5 Culture

Use founder interviews, employee writing, operating documents, and credible independent sources to examine:

- decision-making;
- engineering and product ownership;
- speed versus quality;
- customer proximity;
- hiring bar;
- in-office or remote expectations;
- how conflict and mistakes are handled;
- whether public values are supported by operating examples.

Do not infer actual culture from a careers-page value statement alone.

### 5.6 Careers

Record:

- current role families;
- repeated technical requirements;
- seniority distribution;
- location expectations;
- signs of which systems are being built now;
- roles most relevant to the user’s stated interests.

This section describes the hiring surface. It does not recommend applying.

## 6. Source Discovery

Search in this order:

1. official product and technical documentation;
2. official company and founder writing;
3. founder and technical-leader long-form interviews;
4. product demonstrations and conference talks;
5. customer case studies with concrete details;
6. career pages and detailed job descriptions;
7. reliable independent reporting;
8. critical or conflicting sources;
9. secondary summaries only when primary material is unavailable.

For interviews and podcasts, rank sources by:

- speaker relevance;
- depth and duration;
- availability of a complete transcript;
- technical or operating detail;
- date and current relevance;
- whether the source adds a new research topic.

## 7. Transcript and Media Policy

Default behavior:

- save the transcript when legally and technically available;
- save metadata including title, speakers, publisher, date, URL, duration, and transcript provenance;
- preserve the podcast or video URL;
- do not download video or audio by default;
- do not run speech-to-text by default;
- mark sources without transcripts as `transcript unavailable`;
- distinguish official transcripts, platform captions, third-party transcripts, and generated transcripts;
- do not reproduce copyrighted transcripts in a public repository.

The user may explicitly request audio download or transcription as a separate action.

## 8. Interview Note Series

Each high-value source should receive its own note when it contributes substantial evidence. A source note should include:

- source metadata and raw link;
- a short plain-language summary;
- important claims with attribution;
- concrete product, technical, business, or cultural evidence;
- tensions and contradictions;
- implications for the company research collection;
- unanswered questions;
- links to related company notes.

Do not combine many interviews into one vague summary. The company index should track both discovered sources and completed notes.

## 9. Evidence Labels

Use five simple labels:

| Label | Meaning |
|---|---|
| Direct | Visible in official documentation, product behavior, or a primary record |
| Attributed | Said directly by a founder, employee, customer, or named source |
| Independent | Supported by a credible source outside the company |
| Inferred | Reasoned from multiple facts but not directly confirmed |
| Unverified | A lead or claim that has not been confirmed |

Every important claim should make its evidence type clear in prose or structured metadata.

## 10. Boundaries

Version one will not:

- issue `Join`, `Watch`, or `Pass` judgments;
- decide whether the user should join a company;
- rank companies only by funding or popularity;
- download large media files by default;
- run speech-to-text without an explicit request;
- apply to jobs;
- negotiate compensation;
- treat a customer logo as proof of production adoption;
- treat a founder statement as independent evidence;
- treat a downloaded transcript as completed research.

## 11. Skill Package

Proposed public package:

```text
skills/researching-ai-startups/
├── SKILL.md
├── docs/
│   ├── design.md
│   └── implementation-plan.md
├── evals/
│   ├── scenarios.md
│   ├── baseline.md
│   ├── with-skill.md
│   └── fixtures/
├── references/
│   ├── company-selection.md
│   ├── single-company-research.md
│   ├── source-quality.md
│   ├── interview-notes.md
│   └── output-formats.md
├── templates/
│   ├── company-selection.md
│   ├── company-index.md
│   ├── source-metadata.json
│   └── interview-note.md
└── scripts/
    ├── validate_sources.py
    └── portability_check.py
```

Scripts should be added only if baseline testing proves deterministic validation is useful. Any script must use the Python standard library, support `--help`, return a nonzero exit code on validation failure, and avoid private environment assumptions.

## 12. Test Strategy

Skill development follows RED, GREEN, REFACTOR.

### 12.1 RED: Baseline Without the Skill

Test at least three cases:

1. a well-documented company with many founder interviews;
2. a newer AI infrastructure startup with scattered evidence;
3. a highly promoted startup with weak independent evidence.

Record whether the agent:

- writes a marketing-style overview;
- stops after listing videos;
- confuses claims with evidence;
- fails to preserve source metadata;
- treats downloaded transcripts as analyzed coverage;
- ranks by funding or media attention;
- gives an unsolicited career verdict;
- invents unavailable facts.

### 12.2 GREEN: Test With the Skill

The same cases should demonstrate that the agent:

- selects the correct mode;
- follows the source order;
- explains the product in plain language;
- identifies founders and relevant interviews;
- preserves transcript provenance and metadata;
- produces the defined output files;
- labels evidence and missing information;
- does not make the joining decision.

### 12.3 REFACTOR

Update the skill only in response to observed failures. Repeat the scenarios until the skill consistently follows the design.

## 13. Portability and Public Release Gates

Before publication:

1. scan for private names, internal repositories, local paths, private IPs, chat IDs, tokens, credentials, and project-specific note systems;
2. replace local paths with placeholders such as `<workspace>` and `<output-dir>`;
3. ensure examples work without MemoryKit, Tailscale, Telegram, or a specific HTML renderer;
4. avoid publishing copyrighted transcript content;
5. run the repository’s skill lint and tests;
6. test installation through the documented `skills/` symlink flow;
7. update the README research section;
8. commit and push only after all checks pass.

## 14. Acceptance Criteria

The first version is complete when:

- the skill supports company selection and single-company research;
- all skill content is written in English;
- terminology is plain and concrete;
- source claims and independent evidence remain distinct;
- transcript metadata and provenance are preserved;
- the skill does not decide whether to join;
- tests cover rich, sparse, and weak-evidence companies;
- the package contains no private environment assumptions;
- repository lint and tests pass;
- README installation and discovery information is updated;
- the public repository contains the pushed commit.
