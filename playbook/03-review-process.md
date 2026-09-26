# Review process
How reviews, review loops, PR reviews, and arbitration run: roles, rounds, confidence scoring, finding and verdict format, review records.

## Patterns

- **Review record in the PR body.** Record the rounds, fixed findings with their commits, deferred findings with their owner, and the final verdict in a `## Review` section appended with `gh pr edit --body-file`, because a same-account PR cannot carry a GitHub approval. When there is no PR, put the record in the report to the human. _Sources: README.md, skills/author-ticket/SKILL.md, docs/agents/code-review.md_
- **Review-loop closure.** Close a review loop on `verdict: agree`, or at its round cap once every open finding is upheld and applied or dismissed with a reason that holds. _Sources: skills/coordinator/SKILL.md_
- **Final report categories.** Tell the user what was fixed, deferred, dismissed, and left as follow-ups. _Sources: skills/review-loop/SKILL.md_

### Findings and messages

- **Finding format.** Write each finding as risk (`high`/`medium`/`low`), recommendation (`fix`/`defer`/`ignore`), score, location, the quoted hunk, one sentence of defect, and one sentence of failure scenario naming the failing input or state and the wrong result. _Sources: docs/agents/code-review.md, skills/review-pr/SKILL.md_
- **Confidence rubric.** Score each finding 0 to 100 on a 0/25/50/75/100 rubric, from false positive to certain, for confidence that it is real and will be hit. _Sources: docs/agents/code-review.md, skills/review-pr/SKILL.md_
- **Criterion status.** Mark each acceptance criterion met, partly met, not met, or human-only, with file and line. _Sources: docs/agents/code-review.md, skills/review-pr/SKILL.md_
- **Verdict line.** Grade and list findings by the Reviewing rules in `code-review.md` and end every review reply with `verdict: agree` when no `fix` finding remains, else `verdict: changes requested`. _Sources: docs/agents/code-review.md, skills/author-ticket/SKILL.md, skills/review-loop/SKILL.md_
- **Review message shape.** Open with `Review round <k> for PR #<pr>`, then the criteria table, the findings, the validate exit code, and the verdict line last. _Sources: skills/review-pr/SKILL.md_
- **Spec pass brief.** Have the spec pass report missing or partial requirements, unrequested behaviour, and requirements that look implemented wrongly, quoting the spec line and opening with the first finding. _Sources: skills/review-pr/SKILL.md_

### Roles and launches

- **Author and reviewer roles.** Make this session the author and a peer session the reviewer. _Sources: skills/review-loop/SKILL.md_
- **Author launches its own reviewer.** Launch the reviewer from the worktree with `claude --bg --name reviewer-<n> --model opus --effort high --permission-mode auto "/review-pr <pr> <n> author-<n>"`. _Sources: skills/author-ticket/SKILL.md_ _Conflicts with: Reviewer model with fallback_
- **Reviewer prompt contents.** Name the work, the review focus, and `<author>` in the reviewer prompt, and tell the reviewer to check the work against its spec or acceptance criteria. _Sources: skills/review-loop/SKILL.md_
- **Re-review round message.** After fixing, re-run the gates, commit, push, and message `reviewer-<n>` with `re-review round <k>`. _Sources: skills/author-ticket/SKILL.md_
- **Arbiter launch.** Launch `arbiter-<n>` with `--model fable --effort high` and a prompt holding `/arbitrate-review`, the three session names, the author's report verbatim, and the handoff block. _Sources: README.md, skills/supervise-issue/SKILL.md_

## Strategies

- **Two-pass review.** Run a spec pass and a bug pass in subagents and send risk-rated findings that end in a verdict. _Sources: README.md_
- **Subagent covers, parent filters.** Have the subagent report every issue, uncertain ones included, and drop and grade them in this session by the Reviewing rules. _Sources: skills/review-pr/SKILL.md_
- **Spec discovery fallback.** With no `Spec:` path on the issue, look in commit-message issue references, then a launch-given path, then a `docs/`, `specs/`, or `.scratch/` file matching the branch name, and if nothing turns up have the spec pass report "no spec available" and judge against the criteria alone. _Sources: skills/review-pr/SKILL.md_
- **Score-to-risk mapping.** Grade a score under 50 as `defer` or `ignore`, 50 to 74 as `low` or `medium`, and 75 and up as `medium` or `high`. _Sources: docs/agents/code-review.md_
- **Judge the claim, not the claimant.** Check each finding against the code and the spec or ticket, never against who raised it. _Sources: skills/arbitrate-review/SKILL.md, skills/review-loop/SKILL.md_
- **Out-of-scope defects become follow-ups.** Apply upheld findings, and dismiss a real defect outside the ticket's criteria for this PR, naming it as a follow-up with the sibling ticket that owns it. _Sources: docs/agents/code-review.md, skills/arbitrate-review/SKILL.md_
- **Exhausted loops go to an arbiter.** Send a loop that reaches three rounds without `verdict: agree` to an `arbitrate-review` session, which upholds or dismisses each open finding and pushes the fixes. _Sources: docs/agents/code-review.md, skills/supervise-issue/SKILL.md, README.md_ _Conflicts with: Self-arbitrate at the cap_
- **Reviewer model with fallback.** Launch the reviewer through `spin-peer-session` on `fable` at `medium`, falling back to `opus` at `medium` if the fable launch fails, unless the user names others. _Sources: skills/review-loop/SKILL.md_ _Conflicts with: Author launches its own reviewer_

## Practices

- **Human report lists blockers only.** List only merge-blocking problems in the pre-merge report, each with file, line, one sentence of defect, and the reproducing input. _Sources: docs/agents/code-review.md_
- **Separate spec pass subagent.** Launch one subagent with the diff, the commits, the numbered criteria, the spec text, and a fixed brief. _Sources: skills/review-pr/SKILL.md_
- **Separate bug pass subagent.** Launch one subagent with the diff and the changed files in full to hunt bugs. _Sources: skills/review-pr/SKILL.md_

### Setup and limits

- **Read the code-review doc first.** Read `~/.agents/docs/agents/code-review.md` before reviewing a diff or PR, answering a review, or arbitrating findings. _Sources: AGENTS.md_
- **Reading list.** Read the issue with comments, the spec sections it names, `docs/adr/*.md`, `AGENTS.md`, the global Coding rules, and `code-review.md`. _Sources: skills/arbitrate-review/SKILL.md, skills/review-pr/SKILL.md_
- **Numbered criteria and spec path.** Read `gh issue view <n> --comments` for the numbered criteria and the `Spec:` path. _Sources: skills/review-pr/SKILL.md_
- **PR metadata, diff, and log.** Read `gh pr view <pr> --json title,body,files`, `gh pr diff <pr>`, and `git log origin/<default>..HEAD --oneline`. _Sources: skills/review-pr/SKILL.md, skills/arbitrate-review/SKILL.md_
- **Sibling titles.** Read the sibling ticket titles under the parent so scope creep can name its owner. _Sources: skills/review-pr/SKILL.md_
- **Load matching stack files.** Load each file under `docs/agents/code-review/` whose `detect` entries match the repo. _Sources: docs/agents/code-review.md_
- **Stay read-only.** Run only the repo's validate script and `git` reads, and make no edits, commits, pushes, GitHub comments or reviews, or changes to a remote environment. _Sources: skills/review-pr/SKILL.md_ _Conflicts with: Restore the working tree; Reproduce high-confidence findings_
- **Restore the working tree.** Run the checks the verdict needs, then restore the working tree, leaving tracked files, commits, and the remote untouched. _Sources: docs/agents/code-review.md_ _Conflicts with: Stay read-only_
- **Arbiter is read-only outside the worktree.** Treat everything outside the worktree as read-only when arbitrating. _Sources: skills/arbitrate-review/SKILL.md_

### Grading findings

- **Drop noise.** Drop pre-existing issues, nitpicks, linter or typechecker catches, quality `AGENTS.md` does not require, intentionally silenced issues, intentional changes, and unchanged lines. _Sources: docs/agents/code-review.md_
- **Bug pass targets.** Hunt logic errors, unhandled failure paths, `set -euo pipefail` shell pitfalls, regressions to existing callers, and behaviour that contradicts a touched comment, doc, or runbook. _Sources: skills/review-pr/SKILL.md, skills/review-loop/SKILL.md_
- **Unmet criterion is high.** Grade an unmet criterion `high` and `fix`. _Sources: docs/agents/code-review.md_
- **Scope creep grade.** Grade scope creep `medium` and `fix` unless this ticket is the only place the change can live, and name the sibling ticket or piece that owns it. _Sources: docs/agents/code-review.md, skills/review-pr/SKILL.md_
- **Deferred items name an owner.** Name the ticket or follow-up that should own each deferred item. _Sources: skills/review-pr/SKILL.md_
- **Reproduce high-confidence findings.** Reproduce every finding scored 75 or more where a read-only command can. _Sources: docs/agents/code-review.md_ _Conflicts with: Stay read-only_
- **Reproduce the top finding.** Reproduce the highest-scored finding yourself where a read-only command can. _Sources: skills/review-pr/SKILL.md_

### Rounds

- **Three-round cap.** Cap review at three rounds counting the first, with the author fixing or rebutting findings each round. _Sources: README.md, skills/author-ticket/SKILL.md_
- **Conflict round is free.** Leave the conflict-resolution round out of the three-round count. _Sources: skills/author-ticket/SKILL.md_
- **Full list each round.** Carry the full finding list in every session-to-session round. _Sources: docs/agents/code-review.md_
- **Answer by the Answering rules.** Verify each finding against the code and the spec alone, fix those that hold, and push back on the rest with a reason. _Sources: docs/agents/code-review.md, skills/review-loop/SKILL.md, skills/author-ticket/SKILL.md_
- **Incremental re-review.** On `re-review round <k>`, fetch, diff from the last reviewed sha, check each earlier `fix` finding, bug-pass only the new hunks, and send a new verdict. _Sources: skills/review-pr/SKILL.md_
- **Range-diff for conflict rounds.** On `conflict resolution only`, check the rebase with `git range-diff` against the previous head, review only the hunks that differ, and confirm the gates. _Sources: skills/review-pr/SKILL.md_
- **Loop end condition.** End the loop on `verdict: agree` with no push-back outstanding, or after 3 rounds. _Sources: skills/review-loop/SKILL.md_
- **Self-arbitrate at the cap.** At the round cap, arbitrate each open finding yourself by the Arbitrating rules. _Sources: skills/review-loop/SKILL.md_ _Conflicts with: Exhausted loops go to an arbiter_

### Arbitration

- **Decide by the Arbitrating rules.** Decide each finding by the Arbitrating rules in `code-review.md`. _Sources: skills/arbitrate-review/SKILL.md_
- **List both positions with evidence.** Finish reading only when every open finding is listed with both positions and the evidence each side cited. _Sources: skills/arbitrate-review/SKILL.md_
- **Ask the parties when unclear.** Ask `author-<n>` or `reviewer-<n>` over SendMessage when a position is unclear. _Sources: skills/arbitrate-review/SKILL.md_
- **Reproduce read-only.** Reproduce a finding when a read-only command can. _Sources: skills/arbitrate-review/SKILL.md_
- **One-line rulings.** Uphold or dismiss every open finding with one line quoting the criterion, rule, or failing input. _Sources: docs/agents/code-review.md, skills/arbitrate-review/SKILL.md_
- **Smallest upheld change.** Make the smallest change that resolves each upheld finding, following the Coding rules. _Sources: skills/arbitrate-review/SKILL.md_

### Accepting the outcome

- **Arbitration counts as approval.** Treat an `arbitrated` report as approval. _Sources: skills/supervise-issue/SKILL.md_
- **Review evidence without approval.** Take the author's report and the PR body as the review evidence, since same-account approval is impossible. _Sources: skills/supervise-issue/SKILL.md_

## Where it lives

AGENTS.md holds one rule here, the pointer to read `docs/agents/code-review.md` before any review work, and that doc holds the Reviewing, Answering, and Arbitrating rules: scoring, the finding and verdict format, noise, round lists, the review record, and the pre-merge report. README.md summarizes the two-pass review, the three-round cap, the PR-body record, and the Fable arbiter. The rest lives only in skills: review mechanics in `review-pr`, the peer loop in `review-loop`, reviewer launch and round counting in `author-ticket`, arbiter steps in `arbitrate-review`, arbiter launch and approval in `supervise-issue`, and loop closure in `coordinator`.
