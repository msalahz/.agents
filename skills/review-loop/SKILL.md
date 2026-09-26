---
name: review-loop
description: Run a review loop, where a peer session reviews work while this session fixes the findings, until both agree. Use when the user asks for a review loop or for a peer session to review work.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.6.0"
---

# Review loop

This session is the author. A peer session is the reviewer.

## 1. Launch the reviewer

Launch the reviewer with the `spin-peer-session` skill on model `fable` at effort `medium`, falling back to `opus` at `medium` when the `fable` launch fails, unless the user names others. Name it `review-<author>`, where `<author>` is this session's name from the first line of ListAgents. When a ListAgents row already uses that name, add the lowest free number suffix, such as `review-<author>-2`, so SendMessage reaches the reviewer by name alone. The prompt names the work, the review focus, and `<author>`. It tells the reviewer to reply with SendMessage to `<author>`, since a message's `from` address is a process socket and stops reaching this session when it moves to another process.

The prompt also tells the reviewer to check the work against its spec or acceptance criteria, to hunt logic errors, unhandled failure paths, regressions to existing callers, and behaviour that contradicts a comment or doc the work touches, and to grade and report by the Reviewing rules in `~/.agents/docs/agents/code-review.md`, ending each reply with their verdict line.

Done when: the reviewer is listed in ListAgents under a name no other row uses.

## 2. Loop until agreed

Send rounds with SendMessage. Judge each finding against the code and the spec, not by who raised it. Fix each finding you agree with. Push back on the rest with a reason. The loop ends on a `verdict: agree` reply with no push-back outstanding, or after 3 rounds.

At the cap, arbitrate each open finding by the Arbitrating rules in the same file.

Done when: the reviewer replied `verdict: agree`, or every open finding at the cap is upheld and applied or dismissed.

## 3. Report and clean up

Tell the user what was fixed, deferred, dismissed, and left as follow-ups, then stop the reviewer with `claude stop <id>`.

Done when: the report is delivered and the reviewer is stopped.
