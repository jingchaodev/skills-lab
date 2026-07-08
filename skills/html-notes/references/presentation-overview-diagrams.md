# Presentation Overview Diagrams for Conference Notes

Use when turning raw conference notes / live slide captures into a polished HTML reading layer.

## Reader expectation
Avoid a table-of-contents diagram or a linear summary of note sections. Prefer the kind of overview diagram that appears in a presentation deck: visually clear, architecture-flavored, and understandable at a glance.

## What the diagram must communicate
Extract the core idea from the raw note, then express it visually as a compact system map.

A strong diagram usually contains:

1. **Thesis** — one sentence stating what the talk is really about.
2. **Pressure / failure modes** — why this architecture is needed.
3. **Core primitive / system** — the central abstraction, e.g. `Harness control plane`, `Eval system`, `Agent firewall`, `Inference serving stack`.
4. **Control surface / components** — 4–6 load-bearing modules or mechanisms.
5. **Cross-cutting rails** — 2–3 governance/eval/security/observability/memory rails.
6. **Takeaway** — one sentence the reader should remember in three months.

## Anti-patterns
Avoid these even if they are easy to generate:

- Section-order flow: `Section 1 → Section 2 → Section 3`.
- Generic placeholder: `Problem / Context → Core framework → Career read`.
- Simple Mermaid star graph with no semantic compression.
- Dense SVG with tiny labels.
- Wide SVG that clips on chat/mobile view.
- A diagram that only shows labels from headings rather than extracting the talk's underlying system.

## Recommended extraction template
Before drawing, write this internal schema:

```yaml
title: <presentation title>
thesis: <one-sentence core meaning>
pressure:
  - <failure mode 1>
  - <failure mode 2>
  - <failure mode 3>
  - <failure mode 4>
core: <central primitive/system>
controls:
  - <component/control 1>
  - <component/control 2>
  - <component/control 3>
  - <component/control 4>
  - <component/control 5>
  - <component/control 6>
rails:
  - <cross-cutting rail 1>
  - <cross-cutting rail 2>
  - <cross-cutting rail 3>
takeaway: <one memorable sentence>
```

## Rendering guidance
Use the best rendering path for the job:

- **Mermaid**: good for quickly establishing structure and preserving editable `.mmd` source.
- **HTML/CSS overview board**: best when asked for presentation-quality readability and semantic compression.
- **Canvas/design pass**: use when explicitly requested visual polish approaching a slide/poster.

For workspace wiki HTML notes, a responsive HTML/CSS board is often better than a PNG because it scales cleanly on mobile and can preserve text legibility.

## Visual standard
The final diagram should feel like a keynote overview slide:

- large readable labels
- restrained color palette
- strong central object
- grouped surrounding modules
- visual hierarchy between pressure, core, controls, rails, and takeaway
- no horizontal clipping
- no tiny text
- no decorative complexity that hides the idea

## Verification checklist
Before saying it is done:

- Open the served URL with a cache-busting query.
- Confirm the diagram is visible near the top.
- Confirm it is not clipped on mobile-width rendering.
- Confirm it contains thesis/core/controls/rails/takeaway or equivalent.
- Confirm it is not merely a table of contents.
- If the artifact was criticized for ugliness or simplicity, visually inspect the result; do not rely only on string checks.

## Example mapping
For a note titled `Your Agent Didn't Fail. Your Harness Did.`:

```yaml
thesis: Most production failures are harness failures, not model failures.
pressure:
  - Silent success
  - Self-reported memory
  - State races
  - Hung tools
core: Harness control plane
controls:
  - Context assembly
  - Tool contract
  - Verifier/checker
  - Retry/fallback
  - Receipt trace
  - Authority scope
rails:
  - Guardrails
  - Eval gate
  - Human escalation
takeaway: Model proposes. Harness commits. Receipt proves.
```
