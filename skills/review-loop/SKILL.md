---
name: review-loop
description: Run a review loop, a peer session reviewing work while this session fixes the findings, until both agree. Use when the user asks for a review loop, or for a peer session to review work until agreed.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Review loop

This session is the author. A peer session is the reviewer.

## 1. Launch the reviewer

Launch the reviewer with the `spin-peer-session` skill, on model `opus` and effort `medium` or `fable` at `medium` is available unless the user names others. The prompt names the work, the review focus, and this session's name from the first line of ListAgents. It tells the reviewer to reply with SendMessage to that name. A message's `from` address is a process socket and stops reaching this session when it moves to another process.

Done when: the reviewer is listed in ListAgents.

## 2. Loop until agreed

Send rounds with SendMessage. Fix each finding you agree with. Push back on the rest with a reason. The loop ends when the reviewer agrees with nothing outstanding, or after 5 rounds.

Done when: the reviewer agreed or the round cap was hit.

## 3. Report and clean up

Tell the user what was fixed, deferred, and still disagreed, then stop the reviewer with `claude stop <id>`.

Done when: the report is delivered and the reviewer is stopped.
