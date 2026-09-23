---
name: review-loop
description: Run a review loop, where a peer session reviews work while this session fixes the findings, until both agree. Use when the user asks for a review loop or for a peer session to review work.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Review loop

This session is the author. A peer session is the reviewer.

## 1. Launch the reviewer

Launch the reviewer with the `spin-peer-session` skill on model `fable` at effort `medium`, falling back to `opus` at `medium` when the `fable` launch fails, unless the user names others. The prompt names the work, the review focus, and this session's name from the first line of ListAgents. It tells the reviewer to reply with SendMessage to that name, since a message's `from` address is a process socket and stops reaching this session when it moves to another process.

The prompt also carries these review criteria:

- Check the work against its spec or acceptance criteria. Mark each criterion met, partly met, or not met, with file and line. Flag missing requirements, wrong implementations, and scope creep.
- Hunt bugs: logic errors, unhandled failure paths, regressions to existing callers. Each bug states the failing input or state and the wrong result.
- Report only verified defects on lines the work changed. Leave out pre-existing issues, nitpicks, anything a linter or typechecker catches, and changes that look intentional.
- Give each finding a risk (`high`, `medium`, `low`), a recommendation (`fix`, `defer`, `ignore`), a location, and one sentence on the defect. An unmet criterion is `high` and `fix`.
- End each reply with `verdict: agree` when no `fix` finding remains, else `verdict: changes requested`.

Done when: the reviewer is listed in ListAgents.

## 2. Loop until agreed

Send rounds with SendMessage. Judge each finding against the code and the spec, not by who raised it. Fix each finding you agree with. Push back on the rest with a reason. The loop ends on a `verdict: agree` reply with no push-back outstanding, or after 4 rounds.

At the cap, arbitrate each open finding: uphold or dismiss it, with one line quoting the criterion, rule, or failing input. Apply what you uphold. A real defect outside the work's scope becomes a follow-up.

Done when: the reviewer replied `verdict: agree`, or every open finding at the cap is upheld and applied or dismissed.

## 3. Report and clean up

Tell the user what was fixed, deferred, dismissed, and left as follow-ups, then stop the reviewer with `claude stop <id>`.

Done when: the report is delivered and the reviewer is stopped.
