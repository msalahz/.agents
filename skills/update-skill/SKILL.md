---
name: update-skill
description: Edit an installed skill in place and bump its version. Use when the user asks to change an existing skill, or another skill needs one edited.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.5.0"
---

# Update skill

Change an installed skill the way write-skill made it. The "Skill home" section of `~/.agents/AGENTS.md` holds the paths and format rules.

The argument names the skill and the changes wanted. With either missing, ask for it before anything else. Rename a skill with uninstall-skill then install-skill.

## 1. Locate the skill

A home at `~/.agents/skills/<name>` whose `readlink -f` resolves outside `~/.agents/skills` belongs to a plugin, and the plugin's next update would overwrite the edit. Stop and report.

Done when: the home path, the file list including every sibling file `SKILL.md` links to, and the current `version` are written down.

## 2. Verify the facts

A claim the change encodes that fails verification stays out.

Done when: every fact the edit states has been run and confirmed.

## 3. Draft the edit

Draft under `~/.agents/.scratch/<name>/`, never in the home. Fix what the change leaves behind, such as a rule now stated twice or a step that still names the removed thing, and say so when showing the draft. Run the draft through unslop-writing-for-agents before showing it as a unified diff against the installed file.

Done when: the human has approved the diff.

## 4. Test the edit

Offer three choices: skip all evals, run one eval case on the changed behaviour, or follow skill-creator's default eval flow. Recommend one case for a small change and the default flow for changes spanning several steps or branches. A choice already made for this update stands. Evals follow skill-creator's "Running and evaluating test cases" workflow under the scratch directory, with the installed version as the baseline.

Done when: the choice is recorded and either the user chose to skip all evals or has accepted the selected eval results.

## 5. Bump the version

Bump minor when a step, the frontmatter invocation, or a report contract changes, and patch for wording.

Done when: `version` in the draft differs from the recorded one and follows the rule.

## 6. Write and verify

Done when: the home holds the approved draft, its frontmatter `name` still equals `<name>`, every sibling file `SKILL.md` links to exists inside the home, `readlink ~/.claude/skills/<name>` still resolves to the home, and the scratch directory is gone.

## 7. Reload and report

Reload the skill index if supported, or tell the user a new session picks it up. Reloading adds no eval runs.

Done when: the reload status or new-session instruction is reported, along with the eval results or explicit skip.
