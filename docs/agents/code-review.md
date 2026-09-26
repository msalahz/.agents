# Code review

Load each stack file under `~/.agents/docs/agents/code-review/` whose `detect` entries match the repo.

## Reviewing

- Run the checks the verdict needs, then restore the working tree to how you found it. Tracked files, commits, and the remote stay untouched.
- Mark each acceptance criterion met, partly met, not met, or human-only, with file and line.
- Score each finding 0 to 100 for confidence it is real and will be hit. Reproduce a finding scored 75 or more where a read-only command can.
- Drop pre-existing issues, nitpicks, what a linter or typechecker catches, code quality AGENTS.md does not require, issues the code silences on purpose, intentional changes, and lines the work did not change.
- Give every finding a risk (`high`, `medium`, `low`), a recommendation (`fix`, `defer`, `ignore`), its score, a location, one sentence of defect, and one sentence of failure scenario.
- A score under 50 is `defer` or `ignore`. 50 to 74 is `low` or `medium`. 75 and up is `medium` or `high`.
- An unmet criterion is `high` and `fix`. Scope creep is `medium` and `fix` and names the piece that owns it.
- Session-to-session rounds carry the full finding list.
- End with `verdict: agree` when no `fix` finding remains, else `verdict: changes requested`.

## Answering a review

- Verify each finding against the code and the spec alone. Fix the ones that hold. Push back on the rest with a reason.
- Record the review in the PR body: rounds, findings fixed with commits, findings deferred with their owner, final verdict line. Without a PR, put the record in the report to the human.

## Arbitrating

- Arbitrate after 3 rounds without `verdict: agree`.
- Uphold or dismiss each open finding with one line quoting the criterion, rule, or failing input.
- Apply what you uphold. A real defect outside scope becomes a follow-up.

## Reporting to a human

- The final report a human reads before merge lists only merge-blocking problems, each with file, line, one sentence of defect, and the input that reproduces it.
