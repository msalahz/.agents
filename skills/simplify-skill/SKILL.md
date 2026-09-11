---
name: simplify-skill
description: Cut a skill down to its outcome and the constraints the agent cannot discover on its own, and leave the how to the agent.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Simplify skill

The argument names an installed skill or a path to one. Rewrite it so each step states the **outcome** and only the **constraints** the agent could not discover by looking: house rules, fixed paths, gotchas, and where a human must say yes. Everything else is how, and the agent works that out. Keep a checkable `Done when:` on every step, since the criterion is what does the work the removed how used to do.

## 1. Cut

Show the rewrite as a unified diff against the original, with one line per removed passage saying why it was how and not constraint.

Done when: the human has approved the diff.

## 2. Apply

Apply the approved rewrite through `update-skill`. A path outside `~/.agents/skills` is a draft, so write the rewrite to it directly instead.

Done when: `update-skill` has reported, or the draft file holds the rewrite.
