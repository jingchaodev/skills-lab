# Diagram standard for HTML notes (calibration note)

Born from repeated diagram QA failures: many generated "diagrams" were vertical pill-lists in card costume — no arrows, no spatial meaning, bare labels, and too much whitespace. A good diagram balances density and readability. This file freezes the difference into rules. **Quality bar: a diagram must fully capture the note's core content, look
professional, and NOT be a few-words-per-box sketch.**

## Rule 0 — a diagram must encode RELATIONSHIPS
If arrows/positions/axes don't carry meaning, it is a LIST — render it as a list. Never dress a
bullet list in diagram CSS. Test: delete all edges/positions — if nothing is lost, don't draw it.

## Rule 1 — every node carries TWO layers (minimum)
```
┌──────────────────────┐
│  Title (bold, short) │   ← the concept
│  payload · payload   │   ← 2-5 words of substance: what it does / key mechanism / number
└──────────────────────┘
```
Good: `Scheduler` / `cadence · triggers`. Bad: `Scheduler` alone.
The FOCAL node may carry a third line (the key claim or number). This is the "not too simple"
requirement: the diagram should be readable WITHOUT the surrounding text.

## Rule 2 — one spatial grammar per diagram (pick ONE)
- **left → right** = flow / pipeline / time (inputs → transform → output)
- **center + ring/spokes** = one core with supporting/surrounding elements
- **top → bottom** = hierarchy / stack / layers
- **2-D grid** = comparison matrix (axes must be labeled)
Never mix grammars in one figure. If the content has two grammars, draw two diagrams.

## Rule 3 — label every edge with a VERB
`grounds` · `verifies` · `escalates to` · `feeds` · `blocks`. An unlabeled arrow is a missed
chance to encode the note's actual claims. Numbers/percentages ride on edges or corner badges.

## Rule 4 — visual hierarchy: ONE focal node
Focal node = accent border (--clay) + slightly larger. Everything else neutral gray. If
everything is highlighted, nothing is. Failure/anti-pattern elements: muted red tint, grouped in
a clearly-separated strip — never mixed into the main flow.

## Rule 5 — capture the TL;DR, structurally
Before drawing, list the note's core claims (usually the TL;DR bullets). Each claim must map to
a visible element: a node, an edge label, or an annotation. Coverage check: if a TL;DR clause has
no visual counterpart, the diagram doesn't capture the note. Budget: **5–9 nodes, 4–10 labeled
edges** — fewer = too thin, more = split into two diagrams.

## Rule 6 — technique: inline SVG, not CSS boxes
Hand-authored inline `<svg viewBox="0 0 1040 H">` with:
- rounded rects (`rx="10"`), 1px `--gray-300` borders, white/ivory fills
- `<text>` with `<tspan>` for title/payload lines (13-14px title, 11px payload, system fonts)
- one `<marker>` arrowhead def, curved paths (`<path d="M… C…" >`) for organic flow
- edge labels as small 10-11px text with white halo (`paint-order:stroke; stroke:#fff`)
- `width:100%; height:auto` in a `.diagram` card; `min-width:760px` + horizontal scroll on mobile.
  The wrapper MUST carry the full mobile touch-scroll trio (calibration note — plain
  `overflow-x:auto` alone does NOT drag on iOS):
  ```css
  .diagram-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; touch-action: pan-x pan-y; }
  ```
CSS-box/flex "diagrams" are allowed ONLY for pure stacks/grids (Rule 2's hierarchy/matrix), and
still need payload lines + explicit axis/relationship captions.

## Worked example pattern
A weak architecture overview might start as a 10-pill list. Redraw it into a relationship-bearing SVG: one focal system node in the center, 4–6 infrastructure nodes around it, payload text on every node, verb-labeled edges, and a separated red strip mapping missing pieces to failure modes. One figure should carry the note's thesis.

## Rule 7 — abstract strategy notes need a mechanism, not a constellation
For career, strategy, operating-principle, or decision-framework notes, a hub-and-spoke map of concepts is often too weak even if it has arrows. If the diagram quality feels lower than the surrounding note, the likely issue is that the diagram restates headings instead of showing a compounding mechanism.

Prefer a flywheel / pipeline / before-after transformation that makes the causal chain visible. For the reader career notes, use the pattern in `references/career-strategy-diagrams.md`: current raw material → high-density arena → problem selection → ambitious form → research/eval loop → last-mile artifact → external reputation → higher-quality opportunities, with an optional trap branch for local-optimum work.

## Rule 8 — screenshot self-check before shipping (added after batch redraw QA)
Hand-authored SVG text does NOT reflow — overlap and clipping are invisible until rendered.
After writing/redrawing any diagram, screenshot it with playwright and LOOK at the image:
```bash
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1440,'height':900})
    pg.goto('file:///path/to/note.html'); pg.wait_for_timeout(500)
    pg.screenshot(path='/tmp/check.png', full_page=True); b.close()"
```
Check for: text overlapping edges/nodes, labels clipped at the viewBox boundary, tspan lines
colliding, arrowheads landing inside boxes. Fix and re-screenshot until clean. Never ship a
diagram you have not seen rendered.

## Checklist (run before shipping any diagram)
- [ ] Relationships encoded (Rule 0) — or it's a list
- [ ] Every node has title + payload (Rule 1)
- [ ] Single spatial grammar (Rule 2)
- [ ] Edges labeled with verbs (Rule 3)
- [ ] One focal node; failures separated (Rule 4)
- [ ] TL;DR coverage check passed (Rule 5)
- [ ] Inline SVG, mobile touch-scrollable — overflow-x + webkit + touch-action (Rule 6)
- [ ] For abstract strategy/career notes: mechanism/flywheel/trap is visible, not just a concept constellation (Rule 7)
- [ ] Playwright screenshot inspected: no overlap / clipping (Rule 8)
