# Agent Workspace State

## Project goal
Make skills-lab safely resumable by multiple coding agents.

## Current phase
planning

## Do not redo
- (none yet)

<!-- agentws:generated:start -->
## Active task
No active task.

## Current status
Adopted agentws. REQUIREMENTS.md (mined 2026-07-08) sets product direction: 'authoring + lint + eval + fixtures', not more SKILL.md files. pytest green (3 tests).

## Last known good state
branch `main`, last test: passed

## Recent changes
Tracked edits (this task):
- No tracked edits recorded.
Untracked (new/scratch):
- none

## Next best action
Implement K1 'skill-lint / skill doctor': dir name, SKILL.md casing, frontmatter schema, discoverability path (top-level-only scan), slash-name collisions — the 'installed but invisible, no error' black box is the #1 complaint. Then K2 token-budget lint.

## Pinned files
- REQUIREMENTS.md — mined Ship-next backlog (K1, K2..)

## Blockers / open questions
- none

## Verification
- Last test command: python3 -m pytest tests/ -q
- Last test result: passed
<!-- agentws:generated:end -->
