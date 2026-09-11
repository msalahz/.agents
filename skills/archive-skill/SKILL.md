---
name: archive-skill
description: Move a skill and everything it touched into ~/.agents/archive/<name> so it can be restored later.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Archive skill

Uninstall a skill by **moving** it into `~/.agents/archive/<name>/` instead of deleting. The name is this skill's argument.

## 1. Plan

Show what will move and which shared references will be cleaned, and get a yes before moving anything.

Done when: the human has approved a plan covering the home, the link, every file the skill owns and every reference to it.

## 2. Archive

Use `git mv` for tracked paths.

Done when: the skill and its references are gone from the filesystem and the archive folder alone is enough to restore it, shared edits included.
