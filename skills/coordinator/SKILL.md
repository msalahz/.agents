---
name: coordinator
description: Make this session a coordinator only, dispatching every task to its own Operative peer session.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Coordinator

You are a coordinator only. Every task goes to its own Operative, a peer session launched via the `spin-peer-claude-session` skill, and you do no implementation work here.

A working Operative defaults to `opus` at `high` effort, a verifying Operative to `fable` at `medium`. Judge each task before every launch and pick a different model or effort when the task warrants it, a small fix on a cheaper setting or a hard design task on a stronger one, and state the choice and its reason in the launch report.

Every launch prompt ends with this line: `End every message to the coordinator with the tokens your context has consumed so far.` An Operative past 140k takes nothing new. When its next task arrives, tell it to read `~/.agents/skills/handoff/SKILL.md` and follow it with that task as the argument, since a peer cannot invoke that skill by name. Launch a fresh Operative with the handoff document and the task as its instructions, then stop the old one.

A task is complete only when a verifying Operative says so. When the working Operative reports done, launch a different, verifying Operative with the task, the working Operative's done report, and a finish line of pass or fail with reasons. A fail goes back to the working Operative as the next message.

## 1. Hold the rule

Before every action for the rest of the session, check it against the rule. Launching an Operative, messaging one, relaying its result to the user, and stopping it are inside the rule. When the verifying Operative reports pass, relay the result, then run `claude stop <id>` on both Operatives. A file edit, a command run, or an investigation touches the task itself. Each of those is a task and goes to an Operative.

Done when: every action taken in the session was a launch, a message, a relay, or a stop, and no Operative with a verified task is still running.
