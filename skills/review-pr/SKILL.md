---
name: review-pr
description: Review a pull request against its ticket's acceptance criteria and spec, then hunt bugs in the diff, and send the author a verdict with risk-rated findings. Use when an author-ticket session launches /review-pr with a PR number, ticket number, and author session name.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Review PR

Arguments: `<pr> <n> <author-name>`. This session runs under the display name `reviewer-<n>` and reviews PR `#<pr>` for ticket `#<n>` from inside the PR's worktree, reports to the author session over SendMessage, and waits for re-review requests. Up to three rounds.

Read-only: no edits, no commits, no pushes, no GitHub comments or reviews, nothing against a remote environment. The repo's validate script and `git` reads are the only commands that run.

## 1. Read

1. `gh issue view <n> --comments`: the acceptance criteria, numbered, and the `Spec:` path on the first line. If the ticket carries none, find the spec in this order: issue references in the commit messages, a path the launch gave, a file under `docs/`, `specs/`, or `.scratch/` matching the branch name. If nothing turns up, the spec pass reports "no spec available" and the criteria stand alone.
2. The spec sections the ticket names, `docs/adr/*.md`, `AGENTS.md`, and the Coding and Code review rules in `~/.agents/AGENTS.md`.
3. `gh pr view <pr> --json title,body,files` and `gh pr diff <pr>`, plus `git log origin/<default>..HEAD --oneline` in the worktree.
4. The sibling tickets' titles under the parent, to name scope creep precisely.

Done when: the criteria list, spec text or its absence, and the full diff are in context.

## 2. Spec pass

Launch one subagent with the diff, the commit list, the numbered criteria, the spec text, and this brief:

> Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Open with the first finding.

Add: for each numbered acceptance criterion, state met, partly met, not met, or human-only, with the file and line that meets it. Scope creep names the sibling ticket that owns it.

Done when: every criterion has a status and the subagent's report is in context.

## 3. Bug pass

Launch one subagent with the diff, the changed files in full, and this brief. It hunts logic errors, unhandled failure paths, shell pitfalls under `set -euo pipefail` such as a command substitution's status escaping into a conditional or a pipe hiding an exit code, regressions to existing callers, and behaviour that contradicts the runbooks or comments the diff touches. It scores each finding with this rubric:

> 0: Not confident at all. This is a false positive that doesn't stand up to light scrutiny, or is a pre-existing issue.
> 25: Somewhat confident. This might be a real issue, but may also be a false positive. The agent wasn't able to verify that it's a real issue.
> 50: Moderately confident. The agent was able to verify this is a real issue, but it might be a nitpick or not happen very often in practice. Relative to the rest of the PR, it's not very important.
> 75: Highly confident. The agent double checked the issue, and verified that it is very likely it is a real issue that will be hit in practice. The existing approach in the PR is insufficient.
> 100: Absolutely certain. The agent double checked the issue, and confirmed that it is definitely a real issue, that will happen frequently in practice. The evidence directly confirms this.

And it drops these:

> Pre-existing issues. Something that looks like a bug but is not actually a bug. Pedantic nitpicks that a senior engineer wouldn't call out. Issues that a linter, typechecker, or compiler would catch. General code quality issues (lack of test coverage, general security issues, poor documentation) unless explicitly required in CLAUDE.md or AGENTS.md. Issues called out in those files but explicitly silenced in the code. Changes in functionality that are likely intentional or directly related to the broader change. Real issues on lines the PR did not modify.

Each surviving finding quotes the hunk and states the failing input or state and the wrong result. A finding scored under 50 is dropped; 50 to 74 is `low` or `medium` by consequence; 75 and up is `medium` or `high`.

Reproduce the highest-scored finding yourself where a read-only command can, such as a `tofu plan` on a throwaway copy or a shell snippet.

Done when: the subagent's report is in context and its top finding has been checked.

## 4. Verdict

Run the validate script in the worktree and record its exit code.

Merge both passes into one list. Each finding: risk `high`, `medium`, or `low`; recommendation `fix`, `defer`, or `ignore`; file and line; one sentence of defect; one sentence of failure scenario. A criterion not met is `high` and `fix`. Scope creep is `medium` and `fix` unless the ticket is the only place the change can live. Deferred items name the ticket or follow-up that should own them.

The verdict is `VERDICT: CHANGES REQUESTED` when any finding is `fix`, otherwise `VERDICT: APPROVED`.

Send it to `<author-name>` with SendMessage. First line `Review round <k> for PR #<pr>`, then the criteria table, the findings, the validate exit code, and the verdict line last. If the send fails, run ListAgents and use the row named `author-<n>`.

Done when: the author has the message and it ends with a verdict line.

## 5. Re-review

Wait. On `re-review round <k>`: `git fetch`, read the new commits with `git diff <last reviewed sha>..HEAD`, check each earlier `fix` finding is resolved or answered with a reason you accept, run the bug pass over the new hunks only, and send a new verdict. On `conflict resolution only`: check the rebase with `git range-diff` against the previous head, review only hunks that differ, and confirm the gates, then send the verdict. That round does not count toward the three.

After the third verdict, or after APPROVED, stop and wait for messages.

Done when: the author has the verdict for the round it asked for.
