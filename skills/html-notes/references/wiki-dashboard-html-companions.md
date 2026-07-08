# wiki/dashboard HTML companions

Use this reference when converting workspace wiki notes, especially live AI conference notes, into polished HTML.

## Artifact model

Keep two artifacts with the same slug:

```text
<notes-dir>/<slug>.md
<notes-dir>/_html/<slug>.html
```

- `.md` is the source of truth for wiki links, workspace search, grep, and future patches.
- `.html` is the reading layer for the wiki/static dashboard and mobile review.
- Do not delete or replace the Markdown note unless explicitly asked to abandon the wiki source.

## Dashboard URL pattern

```text
http://<host>:<port><served-notes-url>/_html/<slug>.html
```

If the wiki/static-site host serves non-markdown files directly, a self-contained HTML companion can be opened through the same host.

## Recent/listing routing convention

For a markdown note `<notes-dir>/foo.md`, the wiki/static-site should prefer `<notes-dir>/_html/foo.html` in home/listing/directory views when the HTML companion exists. This preserves Markdown as source while giving readers the polished reading layer by default.

## HTML content pattern for conference notes

Use the existing note structure, not a new narrative:

1. Header: date, track, room, speaker/company metadata.
2. `The whole talk in N lines` summary; do not use `TL;DR` when the note convention prefers a more explicit heading.
3. Optional SVG system diagram when it clarifies the agent architecture.
4. Concept cards matching the Markdown sections.
5. Collapsed `Deeper` details for callout bodies.
6. Open threads and related concepts at the bottom.

## Verification checklist

Before reporting completion:

- Markdown source exists and remains unchanged except intended content patches.
- HTML companion exists under `_html/` with the same stem.
- HTML is self-contained: inline CSS/JS only, no external fonts or CDN dependencies unless explicitly needed.
- `<meta name="viewport" ...>` exists.
- Key section strings from the Markdown appear in the HTML.
- A visible `View raw Markdown source →` link points back to `<served-notes-url>/<slug>.md`.
- Dashboard URL returns 200 or is otherwise reachable.
- If listing routing is enabled, listing links point to the HTML companion rather than the Markdown note.

## Pitfalls

- Do not create HTML only; live notes still need the Markdown source.
- Do not put the HTML in an unrelated export directory if the workflow expects hosted/wiki rendering.
- Do not use `TL;DR` as the summary heading; use `The whole talk in N lines`.
- If a later slide image arrives after the initial note, patch both `.md` and `.html` immediately and verify both contain the new slide details.
