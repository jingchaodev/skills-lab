# Career strategy HTML note pattern

Use this when asked to capture a career framework, essay, thread, or advice into a durable note for the workspace or career notes directory.

## Default artifact pair

- Markdown source: `<notes-dir>/<slug>.md`
- HTML reading layer: `<notes-dir>/_html/<slug>.html`

Keep Markdown as source of truth; HTML is the polished reading layer.

## Required content shape

1. `The whole essay in N lines` — compressed thesis bullets.
2. Core formula / mental model.
3. Translation into career/strategy transition: the reader's concrete career or strategy domain.
4. Scorecard or diagnosis if the note is career-strategy oriented.
5. Main red flag / local optimum.
6. One highest-leverage next action.

## Diagram requirement

If the note synthesizes a framework or causal model, include a diagram by default. Good default: a hub-and-spoke or system-map inline SVG showing how the major levers feed the focal career positioning.

Example structure:

- Focal node: `Career Positioning` / `production agent memory + context reliability`.
- Input nodes: scarce resources, problem selection, ambition, last-mile execution, xG/efficiency, research mentality.
- Verb-labeled edges: funds, prioritizes, raises bar, finishes, converts, validates.
- Risk strip: the main local optimum to avoid.

Follow `references/diagram-standard.md`: title + payload on each node, verb-labeled edges, one focal node, mobile horizontal scroll.

## Tracker update

If the workspace has an index/tracker, add both Markdown and HTML links there.

## User-facing link

When reporting completion, include the browser-openable dashboard or static-server URL, not only the local file path or `file://` link. Verify the URL returns 200 when tools are available.
