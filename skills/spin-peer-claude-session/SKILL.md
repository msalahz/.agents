---
name: spin-peer-claude-session
description: Launch an independent peer Claude session with a chosen model, effort, and instructions. Use when the user asks to spin up a new session, peer session, or independent background session rather than a subagent.
author: Mohammed Zaghloul
version: 0.3.0
---

# Spin peer

`claude --bg` starts a full independent session. It registers as a peer in the
agents list, keeps its own context and lifecycle, and reports to no parent.

## Steps

1. Collect from the request: instructions (required), a short session name, model,
   effort, permission mode, and working directory. Defaults: a name derived from
   the task, the CLI's default model and effort, `auto` permission mode, the
   current directory.
2. Launch from the target directory:

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
3. Confirm registration: the name appears in ListAgents (or `claude agents --json`).
   Missing means the launch failed; report its output verbatim.
4. Report one line in this format:

   Session Title: <name> — ID: <id> — <model>, <effort>, <permission mode> permission mode, agent prompt: <prompt>

   Model, effort, and permission mode are the values the session runs with; write
   `default` for any the user left unset. The agent prompt is the instructions the
   session was launched with.

Done when the session shows in ListAgents and the one-line report is delivered.
