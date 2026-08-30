# Global agent memory

Applies to every repo. A repo's own `docs/agents/*.md`, `CONTEXT.md`, `CONTEXT-MAP.md`,
or `## Agent skills` section always wins over these defaults.

## general rules

- Ignore pruned files and archives.

## Response rules

- Invoke `unslop` before the first written response in each session. Apply it to
  every later response and artifact.
- Apply `writing-for-agents` and `unslop` to every subagent prompt.
- Label every unverified claim `unconfirmed`.
- State when you do not know something.
- During interactive work, ask for important missing details.
- During unattended work, make and label the safest assumption.
- Write each list item on its own line.

## Coding

- Use the simplest solution that meets every requirement.
- Refactor until names explain the code. Write no comments.
- End any session that changed code by running `pnpm validate`; the session is done only when it passes.

## Code review

- Give every finding a risk level: `high`, `medium`, or `low`.
- Give every finding a recommendation: `fix`, `defer`, or `ignore`.

## Ask a human to run:

Ask a human to run these, even when they look routine:

- Anything that targets a non-local environment: deploys, production env files or
  credentials, migrations or seeds against a remote database.
- The Drizzle CLI commands `migrate`, `push`, and `seed`.

## Agent skills

The engineering skills read their per-repo configuration from `docs/agents/*.md`. When a repo has no such files, fall back to the global defaults under `~/.agents/docs/agents/`.

### Issue tracker

Specs live in the repo as markdown at `docs/.scratch/<feature-slug>/spec.md`; issues live on GitHub, via the `gh` CLI. Repos with no GitHub remote keep their tickets on disk beside the spec. See `~/.agents/docs/agents/issue-tracker.md`, or the repo's `docs/agents/issue-tracker.md` if present.

### Triage labels

The five triage roles map to identically-named labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `~/.agents/docs/agents/triage-labels.md`, or the repo's `docs/agents/triage-labels.md` if present.

### Domain docs

Single-context by default, with one `CONTEXT.md` and `docs/adr/` at the repo root. A root `CONTEXT-MAP.md` makes the repo multi-context. See `~/.agents/docs/agents/domain.md`, or the repo's `docs/agents/domain.md` if present.

### Grilling

- Ask at most three questions per round.
- Format choices within a question as a list labeled `a`, `b`, and `c`.

### Background subagents

- Use `bg-low`, `bg-medium`, `bg-high`, `bg-xhigh`, or `bg-max` when launching a
- background subagent at a named reasoning effort. Set the model in the launch
- call. Use `/spin-bg-agent` for the full workflow.
