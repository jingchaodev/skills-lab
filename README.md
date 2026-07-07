# skills-lab

A library of reusable **[Agent Skills](https://code.claude.com/docs/en/skills)** for
Claude Code (and compatible agent harnesses) — plus the authoring principles
behind them.

Each skill is a self-contained, model-invoked capability: a `SKILL.md` with
YAML frontmatter that tells the agent *when* to reach for it and *how* to use
it, sometimes paired with a small zero-dependency script. They're designed to
be **generic and portable** — no proprietary tooling, no company-internal
systems, nothing you can't run on a laptop.

> This repo is as much about *how to write good skills* as it is about the
> skills themselves. See [`docs/authoring-skills.md`](docs/authoring-skills.md).

## Skills

| Skill | What it does |
|-------|--------------|
| [`tmux-runner`](skills/tmux-runner) | Run builds, servers, watchers, and parallel agent tasks in background tmux sessions without blocking the main agent. Covers one-shot vs persistent vs inspectable session lifetimes, fan-out/fan-in, and health-checked servers. |
| [`web-search`](skills/web-search) | DuckDuckGo search from the terminal — a zero-dependency Node script. Text or JSON output. |
| [`web-fetch`](skills/web-fetch) | Fetch a page and extract readable text (or raw HTML, or all links) — zero-dependency Node script with a heuristic Readability-style extractor. |
| [`asciicast-recorder`](skills/asciicast-recorder) | Record polished terminal demos via asciinema + tmux, with idle-time compression and post-hoc trim/shift/compress tooling. |
| [`git-pr-workflow`](skills/git-pr-workflow) | Feature-branch git flow with conventional commits, rebasing, conflict resolution, and PR creation/update via the `gh` CLI. |
| [`pr-review-workflow`](skills/pr-review-workflow) | A disciplined PR-review process: understand intent → review against an 8-lens rubric → post actionable, severity-labeled inline comments. |
| [`ci-cd-triage`](skills/ci-cd-triage) | A tool-agnostic playbook for diagnosing red pipelines — classify the failing stage, read logs first-error-first, and triage build/test/deploy/infra failures. |
| [`incident-notes`](skills/incident-notes) | Structured on-call notes in plain Markdown: timestamped work log, incident table, toil tracking, and clean shift handoffs. |

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

Most skills are pure Markdown and shell. The two with scripts need:

- **`web-search` / `web-fetch`** — Node.js 18+ (uses the built-in global `fetch`; no `npm install`).
- **`asciicast-recorder`** — `asciinema`, `tmux`, `python3`, and optionally `agg` for GIF export.
- **`tmux-runner`** — `tmux`.
- **`git-pr-workflow` / `pr-review-workflow`** — `git` and the [`gh`](https://cli.github.com/) CLI.

## Anatomy of a skill

```
skills/web-search/
├── SKILL.md        # frontmatter (name, description) + usage docs the agent reads
└── search.js       # optional: a self-contained script the skill drives
```

The `description` field is the most important line in the file — it's the only
thing the agent sees when deciding whether a skill is relevant, so it names the
concrete trigger conditions. See the authoring guide for the full rationale.

## License

[MIT](LICENSE). Use them, fork them, adapt them.
