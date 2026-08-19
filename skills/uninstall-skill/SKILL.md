---
name: uninstall-skill
description: Remove an installed skill — its home under ~/.agents/skills and its link in ~/.claude/skills.
disable-model-invocation: true
---

# Uninstall skill

Remove a skill's **home** at `~/.agents/skills/<name>` and its **link** at `~/.claude/skills/<name>`.

The name is this skill's argument. With no argument, list what is installed and ask which one.

## 1. Find both sides

Inspect both paths. The two sides drift apart, and each state is removed differently:

- **Home is a real directory** — removing it deletes the skill's only copy.
- **Home is itself a symlink**, as a skill vendored by a plugin or marketplace is — remove the symlink and leave its target where it is.
- **Home missing, link present** — a dangling link; the link alone goes.
- **Link missing, home present** — the home alone goes.
- **Neither present** — report that nothing is installed under that name and stop.

Done when: the state of both paths is reported.

## 2. Confirm

Show the human exactly what disappears: each path, whether it is a real copy or a symlink, and for a real directory the files it holds. A real home with no copy anywhere else is gone for good — say so when that is the case. Ask for a yes.

Done when: the human has said yes, or the run has stopped.

## 3. Remove, then verify

Remove the link first and the home second, so a failure halfway leaves a home behind rather than a link pointing at nothing.

Verify from the filesystem:

- Neither path exists any more.
- `ls ~/.claude/skills` shows no entry for the name.
- When the home was a symlink, its target is still there.

Done when: every check has been run and its result recorded.

## 4. Reload

Make the running session forget the skill. Ask the host to re-read its skill index — in Claude Code, list the available skills and confirm `<name>` no longer appears. When the host offers no way to re-read the index mid-session, say so plainly and tell the human it disappears in a new session — never present a restart-only host as a reload that worked.

Done when: `<name>` is confirmed gone from this session, or the human has been told a new session is needed.

## 5. Report

Report what was removed, what was left alone, each verification result, and whether the reload took.
