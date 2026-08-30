# Issue tracker: GitHub issues, local specs

**This is the global default for all repos.** A repo may override it by adding its own `docs/agents/issue-tracker.md` at its root, and the repo-local file always wins.

The two artefacts live in different places:

- **Specs stay in the repo** as markdown under `docs/.scratch/<feature-slug>/spec.md`. They are versioned alongside the code they describe and are edited in place as the design changes.
- **Issues live on GitHub.** Use the `gh` CLI, which infers the repo from `git remote -v` when run inside a clone.

Never create a GitHub issue to hold a spec, and never create a `docs/.scratch/.../issues/` file to hold a ticket. If the repo has no GitHub remote, use the fallback at the bottom of this file.

## Specs

- One feature per directory: `docs/.scratch/<feature-slug>/`, with the spec at `spec.md`.
- The spec's header lines carry its own state, for example `Status:`, `Glossary:`, and `History:`. These are the spec's lifecycle, separate from the triage labels that live on GitHub issues.
- A `Tickets:` header line lists the GitHub issue numbers cut from the spec, for example `Tickets: #14, #15, #16`, or `none yet` before any exist.
- Supporting research and requirements notes sit beside the spec in the same directory.

## Issues

- **Create**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies. Start the body with a `Spec: docs/.scratch/<feature-slug>/spec.md` line whenever the issue came from a spec, then add the issue number to that spec's `Tickets:` line.
- **Read**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Triage state is a GitHub label on the issue. See `triage-labels.md` for the role strings.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` in a repo's own `docs/agents/issue-tracker.md` if that repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` then keep only `authorAssociation` of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` (drop `OWNER`/`MEMBER`/`COLLABORATOR`).
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either. Resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

A spec goes to `docs/.scratch/<feature-slug>/spec.md`. A ticket goes to `gh issue create`.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`, then read the `Spec:` path from the body for the surrounding design.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a document, so it stays local; its **child tickets** are GitHub issues.

- **Map**: `docs/.scratch/<effort>/map.md`, holding the Notes / Decisions-so-far / Fog body and an ordered list of its child issue numbers.
- **Child ticket**: a GitHub issue whose body opens with `Part of docs/.scratch/<effort>/map.md`. Label it `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Add its number to the map's list in the order it should be worked. Once claimed, the issue is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies**, the canonical UI-visible representation. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _not_ the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by`, counting open blockers only, which is the live gate. Where dependencies aren't available, fall back to a `Blocked by: #<n>, #<n>` line at the top of the issue body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: walk the map's list in order, keep the issues still open (`gh issue list --state open`), drop any with an open blocker or an assignee; the first survivor wins.
- **Claim**: `gh issue edit <n> --add-assignee @me`, the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.

## Fallback: no GitHub remote

Use this only when the repo has no GitHub remote. Tickets then join the spec on disk.

- Tickets are one file per ticket at `docs/.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file.
- Triage state is a `Status:` line near the top of each ticket file, using the same role strings.
- Comments and conversation history append to the bottom of the file under a `## Comments` heading.
- "Publish to the issue tracker" creates the file; "fetch the relevant ticket" reads it at the referenced path.
- Wayfinding: child tickets are `docs/.scratch/<effort>/issues/NN-<slug>.md` with a `Type:` line and a `Status:` line (`claimed`/`resolved`); blocking is a `Blocked by: NN, NN` line near the top, unblocked when every listed file is `resolved`; the frontier is the open, unblocked, unclaimed file with the lowest number.
