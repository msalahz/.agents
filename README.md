# Agent home for [Mohammed Zaghoul](https://github.com/msalahz)

`~/.agents` is the tracked home for [Mohammed Zaghoul](https://github.com/msalahz) global agent memory and for the skills I
write myself. Claude Code keeps no copy of any of it. `~/.claude` imports and
symlinks straight back here, so this repo is the one place to edit.

## Layout

```
~/.agents/
├── AGENTS.md          global memory, loaded in every session
├── docs/agents/       defaults for repos that ship none of their own
├── skills/            36 skills, some written here, some symlinked out
└── .skill-lock.json   where the GitHub-installed skills came from
```

`AGENTS.md` is the one that matters most. `~/.claude/CLAUDE.md` imports it, so it
loads in every session, in every repo. A repo's own `docs/agents/*.md`,
`CONTEXT.md`, `CONTEXT-MAP.md`, or `## Agent skills` section overrides it.

## Skills

### Where they came from

Five are mine, written here. Twenty-five are Matt Pocock's, symlinked into his
marketplace checkout, so they update when he ships. The other six are copies
pulled from GitHub.

| Skill             | From                                                                     |
| ----------------- | ------------------------------------------------------------------------ |
| `unslop`          | [`pstack`](https://github.com/cursor/plugins/tree/main/pstack) by poteto |
| `humanizer`       | [`blader/humanizer`](https://github.com/blader/humanizer)                |
| `frontend-design` | [`anthropics/skills`](https://github.com/anthropics/skills)              |
| `find-skills`     | [`vercel-labs/skills`](https://github.com/vercel-labs/skills)            |
| `autofix`         | [`coderabbitai/skills`](https://github.com/coderabbitai/skills)          |
| `varlock`         | [`dmno-dev/varlock`](https://github.com/dmno-dev/varlock)                |

Being copies, they see no upstream changes until I reinstall them.

### Adding and removing

| Command                      | Does                                              |
| ---------------------------- | ------------------------------------------------- |
| `/write-skill`               | Builds a new skill end to end, then installs it   |
| `/install-skill <path\|url>` | Copies a source into `skills/<name>` and links it |
| `/uninstall-skill <name>`    | Removes the directory and the link                |

Go through the skills rather than moving directories by hand, so the home and the
link never disagree.

## My skills

The five I wrote. They live in this repo as real directories, so an edit here is
live after a reload.

**User-invoked**

- **[uninstall-skill](./skills/uninstall-skill/SKILL.md).** Remove a skill's home here and its link in `~/.claude/skills`. The one destructive skill in the set, so it stays behind the slash command.

**Model-invoked**

- **[install-skill](./skills/install-skill/SKILL.md).** Install a skill from a path, archive, or git URL into `skills/<name>`, review it against `writing-for-agents`, then link it for Claude Code.
- **[unslop-writing-for-agents](./skills/unslop-writing-for-agents/SKILL.md).** Review a text against `writing-for-agents` and `unslop`, show every fix as a diff, apply on approval.
- **[write-skill](./skills/write-skill/SKILL.md).** Draft, install, and live-test a new skill end to end. Drives `unslop-writing-for-agents` and `install-skill`.
- **[spin-peer-claude-session](./skills/spin-peer-claude-session/SKILL.md).** Launch an independent peer Claude session with its own model, effort, and instructions.

## Skills from others

The other 31. They split on one axis, who can invoke them. **User-invoked**
skills only run when I type them, like `/grill-me`. **Model-invoked** skills run
when I type them or when the agent reaches for one because the task fits.

### Engineering

**User-invoked**

- **[ask-matt](./skills/ask-matt/SKILL.md).** Router over Matt Pocock's user-invoked skills. Ask it which one fits.
- **[grill-with-docs](./skills/grill-with-docs/SKILL.md).** Grilling session that also writes `CONTEXT.md` and ADRs as terms get resolved.
- **[to-spec](./skills/to-spec/SKILL.md).** Turn the current conversation into a spec, no interview.
- **[to-tickets](./skills/to-tickets/SKILL.md).** Break a plan or spec into tracer-bullet tickets with their blocking edges.
- **[implement](./skills/implement/SKILL.md).** Build the work a spec or ticket set describes, driving `/tdd` and closing with `/code-review`.
- **[triage](./skills/triage/SKILL.md).** Move issues and external PRs through the triage state machine.
- **[wayfinder](./skills/wayfinder/SKILL.md).** Plan work too big for one session as a map of decision tickets, resolved one at a time.
- **[improve-codebase-architecture](./skills/improve-codebase-architecture/SKILL.md).** Survey a codebase for deepening opportunities, report them, grill through the one I pick.
- **[setup-matt-pocock-skills](./skills/setup-matt-pocock-skills/SKILL.md).** Configure a repo for the engineering skills. Run once per repo.

**Model-invoked**

- **[tdd](./skills/tdd/SKILL.md).** Red-green-refactor, one vertical slice at a time.
- **[diagnosing-bugs](./skills/diagnosing-bugs/SKILL.md).** Gated diagnosis loop for hard bugs and performance regressions.
- **[code-review](./skills/code-review/SKILL.md).** Reviews a diff on two axes, standards and spec, in parallel sub-agents.
- **[codebase-design](./skills/codebase-design/SKILL.md).** Vocabulary for deep modules: much behaviour, small interface, clean seam.
- **[domain-modeling](./skills/domain-modeling/SKILL.md).** Sharpen a project's domain model and record it in `CONTEXT.md` and ADRs.
- **[prototype](./skills/prototype/SKILL.md).** Throwaway prototype to answer one design question.
- **[research](./skills/research/SKILL.md).** Background agent that answers a question from primary sources and files the findings.
- **[resolving-merge-conflicts](./skills/resolving-merge-conflicts/SKILL.md).** Work a merge or rebase conflict hunk by hunk. Never `--abort`.
- **[wizard](./skills/wizard/SKILL.md).** Generate a bash wizard for steps only a human can do.
- **[autofix](./skills/autofix/SKILL.md).** Apply CodeRabbit review-thread feedback with per-change approval.
- **[varlock](./skills/varlock/SKILL.md).** Handle secrets and env vars without leaking them into logs or context.
- **[frontend-design](./skills/frontend-design/SKILL.md).** Visual direction for new UI that does not read as a template.

### Productivity

**User-invoked**

- **[grill-me](./skills/grill-me/SKILL.md).** Relentless interview about a plan until every branch is resolved.
- **[handoff](./skills/handoff/SKILL.md).** Compact this conversation into a handoff doc for the next agent.
- **[teach](./skills/teach/SKILL.md).** Teach me a concept across sessions, using the current directory as the workspace.
- **[to-questionnaire](./skills/to-questionnaire/SKILL.md).** Turn a decision I cannot make alone into a questionnaire for whoever can.
- **[wait-what](./skills/wait-what/SKILL.md).** Fire this the moment a message does not land. The agent re-pitches it.

**Model-invoked**

- **[grilling](./skills/grilling/SKILL.md).** The interview loop the grill skills are built on.
- **[find-skills](./skills/find-skills/SKILL.md).** Search for a skill that does the thing I just described.

### Writing

**Model-invoked**

- **[unslop](./skills/unslop/SKILL.md).** Cut AI tells from any writing. Always on.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md).** How to write anything an agent reads: skills, `AGENTS.md`, pointer docs.
- **[humanizer](./skills/humanizer/SKILL.md).** The same job as `unslop`, from Wikipedia's signs-of-AI-writing guide.

## House rules

`AGENTS.md` carries them. The short version: `unslop` before writing anything,
label unverified claims, keep code self-explanatory with no comments, and leave
deploys, remote databases, and Drizzle CLI commands to a human.
