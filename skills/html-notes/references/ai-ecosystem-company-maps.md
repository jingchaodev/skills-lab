# AI Ecosystem Company Maps

Use this reference when turning conference exhibitor maps, sponsor lists, schedule/speaker JSON, or startup logos into an HTML market map.

## Core lesson

Do **not** draw AI ecosystem categories as a simple linear stack unless explicitly asked for a supply-chain ladder.

Most AI-company maps are better represented as a **runtime-loop topology**:

```text
User / workflow surface
        ↓
Agent orchestrator / tool loop
        ↔ Model / inference
        ↔ Data / RAG / memory
        ↔ Runtime / sandbox / compute
        ↔ Voice / realtime / media
        ↓
Vertical AI apps / agents
```

With cross-cutting rails:

```text
Security / identity / compliance
Observability / evals / quality
Developer productivity / SDLC
```

And ecosystem/context groups:

```text
Research / community
Adopters / capital / media
Unclassified / OCR uncertain
```

## Data-source pattern

When possible, combine:

1. **Official machine-readable data** — schedule JSON, speakers JSON, sponsors JSON, llms.md, llms-full.md, MCP endpoints.
2. **Image/OCR data** — expo-floor map, booth legend, sponsor wall, slide screenshot.
3. **Manual cleanup** — canonicalize obvious duplicates and preserve uncertainty with `?` or low-confidence labels.

For AI Engineer World's Fair 2026, useful endpoints were:

```text
https://ai.engineer/worldsfair/llms.md
https://ai.engineer/worldsfair/llms-full.md
https://ai.engineer/worldsfair/sessions.json
https://ai.engineer/worldsfair/speakers.json
```

Important caveat: schedule/speaker endpoints may **not** be the same as a full exhibitor/booth API. Label the resulting set accurately, e.g. “union of visible expo-map names and official speaker/session companies.”

## Classification pattern

Use primary categories for readability, but state that many companies span categories.

Suggested categories:

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

## HTML note structure

1. Header with scope, sources, and counts.
2. Key findings.
3. **Runtime-loop ecosystem diagram** — not a linear stack.
4. All companies by primary category as chips/details.
5. Full company table with source, speaker/session counts, confidence.
6. Method/caveats section.
7. Links to CSV/JSON/Markdown artifacts if generated.

## Diagram copy to include

Add explicit wording near the diagram:

> Read this as interaction topology, not a supply-chain ladder. A typical agent run moves back and forth: workflow → orchestrator ↔ model/data/tools/runtime → action/artifact. Evals and security observe or gate the entire loop.

Also include a visible “Not a linear stack” finding when the user has challenged whether layers are really used in order.

## Quality checks

- HTML is self-contained and mobile-friendly.
- Diagram labels clearly distinguish runtime nodes vs cross-cutting rails.
- Low-confidence OCR names are marked with `?` or low confidence.
- Full company table includes source provenance.
- Counts in header match generated CSV/JSON.
- Do not imply “most numerous” = “most profitable.” If asked about profitability, separate absolute-profit public giants, AI-native private revenue leaders, and unprofitable/high-growth startups.
