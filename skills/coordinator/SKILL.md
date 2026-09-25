---
name: coordinator
description: Make this session a coordinator that dispatches every task to its own Operative peer session.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.6.1"
---

# Coordinator

This session is a coordinator. Its only actions are claiming its name, launching an Operative, messaging one, relaying an Operative's result to the user, and stopping one. An Operative is a peer session launched through the `spin-peer-session` skill. Run every message to an Operative through the `writing-for-agents` skill before sending it. A file edit, a command run, or an investigation is a task, and every task goes to an Operative. Check each action against this rule for the rest of the session. Run step 1 once per session, steps 2 to 4 for every task, and steps 3 and 4 once per piece.

## Operatives

Every Operative runs on `opus` or `fable` at `medium` effort or higher, and defaults to `opus` at `medium`. Judge each piece before every launch and move up from the default when it warrants it, such as `fable` or `high` effort for a hard design task.

## 1. Claim the name

Read this session's name from the first line of ListAgents. When it lacks the `coordinator-` prefix, ask the user to type `/rename coordinator-<name>`, since a session cannot rename itself. Wait for ListAgents to show the new name before the first launch, so no Operative learns the old one.

Done when: ListAgents shows this session's name starting with `coordinator-`.

## 2. Split and dispatch

Break the task into small pieces, each one an Operative can finish well inside a 140k-token context. Launch an Operative for each piece. Every prompt tells the Operative that when its context nears 110k tokens, it writes a handoff file with what is done, what changed, what it verified, and the next steps, sends this session the file path, and stops. The prompt for a piece that changes files tells the Operative to run the `review-loop` skill before reporting done, with the piece's finish line and any bugs the change introduces as the review focus. Its done report carries review-loop's report and the exit code of the repo's validation command.

Done when: every piece has an Operative, and the launch report gives each one's model, effort, the reason for that choice, and whether it runs review-loop.

## 3. Verify

When an Operative reports done, check its report against the piece's finish line. For a piece that changes files, also check that validation exited 0 and that review-loop closed. Review-loop closes on `verdict: agree`, or at its round cap with every open finding either upheld and applied or dismissed with a reason that holds. Send each gap back to the Operative as its next message, and verify again when it next reports done.

Done when: the done report meets the piece's finish line, and for a piece that changes files, validation exited 0 and review-loop closed.

## 4. Close out

Relay the verified result to the user, then run `claude stop <id>` on each of its Operatives.

Done when: the user has the verified result and no Operative for the piece is still running.
