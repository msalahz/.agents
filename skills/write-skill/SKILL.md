---
name: write-skill
description: Create and install a personal skill, run one eval case, and add it to the README. Use when the user asks to create, add, write, or scaffold a new skill.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.8.0"
---

# Write skill

Turn a request into an installed skill listed in `~/.agents/README.md`. Use `skill-creator` for design and evals, unslop-writing-for-agents for polish, and install-skill for installation. The "Skill home" section of `~/.agents/AGENTS.md` holds the paths and format rules every step follows.

## 1. Verify the facts

A claim that fails verification stays out. Cache in the skill only what the environment cannot answer with one lookup.

Done when: every fact the draft states has been run and confirmed.

## 2. Design and draft

Invoke `skill-creator` for its capture-intent, interview and draft steps, skipping its package step. Draft under `~/.agents/.scratch/<name>/`. Frontmatter carries `author` from `git config` and `version: "0.1.0"`; formats the user dictates go in verbatim. `agents/openai.yaml` goes in beside `SKILL.md` in the shape the "Skill home" rules give. Run the draft through unslop-writing-for-agents before showing it.

Done when: the human has approved the prose.

## 3. Test the draft

Run one eval case on the skill's main behavior. Skip evals or follow skill-creator's default eval flow only when the user asked for it, and a choice already made for this creation stands. Evals follow skill-creator's "Running and evaluating test cases" workflow under the scratch directory, with no skill as the baseline.

Done when: the user has accepted the eval results or asked to skip evals.

## 4. Confirm README placement

Propose the entry, a relative link to `./skills/<name>/SKILL.md` with a short description, in the section and position that fit the existing ordering, with any inventory counts it changes. Polish it with unslop-writing-for-agents and show it as a unified diff. A placement approval already given for this creation stands.

Done when: the user has approved the README diff, including the section and position of the entry.

## 5. Install and update README

Install the scratch draft through install-skill, with step 6 below in place of its "Reload and test" step so no real-case invocation is added beyond the eval choice in step 3. Apply the README diff after the install checks pass, preserving any README edits made since approval and seeking approval again if the placement or wording must change.

Done when: install-skill's file and link checks pass, the installed home holds `agents/openai.yaml`, the entry appears once in the approved location, its link resolves to the installed `SKILL.md`, and affected counts match the installed inventory.

## 6. Reload and report

Reload the skill index if supported, or tell the user a new session picks it up.

Done when: the reload status or new-session instruction, README location, and eval results or explicit skip are reported.

## 7. Edit later

Done when: every later edit went through update-skill, which carries the version rule.
