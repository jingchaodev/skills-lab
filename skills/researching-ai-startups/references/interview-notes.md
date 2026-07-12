# Interview and Transcript Notes

Use this reference for founder interviews, technical talks, podcasts, conference sessions, YouTube videos, and transcripts.

## Choose sources by added coverage

Rank a source by:

1. speaker relevance;
2. depth and duration;
3. complete transcript availability;
4. technical or operating detail;
5. publication date and current relevance;
6. the uncovered research area it can add.

Prefer the source that closes the largest evidence gap, not merely the most famous interview.

## Verify identity and metadata

Confirm:

- exact title;
- speakers and roles;
- publisher;
- publication date;
- canonical media URL or episode URL;
- duration;
- whether the source is company-hosted, independently hosted, or a promotional mirror;
- transcript availability and provenance.

Allowed transcript provenance values:

- `official`
- `platform-captions`
- `publisher-transcript`
- `third-party`
- `generated`
- `unavailable`

Record language, word count, and important caption or speech-recognition limitations.

## Default media policy

- Save a complete transcript when legally and technically available.
- Save metadata and the canonical media URL.
- Do not download audio or video by default.
- Do not run speech-to-text by default.
- Mark missing transcripts as `unavailable`.
- Do not imply that media was archived when only captions were saved.
- Do not publish copyrighted transcript bodies in a public skill or repository.

The user may explicitly request media download or transcription as a separate action.

## Coverage states

Keep these states separate:

1. **Discovered** — the source has been identified and verified.
2. **Transcript saved** — raw text and provenance are archived.
3. **Note complete** — the full source was read and a substantive note exists.
4. **Index integrated** — the company index reflects what the source adds.

Only states 3 and 4 count as completed research coverage.

## One important source per note

Use `templates/interview-note.md`. Each note should contain:

- source metadata and raw link;
- transcript provenance warning;
- “The whole source in N lines”;
- attributed claims;
- direct or independent checks;
- analysis clearly labeled as inference;
- contradictions and limitations;
- what the source adds beyond existing notes;
- unanswered questions;
- related notes.

Do not combine many interviews into one vague summary. A short source that adds no new evidence may remain in the backlog instead of receiving a note.

## Parallel work

When several transcripts are ready:

- assign one source and one note to each worker;
- give every worker the same evidence and output contract;
- forbid workers from editing the shared company index or source list;
- let one coordinator update shared files after note review;
- verify worker outputs instead of trusting completion reports.

This avoids races, duplicate coverage, and conflicting index states.
