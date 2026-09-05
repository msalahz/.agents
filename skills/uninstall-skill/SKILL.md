---
name: uninstall-skill
description: Uninstall a skill and clean up its related files, configuration, registry entries, and instructions after confirmation.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Uninstall skill

Remove a skill's **home** at `~/.agents/skills/<name>` and its **link** at `~/.claude/skills/<name>`. Find and clean up related files and changes outside those paths too.

The name is this skill's argument. With no argument, list what is installed and ask which one.

## 1. Find both sides

Inspect both paths. The two sides drift apart, and each state calls for a different removal:

- **Home is a real directory.** Inventory every file inside it. Removing it deletes this installed copy.
- **Home is itself a symlink.** A skill vendored by a plugin or marketplace looks like this. Remove the symlink and leave its target alone.
- **Home missing, link present.** A dangling link. The link alone goes.
- **Link missing, home present.** The home alone goes.
- **Neither present.** Report that both paths are absent and continue checking for leftovers.

Done when: the state of both paths is reported.

## 2. Find related files and changes

Read the skill and its bundled scripts and references, when present, to identify what it installs, generates, or changes elsewhere. Search by the skill name, resolved path, and any discovered configuration names. Start with the skill inventory, agent configuration and instructions, and the current project. Follow concrete references to other locations and record the search scope and any inaccessible locations.

Check for:

- Entries in `~/.agents/.skill-lock.json`, README listings, and other discovered installation records.
- References in `AGENTS.md`, `CLAUDE.md`, other skills, and agent instructions.
- Additional skill links or copies, dedicated configuration, helper scripts, hooks, and temporary artifacts.
- Changes made to shared files during setup, including settings that do not contain the skill name.

For each finding, record the exact path, the evidence connecting it to this skill, and the proposed deletion or edit. Delete a whole file only when it belongs exclusively to the skill. In shared files, remove only the attributable entries or instructions and preserve other content. Check whether another installed skill depends on each proposed removal; report any dependency that would break.

Keep plugin source directories, unrelated files, user work produced with the skill, and session history. A name match alone does not establish ownership. Leave uncertain items in place and report them for a decision. If both installation paths and all checked related locations are clear, report that nothing remains to remove and stop.

Done when: every finding has a proposed action or a reason to retain it, and the search scope is recorded.

## 3. Confirm

Show the complete removal plan: each path, whether it is a real copy or a symlink, and every file inside a directory to be deleted. Show a unified diff for each shared file to be edited. Include retained or uncertain items, dependencies affected, and locations that could not be checked. State when a real copy will be permanently deleted and whether another copy is known.

Ask for a yes covering the listed deletions and edits. Approval already given for that exact plan counts. If later findings expand the plan, get approval for those additions before changing them.

Done when: the human has said yes, or the run has stopped.

## 4. Remove, then verify

Remove the link first and the home second, so a failure halfway leaves a home behind rather than a link pointing at nothing. Apply the approved cleanup edits and deletions. Unlink symlinks without deleting their targets.

Verify from the filesystem:

- Neither path exists any more.
- `ls ~/.claude/skills` shows no entry for the name.
- When the home was a symlink, its target is still there.
- Every approved related deletion or edit took effect, and modified structured files still parse.
- Shared files retain unrelated content, and retained files remain intact.
- Repeating the scoped searches finds no unexplained references or leftovers. Record each retained match and its reason.

Done when: every check has been run and its result recorded.

## 5. Reload and test

Use an available skill-index reload mechanism, then check whether `<name>` is absent. If reload or index inspection is unavailable, tell the user a new session is needed and report index verification as pending. Filesystem checks alone do not prove the active index refreshed.

Done when: index absence is verified, or the reload limitation and pending check are reported.

## 6. Report

Report the skills and related files removed, shared-file edits, retained items and reasons, search coverage and gaps, verification results, and reload status. Describe any failures or remaining work explicitly.

Done when: the report accounts for every item in the approved plan and every unresolved finding.
