---
name: spin-bg-agent
description: Launch a background managed subagent with chosen model, effort, and instructions. Use when the user asks for a background agent or subagent that reports back to this session.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.0"
---

# Spin bg agent

The Agent tool launches a managed subagent. It runs in the background, reports to this session through a task notification, and takes follow-ups over SendMessage.

## 1. Collect the request

The instructions are required. Record them, plus whichever of a short name, model, effort, and own worktree the user named. Unnamed options take the session's defaults, and the name defaults to one derived from the task.

Done when: the instructions and every named option are recorded.

## 2. Write the prompt

The prompt is the instructions after the `unslop-writing-for-agents` skill has run on them with every fix applied.

Done when: the fixed prompt is recorded.

## 3. Pick the agent type

The type is `bg-<effort>` when the user named an effort, otherwise `general-purpose`. The `bg-*` definitions live in `~/.agents/agents/`, one per effort level, and Claude Code reads only `~/.claude/agents/`, where each must be a symlink to its home. A link added this turn is invisible to the Agent tool until the next turn, so add it, tell the user, and stop.

Done when: the type is recorded and, for a `bg-*` type, `~/.claude/agents/<type>.md` resolves to `~/.agents/agents/<type>.md`.

## 4. Launch

Launch with the type from step 3, the prompt from step 2, the name as the description, the user's model only when they named one, and a worktree only when they asked for one.

Done when: ListAgents shows the subagent under its type, or the launch error is reported verbatim.

## 5. Report

Report one line in this format:

Subagent: <name> — type: <agent type> — <model>, <effort>, agent prompt: <prompt>

Model and effort are the values the subagent runs with; write `default` for any the user left unset. The agent ID stays out of the report.

Done when: the one-line report is delivered.
