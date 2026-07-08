# Batch conference-note HTMLization

Use when asked to HTML-ize a date range or a batch of live conference notes, for example “turn these conference notes into HTML”.

## Goal

Preserve Markdown as source of truth and create missing `_html/<same-stem>.html` companions for every date-scoped conference note. Do not rewrite the underlying notes unless restructuring is requested.

## Workflow

1. **Audit first**
   - Identify date-scoped conference Markdown notes, usually top-level `<notes-dir>/*.md` with date-like names or other project-specific naming patterns.
   - Exclude archive/product/company/model/reference notes unless explicitly asked for the entire wiki.
   - For each candidate, check whether `<notes-dir>/_html/<same-stem>.html` exists.

2. **Generate only missing companions**
   - Keep the Markdown file unchanged.
   - Write a self-contained HTML reading layer with inline CSS, viewport metadata, a readable title, a short summary, a TOC when useful, and a visible raw Markdown link: `<served-notes-url>/<same-stem>.md`.
   - Use a patchable multi-line HTML structure; avoid giant one-line bodies.
   - If the source note already has a strong framework, preserve it. If the source is rough, render faithfully rather than inventing new claims.

3. **Verify the batch**
   - Count source notes and HTML companions; final coverage should be `N / N`.
   - For every companion, verify: `<!doctype html>`, viewport meta, raw Markdown link, no external JS/CSS/font dependency, file size > trivial stub.
   - Spot-check representative direct URLs: `<served-html-url>` returns `200 OK`.
   - Check that directory/listing routes prefer `_html/<stem>.html` links where companions exist. Recency-scoped listings may omit older notes, so do not treat absence from those listings as failure.

4. **Report clearly**
   - Give counts: source notes, existing HTML, newly generated HTML, final coverage.
   - Provide the directory URL and a few representative links.
   - State that Markdown remains the source of truth and HTML is the reading layer.

## Batch diagram REDRAW (calibration note — 27-file parallel redraw)

Use when existing HTML companions have weak diagrams (pill-lists in card costume) and they need to be redrawn to the `diagram-standard.md` bar. Proven workflow:

1. **Shard across parallel agents** — 4–5 files per agent. Every agent gets the SAME spec:
   - Read `references/diagram-standard.md` first (all rules, mandatory).
   - Read THAT note's own TL;DR → map claims to visual elements (Rule 5) before drawing.
   - One shared visual language across the whole batch: same palette, same font sizes,
     verb-labeled edges, one focal accent color — so the wiki reads as one product.
   - **Surgical edit: replace ONLY the diagram section.** Do not touch prose, TOC, or layout.
   - Self-check via playwright screenshot (Rule 7) before reporting done.
2. **Orchestrator spot-checks** the agents' screenshots (don't trust "done" claims) — then one
   commit for the whole batch via git-sync.
3. **Mobile scroll injection** — when retrofitting many files, batch-inject the touch-scroll trio
   (`overflow-x:auto; -webkit-overflow-scrolling:touch; touch-action:pan-x pan-y`) on every wide
   diagram/table wrapper with a script, not by hand; verify by grep-count afterwards.

Related but OUT of this skill's scope: bugs in the host wiki/static-site app itself. App routing, cache, and navigation bugs belong in that app repo, not in the note artifacts.

## Pitfalls

- Do not use a recency-scoped listing as the only routing verification; it is recency-scoped and may omit older conference notes.
- Do not convert non-conference wiki pages just because they live under the notes directory.
- Do not claim “all notes” unless the audit scope is explicit and the final coverage check is clean.
- Do not bury the raw Markdown link; readers need a visible escape hatch from the polished reading layer back to the editable source.
