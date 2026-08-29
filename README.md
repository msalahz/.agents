# Agent home for [Mohammed Zaghloul](https://github.com/msalahz)

`~/.agents` is the tracked home for my global agent instructions, repository
defaults, and installed skills. Edit them here.

Claude Code loads the instructions through `~/.claude/CLAUDE.md`, which imports
`~/.agents/AGENTS.md`. Personal and copied skills are linked from
`~/.claude/skills` back into this repo. Skills from Matt Pocock point the other
way: entries under `skills/` are symlinks into his Claude Code marketplace
checkout.

## Layout

```text
~/.agents/
├── AGENTS.md                  global instructions loaded in every repo
├── docs/agents/               defaults for repos without their own guidance
│   ├── code-review/           Drizzle, React, TanStack Start, and TypeScript
│   ├── domain.md              domain-documentation conventions
│   ├── issue-tracker.md       local issue-tracker conventions
│   └── triage-labels.md       triage roles and state transitions
├── skills/                    39 installed skills
├── .skill-lock.json           metadata written by `npx skills`
└── README.md
```

A repo can override the defaults with its own `docs/agents/*.md`, `CONTEXT.md`,
`CONTEXT-MAP.md`, or `## Agent skills` section.

## Skill inventory

The 39 entries under `skills/` have three different ownership models.

| Kind | Count | Update path |
| --- | ---: | --- |
| Personal skills | 10 | Edit the directory in this repo |
| Matt Pocock skills | 24 | Update the Claude Code marketplace checkout |
| Copied third-party skills | 5 | Reinstall or update the local copy |

### Personal skills

These are real directories tracked in this repo.

- [`install-skill`](./skills/install-skill/SKILL.md) installs a skill into this home and links it for Claude Code.
- [`review-loop`](./skills/review-loop/SKILL.md) alternates peer review and fixes until both sessions agree.
- [`spin-bg-agent`](./skills/spin-bg-agent/SKILL.md) launches a managed background subagent at a chosen effort level.
- [`spin-peer-claude-session`](./skills/spin-peer-claude-session/SKILL.md) launches an independent Claude session.
- [`to-html`](./skills/to-html/SKILL.md) renders a report as one self-contained HTML file.
- [`uninstall-skill`](./skills/uninstall-skill/SKILL.md) removes a skill and its Claude Code link.
- [`unslop-writing-for-agents`](./skills/unslop-writing-for-agents/SKILL.md) applies the agent-writing and `unslop` rules together.
- [`update-skill`](./skills/update-skill/SKILL.md) edits an installed skill and bumps its version.
- [`worktree-stash`](./skills/worktree-stash/SKILL.md) completes work in a worktree and returns it as a named stash.
- [`write-skill`](./skills/write-skill/SKILL.md) builds, installs, and live-tests a personal skill.

### Matt Pocock skills

These entries are symlinks into
`~/.claude/plugins/marketplaces/mattpocock/skills/`.

**Engineering**

- [`ask-matt`](./skills/ask-matt/SKILL.md) routes a task to the right skill or workflow.
- [`codebase-design`](./skills/codebase-design/SKILL.md) supplies the shared vocabulary for deep modules and clean seams.
- [`diagnosing-bugs`](./skills/diagnosing-bugs/SKILL.md) runs the evidence-first loop for bugs and regressions.
- [`domain-modeling`](./skills/domain-modeling/SKILL.md) sharpens domain terms and records decisions.
- [`grill-with-docs`](./skills/grill-with-docs/SKILL.md) stress-tests a plan while maintaining domain docs.
- [`implement`](./skills/implement/SKILL.md) implements work described by a spec or ticket set.
- [`improve-codebase-architecture`](./skills/improve-codebase-architecture/SKILL.md) finds and works through module-deepening opportunities.
- [`prototype`](./skills/prototype/SKILL.md) builds a throwaway implementation to answer one design question.
- [`research`](./skills/research/SKILL.md) researches primary sources and writes the findings into the repo.
- [`resolving-merge-conflicts`](./skills/resolving-merge-conflicts/SKILL.md) resolves an in-progress merge or rebase hunk by hunk.
- [`setup-matt-pocock-skills`](./skills/setup-matt-pocock-skills/SKILL.md) installs the repo-level defaults used by the engineering workflows.
- [`tdd`](./skills/tdd/SKILL.md) works red, green, refactor in vertical slices.
- [`to-spec`](./skills/to-spec/SKILL.md) turns the current conversation into a spec.
- [`to-tickets`](./skills/to-tickets/SKILL.md) splits a plan into tracer-bullet tickets with blocking edges.
- [`triage`](./skills/triage/SKILL.md) moves issues and external PRs through the triage states.
- [`wayfinder`](./skills/wayfinder/SKILL.md) maps work too large for one session into decision tickets.
- [`wizard`](./skills/wizard/SKILL.md) writes an interactive shell guide for human-only operations.

**Productivity and writing**

- [`grill-me`](./skills/grill-me/SKILL.md) stress-tests a plan or design through questions.
- [`grilling`](./skills/grilling/SKILL.md) provides the interview loop used by the grill skills.
- [`handoff`](./skills/handoff/SKILL.md) compacts a conversation into a handoff document.
- [`teach`](./skills/teach/SKILL.md) teaches a concept using the current workspace.
- [`to-questionnaire`](./skills/to-questionnaire/SKILL.md) turns an unresolved decision into questions for the person who can answer them.
- [`wait-what`](./skills/wait-what/SKILL.md) asks the agent to re-pitch a message that did not land.
- [`writing-for-agents`](./skills/writing-for-agents/SKILL.md) defines how to write skills and other agent-facing instructions.

### Copied third-party skills

These are real directories in this repo. They do not receive upstream changes
until they are updated or reinstalled.

| Skill | Source |
| --- | --- |
| [`autofix`](./skills/autofix/SKILL.md) | [`coderabbitai/skills`](https://github.com/coderabbitai/skills) |
| [`find-skills`](./skills/find-skills/SKILL.md) | [`vercel-labs/skills`](https://github.com/vercel-labs/skills) |
| [`frontend-design`](./skills/frontend-design/SKILL.md) | [`anthropics/skills`](https://github.com/anthropics/skills) |
| [`unslop`](./skills/unslop/SKILL.md) | [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack) by poteto |
| [`varlock`](./skills/varlock/SKILL.md) | [`dmno-dev/varlock`](https://github.com/dmno-dev/varlock) |

`.skill-lock.json` is installer metadata, not the authoritative inventory. it does not list every marketplace symlink.

## Managing skills

| Command | Action |
| --- | --- |
| `/write-skill` | Build, install, and test a new personal skill |
| `/install-skill <path-or-url>` | Copy a skill into `skills/<name>` and link it |
| `/update-skill <name>` | Edit an installed skill and bump its version |
| `/uninstall-skill <name>` | Remove the skill directory and its link |

Use these workflows instead of moving skill directories by hand. They keep this
home and `~/.claude/skills` in sync.

## House rules

[`AGENTS.md`](./AGENTS.md) is the source of truth. In short:

- Run `unslop` before writing.
- Mark every claim that has not been verified as `unconfirmed`.
- Prefer the simplest implementation that meets the requirements.
- Use self-explanatory code instead of comments.
- Run `pnpm validate` after changing code.
- Leave deploys, remote database operations, and Drizzle CLI commands to a human.
