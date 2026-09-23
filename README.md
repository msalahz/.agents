# Agent home for [Mohammed Zaghloul](https://github.com/msalahz)

`~/.agents` is the tracked home for my global agent instructions, repository
defaults, and installed skills. Edit them here.

Claude Code loads the instructions through `~/.claude/CLAUDE.md`, which imports
`~/.agents/AGENTS.md`. Personal and copied skills are linked from
`~/.claude/skills` back into this repo. Codex reads `skills/` here directly. Plugin skills
point the other way: entries under `skills/` are symlinks into the Claude Code
marketplace checkouts.

## Layout

```text
~/.agents/
├── AGENTS.md                  global instructions loaded in every repo
├── docs/agents/               defaults for repos without their own guidance
│   ├── code-review/           Drizzle, React, TanStack Start, and TypeScript
│   ├── domain.md              domain-documentation conventions
│   ├── issue-tracker.md       local issue-tracker conventions
│   └── triage-labels.md       triage roles and state transitions
├── skills/                    48 installed skills
├── .skill-lock.json           metadata written by `npx skills`
└── README.md
```

A repo can override the defaults with its own `docs/agents/*.md`, `CONTEXT.md`,
`CONTEXT-MAP.md`, or `## Agent skills` section.

## Skill inventory

The 48 entries under `skills/` have four different ownership models.

| Kind | Count | Update path |
| --- | ---: | --- |
| Personal skills | 18 | Edit the directory in this repo |
| Matt Pocock skills | 25 | Update the Claude Code marketplace checkout |
| Other plugin skills | 4 | Update the plugin in Claude Code |
| Copied third-party skills | 1 | Reinstall or update the local copy |

### Personal skills

These are real directories tracked in this repo.

- [`arbitrate-review`](./skills/arbitrate-review/SKILL.md) settles a review loop that ran out of rounds by deciding and applying each open finding.
- [`archive-skill`](./skills/archive-skill/SKILL.md) moves a skill and everything it touched into `archive/<name>` so it can be restored.
- [`author-ticket`](./skills/author-ticket/SKILL.md) implements one sub-issue in a worktree, opens the PR, and runs the review loop with a reviewer session.
- [`coordinator`](./skills/coordinator/SKILL.md) turns the session into a coordinator that splits each task into pieces sized for one Operative peer session and has a second Operative verify each piece.
- [`favicon-generator`](./skills/favicon-generator/SKILL.md) generates favicons, touch icons, and a web manifest from a brand logo.
- [`install-skill`](./skills/install-skill/SKILL.md) installs a skill into this home and links it for Claude Code.
- [`knowledge-wiki`](./skills/knowledge-wiki/SKILL.md) keeps a verbatim wiki of domain expert answers inside a repo, with setup, ingest, ask, and lint.
- [`reply`](./skills/reply/SKILL.md) answers a question in text without changing anything.
- [`review-loop`](./skills/review-loop/SKILL.md) has a peer session review work against its spec while this session fixes the findings, until the reviewer agrees or 4 rounds pass and this session arbitrates.
- [`review-pr`](./skills/review-pr/SKILL.md) reviews a PR against its ticket's acceptance criteria, hunts bugs, and sends the author a verdict.
- [`simplify-skill`](./skills/simplify-skill/SKILL.md) cuts a skill down to its outcome and the constraints the agent cannot discover.
- [`spin-bg-agent`](./skills/spin-bg-agent/SKILL.md) launches a managed background subagent at a chosen effort level.
- [`spin-peer-session`](./skills/spin-peer-session/SKILL.md) launches an independent background Claude session with its own model, effort, and permission mode.
- [`supervise-issue`](./skills/supervise-issue/SKILL.md) drives a parent issue to completion through author and reviewer sessions, merging each approved PR.
- [`uninstall-skill`](./skills/uninstall-skill/SKILL.md) removes a skill and its Claude Code link.
- [`unslop-writing-for-agents`](./skills/unslop-writing-for-agents/SKILL.md) applies the agent-writing and `unslop` rules together.
- [`update-skill`](./skills/update-skill/SKILL.md) edits an installed skill through `skill-creator` and bumps its version.
- [`write-skill`](./skills/write-skill/SKILL.md) designs a skill with `skill-creator`, installs it, and live-tests it.

### Matt Pocock skills

These entries are symlinks into
`~/.claude/plugins/marketplaces/mattpocock/skills/`.

**Engineering**

- [`ask-matt`](./skills/ask-matt/SKILL.md) routes a task to the right skill or workflow.
- [`code-review`](./skills/code-review/SKILL.md) reviews changes since a fixed point against the repo's coding standards and the originating spec.
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

### Other plugin skills

These entries are symlinks into other marketplace checkouts under
`~/.claude/plugins/marketplaces/`. Claude Code registers them through the
plugin, so they have no link in `~/.claude/skills`.

- [`claude-api`](./skills/claude-api/SKILL.md) is Anthropic's reference for the Claude API and SDKs: model IDs, pricing, tool use, caching, and model migration.
- [`eli5`](./skills/eli5/SKILL.md) explains a topic with a dead-simple picture.
- [`frontend-design`](./skills/frontend-design/SKILL.md) is Anthropic's guidance for distinctive, intentional UI design.
- [`skill-creator`](./skills/skill-creator/SKILL.md) is Anthropic's skill design, eval, and description-optimization loop. `write-skill` and `update-skill` wrap it; the "Skill home" section of `AGENTS.md` tells it where skills live here.

### Copied third-party skills

These are real directories in this repo. They do not receive upstream changes
until they are updated or reinstalled.

| Skill | Source |
| --- | --- |
| [`unslop`](./skills/unslop/SKILL.md) | [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack) by poteto |

`.skill-lock.json` is installer metadata, not the authoritative inventory. It does not list every marketplace symlink.

## Managing skills

| Command | Action |
| --- | --- |
| `/write-skill` | Design a skill with `skill-creator`, install it, and test it |
| `/install-skill <path-or-url>` | Copy a skill into `skills/<name>` and link it |
| `/update-skill <name>` | Edit an installed skill, test it, and bump its version |
| `/uninstall-skill <name>` | Remove the skill directory and its link |
| `/simplify-skill <name>` | Cut a skill down to outcome and constraints |

Use these workflows instead of moving skill directories by hand. They keep this
home and `~/.claude/skills` in sync. Skills are created and edited in place
under `skills/`; review changes with `git diff` and revert with git. Eval
workspaces go to `.scratch/`, which git ignores.

## Supervised issue flow

`/supervise-issue <parent>` completes a parent GitHub issue one sub-issue at a
time. Every sub-issue gets its own worktree, author session, and reviewer
session. The supervisor writes no code. It plans, launches sessions, merges
approved PRs, and moves the project board.

```text
supervisor-<parent>        supervise-issue    plans, merges, tracks the board
├── author-<n>             author-ticket      one per sub-issue, in .claude/worktrees/<n>-<slug>
│   └── reviewer-<n>       review-pr          launched by the author, read-only
└── arbiter-<n>            arbitrate-review   only after 3 unresolved review rounds
```

1. **Preflight.** The supervisor checks that `.claude/settings.local.json`
   allows `Bash(gh pr merge *)`, that you ran `/rename supervisor-<parent>`,
   that `.claude/worktrees` is git-ignored, and that the default branch has
   nothing unpushed. The parent should sit on a project board whose Status
   field holds Backlog, Ready, In progress, In review, and Done. Without one
   it falls back to labels.
2. **Plan.** It reads each sub-issue's `## Blocked by` list, labels, and spec
   path, then marks the ticket as agent or human work with `high` or `medium`
   effort. It posts that table on the parent and waits for you to confirm it.
3. **Launch a wave.** A wave is every agent ticket whose blockers have merged.
   Each one gets a worktree branched from origin, an `author-<n>` session on
   Opus running `/author-ticket`, and In progress on the board.
4. **Author.** The author reads the ticket, spec, ADRs, and prior art,
   implements through `implement`, runs the repo's gates, and opens the PR.
   Acceptance criteria that need a remote environment go back to the
   supervisor as human-only.
5. **Review.** The author launches `reviewer-<n>` with `/review-pr`. The
   reviewer runs a spec pass and a bug pass in subagents and sends risk-rated
   findings that end in a verdict. The author fixes or rebuts them for up to
   three rounds, then writes the outcome into a `## Review` section of the PR
   body. A same-account PR cannot carry a GitHub approval, so that section is
   the review record.
6. **Arbitrate.** When three rounds end with findings still open, the
   supervisor launches `arbiter-<n>` on Fable with `/arbitrate-review`. The
   arbiter upholds or dismisses each finding, pushes fixes for the ones it
   upholds, and reports.
7. **Merge.** The supervisor merges only when the PR is mergeable and every CI
   check passes. It stops the ticket's sessions, removes the worktree,
   squash-merges, deletes the branch, and moves the ticket to Done. Then it
   tells the other open authors to rebase and launches the next wave. A
   conflict goes back to the author as `Rebase #<n> onto <default>`, followed
   by one review round on the resolution.
8. **Hand back.** When only human tickets remain, the supervisor sets them to
   Ready, comments on the parent with the merged PRs, review rounds, and
   follow-ups, and stops. Once you say the parent is complete, it removes the
   sessions, closes the parent, and deletes its state.

Sessions talk over SendMessage. The supervisor acts on these first lines:

| Report line | From | Supervisor action |
| --- | --- | --- |
| `PR #<pr> opened for #<n>` | author | Board to In review |
| `PR #<pr> approved for #<n> after round <k>` | author | Merge |
| `PR #<pr> rebased and approved` | author | Merge |
| `PR #<pr> unresolved for #<n> after 3 rounds` | author | Launch the arbiter |
| `PR #<pr> arbitrated for #<n>` | arbiter | Merge |

The supervisor keeps its state in `.scratch/<repo>-issue-<parent>/state.md`, so a
resumed supervisor picks up where the last one stopped. No session in the flow
deploys, reads production secrets, or changes a remote environment. Those
steps stay on the human tickets.

## House rules

[`AGENTS.md`](./AGENTS.md) is the source of truth. In short:

- Run `unslop` before writing.
- Mark every claim that has not been verified as `unverified`.
- Prefer the simplest implementation that meets the requirements.
- Use self-explanatory code instead of comments.
- Run `pnpm validate` after changing code.
- Leave deploys, remote database operations, and Drizzle CLI commands to a human.
