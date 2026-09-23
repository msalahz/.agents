---
name: ticket-to-pr
description: Carry a GitHub issue or ticket file to an open pull request through a background agent, pausing at each step with a recommendation. Use when the user asks to implement or ship a ticket with a background agent.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.1"
---

# Ticket to PR

Carry one ticket from reading it to an open pull request. A background agent does the implementation in its own worktree; this session designs its prompt, reviews its work, and ships.

The argument is the task path: a GitHub issue URL or number, or a repo-relative path to a spec or ticket markdown file. With no argument, ask for it before anything else.

Every step below ends by asking the human, with one recommendation per question, and moves on their answer. Ask at most three questions per round, with choices listed `a`, `b`, `c`. Recommend the default the step names unless the ticket gives a reason to differ, and say the reason when it does.

## 1. Read the task

Read the ticket. A GitHub issue comes from `gh issue view <number> --json number,title,body,labels,comments`; a file comes from disk. Follow the pointers it carries: a spec path, a parent ticket, a `docs/decisions/` topic, glossary entries in `CONTEXT.md`, and the repo's `AGENTS.md`.

Show a two-line summary and the acceptance criteria as written, then ask whether that is the scope to build. Recommend the ticket's own criteria, with sibling tickets named as out of scope.

Done when: the human has confirmed the scope, with any exclusions written down.

## 2. Name the worktree

Propose `<issue-number>-<title-words>`, hyphen-separated, at most four parts in total, for both the worktree and the branch. The worktree lives at `.claude/worktrees/<name>` inside the repo. The branch starts from the default branch. `git check-ignore .claude/worktrees` confirms git ignores the directory. Ask the human to confirm or rename.

Create it with:

```
git worktree add -b <name> .claude/worktrees/<name> <default-branch>
```

Done when: `git worktree list` shows the new worktree on the new branch.

## 3. Pick the runtime

Ask which model and effort the agent runs with, recommending `opus` and `high`. Recommend `xhigh` when the ticket spans more than one domain. Ask which implementation skill the agent follows, recommending the mattpocock `implement` skill at `~/.claude/plugins/marketplaces/mattpocock/skills/engineering/implement/SKILL.md`.

Done when: model, effort, and the implementation skill path are recorded.

## 4. Write the prompt

Draft the agent prompt with these parts, in this order, as plain paragraphs and short lists:

- The ticket, by number and title, and the repo.
- The worktree path and branch, with every command run from there and `pnpm install` first when `node_modules` is missing.
- The implementation skill path, followed at every step except two: the agent commits nothing, and the review is done by the parent session.
- When the ticket adds or reshapes UI, the `frontend-design` skill path at `~/.agents/skills/frontend-design/SKILL.md`, followed for every UI change.
- Match the existing code patterns, abstractions, and design choices in the prior-art files and their neighbours. Extend an abstraction that already exists before adding a new one. Where the ticket leaves a choice open, name the file being matched.
- Files to read before changing anything: the ticket, the spec sections the ticket names, the binding `docs/decisions/` file, the `CONTEXT.md` entries, `AGENTS.md`, the output of `pnpm dlx @tanstack/intent@latest list` with any matching skill loaded, and the prior-art files the ticket points at.
- Scope as the acceptance criteria from step 1, numbered.
- Out of scope, naming the sibling tickets that own each item.
- Human-only steps: `db:migrate`, `db:push`, `db:seed`, and any remote environment.
- The coding rules from the Coding section of `~/.agents/AGENTS.md`.
- A done-when line that names two conditions, the repo's validate script passing and the changes sitting uncommitted in the worktree.
- A report format listing files changed, test and validate output verbatim, and follow-ups noticed but left alone.

Run the draft through `unslop-writing-for-agents`, show the unified diff, and ask for approval.

Done when: the human has approved the prompt.

## 5. Launch

Follow `spin-bg-agent` with the type `bg-<effort>`, the model from step 3, the prompt from step 4, and `<name>` as the description. Deliver its one-line report and tell the human the review starts when the agent reports back.

Done when: the subagent shows as running and the one-line report is delivered.

## 6. Review loop

When the agent reports, run `git status` and `git diff` inside the worktree and read every changed file against the acceptance criteria, the binding decisions file, and the Coding section of `~/.agents/AGENTS.md`. Give each finding a risk level (`high`, `medium`, `low`) and a recommendation (`fix`, `defer`, `ignore`). Show the findings and ask which to send. Recommend sending every `fix`.

Send the agreed findings to the agent with `SendMessage` and wait for its reply. Read the new diff and repeat.

Done when: the human and the agent agree nothing is left to fix, and the repo's validate script passes inside the worktree.

## 7. Ship

Ask before each of these five, recommending all five:

1. Commit on the worktree branch, ending the message with the trailers the session's attribution guidance names.
2. Push the branch with `git push -u origin <name>`.
3. Open the pull request with `gh pr create`, with a body that says `Closes #<number>` and ends with the attribution the session names for pull requests.
4. Comment on the ticket with the PR URL through `gh issue comment`.
5. Mark the ticket as in review. Change its triage label to `ready-for-human` with `gh issue edit --remove-label <agent label> --add-label ready-for-human`, reading both names from the triage-labels doc. When the issue sits on a GitHub Project, set its Status field to In review with `gh project item-edit`; a token without the `project` scope needs `gh auth refresh -s project`, which the human runs. The issue closes when the PR merges, through the `Closes` line; leave it open.

A file-based ticket has no issue to close, comment on, or relabel; steps 3 to 5 then link the ticket path in the PR body instead.

Done when: each step the human approved has run and its URL or hash is recorded.

## 8. Report

One paragraph: the worktree path, the branch, the PR URL, the ticket comment, and every human step still open, such as applying a migration.

Done when: the paragraph is delivered.
