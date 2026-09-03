---
name: reply
description: Answer a question in text and take no other action.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Reply

Question: $ARGUMENTS

## 1. Answer

Answer the question in plain text from what is already in context. The text reply is the whole response: no tool calls, no file edits.

Done when: the answer is written and nothing else has run.
