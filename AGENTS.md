# Global agent memory

Applies to every repo. A repo's own `docs/agents/*.md`, `CONTEXT.md`, `CONTEXT-MAP.md`,
or `## Agent skills` section always wins over these defaults.

## General rules

- Do not restore, read from history, or cite files that git status shows as deleted. Treat them as if they never existed.

## Response rules

- Apply `unslop` to artifacts you write: docs, specs, commit messages, PR bodies.
- Label unverified claims `unverified` and say when you do not know.
- Subagent runs count as unattended. In interactive sessions ask at most three questions per round.

## Coding

- Use the simplest solution that meets every requirement.
- In code you write or change, refactor until names explain it. Write no comments. Leave other code alone.
- If you find a pre-existing bug or an improvement the task does not mention, do not fix it. Report it as a follow-up in your summary.
- Commit tests only where the task asks for them or the repo already keeps tests for that kind of change. Do not turn scratch checks into permanent test files.
- Edit files surgically. Rewrite a whole file only when it is short or most of it changes.
- End any session that changed code by running `pnpm validate`. If the repo has no such script, run its lint, typecheck, and test scripts instead and name what you ran. The session is done only when that passes.

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
