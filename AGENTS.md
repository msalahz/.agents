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

### Skill home

`~/.claude/CLAUDE.md` imports this file with `@~/.agents/AGENTS.md`. This file is the source of truth; edit here, not there. `~/.agents/skills` is the one inventory of every skill on this machine. Two kinds of entry live there, linked in opposite directions:

- **Personal and copied skills.** Real directories, tracked in this repo. Each is linked into Claude Code with `ln -s ../../.agents/skills/<name> ~/.claude/skills/<name>`. Codex reads `~/.agents/skills` directly and needs no link.
- **Plugin skills.** Installed by Claude Code under `~/.claude/plugins/` and updated by it. The link runs the opposite way: the plugin's skill directory stays where Claude Code put it, and a symlink is created in the home with `ln -s ~/.claude/plugins/marketplaces/<marketplace>/<path-to-skill> ~/.agents/skills/<name>`, then listed in `.gitignore`. Never copy a plugin skill into the home or link it into `~/.claude/skills`, since the plugin already registers it and would overwrite edits.

Any skill that creates or edits a skill, `skill-creator` included, follows these rules:

- Draft and edit in a scratch copy, never in the home. Put eval workspaces at `~/.agents/.scratch/<name>/`, not beside the skill.
- Install and remove only through `install-skill` and `uninstall-skill`, which keep the home and the link in sync. Do not package a `.skill` file.
- Edit a personal skill only through `update-skill`. A home that resolves outside `~/.agents/skills` is a plugin skill and is not edited here.
- Frontmatter carries `name`, `description`, and a `metadata` block with quoted `author` and `version`. `disable-model-invocation` is allowed even though `quick_validate.py` rejects it.
- Body uses one `## N. Title` section per step, each ending with a `Done when:` line.
- Descriptions state what the skill does and when it triggers, without padding. Prove triggering with skill-creator's eval loop instead of a pushy description.
