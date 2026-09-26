# Engineering practice
Coding rules, validation gates and CI, UI checks in the browser, and the favicon generator.

## Patterns

- **Config-driven generator.** Have the script read one JSON config and write every output into the repo, so a rerun reproduces the result. _Sources: skills/favicon-generator/SKILL.md_

## Strategies

- **CI is the arbiter.** When a local build fails only because a secret manager or its secrets are unreachable, report that and let CI decide; fix any other failure before commit. _Sources: skills/author-ticket/SKILL.md, skills/supervise-issue/SKILL.md_

## Practices

### Coding

- **Read the global coding rules.** Read the Coding rules in `~/.agents/AGENTS.md` before writing code. _Sources: skills/author-ticket/SKILL.md_
- **Simplest solution.** Use the simplest solution that meets every requirement. _Sources: AGENTS.md_
- **Match prior art.** Read the prior-art files the ticket names and their neighbours, and match their code patterns, abstractions, design choices, theme, and file layout. _Sources: AGENTS.md, skills/author-ticket/SKILL.md_
- **Extend before adding.** Extend an abstraction that already exists before adding a new one. _Sources: AGENTS.md_
- **Names over comments.** In code you write or change, refactor until the names explain it, and write no comments. _Sources: AGENTS.md_
- **Leave other code alone.** Refactor only the code you write or change. _Sources: AGENTS.md_
- **Report out-of-scope finds.** Report a pre-existing bug or an unrequested improvement as a follow-up in the summary instead of fixing it. _Sources: AGENTS.md_
- **Pin dependencies.** Pin dependencies to exact versions instead of `latest`. _Sources: AGENTS.md_
- **Reuse the implement skill.** Follow `~/.agents/skills/implement/SKILL.md`, swap its `/code-review` step for the review loop, and apply `/tdd` only where the repo already keeps tests of that kind. _Sources: skills/author-ticket/SKILL.md_

### Validation and UI checks

- **End with pnpm validate.** End any session that changed code by running `pnpm validate`. _Sources: AGENTS.md_
- **Validation fallback.** When the repo has no `validate` script, run its lint, typecheck, and test scripts and name what you ran. _Sources: AGENTS.md_
- **Done means green.** Call the session done only when validation passes. _Sources: AGENTS.md_
- **Gate set.** Run the repo's validate script and its build, plus `tofu fmt -check` and `tofu validate` for infrastructure changes. _Sources: skills/author-ticket/SKILL.md_
- **Real exit codes.** Run the repo's validate script and the gates the author used, and read each real exit code, with no `| tail` or `| head` and with `set -o pipefail` when a pipe is unavoidable. _Sources: skills/arbitrate-review/SKILL.md, skills/author-ticket/SKILL.md_
- **Record the validate exit code.** Run the validate script and record its exit code in the review. _Sources: skills/review-pr/SKILL.md_
- **All checks pass.** Require `gh pr checks --json name,state,bucket` to show every bucket as `pass`. _Sources: skills/supervise-issue/SKILL.md_
- **Criteria met or marked.** Treat implementation as done when the diff meets every numbered criterion or the criterion is marked human-only. _Sources: skills/author-ticket/SKILL.md_
- **Check UI in Chrome.** Before calling a UI change done or pushing it, open it in the user's Chrome tab on the dev server, following the repo's browser-testing instructions. _Sources: AGENTS.md, skills/author-ticket/SKILL.md_
- **One shared dev server.** Use the dev server already running, and subagents use it too; if none is running, start one and say so. _Sources: AGENTS.md_

### Favicon generator

- **State the input precondition.** Require a single-color glyph on a transparent background as the source logo; the script uses only its alpha channel. _Sources: skills/favicon-generator/SKILL.md_
- **Color as hex.** Ask for the glyph color as a hex value. _Sources: skills/favicon-generator/SKILL.md_
- **Sample from a screenshot.** When the user gives a screenshot of an icon to match, sample its stroke color with sharp and confirm the hex with the user. _Sources: skills/favicon-generator/SKILL.md_
- **Ask for manifest fields.** Ask for manifest `name`, `short_name`, `theme_color`, and `background_color` every time instead of filling them from `package.json`. _Sources: skills/favicon-generator/SKILL.md_
- **Overridable defaults.** Offer defaults the user can override: coverage `1`, touch coverage `0.7`, white glyph on `#1f1f1f`, display `standalone`. _Sources: skills/favicon-generator/SKILL.md_
- **Config lives in the repo.** Copy the example config to `<repo>/scripts/favicons.config.json` and fill it with the collected values. _Sources: skills/favicon-generator/SKILL.md_
- **Config-relative paths.** Write `source` and `outputDir` relative to the config file. _Sources: skills/favicon-generator/SKILL.md_
- **Install once with pnpm.** Install the script's dependencies with `pnpm install --dir <skill>/scripts`, then run `pnpm --dir <skill>/scripts generate <config>`. _Sources: skills/favicon-generator/SKILL.md_
- **Output file checklist.** Finish generation only when the seven named icon and manifest files exist in the public directory. _Sources: skills/favicon-generator/SKILL.md_
- **Visual check.** Upscale the 32px favicon with nearest-neighbour to about 192px on white and dark tiles, view it, and confirm the glyph is centred, unclipped, and legible. _Sources: skills/favicon-generator/SKILL.md_
- **Fix through the config.** Fix clipping or contrast by changing the config and rerunning generation. _Sources: skills/favicon-generator/SKILL.md_
- **Leave the app head alone.** Report the printed head link block for the user to paste instead of editing the app head. _Sources: skills/favicon-generator/SKILL.md_
- **Favicon report.** Report the files written, the config path, the head link block, and the regeneration command. _Sources: skills/favicon-generator/SKILL.md_

## Where it lives

The coding rules, the `pnpm validate` ending and its fallback, dependency pinning, and the Chrome UI check with the shared dev server all sit in the Coding section of AGENTS.md. None of this category's rules appear in docs/agents. The gate set, exit-code reading, CI as arbiter, PR check buckets, and criteria completion appear only in the author-ticket, arbitrate-review, review-pr, and supervise-issue skills, and every favicon rule lives only in skills/favicon-generator/SKILL.md.
