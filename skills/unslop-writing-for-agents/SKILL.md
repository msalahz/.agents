---
name: unslop-writing-for-agents
description: Run a text by the writing-for-agents and unslop skills, then apply every fix. Use when reviewing or polishing a skill, AGENTS.md, or other agent-facing text.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Unslop writing for agents

The text is this skill's argument, a file path or inline prose. With no argument, ask for it.

## 1. Review

Invoke the `writing-for-agents` and `unslop` skills and review the text against both.

Done when: every finding is collected.

## 2. Fix and show

Fix every finding. Show the fixed version as a unified diff against the original,
then wait for approval to apply it.

Done when: the approved diff is applied, or the run has stopped without approval.
