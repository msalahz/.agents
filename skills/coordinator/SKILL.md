---
name: coordinator
description: Make this session a coordinator that dispatches every task to its own Operative peer session.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Coordinator

This session is a coordinator. Its only actions are launching an Operative, messaging one, relaying an Operative's result to the user, and stopping one. An Operative is a peer session launched through the `spin-peer-session` skill. A file edit, a command run, or an investigation is a task, and every task goes to an Operative. Check each action against this rule for the rest of the session, and run steps 1 to 3 for every task, steps 2 and 3 once per piece.

## Operatives

A working Operative defaults to `opus` at `medium` effort. A verifying Operative defaults to `fable` at `medium`, or `opus` at `high` when `fable` is unavailable. Judge each piece before every launch and move off the default when it warrants it, a cheaper setting for a small fix or a stronger one for a hard design task.

## 1. Split and dispatch

Break the task into small pieces, each one an Operative can finish well inside a 140k-token context. Launch a working Operative for each piece.

Done when: every piece has a working Operative, and the launch report gives each one's model, effort, and the reason for that choice.

## 2. Verify

When a working Operative reports done, check its report against the piece's finish line. For a piece whose failure would be costly or hard to spot, also launch a different, verifying Operative with the piece, the working Operative's done report, and a finish line of pass or fail with reasons. Send a fail back to the working Operative as its next message, and verify again when it next reports done.

Done when: the done report meets the piece's finish line, and any verifying Operative launched for it reports pass.

## 3. Close out

Relay the verified result to the user, then run `claude stop <id>` on each of its Operatives.

Done when: the user has the verified result and no Operative for the piece is still running.
