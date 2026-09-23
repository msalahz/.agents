---
name: spin-peer-session
description: Launch an independent peer Claude session with a chosen model, effort, and instructions. Use when the user asks to spin up a new, peer, or background session rather than a subagent.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Spin peer session

`claude --bg` starts a full independent session. It registers as a peer in the
agents list, keeps its own context and lifecycle, and reports to no parent.

## 1. Collect the request

Collect from the request: instructions (required), a short session name, model,
effort, permission mode, and working directory. Defaults: a name derived from
the task, the CLI's default model and effort, `auto` permission mode, the
current directory.

Done when: the instructions and every named option are recorded.

## 2. Write the prompt

Run the instructions through the `unslop-writing-for-agents` skill and apply
every fix. The fixed text is the prompt.

Done when: the fixed prompt is recorded.

## 3. Launch

Launch from the target directory:

```bash
cd <dir> && claude --bg -n "<name>" --model <model> --effort <level> \
  --permission-mode auto "<prompt>"
```

Pass `--model` and `--effort` only for values the user named; `claude --help`
lists the accepted values. A background session blocks on a permission prompt
until someone attaches, so pick a mode that covers the task: `auto` by default,
or the mode the user names. Use `bypassPermissions` only when the user asks for
it.

Done when: the launch output shows a session ID.

## 4. Confirm registration

The name appears in ListAgents or `claude agents --json`. If it is missing, the
launch failed; report the launch output verbatim.

Done when: the session is listed, or the failure is reported.

## 5. Report

Report one line in this format:

Session Title: <name> — ID: <id> — <model>, <effort>, <permission mode> permission mode, agent prompt: <prompt>

The ID is the short ID the launch prints. Model, effort, and permission mode
are the values the session runs with; write `default` for any the user left
unset. The agent prompt is the prompt from step 2.

Done when: the one-line report is delivered.
