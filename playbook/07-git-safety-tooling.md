# Git, safety, and tooling
Branches, worktrees, commits, PRs, merges and rebases; human-only and remote actions, permission modes; gh, shell scripts, and human-run wizards.

## Patterns

### Branches, rebases, and PRs

- **In-repo worktree naming.** Name a git worktree created inside the repo root `worktree-<name>` so `pnpm validate` skips it. _Sources: AGENTS.md_ _Conflicts with: Ticket worktree shares the branch name_
- **Ticket worktree shares the branch name.** Implement a ticket in `.claude/worktrees/<worktree>` on the branch of the same name. _Sources: skills/author-ticket/SKILL.md_ _Conflicts with: In-repo worktree naming_
- **Rebase request message.** When a PR is CONFLICTING, message its author with the first line `Rebase #<n> onto <default>`, naming the merged PRs and files, and follow the resolution with one review round. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **Author rebase on request.** On `Rebase #<n> onto <default>`, fetch, rebase, resolve keeping both sides' intent, re-run the gate, push with `git push --force-with-lease`, and request `re-review round <k>, conflict resolution only`. _Sources: skills/author-ticket/SKILL.md_
- **PR title shape.** Open the PR against the default branch with the title `<type>: <summary> (#<n>)`. _Sources: skills/author-ticket/SKILL.md_
- **PR body contents.** List what changed, each criterion and how the diff meets it, criteria left to the human and why, follow-ups left alone, `Closes #<n>`, then the attribution line. _Sources: skills/author-ticket/SKILL.md_

### Scripts and session tooling

- **Bounded gh retry.** Run `gh` up to three times with five seconds between attempts, and print the failed command to stderr on giving up. _Sources: skills/supervise-issue/scripts/gh-retry.sh_
- **Sibling scripts by own directory.** Locate helper scripts through `$(cd "$(dirname "$0")" && pwd)`. _Sources: skills/supervise-issue/scripts/project-status.sh_
- **Query, then mutate the project board.** Query the issue's project items with GraphQL, pick the ids in Python, then run `updateProjectV2ItemFieldValue`. _Sources: skills/supervise-issue/scripts/project-status.sh_

## Strategies

- **Default to auto permission mode.** Pick a permission mode that covers the whole task, defaulting to `auto`, because a background session blocks on a permission prompt until someone attaches. _Sources: skills/spin-peer-session/SKILL.md_

## Practices

### Branches, commits, and pushes

- **Respect deleted files.** Treat files git status shows as deleted as removed on purpose, and do not restore them, read them from history, or cite them. _Sources: AGENTS.md_
- **Stay on the current branch.** Work on the current branch, main included, unless the user or the running skill names another. _Sources: AGENTS.md_
- **Worktree only on demand.** Use a worktree only when the user asks or a ticket or PR flow needs one. _Sources: AGENTS.md_
- **Run everything in the worktree.** Run every ticket command inside the ticket's worktree. _Sources: skills/author-ticket/SKILL.md_
- **Name the checkout with git -C.** Give every git command its checkout as `git -C <path>`. _Sources: skills/supervise-issue/SKILL.md_
- **Launch in a subshell.** Run every session launch in a `(cd <worktree> && ...)` subshell, because a bare `cd` moves the session's working directory. _Sources: skills/supervise-issue/SKILL.md_
- **Small conventional commits.** Make small logical commits with conventional-commit subjects. _Sources: skills/author-ticket/SKILL.md_
- **One commit per finding.** When fixing review findings, commit each with a conventional-commit subject that names the finding. _Sources: skills/arbitrate-review/SKILL.md_
- **Own attribution trailer.** End each commit with the trailer this session's attribution guidance names, and never copy a model name from anywhere else. _Sources: skills/author-ticket/SKILL.md, skills/arbitrate-review/SKILL.md_
- **Push with upstream.** Push a ticket branch with `git push -u origin <worktree>`. _Sources: skills/author-ticket/SKILL.md_
- **Author never merges.** Leave every merge to the supervisor. _Sources: skills/author-ticket/SKILL.md_
- **Author force-pushes only for a requested rebase.** Force-push only to finish a rebase the supervisor asked for. _Sources: skills/author-ticket/SKILL.md_
- **Arbiter never force-pushes.** Push arbiter fixes with `git push origin <branch>`. _Sources: skills/arbitrate-review/SKILL.md_
- **Resolve conflicts with the skill.** Resolve every merge or rebase conflict with the resolving-merge-conflicts skill. _Sources: skills/author-ticket/SKILL.md_

### Merging

- **Preflight before a run.** Confirm `.claude/settings.local.json` allows `Bash(gh pr merge *)` so merges are not refused, the session is renamed `supervisor-<parent>`, `git check-ignore .claude/worktrees` succeeds, and `git log origin/<default>..<default>` prints nothing. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **Batch preflight misses.** Collect every preflight miss and ask the user to fix them in one message, since the session cannot edit its own settings. _Sources: skills/supervise-issue/SKILL.md_
- **Merge gate.** Merge only when `mergeable` is MERGEABLE, `mergeStateStatus` is CLEAN, and every CI check passes. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **Merge sequence.** Stop the ticket's sessions, remove the worktree, squash-merge, delete the branch, move the ticket to Done, tell other authors to rebase, then launch the next wave. _Sources: README.md_
- **One command per merge step.** Run the merge close-out steps in order, each as its own command. _Sources: skills/supervise-issue/SKILL.md_
- **Remove the worktree before merging.** Force-remove and prune the ticket's worktree first, because branch deletion fails while a worktree holds the branch. _Sources: skills/supervise-issue/SKILL.md_
- **Bare squash merge.** Run `gh pr merge <pr> --squash --delete-branch` bare and alone, with no retry wrapper, `;`, or `&&`, so the allow rule matches. _Sources: skills/supervise-issue/SKILL.md_
- **Sync the default branch after merging.** Delete the local branch, fetch, and run `merge --ff-only origin/<default>`. _Sources: skills/supervise-issue/SKILL.md_
- **Warn open PRs after a merge.** Tell every author with an open PR which files the merge touched, so it rebases before its next round. _Sources: skills/supervise-issue/SKILL.md_

### Human-only and remote actions

- **Human runs non-local actions.** Ask a human to run anything that targets a non-local environment (deploys, production env files or credentials, remote migrations or seeds), even when it looks routine, because it changes shared state that is hard to undo. _Sources: AGENTS.md_
- **Human runs the Drizzle CLI.** Ask a human to run Drizzle CLI `migrate`, `push`, and `seed`, because they change shared state that is hard to undo. _Sources: AGENTS.md_
- **Never touch a remote environment.** Whatever the ticket says, author and arbiter sessions never deploy, run `tofu apply`, mutate with `gcloud`, change DNS, read production or staging secrets, or change a remote environment; those stay on human tickets. _Sources: README.md, skills/author-ticket/SKILL.md, skills/arbitrate-review/SKILL.md_
- **Offline infra commands are fine.** Run `tofu init -backend=false`, `tofu validate`, and offline plans freely. _Sources: skills/author-ticket/SKILL.md_
- **Remote criteria go human-only.** Report an acceptance criterion that needs a remote environment or credentials to the supervisor or parent as human-only, without attempting it. _Sources: README.md, docs/agents/delegation.md, skills/author-ticket/SKILL.md_
- **Human-run list in subagent reports.** As a subagent, report every "Ask a human to run" step as a step a human runs. _Sources: docs/agents/delegation.md_
- **Impersonation checks go to the human.** Hand a check that needs impersonating another user to the human with the human-only criteria. _Sources: skills/author-ticket/SKILL.md_

### Permission modes

- **Auto mode for ticket peers.** Launch ticket peer sessions with `--permission-mode auto`, since `bypassPermissions` is refused and same-class sessions receive peer messages without human approval. _Sources: skills/supervise-issue/SKILL.md_ _Conflicts with: bypassPermissions only on request_
- **bypassPermissions only on request.** Use `bypassPermissions` only when the user asks for it. _Sources: skills/spin-peer-session/SKILL.md_ _Conflicts with: Auto mode for ticket peers_

### gh, scripts, and wizards

- **Retry gh calls.** Route every gh call through `gh-retry.sh`, because the API drops TLS handshakes. _Sources: skills/supervise-issue/SKILL.md_
- **Bare gh pr checks.** Run `gh pr checks` bare, because its non-zero exit on pending or failed checks is an answer, not a fault. _Sources: skills/supervise-issue/SKILL.md_
- **Strict bash.** Start every script with `set -euo pipefail`. _Sources: skills/supervise-issue/scripts/project-status.sh_
- **Fail with known options.** When input is unknown, exit with a message listing the known values, such as the known statuses or the fact that the issue is not on the project. _Sources: skills/supervise-issue/scripts/project-status.sh_
- **Find repo root.** Locate the repo root with `git rev-parse --show-toplevel`, or use the current directory outside git. _Sources: skills/knowledge-wiki/SKILL.md_
- **Automate human-run scripts.** In scripts and wizards a human runs, automate every step a script can do. _Sources: AGENTS.md_
- **Recommended defaults in prompts.** Give every script or wizard prompt that needs input a recommended default. _Sources: AGENTS.md_
- **Install dependencies first.** Run `pnpm install` before anything else when `node_modules` is missing. _Sources: skills/author-ticket/SKILL.md_
- **Load TanStack intent skills.** Run `pnpm dlx @tanstack/intent@latest list` and load each matching skill with `pnpm dlx @tanstack/intent@latest load <package>#<skill>`. _Sources: skills/author-ticket/SKILL.md_

## Where it lives

AGENTS.md holds the branch, deleted-file, worktree, human-only, and human-run script rules, and docs/agents/delegation.md holds the two subagent rules on human-run steps and remote criteria. Every other rule, including the merge flow, rebase protocol, commit and push rules, permission modes, and gh handling, lives only inside the author-ticket, supervise-issue, arbitrate-review, spin-peer-session, and knowledge-wiki skills and the supervise-issue scripts. README.md restates the preflight, merge gate, merge sequence, rebase message, and remote limits from the supervise-issue flow.
