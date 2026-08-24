---
name: unslop-writing-for-agents
description: Run a text by the writing-for-agents and unslop skills, then apply every fix. Use when reviewing or polishing a skill, AGENTS.md, or other agent-facing text.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Unslop writing for agents

The text is this skill's argument, a file path or inline prose. With no argument, ask for it.

## 1. Review

Invoke the `writing-for-agents` and `unslop` skills and review the text against both.

Done when: every finding is collected.

## 2. Fix and show

Fix every finding. Show the fixed version as a unified diff against the original. A request from another skill applies the fix straight away and reports it; a request from the user waits for approval first.

Done when: the fixed text is applied, or an interactive run has stopped without approval.
