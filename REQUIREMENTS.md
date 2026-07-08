# Requirements — mined from the ecosystem (2026-07-08)

Sources: GitHub issues of anthropics/claude-code (+ anthropics/skills check) and HN. Mined by a
cross-vendor worker (GPT-5.5/codex), citations spot-verified. The mining's own conclusion:
**skills-lab's product direction is "authoring + lint + eval + fixtures", not "more SKILL.md files".**

## Ship next

| id | Requirement | Evidence |
|----|-------------|----------|
| K1 | **`skill-lint` / skill doctor**: checks dir name, SKILL.md casing, frontmatter schema (incl. accepted-casing quirks and runtime-vs-validator drift), discoverability path (top-level-only scan!), slash-name collisions — the "installed but invisible, no error" black box is the #1 complaint. | claude-code#65538, #69180, #18192, #40640, #68871, #70141, #70667, #49835; HN 47103518 |
| K2 | **Token-budget lint**: description + body size caps, eager/lazy classification, "post-use residue" check (body persists in context all session) — skills cost ~800-1200 tokens/turn when authored carelessly. | claude-code#75376, #74473, #69627, #70062 |
| K3 | **Trigger-collision simulator**: negative-sample test set ("these queries must NOT trigger"), alarms on generic words/product names — overwide descriptions misfire and drag in huge references. | claude-code#74621, #66643 |
| K4 | **Multilingual trigger paraphrases** in the authoring template (+ zh/en test phrases): English-only descriptions produced "zero triggers over 45 days" for a non-English user — we author bilingual already; codify it as a template rule. | claude-code#68086 |
| K5 | **Rendered-content fixture test**: install → read back → diff (the injection layer silently strips `$1`-style text and corrupts code blocks). | claude-code#75097, #75183 |
| K6 | **Per-skill eval harness** for high-value skills: golden prompts, expected tool use, failure examples, regression score. | HN 48291982 |
| K7 | **Invocation card** per skill: canonical name, aliases, namespace, slash usage, troubleshooting. | claude-code#71584, #73716, #66895 |

## Watch (not building yet)

- Event-triggered skills (hook → command → skill wrapper patterns): real demand, but semantics
  are moving under the platform. | claude-code#74276, #66446
- Portable/cross-agent skill packaging (Claude native + AGENTS.md export + capability manifest):
  wait for conventions to settle. | HN 47830722, 47613527

## Intake

Quarterly re-mine; user issues on trigger misfires become K3's negative-sample set.
