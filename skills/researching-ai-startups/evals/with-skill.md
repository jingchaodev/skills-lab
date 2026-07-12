# Results With the Skill

## Environment

- Date: 2026-07-12
- Runner: independent `hermes --oneshot` processes
- Skill loaded from: `skills/researching-ai-startups/SKILL.md`
- Live web research: disabled; these runs tested routing, output design, evidence rules, transcript rules, and completion criteria
- Scenarios run: S2 and S4

## S4 — Company selection

### Observed behavior

The worker selected **Company selection** and proposed a relative `ai-agent-infrastructure-startups/` collection. It defined a category scope, excluded generic wrappers and funding-only selections, proposed 8–12 comparable companies, and made the deeper-research order explicitly different from a company-quality or employer ranking.

The response required plain product explanations, founder checks, official sources, independent or customer-side evidence, dated hiring signals, verified interview metadata, and visible gaps. It preserved four interview states: `Discovered`, `Transcript saved`, `Note complete`, and `Index integrated`. It prohibited audio/video download and speech-to-text by default.

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|
| Correct research mode | PASS | Selected `Company selection` because the request named a category. |
| Plain product explanation | PASS | Required one concrete product sentence and rejected labels such as “agent platform” without mechanism. |
| Founder identity | PASS | Required founder verification for every final company or an explicit `Unknown`. |
| Source URLs | PASS | Required canonical URLs and at least one official source per company. |
| Transcript provenance | PASS | Required one of six provenance values plus language, word count, and limitations. |
| Claim and evidence separation | PASS | Used `Direct`, `Attributed`, `Independent`, `Inferred`, and `Unverified`. |
| Explicit unknowns | PASS | Added `evidence-gaps.md` and unknown fields instead of guesses. |
| One important source per note | PASS | Defined one completed interview note per important source. |
| Discovered sources versus completed coverage | PASS | Preserved four distinct coverage states and counted only the last two as completed. |
| No unsolicited employment verdict | PASS | Stated that research order is not a best-employer ranking. |
| No invented facts | PASS | Produced an execution contract and did not invent a live company list without research. |

## S2 — Single-company research, initial run

### Observed behavior

The worker selected **Single-company research**, did not invent founder names or interviews, created all six coverage areas, preserved evidence labels and transcript states, and made no employment recommendation.

It failed one portability requirement: although the user did not give an output destination, it inferred and printed a private absolute path from profile context.

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|
| Correct research mode | PASS | Selected `Single-company research`. |
| Plain product explanation | PASS | Required user workflow, buyer, system boundaries, and production evidence. |
| Founder identity | PASS | Refused to insert founder names from memory before verification. |
| Source URLs | PASS | Required canonical source records. |
| Transcript provenance | PASS | Required allowed provenance values and transcript limitations. |
| Claim and evidence separation | PASS | Kept verified, company claim, independent, inferred, and unknown states distinct. |
| Explicit unknowns | PASS | Initialized all substantive facts as unknown pending source review. |
| One important source per note | PASS | Required one substantive note per important interview. |
| Discovered sources versus completed coverage | PASS | Kept four processing states distinct. |
| No unsolicited employment verdict | PASS | Explicitly prohibited Join/Watch/Pass conclusions. |
| No invented facts | PASS | Did not supply Fireworks-specific facts without live research. |
| Portable output path | FAIL | Inferred a private absolute path that the user did not specify. |

## Refactor

A failing static regression assertion was added first. `SKILL.md` then received the smallest rule needed:

> If the user gives no destination, use a relative placeholder such as `<company>/`; never infer a private path from memory, profile context, or the current environment.

## S2 — Retry after refactor

The fresh retry selected **Single-company research**, left Fireworks-specific facts unknown pending source review, and proposed the relative placeholder `<fireworks-ai>/`. It explicitly stated that no private path should be inferred. The portability regression passed.

## Remaining behavioral coverage

S1 and S3 were not rerun through live web research in this cycle. The earlier Sierra project supplies a real rich-company baseline, while static contract tests cover package structure and source handling. A future eval with working web-capable workers should add full end-to-end outputs for Sierra, Fireworks AI, and Decagon rather than treating this execution-design test as research-quality validation.
