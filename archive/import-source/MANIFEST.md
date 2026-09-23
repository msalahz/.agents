# Archived: import-source

Archived 2026-09-23 by the archive-skill workflow.

## Files moved

| From | To |
| --- | --- |
| ~/.agents/skills/import-source/CONTEXT.md | ~/.agents/archive/import-source/CONTEXT.md |
| ~/.agents/skills/import-source/SKILL.md | ~/.agents/archive/import-source/SKILL.md |
| ~/.agents/skills/import-source/agents/openai.yaml | ~/.agents/archive/import-source/agents/openai.yaml |
| ~/.agents/skills/import-source/evals/evals.json | ~/.agents/archive/import-source/evals/evals.json |
| ~/.agents/skills/import-source/evals/fixtures/repo/docs/agents/import-source.md | ~/.agents/archive/import-source/evals/fixtures/repo/docs/agents/import-source.md |
| ~/.agents/skills/import-source/evals/fixtures/repo/notes/billing-questionnaire.md | ~/.agents/archive/import-source/evals/fixtures/repo/notes/billing-questionnaire.md |

## Link removed

`~/.claude/skills/import-source` -> `../../.agents/skills/import-source`

## Shared edits

- README.md: removed this bullet under "Personal skills":

  - [`import-source`](./skills/import-source/SKILL.md) writes one source document word for word as a markdown file under `docs/`.
- README.md: lowered the "installed skills" count, the "entries under `skills/`" count, and the "Personal skills" count by one.

## Restore

Restore: `git mv ~/.agents/archive/import-source ~/.agents/skills/import-source`, remove `MANIFEST.md` from it, then `ln -s ../../.agents/skills/import-source ~/.claude/skills/import-source`, then re-add the README bullet under "Personal skills" in alphabetical order and raise the three counts by one.
