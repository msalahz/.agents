---
name: author-ticket
description: Implement one GitHub sub-issue in its own worktree as the author session of a supervised run, open the PR, and drive a three-round review loop with a reviewer session. Use when a supervise-issue session launches /author-ticket with a ticket number, worktree name, and supervisor name.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.1"
---

# Author ticket

Arguments: `<n> <worktree> <supervisor-name>`. This session runs under the display name `author-<n>`, set by the supervisor at launch. It implements ticket `#<n>` in `.claude/worktrees/<worktree>` on the branch of the same name, opens the PR, launches its own reviewer, and reports to the supervisor with the fixed lines in step 6. It never merges, never force-pushes except a rebase the supervisor asked for, and never touches a remote environment.

Every command runs inside the worktree; `pnpm install` comes first when `node_modules` is missing.

## 1. Read

In this order, before changing anything:

1. `gh issue view <n> --comments`: scope, acceptance criteria, `## Blocked by`, the `Spec:` path on the first line, the parent number.
2. The spec sections the ticket names, and any research notes beside the spec.
3. `docs/adr/*.md`, `AGENTS.md`, the runbooks the ticket points at.
4. The Coding rules in `~/.agents/AGENTS.md`.
5. `pnpm dlx @tanstack/intent@latest list`; load any skill matching the task with `pnpm dlx @tanstack/intent@latest load <package>#<skill>`.
6. The prior-art files the ticket names and their neighbours.

Scope is exactly the ticket's acceptance criteria. Sibling tickets under the same parent own everything else, even when adjacent. A gap that belongs to a sibling goes in the PR body, not the diff. A criterion that needs a remote environment or credentials goes to the supervisor in the PR-opened report as a human-only criterion; do not attempt it.

Done when: every file above has been read and the criteria are listed, numbered.

## 2. Implement

Follow the implement skill at `~/.agents/skills/implement/SKILL.md` with two substitutions: its `/code-review` step is the loop in step 5, and `/tdd` applies only where the repo already keeps tests of that kind. Resolve any merge or rebase conflict with the skill at `~/.agents/skills/resolving-merge-conflicts/SKILL.md`.

Limits that hold whatever the ticket says: no deploys, no `tofu apply`, no `gcloud` mutations, no DNS changes, no reading of production or staging secrets. `tofu init -backend=false`, `tofu validate`, and offline plans are fine.

Done when: every numbered criterion is met by the diff, or marked human-only.

## 3. Gate

Run the repo's validate script, its build, and for infrastructure changes `tofu fmt -check` and `tofu validate`. Read the real exit code of each: no `| tail`, no `| head` on a gate, and `set -o pipefail` when a pipe is unavoidable. A local build that fails only because a secret manager is unreachable is reported as such, with CI as the arbiter; anything else is fixed before commit.

Done when: each gate's real exit code has been read.

## 4. Commit and open the PR

Small logical commits with conventional-commit subjects. Each message ends with the trailer this session's own attribution guidance names; do not copy a model name from anywhere else. Push with `git push -u origin <worktree>`.

Open the PR against the default branch with `gh pr create`, title `<type>: <summary> (#<n>)`. Body: what changed; each acceptance criterion and how the diff meets it; criteria left to a human and why; follow-ups noticed and left alone; `Closes #<n>`; then the pull-request attribution line the session's guidance names. Plain and specific.

Report to the supervisor, first line `PR #<pr> opened for #<n>`, then the URL and any human-only criteria.

Done when: the PR exists and the supervisor has the opened line.

## 5. Review loop

Launch the reviewer from the worktree:

```
claude --bg --name reviewer-<n> --model opus --effort xhigh --permission-mode auto "/review-pr <pr> <n> author-<n>"
```

Wait for its message. It ends with `VERDICT: APPROVED` or `VERDICT: CHANGES REQUESTED` and lists findings with a risk level and a recommendation.

On changes requested: fix every `fix` finding you agree with; for each you reject, reply with the reason. Re-run step 3, commit, push, and message `reviewer-<n>` with `re-review round <k>`. Three rounds in total, counting the first.

When the supervisor sends `Rebase #<n> onto <default>`: `git fetch origin`, `git rebase origin/<default>`, resolve with the resolving-merge-conflicts skill keeping both sides' intent, re-run step 3, `git push --force-with-lease origin <worktree>`, then message `reviewer-<n>` with `re-review round <k>, conflict resolution only`. That round does not count toward the three.

Done when: the reviewer has sent APPROVED, or three rounds have passed.

## 6. Record, report, and wait

Append a `## Review` section to the PR body with `gh pr edit <pr> --body-file`: the rounds run, the findings fixed with their commits, the findings deferred with the ticket that owns each, and the final verdict line. That section is the only record of the review, since a same-account PR cannot carry a GitHub approval.

Then send the supervisor one of these first lines, then the detail:

- `PR #<pr> approved for #<n> after round <k>`: two lines on what changed during review.
- `PR #<pr> rebased and approved`: what conflicted and how it was resolved.
- `PR #<pr> unresolved for #<n> after 3 rounds`: each open finding on one line with both positions.

If the send to `<supervisor-name>` fails, run ListAgents and use the row whose name starts with `supervisor`. Then stop and wait; start nothing else.

Done when: the supervisor has the report line.
