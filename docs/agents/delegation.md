# Delegation

## Breaking work down

- Size each piece to finish well inside a 140k-token context.
- Cut vertical slices. Each is demoable alone and names the pieces that block it.
- Work the frontier: any piece whose blockers are done.
- Sequence a wide refactor as expand, migrate in batches, contract.
- Give screenshot-heavy checks their own piece. Images fill context fast.
- Scope each piece to its acceptance criteria.
- Steps of the skill you are running stay in this session unless the skill says to delegate them.

## Launching

- An orchestrator only plans, launches, messages, verifies, and cleans up.
- Default to `opus` at `medium`. Move up for hard design, scripts, or work across more than one domain. State model, effort, and the reason at every launch.
- Launch a reviewer on `fable` at `medium` or `high`. When `fable` is unavailable, use `opus` at `medium` or `high`.
- Name sessions `<role>-<n>`. A session cannot rename itself, so ask me to type `/rename <role>-<n>` before the first launch and wait for ListAgents to show it. On a collision add the lowest free number suffix.
- Address a session by name over SendMessage. Its `from` address is a process socket and goes stale. When a send fails, find the name by prefix in ListAgents.
- Send an addition to a running piece as a follow-up message.
- Keep the task list of a run longer than one context in a file the run updates, such as `TASKS.md` or the work log the skill names.
- When a subagent asks a question, relay it to me if I am present. If I am away, decide it yourself and tell the subagent the decision and the reason.

## Running as a subagent

- Send a question to your parent session and keep working on what does not depend on the answer. Stop only when nothing is left that the answer does not gate. With no parent session, decide it yourself and record the decision and the reason in the report.
- The "Ask a human to run" list still applies. Report those as steps a human runs.
- A gap that belongs to a sibling piece goes in the report, not the diff. A criterion that needs a remote environment or credentials is reported as human-only.
- When your brief names a handoff file, read it first and skip what it settles.
- When your context nears 110k tokens, write a handoff of at most 100 lines with sections done, changed, verified, machine state, next steps, gotchas, and follow-ups. Send the parent the path and stop.
- Open a report with the fixed first line your brief names.
- End a done report with three headings in this order:
  - `Blocked on me`: every step a human runs or approves, listed here and nowhere else.
  - `Changed`: what is done per criterion, files changed, validation exit code.
  - `Found`: review outcome and follow-ups.

## Verifying a report

- Check each done report against the piece's finish line, its log or handoff, a validation exit code of 0, and a closed review.
- Send each gap back as the next message. Verify again on the next report.
