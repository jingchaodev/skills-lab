# skills-lab

A library of reusable **[Agent Skills](https://code.claude.com/docs/en/skills)** for
Claude Code (and compatible agent harnesses) — plus the authoring principles
behind them.

Each skill is a self-contained, model-invoked capability: a `SKILL.md` with
YAML frontmatter that tells the agent *when* to reach for it and *how* to use
it, sometimes paired with a small zero-dependency script. Every skill here is
**generic and portable** — no proprietary tooling, no company-internal systems,
nothing you can't run on a laptop.

> This repo is as much about *how to write good skills* as it is about the
> skills themselves. See [`docs/authoring-skills.md`](docs/authoring-skills.md).

## Skills

**Research & information**
| Skill | What it does |
|-------|--------------|
| [`deep-research`](skills/deep-research) | Decompose a question, fan out searches across web/code/docs, read the best sources, refine on gaps, and synthesize a cited answer. |
| [`fact-check`](skills/fact-check) | Verify a claim against multiple independent sources and return a structured verdict with confidence and citations. |
| [`search-strategy`](skills/search-strategy) | Search any corpus effectively — pick the right source, craft precise queries, iterate, filter, and switch keyword↔semantic. |
| [`web-search`](skills/web-search) | DuckDuckGo search from the terminal — zero-dependency Node script, text or JSON output. |
| [`web-fetch`](skills/web-fetch) | Fetch a page and extract readable text (or raw HTML, or all links) — zero-dependency Node script. |

**Code, review & delivery**
| Skill | What it does |
|-------|--------------|
| [`git-pr-workflow`](skills/git-pr-workflow) | Feature-branch git flow, conventional commits, rebasing, conflict resolution, and PRs via the `gh` CLI. |
| [`pr-review-workflow`](skills/pr-review-workflow) | Understand intent → review against an 8-lens rubric → post actionable, severity-labeled inline comments. |
| [`design-review`](skills/design-review) | Review a technical design (or defend your own) against a rubric: problem, alternatives, failure modes, operability, cost. |
| [`call-chain-tracing`](skills/call-chain-tracing) | Trace a request/value hop-by-hop across services and code to find where it's transformed, filtered, or dropped. |
| [`coverage-and-test-reports`](skills/coverage-and-test-reports) | Interpret coverage metrics and CI test-run failures; prioritize the gaps that actually matter (risk-based, not 100%-chasing). |
| [`ci-cd-triage`](skills/ci-cd-triage) | Diagnose red pipelines — classify the failing stage, read logs first-error-first, triage build/test/deploy/infra failures. |

**Operations & infrastructure**
| Skill | What it does |
|-------|--------------|
| [`tmux-runner`](skills/tmux-runner) | Run builds, servers, watchers, and parallel agent tasks in background tmux sessions without blocking the main agent. |
| [`aws-cli-safety`](skills/aws-cli-safety) | Safe, effective AWS CLI use — read-before-write, least privilege, prod caution, `--dry-run`, `--query`/`jq`, pagination. |
| [`change-management`](skills/change-management) | Author and run production change records: what/why/blast-radius/rollback/verification, risk tiers, approval flow. |
| [`operational-readiness-review`](skills/operational-readiness-review) | Run or prepare for a launch-readiness review: monitoring, runbooks, on-call, capacity, rollback, durability, load testing. |
| [`security-review-gate`](skills/security-review-gate) | Pause on security-sensitive requests (secrets, PII, auth, IAM), consult the standard before acting, never emit insecure code. |

**Oncall & incident response**
| Skill | What it does |
|-------|--------------|
| [`oncall-context-system`](skills/oncall-context-system) | A file-based shift-memory system so oncall context never evaporates — ticket ledger, deadline calendar, working-on tracker, gaps log, daily logs, and handoff lifecycle. |
| [`ticket-triage`](skills/ticket-triage) | Categorize, prioritize, and destale a ticket queue; investigate 3+ tickets in parallel with read-only sub-agents, then reconcile in one pass. |
| [`alarm-correlation`](skills/alarm-correlation) | Cluster related alarms, assess systemic-vs-transient severity, and trace cross-service dependency chains to a root cause. |
| [`incident-response`](skills/incident-response) | Handle a live sev1/sev2 — impact quantification, primary/secondary linking, the resolution-summary gate, and outage comms. |
| [`runbook-authoring`](skills/runbook-authoring) | Write agent-consumable service runbooks: alarm-definition blocks, ranked-likelihood investigation tables, quality tiers, and agent-routing metadata. |
| [`postmortem`](skills/postmortem) | Write and facilitate a blameless postmortem — timeline, impact, root cause, and concrete preventive action items. |
| [`evidence-discipline`](skills/evidence-discipline) | Ground every operational claim in a traceable source, label its evidence tier, and never present correlation as causation. |

**Writing & communication**
| Skill | What it does |
|-------|--------------|
| [`technical-writing`](skills/technical-writing) | Write clear long-form docs (design docs, proposals, narratives) — structure, lead with the point, data over adjectives, self-review pass. |
| [`doc-review-comments`](skills/doc-review-comments) | Review someone else's prose: does it answer its question, is the structure sound, what's missing — with severity-labeled comments. |
| [`writing-style-capture`](skills/writing-style-capture) | Extract and reproduce a person's or brand's writing voice from samples, via a reusable style card. |
| [`architecture-diagram`](skills/architecture-diagram) | Generate clean architecture diagrams as code (Mermaid / Graphviz / PlantUML / SVG) — with a tool decision table. |

**Thinking, judgment & meta**
| Skill | What it does |
|-------|--------------|
| [`socratic-questioning`](skills/socratic-questioning) | Ask focused questions to reach shared understanding before acting — with a grill-vs-act decision model. |
| [`engineering-judgment`](skills/engineering-judgment) | Operate at senior/staff/principal level: scope, ambiguity, influence without authority, and when "good enough" wins. |
| [`behavioral-interview`](skills/behavioral-interview) | Run or prepare for competency/behavioral interviews — STAR, competency areas, probing for real signal, level calibration. |
| [`technical-interview`](skills/technical-interview) | Run or prepare for coding and system-design interviews — round types, calibration rubric, interviewer prep doc, debrief writing, candidate coaching. |
| [`asciicast-recorder`](skills/asciicast-recorder) | Record polished terminal demos via asciinema + tmux, with idle-time compression and post-hoc trimming. |
| [`agent-retrospective`](skills/agent-retrospective) | An agent analyzing its own session transcripts to find friction and missed corrections, then proposing durable improvements. |

## Installing

Skills live in a `skills/` directory that your agent reads. For Claude Code,
symlink (or copy) any skill into your skills directory:

```bash
git clone https://github.com/jingchaodev/skills-lab.git
cd skills-lab

# Install a single skill for your user
ln -s "$PWD/skills/tmux-runner" ~/.claude/skills/tmux-runner

# ...or install them all
for d in skills/*/; do
  ln -s "$PWD/$d" ~/.claude/skills/"$(basename "$d")"
done
```

Then the agent picks them up automatically — it reads each `SKILL.md`
frontmatter and invokes the skill when the `description` matches the task.

## Requirements

Most skills are pure Markdown and shell. The ones with extra needs:

- **`web-search` / `web-fetch`** — Node.js 18+ (built-in global `fetch`; no `npm install`).
- **`asciicast-recorder`** — `asciinema`, `tmux`, `python3`, optionally `agg` for GIF export.
- **`tmux-runner`** — `tmux`.
- **`git-pr-workflow` / `pr-review-workflow`** — `git` and the [`gh`](https://cli.github.com/) CLI.
- **`aws-cli-safety`** — the AWS CLI.
- **`architecture-diagram`** — any of Mermaid, Graphviz, or PlantUML (your choice).

## Anatomy of a skill

```
skills/web-search/
├── SKILL.md        # frontmatter (name, description) + usage docs the agent reads
└── search.js       # optional: a self-contained script the skill drives
```

The `description` field is the most important line in the file — it's the only
thing the agent sees when deciding whether a skill is relevant, so it names the
concrete trigger conditions. See [`docs/authoring-skills.md`](docs/authoring-skills.md)
for the full rationale.

## License

[MIT](LICENSE). Use them, fork them, adapt them.
