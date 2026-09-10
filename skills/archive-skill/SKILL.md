---
name: archive-skill
description: Move a skill and everything it touched into ~/.agents/archive/<name> so it can be restored later.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Archive skill

Uninstall a skill by **moving** instead of deleting. The name is this skill's argument.

## 1. Plan

Find the skill's home, its link in `~/.claude/skills`, the files it owns, and every reference to it in shared files (README, `.gitignore`, `.skill-lock.json`, agent instructions, other skills). Show the plan and get a yes before moving anything.

Done when: the human has approved a plan covering every file and reference found.

## 2. Archive

Move the home and owned files into `~/.agents/archive/<name>/`, clean the shared references, and leave a short manifest there recording where each file came from and how to reverse the shared edits. Use `git mv` for tracked paths.

Done when: the skill and its references are gone from the filesystem and the archive folder alone is enough to restore it.
