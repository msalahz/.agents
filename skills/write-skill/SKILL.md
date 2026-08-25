---
name: write-skill
description: Build, install, and live-test a new personal skill end to end. Use when the user asks to create, add, write, or scaffold a new skill.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Write skill

Turn a request into an installed, tested skill by chaining two existing flows:
draft with unslop-writing-for-agents, install with install-skill.

## 1. Verify the facts

Verify every fact the new skill will encode. Run the command, read the
`--help`, reproduce the behavior; a claim that fails verification stays out.
Cache in the skill only what the environment cannot answer with one lookup.

Done when: every fact the draft states has been run and confirmed.

## 2. Draft

Draft the skill prose by following
`~/.claude/skills/unslop-writing-for-agents/SKILL.md`: invoke
`writing-for-agents` and `unslop`, fix every finding, show the draft, and
wait for approval. Format the draft like
`~/.claude/skills/install-skill/SKILL.md`: frontmatter carries `name`
(lowercase letters, digits, hyphens), `description`, and a `metadata:` block
with quoted `author: "<User Name> <<user email>>"` (resolve both from
`git config user.name` and `git config user.email`) and `version` starting
at "0.1.0"; the body uses one numbered `## N. Title` section per step, each
ending with a `Done when:` line. Fold amendments in; the user's dictated
formats go in verbatim.

Done when: the human has approved the prose.

## 3. Install

Write the confirmed draft to a scratch directory and install it by following
`~/.claude/skills/install-skill/SKILL.md` with that directory as the source
(home `~/.agents/skills/<name>`, link `~/.claude/skills/<name>`).

Done when: install-skill's checks pass.

## 4. Reload and test

Reload the skill index (`/reload-skills`, or tell the user a new session picks
it up), then run the skill once on a real case and report what it produced.

Done when: the skill shows in the skill index and one real invocation has run
and been reported.

## 5. Edit later

Make every later edit with `~/.claude/skills/update-skill/SKILL.md`; it
carries the version rule.

Done when: the later edit went through update-skill.
