---
name: write-skill
description: Build, install, and live-test a new personal skill end to end. Use when the user asks to create, add, write, or scaffold a new skill.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.0"
---

# Write skill

Turn a request into an installed, tested skill by chaining three flows: design and test with `skill-creator`, polish with unslop-writing-for-agents, install with install-skill. The "Skill home" section of `~/.agents/AGENTS.md` holds the paths and format rules every step follows.

## 1. Verify the facts

Verify every fact the new skill will encode. Run the command, read the `--help`, reproduce the behavior. A claim that fails verification stays out. Cache in the skill only what the environment cannot answer with one lookup.

Done when: every fact the draft states has been run and confirmed.

## 2. Design and draft

Invoke the `skill-creator` skill for its capture-intent, interview, and draft steps. Draft at `~/.agents/.scratch/<name>/skill/` and keep evals and run outputs under `~/.agents/.scratch/<name>/`. Skip skill-creator's package step; step 4 installs instead.

Before showing the draft, apply the house format: frontmatter `name` (lowercase letters, digits, hyphens), `description`, and a `metadata:` block with quoted `author: "<User Name> <<user email>>"` (from `git config user.name` and `git config user.email`) and `version: "0.1.0"`; body as one `## N. Title` section per step, each ending with a `Done when:` line. The user's dictated formats go in verbatim.

Run the draft through `~/.claude/skills/unslop-writing-for-agents/SKILL.md`, fix every finding, show the draft, and wait for approval. Fold amendments in.

Done when: the human has approved the prose.

## 3. Test the draft

Follow skill-creator's "Running and evaluating test cases" on the scratch draft: with-skill and baseline runs, assertions, grading, and the viewer. When the user asks to skip evals, run the draft once on one real case instead. Fold what the results show back into the draft and repeat until the user is satisfied.

Done when: the user has accepted the test results.

## 4. Install

Install the scratch draft by following `~/.claude/skills/install-skill/SKILL.md` with `~/.agents/.scratch/<name>/skill/` as the source.

Done when: install-skill's checks pass.

## 5. Reload and test

Reload the skill index (`/reload-skills`, or tell the user a new session picks it up), then run the installed skill once on a real case and report what it produced.

Done when: the skill shows in the skill index and one real invocation has run and been reported.

## 6. Edit later

Make every later edit with `~/.claude/skills/update-skill/SKILL.md`; it carries the version rule.

Done when: the later edit went through update-skill.
