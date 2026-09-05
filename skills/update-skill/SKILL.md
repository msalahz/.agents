---
name: update-skill
description: Edit an installed skill in place and bump its version. Use when the user asks to change an existing skill, or another skill needs one edited.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.0"
---

# Update skill

Change an installed skill the way write-skill made it. The "Skill home" section of `~/.agents/AGENTS.md` holds the paths and format rules.

The argument names the skill and the changes wanted. With either missing, ask for it before anything else. Rename a skill with uninstall-skill then install-skill.

## 1. Locate the skill

The home is `~/.agents/skills/<name>`. Run `readlink -f` on it and confirm the result still sits under `~/.agents/skills`. A home that resolves elsewhere belongs to a plugin, and the plugin's next update would overwrite the edit. Stop and report.

Read `SKILL.md` and every sibling file it links to, in full. Record the current `version`.

Done when: the home path, the file list and the current version are written down.

## 2. Verify the facts

Verify every fact the change will encode. Run the command, read the `--help`, reproduce the behaviour. A claim that fails verification stays out.

Done when: every fact the edit states has been run and confirmed.

## 3. Draft the edit

Copy the home to `~/.agents/.scratch/<name>/skill/` and a second copy to `~/.agents/.scratch/<name>/skill-snapshot/`. Apply the requested changes to the first copy. Then hunt for what the change leaves behind: a rule now stated twice, a column that only ever holds one value, a step that still names the removed thing. Fix those too and say so when showing the draft.

Run the copy through `~/.claude/skills/unslop-writing-for-agents/SKILL.md`, fix every finding, and show the result as a unified diff against the installed file. Wait for approval. Fold amendments in and show the diff again.

Done when: the human has approved the diff.

## 4. Test the edit

Ask the user to choose before running evals:

- Skip all evals. The version bump and file and link checks still apply.
- Run one eval case focused on the changed behaviour.
- Follow skill-creator's default eval flow.

Recommend one case for a small change and the default flow for changes spanning several steps or branches. If the user already chose for this update, use that choice. Otherwise, wait for their answer.

For either eval option, read `~/.agents/skills/skill-creator/SKILL.md` and follow its "Running and evaluating test cases" workflow with the snapshot as the baseline and the edited copy as the skill, under `~/.agents/.scratch/<name>/`. The one-case option limits the run to one comparison; the default option follows skill-creator's case-selection guidance. Show the results to the user.

Done when: the choice is recorded and either the user chose to skip all evals or has accepted the selected eval results.

## 5. Bump the version

Bump minor when a step, the frontmatter invocation, or a report contract changes, and patch for wording. Set it in the draft before writing.

Done when: `version` in the draft differs from the recorded one and follows the rule.

## 6. Write and verify

Copy the approved draft over the home, then delete `~/.agents/.scratch/<name>/`. Check:

- Frontmatter `name` still equals `<name>`.
- Every sibling file `SKILL.md` links to exists inside the home.
- `readlink ~/.claude/skills/<name>` still resolves to the home.

Done when: every check has been run and its result recorded, and the scratch directory is gone.

## 7. Reload and report

Reload the skill index if supported, or tell the user a new session picks it up. Report the eval results from step 4, or state that the user chose to skip all evals. Reloading adds no eval runs.

Done when: the reload status or new-session instruction is reported, along with the eval results or explicit skip.
