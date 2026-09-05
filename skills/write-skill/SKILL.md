---
name: write-skill
description: Create and install a personal skill, offer eval choices, and add it to the README. Use when the user asks to create, add, write, or scaffold a new skill.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.5.0"
---

# Write skill

Turn a request into an installed skill listed in `~/.agents/README.md`. Use `skill-creator` for design and selected evals, unslop-writing-for-agents for polish, and install-skill for installation. The "Skill home" section of `~/.agents/AGENTS.md` holds the paths and format rules every step follows.

## 1. Verify the facts

Verify every fact the new skill will encode. Run the command, read the `--help`, reproduce the behavior. A claim that fails verification stays out. Cache in the skill only what the environment cannot answer with one lookup.

Done when: every fact the draft states has been run and confirmed.

## 2. Design and draft

Invoke the `skill-creator` skill for its capture-intent, interview, and draft steps. Draft at `~/.agents/.scratch/<name>/skill/` and keep evals and run outputs under `~/.agents/.scratch/<name>/`. Skip skill-creator's package step; step 5 installs instead. Step 3 governs all eval runs.

Before showing the draft, apply the house format: frontmatter `name` (lowercase letters, digits, hyphens), `description`, and a `metadata:` block with quoted `author: "<User Name> <<user email>>"` (from `git config user.name` and `git config user.email`) and `version: "0.1.0"`; body as one `## N. Title` section per step, each ending with a `Done when:` line. The user's dictated formats go in verbatim.

Run the draft through `~/.claude/skills/unslop-writing-for-agents/SKILL.md`, fix every finding, show the draft, and wait for approval. Fold amendments in.

Done when: the human has approved the prose.

## 3. Test the draft

Ask the user to choose before running evals:

- Skip all evals. The file and link checks still apply.
- Run one eval case focused on the skill's main behavior.
- Follow skill-creator's default eval flow.

Recommend one case for a skill with a single, narrow workflow and the default flow for skills spanning several steps or branches. If the user already chose for this creation, use that choice. Otherwise, wait for their answer.

For either eval option, read `~/.agents/skills/skill-creator/SKILL.md` and follow its "Running and evaluating test cases" workflow with the scratch draft as the skill and no skill as the baseline. Keep the runs under `~/.agents/.scratch/<name>/`. The one-case option limits the run to one comparison; the default option follows skill-creator's case-selection guidance. Show the results to the user. Fold amendments into the draft and repeat the selected eval flow until the user accepts the results.

Done when: the choice is recorded and either the user chose to skip all evals or has accepted the selected eval results.

## 4. Confirm README placement

Read `~/.agents/README.md` and recommend the section and position that fit the new skill and the existing ordering. Show the proposed entry with a relative link to `./skills/<name>/SKILL.md`, a short description, and enough surrounding text to make the placement clear. Include any inventory counts affected by the addition, verified against the installed inventory and planned addition.

Polish the proposed README change with unslop-writing-for-agents. Show it as a unified diff and ask the user to confirm the recommended placement and wording before editing the README. Reuse an explicit placement approval already given for this creation. Fold amendments in and show the revised diff for approval.

Done when: the user has approved the README diff, including the section and position of the entry.

## 5. Install and update README

Install the scratch draft by following `~/.claude/skills/install-skill/SKILL.md` with `~/.agents/.scratch/<name>/skill/` as the source. For this workflow, replace install-skill's "Reload and test" step with step 6 below. The eval choice in step 3 governs testing throughout installation and reload; neither adds a real-case invocation.

After installation checks pass, apply the approved README diff. Confirm the skill appears once in the approved location, its relative link resolves to the installed `SKILL.md`, and affected counts match the installed inventory. If the README has changed since approval, preserve those edits and seek approval again if the proposed placement or wording must change.

Done when: install-skill's file and link checks pass and the approved README entry and affected counts are verified.

## 6. Reload and report

Reload the skill index if supported, or tell the user a new session picks it up. Report the installed skill, its README section, and the eval results from step 3 or the user's explicit skip.

Done when: the reload status or new-session instruction, README location, and eval results or explicit skip are reported.

## 7. Edit later

Make every later edit with `~/.claude/skills/update-skill/SKILL.md`; it carries the version rule.

Done when: the later edit went through update-skill.
