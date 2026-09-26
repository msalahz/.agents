# Skill structure
The shape of a skill: frontmatter, openai.yaml metadata and invocation policy, step sections, descriptions, minimal and composite skills.

## Patterns

- **Frontmatter fields.** Give `SKILL.md` frontmatter a `name`, a `description`, and a `metadata` block with quoted `author` and `version`, allowing `disable-model-invocation: true` even though `quick_validate.py` rejects that key. _Sources: AGENTS.md, skills/archive-skill/SKILL.md, skills/install-skill/SKILL.md, skills/uninstall-skill/SKILL.md, skills/arbitrate-review/SKILL.md_
- **openai.yaml sidecar.** Put `agents/openai.yaml` beside `SKILL.md` with a title-case `interface.display_name` and a 25 to 64 character `interface.short_description`. _Sources: AGENTS.md, skills/write-skill/SKILL.md, skills/arbitrate-review/agents/openai.yaml, skills/author-ticket/agents/openai.yaml, skills/coordinator/agents/openai.yaml, skills/review-loop/agents/openai.yaml, skills/review-pr/agents/openai.yaml, skills/supervise-issue/agents/openai.yaml, skills/spin-bg-agent/agents/openai.yaml, skills/spin-peer-session/agents/openai.yaml, skills/reply/agents/openai.yaml, skills/favicon-generator/agents/openai.yaml_

### Body layout

- **Numbered steps with Done when.** Write the body as one `## N. Title` section per step, each ending in a `Done when:` line, even when the skill has a single step. _Sources: AGENTS.md, skills/archive-skill/SKILL.md, skills/reply/SKILL.md, skills/arbitrate-review/SKILL.md_ _Conflicts with: Process list and catalogue_
- **Process list and catalogue.** Build a reference-heavy skill as a short Process list followed by a catalogue of rules, without numbered steps or `Done when:` lines. _Sources: skills/unslop/SKILL.md_ _Conflicts with: Numbered steps with Done when_
- **Step cadence.** State which steps run once per session, which per task, and which per piece. _Sources: skills/coordinator/SKILL.md_
- **Bold defined terms.** Bold each defining word in the one-paragraph intro, name the argument there, and reuse those exact words through the body. _Sources: skills/archive-skill/SKILL.md, skills/install-skill/SKILL.md_
- **Arguments substitution.** Embed `$ARGUMENTS` in the body where the user's input belongs, as in `Question: $ARGUMENTS`. _Sources: skills/reply/SKILL.md_
- **Arguments line up front.** Open the body with `Arguments: <pr> <n>` and a paragraph stating the session's role, display name, working directory, and limits. _Sources: skills/arbitrate-review/SKILL.md_

### Skill shapes

- **Minimal skill.** Keep a skill to a few short steps with its principles in the intro, so it models the brevity it asks for. _Sources: skills/simplify-skill/SKILL.md_
- **Composition skill.** Write a thin skill that runs two other skills in order and carries no rules of its own. _Sources: skills/unslop-writing-for-agents/SKILL.md_
- **Operation dispatch.** Take `<operation> [argument]`, list the operations and stop when none is given, and after resolving config run only the section that matches the operation. _Sources: skills/knowledge-wiki/SKILL.md_
- **Supporting files by link.** Move terms into a `CONTEXT.md` and output shapes into a `FORMATS.md` beside the skill, and link both from `SKILL.md`. _Sources: skills/knowledge-wiki/SKILL.md_
- **Formats file of templates.** Hold a fenced markdown template in `FORMATS.md` for every shape the skill writes. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Self-contained script package.** Bundle the script, its `package.json`, and an example config under the skill's `scripts/` folder. _Sources: skills/favicon-generator/SKILL.md_

## Strategies

- **Cache only what one lookup cannot answer.** Put a fact in the skill only when the environment cannot give it in a single lookup. _Sources: skills/write-skill/SKILL.md_
- **Outcome plus undiscoverable constraints.** Rewrite each step to state its outcome and only the constraints the agent could not find by looking. _Sources: skills/simplify-skill/SKILL.md_
- **Done when replaces how.** Keep a checkable `Done when:` on every step, because that line does the work the deleted how-to text used to do. _Sources: skills/simplify-skill/SKILL.md_

## Practices

- **Descriptions state what and when.** Write each description as what the skill does plus when it triggers, with no padding. _Sources: AGENTS.md, skills/install-skill/SKILL.md_
- **Mirror invocation policy for Codex.** Set `policy.allow_implicit_invocation: false` in `openai.yaml` exactly when the frontmatter has `disable-model-invocation: true`, and leave the policy block out of model-invocable skills. _Sources: AGENTS.md, skills/arbitrate-review/agents/openai.yaml, skills/author-ticket/agents/openai.yaml, skills/coordinator/agents/openai.yaml, skills/review-pr/agents/openai.yaml, skills/supervise-issue/agents/openai.yaml, skills/reply/agents/openai.yaml, skills/review-loop/agents/openai.yaml, skills/spin-bg-agent/agents/openai.yaml, skills/spin-peer-session/agents/openai.yaml_
- **Keep openai.yaml in sync.** Write `agents/openai.yaml` when the home lacks one, and update it whenever an edit changes the display name, short description, or `disable-model-invocation`. _Sources: skills/update-skill/SKILL.md_
- **What counts as a constraint.** Keep house rules, fixed paths, gotchas, and points where a human must say yes, and leave the rest of the how to the agent. _Sources: skills/simplify-skill/SKILL.md_
- **Ask for missing input.** Accept the text as a file path or inline prose, and ask for it when no argument is given. _Sources: skills/unslop-writing-for-agents/SKILL.md_
- **Format rules live in AGENTS.md.** Point to the "Skill home" section of `~/.agents/AGENTS.md` for skill paths and format rules instead of restating them in a skill. _Sources: skills/update-skill/SKILL.md_

## Where it lives

The "Skill home" section of AGENTS.md holds the frontmatter fields, the `openai.yaml` shape, the invocation-policy mirror, numbered steps with `Done when:`, and the what-and-when description rule. No file under docs/agents covers skill structure. The rest appears only inside individual skills: caching and constraint rules in write-skill and simplify-skill, the sync rule in update-skill, and the body layouts and skill shapes in arbitrate-review, coordinator, reply, archive-skill, install-skill, unslop, unslop-writing-for-agents, knowledge-wiki, and favicon-generator.
