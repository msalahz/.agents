---
name: reply
description: Answer a question in text without changing anything.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Reply

Question: $ARGUMENTS

## 1. Answer

Reply with an answer to the question in plain text. Read and run whatever finding the answer needs, and change nothing: no file edits, no commands that alter state.

Done when: the answer is written and nothing has changed.
