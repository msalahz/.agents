---
name: spin-peer-codex-session
description: Launch an independent peer Codex session that lists in the Codex desktop app, then message it and read its replies. Use when the user asks to spin up a Codex session or a Codex peer session, rather than a one-shot Codex delegation.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Spin peer Codex session

`scripts/codex_peer.py` starts a Codex thread over the app-server protocol. The
desktop app lists the thread under its name. One `codex app-server` per machine
hosts every peer. The script starts it on demand at
`~/.claude/codex-peer.sock` and logs to `~/.claude/codex-peer.log`. A peer
speaks only when sent a turn.

Script: `~/.claude/skills/spin-peer-codex-session/scripts/codex_peer.py`.
`--help` lists every flag.

## 1. Collect the request

Collect from the request: instructions (required), a short unique session name,
model, effort, sandbox, approval, and working directory. Defaults: a name
derived from the task, the model and effort in `~/.codex/config.toml`,
`workspace-write` sandbox with `on-request` approvals, the current directory.

Done when: the instructions and every named option are recorded.

## 2. Write the prompt

Run the instructions through the `unslop-writing-for-agents` skill and apply
every fix. The fixed text is the prompt.

Done when: the fixed prompt is recorded.

## 3. Launch

`new` blocks until the first turn ends, so run it as a background command:

```bash
python3 ~/.claude/skills/spin-peer-codex-session/scripts/codex_peer.py new \
  --name "<name>" --cwd "<dir>" --model <model> --effort <effort> \
  --sandbox <sandbox> --approval <approval> "<prompt>"
```

Omit `--model` and `--effort` when the user named none; effort passes through
as given. Codex's `auto_review` reviewer answers approval requests, so the peer
never waits on a prompt. Bypass is `--sandbox danger-full-access --approval
never`, only when the user asks for it.

The output opens with `thread_id`, `name`, `model`, `effort`, `sandbox`,
`approval`, and `attach` lines, then a blank line, then the reply. Keep the
`thread_id`; every later command uses it. Exit 2 means the turn outlived
`--timeout` (default 540 s) and is still running. Use `read <thread_id>` later.
Any other non-zero exit is a failure. Report its output verbatim.

Done when: the output shows a `thread_id` line and a reply, or exit 2 with the
thread id.

## 4. Report

Report the session in this format:

Session Title: <name>; ID: <thread_id>; <model>, <effort>, <sandbox> sandbox, <approval> approval

Then write `Attach: codex resume <thread_id>` and `Agent prompt: <prompt>` on
separate lines.

Copy model, effort, sandbox, and approval from the launch output. These are the
values the peer runs with, including model and effort resolved from config. The
agent prompt is the prompt from step 2.

Done when: the report is delivered.

## Later turns

- `send <thread_id> "<message>"` runs one more turn and prints the reply, with
  the same blocking, timeout, and exit rules as `new`. Run it in the
  background.
- `read <thread_id>` prints the newest available reply and the actual latest
  turn's status without starting a turn. While a turn is running, the reply may
  belong to the preceding turn.
- `stop` stops the shared app-server. Threads survive it; the next `new` or
  `send` starts a fresh server.
