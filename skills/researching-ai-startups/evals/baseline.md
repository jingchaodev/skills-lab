# Baseline Results Without the Skill

## Environment

- Date: 2026-07-12
- Model requested: GPT-5.6-sol
- Skill available: no
- Fresh-agent attempts: five delegated workers initially timed out before producing tokens
- Fallback runner: independent `hermes --oneshot` processes with live search/browser tools
- Completed live RED scenarios: S1 (Sierra) and S3 (Decagon)
- Complete outputs: `runs/s1-red.md` and `runs/s3-red.md`

## Live baseline limitation

The first batch asked two workers to research two scenarios each with web access. Both workers timed out after three 90-second attempts and returned no content. The second batch split S1, S2, and S3 into separate no-tool tasks. All three workers timed out before producing any tokens.

These transport failures are not counted as behavioral failures. No synthetic model output is substituted for missing results.

## Live RED runs

After the delegated transport failed, the same scenarios were executed through independent one-shot agents with live search/browser access and without loading the skill.

### S1 — Sierra

The baseline produced a useful sourced employer brief and explicit unknowns. It distinguished company-authored technical evidence from independent verification, but used an informal evidence vocabulary and reported transcript availability without the structured provenance contract used by the skill.

### S3 — Decagon

The baseline correctly warned that customer metrics and culture language were company-controlled. One interview entry linked to a YouTube search-results page instead of a verified canonical episode URL, and transcript availability was described informally. This is a concrete metadata-quality failure that the skill should prevent.

## Prior observed baseline: Sierra research series

The Sierra research series was completed before `researching-ai-startups` existed. It provides real observed workflow evidence from a rich-company case.

### Observed behavior

1. Source discovery, transcript retrieval, company coverage, and note production had to be assembled manually across several steps rather than selected through a reusable company-research mode.
2. Downloaded transcripts and completed source notes required an explicit distinction. Raw transcript presence alone did not establish current research coverage.
3. Parallel source-note workers received enough freedom to produce individually polished pages with inconsistent collection-level visual systems. Structural HTML checks passed even though the series did not feel unified.
4. Shared index edits had to remain centralized after parallel workers created independent note pairs; otherwise coverage counts and shared metadata would have been race-prone.
5. Source metadata and transcript provenance were captured for the project, but there was no portable, public contract that another agent could apply to a different company and output location.

### Evaluation

| Dimension | Result | Evidence |
|---|---|---|
| Correct research mode | PARTIAL | The work achieved a single-company research series, but mode selection was manually orchestrated rather than reusable. |
| Plain product explanation | PASS | The series explained Sierra's product, company formation, context engineering, evaluation, deployment, pricing, and culture. |
| Founder identity | PASS | Founder-focused sources covered Bret Taylor and Clay Bavor. |
| Source URLs | PASS | Canonical source URLs and transcript metadata were preserved. |
| Transcript provenance | PASS | Transcript files and provenance were recorded, but the rule emerged during execution rather than before it. |
| Claim and evidence separation | PARTIAL | Source-specific notes separated attribution and synthesis, but the company-wide evidence vocabulary was not established at the start. |
| Explicit unknowns | PASS | Coverage gaps and future research targets were maintained in the series index. |
| One important source per note | PASS | High-value interviews received separate Markdown and HTML notes. |
| Discovered sources versus completed coverage | FAIL initially; PASS after correction | The workflow needed an explicit rule that downloaded transcripts are backlog, not published coverage. |
| No unsolicited employment verdict | PASS | The series built company understanding without issuing a join decision. |
| No invented facts | PASS | Notes were grounded in complete transcripts and source material. |

## Failure patterns the skill must address

- Choose company selection or single-company research explicitly.
- Define the coverage map before searching.
- Keep discovered sources, downloaded transcripts, and completed notes as separate states.
- Establish one shared collection contract before parallel note production.
- Keep shared index edits with one writer.
- Preserve source metadata and transcript provenance in a portable format.
- Separate attributed statements, independent evidence, and inference from the start.

## Behavioral baseline coverage

S1, S2, and S3 now have complete same-prompt RED/GREEN live-web outputs under `evals/runs/`. The initial delegated-runner failures remain recorded because they explain the switch to independent one-shot agents; no missing output was synthesized.
