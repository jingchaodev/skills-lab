# Authoring good Agent Skills

Notes on writing skills that an agent will actually invoke at the right time and
use correctly. This is the reasoning behind every skill in this repo.

## What a skill is

A skill is a unit of **progressive disclosure** for an agent. The agent's base
context stays small; it only pulls in a skill's full instructions when a task
matches. A skill is:

- a `SKILL.md` file with YAML frontmatter (`name`, `description`), and
- a Markdown body of instructions, optionally alongside scripts or reference files.

The agent sees only the `description` up front. It reads the body **after** it
decides the skill is relevant. So the two jobs — *get selected* and *be useful
once selected* — are handled by two different parts of the file.

## The `description` is the whole ballgame for selection

The `description` is the only text the agent uses to decide whether to open the
skill. Optimize it for **recall at the moment of need**, not for prose.

**Do:**
- Lead with what it does, then enumerate concrete trigger phrases and situations.
- Use the words a user would actually say ("review a PR", "build is red", "record a demo").
- Include the failure/entry conditions ("...when tests fail in CI but pass locally").

**Don't:**
- Be vague ("A helpful tool for developers").
- Describe implementation ("Uses a regex parser and the fetch API") — the agent doesn't select on that.

Compare:

> ❌ `description: Utilities for working with the web.`
>
> ✅ `description: Web search via DuckDuckGo. Use when the user needs to look up current information online, find documentation, research errors, or discover external resources.`

The second one fires reliably; the first one is a coin flip.

## Write the body for an agent, not a human

The reader is a model that will act on the instructions immediately. That
changes how you write:

- **Front-load the mental model.** The `tmux-runner` skill opens with the one
  concept that makes everything else make sense — *a session dies when its
  command exits*. Get the load-bearing idea in first.
- **Show, don't describe.** Copy-pasteable commands beat paragraphs. Every claim
  should come with the command that acts on it.
- **Make the happy path obvious and the edge cases available.** Lead with the
  common case; put the "when X goes wrong" material in clearly-labeled sections.
- **State the gotchas explicitly.** "Do NOT redirect the stdout of a TUI program"
  prevents a whole class of failures. Agents follow explicit prohibitions well.
- **Use tables for decision points.** A "which mode when" table lets the agent
  branch correctly without prose parsing.

## Keep skills generic and self-contained

A skill that depends on one company's internal tools only works in one company.
The skills here deliberately:

- **Use ubiquitous tools** (`git`, `gh`, `tmux`, `curl`, Node's built-in `fetch`)
  so they run anywhere.
- **Ship zero-dependency scripts** where a script is needed — no `npm install`,
  no lockfile, no supply chain. `search.js` and `fetch.js` are single files that
  use only the standard library.
- **Parameterize environment** instead of hard-coding paths (e.g.
  `INCIDENT_NOTES_DIR` in `incident-notes`).

If your skill wraps a proprietary system, split it: keep the *reusable pattern*
(how to triage a failure, how to structure a review) generic, and isolate the
tool-specific calls so they're easy to swap.

## Scripts vs. pure instructions

Add a script only when the task genuinely needs execution the agent can't do
inline:

- **Pure Markdown** is right for workflows, playbooks, and orchestration of
  tools the agent already has (`git-pr-workflow`, `ci-cd-triage`).
- **A script** is right when you need deterministic parsing or a capability the
  agent lacks (`web-search` parses DuckDuckGo's HTML; `web-fetch` extracts
  readable text). Keep it dependency-free and give it a `--help` and a
  machine-readable (`--json`) mode so the agent can compose it.

## A checklist

Before shipping a skill, confirm:

- [ ] The `description` names concrete trigger conditions in the user's words.
- [ ] The body opens with the core mental model or the happy-path command.
- [ ] Gotchas and prohibitions are called out explicitly.
- [ ] Every instruction has a runnable command, not just prose.
- [ ] No dependency on tools that don't exist outside one organization.
- [ ] Any script is zero-dependency, has `--help`, and (ideally) a `--json` mode.
- [ ] You've actually run it end-to-end.
