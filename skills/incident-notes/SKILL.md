---
name: incident-notes
description: Keep structured on-call / incident notes — track tickets and incidents, log work with timestamps, record toil-reduction improvements, and prepare clean shift handoffs. Use when the user is on call, working incidents, or preparing a handoff.
---

# Incident & On-Call Notes

Maintain a structured, plain-Markdown log of an on-call rotation: what you
worked, how you fixed it, what toil you eliminated, and what the next person
needs to know. Everything is local Markdown — no proprietary tooling required,
works with any editor, Obsidian vault, or git repo.

## Notes Location

Pick one directory and stick to it. Sensible default:

```bash
NOTES="${INCIDENT_NOTES_DIR:-$HOME/notes/oncall}"
mkdir -p "$NOTES"
```

Set `INCIDENT_NOTES_DIR` in your shell profile to point anywhere (a synced
folder, a git repo, an Obsidian vault).

## Finding the Active Note

One note per rotation, named by ISO week:

```bash
# Path convention: oncall-YYYY-Www.md  (e.g. oncall-2026-W28.md)
CURRENT="$NOTES/oncall-$(date +%Y)-W$(date +%V).md"

# Most recent existing note
ls -t "$NOTES"/oncall-*.md 2>/dev/null | head -1
```

## Note Structure

```markdown
# On-Call YYYY-Www

## Summary
- Rotation: YYYY-MM-DD → YYYY-MM-DD
- Handoff from: <name>
- Handoff to: <name>

## Incidents
| # | Time | Severity | Summary | Resolution | Duration | Follow-up |
|---|------|----------|---------|------------|----------|-----------|

## Toil / Improvements
- Automation added, runbooks written, alerts tuned, root-cause fixes.

## Recurring Issues
- Patterns worth escalating or fixing permanently.

## Handoff Notes
- Open threads and context the next on-call needs.

## Log
- Timestamped work log (newest at bottom).
```

Create it from a template:

```bash
CURRENT="$NOTES/oncall-$(date +%Y)-W$(date +%V).md"
[ -f "$CURRENT" ] || cat > "$CURRENT" <<EOF
# On-Call $(date +%Y)-W$(date +%V)

## Summary
- Rotation: $(date +%Y-%m-%d) → 
- Handoff from: 
- Handoff to: 

## Incidents
| # | Time | Severity | Summary | Resolution | Duration | Follow-up |
|---|------|----------|---------|------------|----------|-----------|

## Toil / Improvements

## Recurring Issues

## Handoff Notes

## Log
EOF
echo "Created $CURRENT"
```

## Operations

### Append to the Log

```bash
CURRENT=$(ls -t "$NOTES"/oncall-*.md | head -1)
echo "- $(date '+%Y-%m-%d %H:%M') — <what you did / what you found>" >> "$CURRENT"
```

Example entry:

```
- 2026-07-07 14:30 — Investigated INC-1234 (Sev2, checkout API 5xx spike). Root cause: DB connection pool exhausted under load. Bumped pool size + added an alarm on pool saturation.
```

### Add an Incident Row

Append a row to the `## Incidents` table:

| Field | Description |
|-------|-------------|
| # | Sequential number |
| Time | `YYYY-MM-DD HH:MM` |
| Severity | Sev1 / Sev2 / Sev3 / Low |
| Summary | Brief description |
| Resolution | What fixed it |
| Duration | Time to resolve (`45m`, `2h`, `ongoing`) |
| Follow-up | Link/ID of the follow-up task, or `—` |

### Per-Incident Deep-Dive Note

For non-trivial incidents, create a dedicated file and link it from the log:

```bash
INC=INC-1234
cat > "$NOTES/incident-$INC.md" <<EOF
---
created: $(date +%Y-%m-%d)
incident: $INC
severity: Sev2
---

# $INC — <title>

## Impact
- Who/what was affected, for how long.

## Timeline
- HH:MM — detection
- HH:MM — mitigation
- HH:MM — resolution

## Root Cause
<the actual cause, not the symptom>

## Fix
<what was done, links to PRs>

## Follow-ups
- [ ] Permanent fix / guardrail
- [ ] Runbook update
EOF
echo "Created $NOTES/incident-$INC.md"
```

## Preparing a Handoff

At end of rotation, fill in `## Handoff Notes` with:

1. **Open incidents** — anything still `ongoing`, with current state and next step.
2. **Watch items** — things that looked shaky but didn't page.
3. **In-flight changes** — deploys or fixes you started but didn't finish.
4. **Context** — anything the next person would waste time rediscovering.

Then produce a quick summary for the handoff message:

```bash
CURRENT=$(ls -t "$NOTES"/oncall-*.md | head -1)
echo "=== Handoff summary ==="
sed -n '/## Handoff Notes/,/## Log/p' "$CURRENT" | sed '$d'
echo "=== Open incidents ==="
grep -i "ongoing" "$CURRENT" || echo "None open."
```

## Tips

- **Log in real time, not at end of shift.** You will not remember the timeline later.
- **Write root cause, not symptom.** "Pool exhausted" is a cause; "API returned 500s" is a symptom.
- **Every recurring issue is a toil-reduction opportunity** — capture it so the pattern gets fixed, not just the instance.
- **A good handoff is a gift.** Ten minutes writing it saves the next on-call an hour of rediscovery.
- **Keep it in git or a synced folder** so history survives and is searchable across rotations.
