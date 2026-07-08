# Conference-note architecture diagrams

Use this when converting live conference notes or batch note sets into HTML reading layers.

## Principle

A diagram is not a visual table of contents. Do not map section 1 → section 2 → section 3 unless the talk itself is explicitly a staged rollout, pipeline, or chronological process.

The default diagram should express the talk's **core architecture or system idea**.

Good diagram centers:
- central primitive: `agent action ledger`, `eval system`, `agent firewall`, `harness architecture`
- runtime loop: observe → plan → act → verify → update memory
- hub-and-spoke architecture: orchestrator connected to model, tools, data, runtime, human review
- cross-cutting rails: security, identity, observability, evals, governance, CI/CD
- bottleneck topology: where latency, trust, cost, context, or compliance constrains the system
- ecosystem topology: who supplies models, compute, data, tools, evals, security, apps

## Workflow

1. Read the note's top summary and section headings, but do not simply reuse them as nodes.
2. Ask: "What system is this talk really explaining?"
3. Name the center node as that system/primitive.
4. Add 4–6 surrounding nodes as components, constraints, or feedback mechanisms.
5. Add 2–3 rails only if they are truly cross-cutting.
6. Label the diagram as `core idea map — not a table of contents` when the risk of misreading is high.

## Examples

### Evals talk
Bad: `Why evals → scorer toolkit → production`

Good:
```text
Eval system
├─ test-case distribution
├─ expected behavior
├─ judge/scorer
├─ aggregate metric
├─ production refresh
└─ policy/RAG for judges
Rails: runtime harness · adversarial cases · regression gate
```

### Agent security talk
Bad: `Intro → attacks → mitigations → conclusion`

Good:
```text
Agent firewall
├─ untrusted input
├─ prompt/tool boundary
├─ policy engine
├─ action approval
├─ secret/data isolation
└─ audit log
Rails: prompt-injection defense · least privilege · runtime monitoring
```

### AI ecosystem market map
Bad: a vertical stack that implies every request uses every layer in order.

Good:
```text
User/workflow surface → Agent orchestrator ↔ model/data/tools/runtime → artifact/action
Cross-cutting rails: security/identity, observability/evals, developer productivity
```

## Pitfalls

- Do not auto-generate diagrams by turning bullets into sequential boxes.
- Do not label non-sequential categories with arrows that imply runtime order.
- Do not bury the diagram's main insight in surrounding prose; the diagram itself should carry the idea.
- If later slides reveal a sharper primitive set, rewrite the hero diagram instead of leaving the early generic one.
