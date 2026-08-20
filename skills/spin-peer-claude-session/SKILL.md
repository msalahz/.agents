---
name: spin-peer-claude-session
description: Launch an independent peer Claude session with a chosen model, effort, and instructions. Use when the user asks to spin up a new session, peer session, or independent background session rather than a subagent.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.1"
---

# Spin peer Claude session

`claude --bg` starts a full independent session. It registers as a peer in the
agents list, keeps its own context and lifecycle, and reports to no parent.

## 1. Collect the request

Collect from the request: instructions (required), a short session name, model,
effort, permission mode, and working directory. Defaults: a name derived from
the task, the CLI's default model and effort, `auto` permission mode, the
current directory.

Done when: the instructions and every named option are recorded.

## 2. Launch

Launch from the target directory:

```bash
cd <dir> && claude --bg -n "<name>" --model <model> --effort <level> \
  --permission-mode auto "<instructions>"
```

Omit `--model` and `--effort` when the user named none. Model takes an alias
(`fable`, `opus`, `sonnet`, `haiku`) or a full ID; effort is one of `low`,
`medium`, `high`, `xhigh`, `max`. Permission prompts in a background session
block until someone attaches, so the mode must cover the task: `auto` by
default, any mode the user names instead (`bypassPermissions` only when they
ask for it).

Done when: the launch output shows a session ID.

## 3. Confirm registration

The name appears in ListAgents (or `claude agents --json`). Missing means the
launch failed; report its output verbatim.

Done when: the session is listed, or the failure is reported.

## 4. Report

Report one line in this format:

Session Title: <name> — ID: <id> — <model>, <effort>, <permission mode> permission mode, agent prompt: <prompt>

Model, effort, and permission mode are the values the session runs with; write
`default` for any the user left unset. The agent prompt is the instructions the
session was launched with.

Done when: the one-line report is delivered.
