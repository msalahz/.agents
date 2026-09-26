---
name: arbitrate-review
description: Settle a review loop that ran out of rounds by deciding each open finding, applying the ones upheld, and reporting to the supervisor. Use when a supervise-issue session launches /arbitrate-review with a PR number and ticket number.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Arbitrate review

Arguments: `<pr> <n>`. The author and the reviewer of PR `#<pr>` for ticket `#<n>` disagreed after three rounds. This session runs under the display name `arbiter-<n>` from the PR's worktree, decides each open finding, applies what it upholds, and reports to the supervisor. Everything outside the worktree is read-only, and the remote-environment limits of the author apply here too.

## 1. Read

1. The launch message. It carries the author's and reviewer's session names and the author's unresolved report verbatim: each open finding with the reviewer's position and the author's. Nothing about the dispute exists on GitHub, so this message is the only source; when a position is unclear, ask `author-<n>` or `reviewer-<n>` over SendMessage.
2. `gh issue view <n> --comments`, the spec sections it names, `docs/adr/*.md`, `AGENTS.md`, the Coding rules in `~/.agents/AGENTS.md`, and the Arbitrating rules in `~/.agents/docs/agents/code-review.md`.
3. `gh pr view <pr> --json body` and `gh pr diff <pr>`.

Done when: every open finding is listed with both positions and the evidence each side cited.

## 2. Decide

For each finding, check the claim against the code and the ticket, not against who said it. Reproduce it when a read-only command can. Decide each by the Arbitrating rules. A finding that is real but outside the ticket's criteria is dismissed for this PR and named as a follow-up with the sibling ticket that owns it.

Done when: every finding has a decision and a one-line reason.

## 3. Apply

For each upheld finding, make the smallest change that resolves it, following the Coding rules. Run the repo's validate script and the gates the author used, reading real exit codes. Commit with a conventional-commit subject that names the finding, ending with the trailer this session's own attribution guidance names. Push with `git push origin <branch>`; never force-push.

Done when: the upheld findings are fixed, the gates pass, and the push is on the PR.

## 4. Report

Message the supervisor named in the launch message, falling back to the ListAgents row whose name starts with `supervisor`. First line `PR #<pr> arbitrated for #<n>`, then one line per finding: decision, reason, and the commit that applied it or the follow-up it became. Then stop and wait.

Done when: the supervisor has the report line.
