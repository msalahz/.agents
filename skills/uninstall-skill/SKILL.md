---
name: uninstall-skill
description: Remove an installed skill, both its home under ~/.agents/skills and its link in ~/.claude/skills.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.1"
---

# Uninstall skill

Remove a skill's **home** at `~/.agents/skills/<name>` and its **link** at `~/.claude/skills/<name>`.

The name is this skill's argument. With no argument, list what is installed and ask which one.

## 1. Find both sides

Inspect both paths. The two sides drift apart, and each state calls for a different removal:

- **Home is a real directory.** Removing it deletes the skill's only copy.
- **Home is itself a symlink.** A skill vendored by a plugin or marketplace looks like this. Remove the symlink and leave its target alone.
- **Home missing, link present.** A dangling link. The link alone goes.
- **Link missing, home present.** The home alone goes.
- **Neither present.** Report that nothing is installed under that name and stop.

Done when: the state of both paths is reported.

## 2. Confirm

Show the human exactly what disappears: each path, whether it is a real copy or a symlink, and for a real directory the files it holds. A real home with no copy anywhere else is gone for good. Say so when that is the case. Ask for a yes.

Done when: the human has said yes, or the run has stopped.

## 3. Remove, then verify

Remove the link first and the home second, so a failure halfway leaves a home behind rather than a link pointing at nothing.

Verify from the filesystem:

- Neither path exists any more.
- `ls ~/.claude/skills` shows no entry for the name.
- When the home was a symlink, its target is still there.

Done when: every check has been run and its result recorded.

## 4. Reload and test

Reload the skill index (`/reload-skills`, or tell the user a new session picks
it up), then confirm `<name>` no longer shows in the skill index and report
its absence.

Done when: the skill is gone from the skill index and its absence has been
reported.

## 5. Report

Report what was removed, what was left alone, each verification result, and whether the reload took.
