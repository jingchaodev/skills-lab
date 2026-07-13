# Results With the Skill

## Environment

- Date: 2026-07-12
- Runner: independent `hermes --oneshot` processes
- Skill loaded from: `skills/researching-ai-startups/SKILL.md`
- Execution-design runs: S2 and S4
- Live web research runs: S1 and S3
- Complete live outputs: `runs/s1-green.md` and `runs/s3-green.md`

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

## S1 and S3 — Live web research

The same no-skill and with-skill prompts were run through independent agents with live search/browser access. Complete outputs are preserved under `evals/runs/`.

### S1 — Sierra result

The skill-guided run used explicit `Direct`, `Attributed`, and `Unknown` labels. It treated customer metrics as vendor-published rather than audited, preserved the missing founder-responsibility split, and used `status: unavailable` with `provenance: unavailable` when platform captions could not be verified. It also separated job-listing signals from proof of architecture or future headcount.

### S3 — Decagon result

The skill-guided run separated the company’s resolution metric from independent validation, used an external job description only as evidence of current engineering demand, and preserved unknown product boundaries. It found a canonical No Priors episode URL where the baseline returned a search-results URL. It labeled one transcript path as unverified platform captions and one as a discovered publisher transcript whose contents had not been reviewed.

### Same-prompt comparison

| Dimension | RED | GREEN |
|---|---|---|
| Evidence vocabulary | Informal and inconsistent | Direct/Attributed/Independent/Unverified/Unknown |
| Canonical interview URL | One S3 search-results URL | Canonical episode URLs |
| Transcript handling | Availability described informally | Provenance plus retrieval limitation |
| Customer metrics | Caveated | Explicitly attributed and not treated as audited |
| Culture | Company-authored caveat | Company-authored caveat plus missing lived-experience evidence |
| Unknowns | Present | Present and tied to next evidence needed |
| Employment verdict | None | None |

## S2 — Sparse public evidence

The same-prompt live RED/GREEN pair is preserved as `runs/s2-red.md` and `runs/s2-green.md`. The skill-guided run reconciled Fireworks’ official seven-person founding-team roster against a narrower investor profile and kept the discrepancy as an evidence gap. It used canonical episode/video URLs rather than search-results pages. Every interview records exact transcript `status`, exact `provenance`, and a separate research state.

## Behavioral coverage

All three required company types now have complete live RED/GREEN outputs:

- S1: rich public evidence — Sierra;
- S2: scattered public evidence — Fireworks AI;
- S3: marketing-heavy and independently limited evidence — Decagon.

S4 separately verifies company-selection routing. The original delegated-runner timeout remains documented, but it no longer leaves a required scenario uncovered.
