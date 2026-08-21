# Global agent memory

Applies to every repo. A repo's own `docs/agents/*.md`, `CONTEXT.md`, `CONTEXT-MAP.md`,
or `## Agent skills` section always wins over these defaults.

## Response rules

- Invoke the `unslop` skill before writing anything in a session, then hold to it
  for every response and artifact after.
- Write subagent prompts with the `writing-for-agents` and `unslop` skills applied.
- Label every unverified claim `unconfirmed`. Say when you do not know.
- Ask about missing important details when interactive. When unattended, make the
  safest assumption and label it.
- Put each item of a list on a new line.

## Coding

- KISS: the simplest solution that meets all the requirements.
- Make code self-explanatory. Refactor until the names carry the meaning, and write no comments.
- A *why* (constraint, invariant, workaround) goes in `docs/code-notes.md`, under a
  heading per source-file path.
- A decision goes in `docs/adr/`.

## Code review

- Every finding carries a risk level (high / medium / low) and a recommendation
  (fix / defer / ignore).

## Human-only operations

Ask a human to run these, even when they look routine:

- Anything that targets a non-local environment: deploys, production env files or
  credentials, migrations or seeds against a remote database.
- Drizzle CLI: `migrate`, `push`, `seed`.

## Agent skills

The engineering skills read their per-repo configuration from `docs/agents/*.md`. When a repo has no such files, fall back to the global defaults under `~/.agents/docs/agents/`.

### Issue tracker

Issues and specs live as local markdown files under `docs/.scratch/<feature-slug>/` in each repo. See `~/.agents/docs/agents/issue-tracker.md`, or the repo's `docs/agents/issue-tracker.md` if present.

### Triage labels

The five triage roles map to identically-named labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `~/.agents/docs/agents/triage-labels.md`, or the repo's `docs/agents/triage-labels.md` if present.

### Domain docs

Single-context by default, with one `CONTEXT.md` and `docs/adr/` at the repo root. A root `CONTEXT-MAP.md` makes the repo multi-context. See `~/.agents/docs/agents/domain.md`, or the repo's `docs/agents/domain.md` if present.

### Grilling

Each round asks at most 3 questions from the frontier, most valuable first. The rest waits for later rounds.
