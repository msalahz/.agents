---
name: spin-bg-agent
description: Launch a background managed subagent with chosen model, effort, and instructions. Use when the user asks for a background agent or subagent that reports back to this session.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.1"
---

# Spin bg agent

The Agent tool launches a managed subagent: it runs in the background, reports to this session through a task notification, and takes follow-ups over SendMessage.

## 1. Collect the request

Collect from the request: instructions (required), a short name, model, effort, and whether it needs its own worktree. Defaults: a name derived from the task, the session's model and effort, the current directory. Permission mode is the parent session's; a subagent's permission prompts surface here.

Done when: the instructions and every named option are recorded.

## 2. Write the prompt

Run the instructions through the `unslop-writing-for-agents` skill and apply every fix. The fixed text is the prompt.

Done when: the fixed prompt is recorded.

## 3. Pick the agent type

Effort lives in the agent definition, not in the launch call, so this skill ships one definition per level in its `agents/` folder: `bg-low`, `bg-medium`, `bg-high`, `bg-xhigh`, `bg-max`. Any skill that launches a subagent at a named effort uses them the same way. The type is `bg-<effort>` when the user named an effort, otherwise `general-purpose`.

A definition written during a session stays invisible to that session's Agent tool. When `~/.claude/agents/bg-<effort>.md` is missing, copy it there from `agents/`, tell the user a new session picks it up, and stop.

Done when: the type is recorded and its definition exists under `~/.claude/agents/`.

## 4. Launch

Call the Agent tool with `subagent_type` from step 3, `prompt` set to the prompt from step 2, `description` set to the name, `model` set when the user named one (`fable`, `opus`, `sonnet`, `haiku`; the override wins over the definition), and `isolation: "worktree"` only when they asked for one. Leave `run_in_background` unset when the tool offers it; subagents run in the background by default.

Done when: the tool result carries an agent ID.

## 5. Confirm registration

ListAgents shows the subagent under its ID and agent type. Missing means the launch failed; report the tool's error verbatim.

Done when: the subagent is listed, or the failure is reported.

## 6. Report

Report one line in this format:

Subagent: <name> — type: <agent type> — <model>, <effort>, agent prompt: <prompt>

Model and effort are the values the subagent runs with; write `default` for any the user left unset. The agent ID stays out of the report. The result arrives as a task notification; a follow-up goes through SendMessage to the same agent.

Done when: the one-line report is delivered.
