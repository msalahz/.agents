# Archived: reviewer

Archived 2026-09-11 by the archive-skill workflow.

## Files moved

| From | To |
| --- | --- |
| ~/.agents/skills/reviewer/SKILL.md | ~/.agents/archive/reviewer/SKILL.md |
| ~/.agents/docs/agents/reviewer.md | ~/.agents/archive/reviewer/docs/agents/reviewer.md |
| ~/.agents/CONTEXT.md | ~/.agents/archive/reviewer/CONTEXT.md |

`docs/agents/reviewer.md` is the per-repo configuration only this skill reads. `CONTEXT.md` held only the review vocabulary this skill and `review-loop` share; both files arrived in commit 0f40f7b with the skill.

## Link removed

`~/.claude/skills/reviewer` -> `../../.agents/skills/reviewer`

## Shared edits

- README.md: removed the `reviewer` bullet under "Personal skills"; removed the `reviewer.md` line from the layout tree; lowered "installed skills" and "Personal skills" counts by one.

## Restore

`git mv ~/.agents/archive/reviewer ~/.agents/skills/reviewer`, then move `docs/agents/reviewer.md` back to `~/.agents/docs/agents/reviewer.md` and `CONTEXT.md` back to `~/.agents/CONTEXT.md`, then `ln -s ../../.agents/skills/reviewer ~/.claude/skills/reviewer`, then re-add the README bullet and tree line and raise the two skill counts by one.
