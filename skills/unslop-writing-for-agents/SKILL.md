---
name: unslop-writing-for-agents
description: Run a text by the writing-for-agents and unslop skills, then apply every fix.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <mohammed@devpluscoder.com>"
  version: "0.1"
---

The text is this skill's argument, a file path or inline prose. With no argument, ask for it.

Invoke the `writing-for-agents` and `unslop` skills. Fix every finding. Show the fixed
version, then wait for approval to apply it.
