# Conference ecosystem maps from expo screenshots + official schedule data

Use when the reader benefits from a market-map / ecosystem diagram from a conference expo floor, sponsor map, or speaker-company list.

## Trigger

User asks for an HTML note or diagram that includes expo companies, speaker companies, or how the AI ecosystem layers interact.

## Workflow

1. **Collect sources**
   - Use official machine-readable endpoints when available, e.g. `sessions.json`, `speakers.json`, `llms.md`, or `llms-full.md`.
   - Use image OCR / vision on expo maps for booth logos and legend entries.
   - Treat screenshot-derived names as lower confidence than official JSON.

2. **Normalize company names**
   - Deduplicate obvious variants: `Amazon Web Services (AWS)` → `AWS`, `Arize` → `Arize AI`, `Weights & Biases by CoreWeave` → `Weights & Biases`, etc.
   - Remove parser artifacts like file extensions or empty pseudo-companies.
   - Preserve uncertain OCR with `?` and mark confidence low.

3. **Do not overclaim source coverage**
   - If official endpoints expose sessions/speakers but not exhibitors/booths, say so explicitly.
   - Use wording like: “union of official speaker/session companies and visible expo-map companies,” not “complete official exhibitor list.”

4. **Classify by primary ecosystem layer**
   Recommended layers for AI ecosystem maps:
   - Model labs & inference APIs
   - Compute / cloud / runtime / hardware
   - Data / RAG / retrieval / databases
   - Agent frameworks / orchestration / tools
   - Observability / evals / ML quality
   - Security / identity / compliance
   - AI coding / developer productivity
   - Voice / realtime / media
   - Enterprise SaaS / workflow / integrations
   - Vertical AI apps / agents
   - Research / academia / community
   - Capital / services / adopters / media
   - Unclassified / OCR uncertain

5. **Render the HTML note as a layered map**
   - Header: source scope, counts, caveat.
   - Key findings: 3–5 market-structure observations.
   - Main diagram: layer cards with company chips and dependency/feedback interpretation.
   - “All companies by layer”: collapsible groups.
   - “Full company table”: company, primary layer, sources, speaker/session counts, confidence.
   - Artifacts: write companion CSV and JSON when useful.

## Ecosystem interaction framing

Use this default dependency / feedback loop:

```text
Models & inference
→ Compute / runtime
→ Data / RAG / memory
→ Agent tools / orchestration
→ Developer productivity
→ Observability / evals
→ Security / identity / compliance
→ Voice / realtime / media
→ Enterprise workflow / integrations
→ Vertical AI apps
→ Research / community
→ Adopters / capital / media
```

Explain that the flow is not a strict supply chain: observability/evals and security wrap the whole loop, enterprise SaaS becomes both context and tool surface, and vertical apps package the stack into workflows.

## Quality checks

- Verify HTML is self-contained, has viewport, no external JS/CSS.
- Verify key known companies appear in the HTML and CSV.
- Verify company counts after dedupe.
- Spot-check that parser/OCR garbage did not become a company row.
- State that many companies span multiple layers; the classification is a primary-layer simplification.
