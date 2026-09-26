---
name: supervise-issue
description: Drive a parent GitHub issue to completion by running phased author sessions and a reviewer session per sub-issue, merging each approved PR, and tracking status on a project board. Use when the user types /supervise-issue with an issue number or URL.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.0"
---

# Supervise issue

The argument is a parent issue, as a number or URL. This session is the supervisor. It never writes code. It plans, launches `author-ticket` sessions per sub-issue one phase at a time, watches the reports, merges approved PRs, moves the board, and hands the human-only tickets back.

Sessions talk over SendMessage. The author launches its own `review-pr` session and runs the review loop; the supervisor hears only the fixed report lines listed under step 5. A loop that runs out of rounds goes to an `arbitrate-review` session.

State lives at `~/.agents/.scratch/<repo>-issue-<n>/state.md`: a table of ticket, worktree, branch, current phase, author ids one per phase, reviewer id, PR, status, plus the launch and cleanup recipes below, kept current so a resumed session can carry on from it. Handoff files sit beside it.

The supervisor breaks each ticket into phases by the Breaking-work-down rules in `~/.agents/docs/agents/delegation.md`, and sizes every author, reviewer, and arbiter launch against that bound before it runs. Each phase is a fresh session under the same name `author-<n>`, so the reviewer still reaches it:

- `implement`: author-ticket steps 1 to 3 and the commits of step 4, ending before the push.
- `pr`: the browser checks the Coding rules in `~/.agents/AGENTS.md` ask of a UI change, then the push, PR, and opened report of step 4. Screenshots fill context fast, so this phase stands alone.
- `review`: author-ticket steps 5 and 6. Its prompt also carries a reviewer copy of the handoff block and tells the author to append it to the reviewer launch prompt.

Every launch prompt carries the handoff block below. Its `<file>` is an absolute path in the state directory: `handoff-<n>.md` for an author, `handoff-<n>-reviewer.md` for a reviewer, `handoff-<n>-arbiter.md` for an arbiter.

```
Handoff file: <file>. Write it as the Running-as-a-subagent rules in ~/.agents/docs/agents/delegation.md say, and also when this phase's work is done and a later phase remains. Then send <supervisor-name> a message whose first line is `Handoff written for #<n>` and whose second line is the file path, and stop.
```

Three helpers sit in `scripts/`:

- `gh-retry.sh <gh args...>` runs a gh command up to three times, five seconds apart, since the API drops TLS handshakes often enough to break a single call. Every gh call goes through it except two: `gh pr merge`, which must run bare so the allow rule matches, and `gh pr checks`, whose non-zero exit on a pending or failed check is an answer, not a fault.
- `project-status.sh <owner> <project-number> <repo> <issue> <status>` sets the project's Status field for the item that tracks the issue. Status names match exactly, such as `"In progress"`.
- `session-uuid.sh <name> [cwd]` prints the full session id of the newest background session with that display name, narrowed by working directory when given.

Every git command names its checkout with `git -C <path>`, and every launch runs in a `(cd <worktree> && ...)` subshell, because a bare `cd` moves the session's working directory and a later command lands in the wrong checkout.

## 1. Preflight

Check each item and collect the misses. Ask the user to fix them in one message, since the classifier refuses to let this session edit its own settings:

- `.claude/settings.local.json` allows `Bash(gh pr merge *)`. Without it the classifier refuses every merge as "Merge Without Review".
- The user has run `/rename supervisor-<n>` so the session name stays put. Names are otherwise generated from the first prompt and change after the first turn.
- `git check-ignore .claude/worktrees` succeeds, and `git log origin/<default>..<default>` prints nothing, so the default branch has nothing unpushed. Sub-issue branches start from origin.
- `~/.agents/skills/implement/SKILL.md` and `~/.agents/skills/resolving-merge-conflicts/SKILL.md` resolve. Both are human-invocation skills, so authors read them by path.
- The issue sits on a GitHub project with a single-select Status field holding Backlog, Ready, In progress, In review, Done. Read the project number from the issue's `projectItems`. With no project, fall back to labels `in-progress`, `in-review`, and closing the issue.

Then run ListAgents once and record the line "This session is `<name> [ref]`". That name goes to every author.

Done when: every item passes, or the user has been given the exact fix for each miss and confirmed it is applied.

## 2. Plan

Read the parent with `gh issue view <n>` and its sub-issues through the GraphQL `subIssues` connection. For each sub-issue read the body, the `## Blocked by` list, the labels, and the spec path on its first line. Build the table: ticket, blockers, effort, phases, agent or human. `ready-for-human` tickets and tickets whose acceptance criteria need a remote environment are human; everything else is agent work. Effort is `high` for tickets that touch scripts or more than one domain, `medium` otherwise. Phases default to `implement, pr, review`; a small ticket may merge two, as `implement+pr`, when one session can finish the merged work inside the same bound.

Post the table as a comment on the parent and show it to the user with at most three questions, each with choices `a`, `b`, `c` and a recommendation. Ask only what changes the work: status tracking when there is no project, effort overrides, and what to do with human-only criteria found inside agent tickets.

Done when: the user has confirmed the table and the order, and the state file holds it.

## 3. Launch a wave

A wave is every agent ticket whose blockers are all merged. For each ticket, from the repo root:

```
git -C <repo> fetch origin
git -C <repo> worktree add -b <n>-<slug> .claude/worktrees/<n>-<slug> origin/<default>
(cd <repo>/.claude/worktrees/<n>-<slug> && claude --bg --name author-<n> --model opus --effort <effort> --permission-mode auto "<prompt>")
scripts/project-status.sh <owner> <project> <repo> <n> "In progress"
```

The prompt holds, on separate lines, `/author-ticket <n> <n>-<slug> <supervisor-name>`, `Phase <phase>: <the author-ticket steps it covers>. Run only these.`, and the handoff block.

`--permission-mode auto` is deliberate. The classifier refuses `bypassPermissions` launches, and a session in the same permission class as the supervisor receives peer messages without a human approving each one.

Record the short id `claude --bg` prints and the phase, then subscribe to each new author by sending `author-<n>` a SendMessage with `notify_when_idle: true` and no message. Names are exact: `author-<n>`, `reviewer-<n>`, `arbiter-<n>`.

Done when: every ticket in the wave has a worktree, a running author, In progress on the board, an idle subscription, and a row in the state file.

## 4. Monitor

There is no polling. CronCreate is refused by the classifier, so the only inputs are author messages and idle notices. An idle notice repeats with the same timestamp; a repeat is a no-op. An idle notice whose text says the author is waiting on its reviewer is also a no-op, apart from renewing the subscription.

Act on these:

- An author idle with no report and no reviewer running: read `claude logs <id>`, then message it with what is missing.
- An author stopped after writing its handoff file: a planned phase end. Handle the file as in step 5 if its message has not arrived.
- An author exited with no handoff file: `claude agents --json --all` shows it as done. Resume it with `claude --bg --resume $(scripts/session-uuid.sh author-<n> <worktree>) --permission-mode auto "<what to do next>"` from the worktree. The short id opens an interactive picker and hangs, so only the full id works.
- An author reporting a human-only acceptance criterion: propose moving it to the human ticket, strikethrough on the source with a "moved to #m" note, the criterion appended on the target, one comment on the source. Do it only on the user's yes.

Done when: every live session has a subscription and every notice has been handled or dismissed.

## 5. Handle reports

Workers send fixed first lines. Match on them:

- `PR #<pr> opened for #<n>`: set In review.
- `PR #<pr> approved for #<n> after round <k>` or `PR #<pr> rebased and approved`: go to step 6.
- `PR #<pr> unresolved for #<n> after 3 rounds`: launch the arbiter from the worktree with `claude --bg --name arbiter-<n> --model fable --effort high --permission-mode auto "<prompt>"` and subscribe, where the prompt holds, on separate lines, `/arbitrate-review <pr> <n>`, then `Author: author-<n>. Reviewer: reviewer-<n>. Supervisor: <supervisor-name>.`, then the author's full unresolved report verbatim, then the handoff block. No record of the dispute exists on GitHub, so the launch message is the arbiter's only source. Its `PR #<pr> arbitrated for #<n>` report is treated as approval.
- `Handoff written for #<n>`: read the file on the second line, then `claude stop` the sender. Launch its successor from the worktree with the sender's name and first-launch flags, so an author comes back as `--name author-<n>`. The prompt holds, on separate lines, a skill line, a phase line, `Read <file> first and skip re-reading what it settles.`, and the handoff block. An author's skill line is `Read ~/.agents/skills/author-ticket/SKILL.md, arguments <n> <n>-<slug> <supervisor-name>`, and its phase line is the one from step 3. An author continues the same phase after a context-bound handoff and moves to the plan's next phase otherwise. A reviewer or arbiter gets its first launch's command line and no phase line. Record the new session id and phase in the state file, and subscribe.

A `[Cross-session delivery notice]` saying a message was held means the peer runs in another permission class; relaunch it with `--permission-mode auto`.

Done when: each report line has produced its board change, merge, or launch.

## 6. Merge and close out a ticket

In this order, each as its own command:

1. `gh pr view <pr> --json mergeable,mergeStateStatus` is MERGEABLE and CLEAN. CONFLICTING means another PR landed first: send the author a message whose first line is `Rebase #<n> onto <default>`, naming the merged PRs and the files they touched. The author rebases, resolves, pushes, and gets one review round scoped to the conflict resolution. Wait for `PR #<pr> rebased and approved`.
2. `gh pr checks <pr> --json name,state,bucket`, called bare, shows every check with bucket `pass`. Any other bucket means not ready. CI is the arbiter; a local build that fails on missing secrets does not count against the PR. A GitHub approval is impossible when the same account authored the PR, so the review evidence is the author's report and the PR body.
3. `claude stop <id>` for the author, the reviewer, and the arbiter if one ran, each id being the short `id` field of its row in `claude agents --json`, found by name. Their working directory is about to go. Keep them; `claude rm` waits for step 8.
4. `git -C <repo> worktree remove --force .claude/worktrees/<n>-<slug>` then `git -C <repo> worktree prune`, and `rm -rf` any leftover directory. The merge's branch deletion fails while a worktree holds the branch.
5. `gh pr merge <pr> --squash --delete-branch`, bare and alone on its command line, not through the retry wrapper. The allow rule matches the whole command, so a wrapper prefix, a `;`, or a `&&` chain is refused.
6. `git -C <repo> branch -D <n>-<slug>`, then `git -C <repo> fetch origin` and `git -C <repo> merge --ff-only origin/<default>`.
7. Board Done; `gh issue view <n>` should already be CLOSED through the PR's `Closes` line, otherwise close it.
8. Message every author with an open PR that `<default>` moved and which files the merge touched, so it rebases before its next round. Then launch the next wave with step 3.

Done when: the PR is merged, the board says Done, the sessions are stopped, the worktree and branch are gone, and the state row is updated.

## 7. Hand back

When no agent ticket is left, set each human ticket to Ready and comment on the parent: which PRs merged, the review rounds each took, the follow-ups the authors and reviewers reported and left alone, and what the human tickets now carry. Tell the user the same in one message and stop.

Done when: the comment is posted and the user has the summary.

## 8. Final cleanup

When the user says the parent is complete: `claude rm <id>` for every session in the state file, close the parent if still open, and delete the state directory.

Done when: `claude agents --json --all` lists none of the ids and the parent is closed.
