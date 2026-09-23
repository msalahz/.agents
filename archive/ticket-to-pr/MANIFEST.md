# Archived: ticket-to-pr

Archived 2026-09-23 by the archive-skill workflow.

## Files moved

| From | To |
| --- | --- |
| ~/.agents/skills/ticket-to-pr/SKILL.md | ~/.agents/archive/ticket-to-pr/SKILL.md |
| ~/.agents/skills/ticket-to-pr/agents/openai.yaml | ~/.agents/archive/ticket-to-pr/agents/openai.yaml |
| ~/.agents/skills/ticket-to-pr/evals/evals.json | ~/.agents/archive/ticket-to-pr/evals/evals.json |
| ~/.agents/skills/ticket-to-pr/evals/fixtures/64-status-colour-swatch.md | ~/.agents/archive/ticket-to-pr/evals/fixtures/64-status-colour-swatch.md |

## Link removed

`~/.claude/skills/ticket-to-pr` -> `../../.agents/skills/ticket-to-pr`

## Shared edits

- README.md: removed this bullet under "Personal skills":

  - [`ticket-to-pr`](./skills/ticket-to-pr/SKILL.md) carries a ticket to an open pull request through a background agent, asking at each step.
- README.md: lowered the "installed skills" count, the "entries under `skills/`" count, and the "Personal skills" count by one.

## Restore

Restore: `git mv ~/.agents/archive/ticket-to-pr ~/.agents/skills/ticket-to-pr`, remove `MANIFEST.md` from it, then `ln -s ../../.agents/skills/ticket-to-pr ~/.claude/skills/ticket-to-pr`, then re-add the README bullet under "Personal skills" in alphabetical order and raise the three counts by one.
