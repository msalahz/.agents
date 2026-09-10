---
name: uninstall-skill
description: Uninstall a skill and clean up its related files, configuration, registry entries, and instructions after confirmation.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Uninstall skill

Remove a skill's **home** at `~/.agents/skills/<name>` and its **link** at `~/.claude/skills/<name>`, plus whatever it left elsewhere.

The name is this skill's argument. With no argument, list what is installed and ask which one.

## 1. Find both sides

A home that is itself a symlink belongs to a plugin: the symlink goes, its target stays. A dangling link or an unlinked home is still a removal. When neither exists, say so and keep looking for leftovers.

Done when: the state of both paths is reported.

## 2. Find related files and changes

Look for what the skill installed, generated or changed elsewhere: installation records such as `~/.agents/.skill-lock.json` and the README, agent instructions, other skills, the current project, and shared settings edited during setup that may not carry the skill's name.

Delete a whole file only when it belongs to the skill alone; in shared files remove only the attributable entries. Keep plugin source directories, user work produced with the skill, and session history. A name match alone does not establish ownership; leave uncertain items in place and report them. Report any dependency of another installed skill that a removal would break.

Done when: every finding has a proposed action or a reason to retain it, and the search scope, including locations that could not be checked, is recorded.

## 3. Confirm

Show the complete plan: every path and every file inside it, a unified diff per shared file, the retained and uncertain items, and whether a real copy being deleted has another known copy. Get a yes before changing anything, and again for anything added to the plan later.

Done when: the human has said yes, or the run has stopped.

## 4. Remove, then verify

Remove the link before the home, so a failure halfway leaves a home behind rather than a link pointing at nothing. Unlink symlinks without deleting their targets.

Done when: neither path exists, a symlinked home's target is intact, every approved edit and deletion took effect with structured files still parsing and unrelated content preserved, and repeating the searches finds nothing unexplained.

## 5. Reload and test

Filesystem checks alone do not prove the active skill index refreshed.

Done when: the index no longer lists `<name>`, or reload is unavailable and the user has been told a new session is needed with the index check reported as pending.

## 6. Report

Describe failures and remaining work explicitly.

Done when: the report accounts for every item in the approved plan, every retained or unresolved finding, the search coverage and gaps, verification results, and reload status.
