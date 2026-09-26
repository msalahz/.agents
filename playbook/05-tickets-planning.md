# Tickets and planning

Issue tracker, specs, tickets, triage labels, board status, plan tables, and scoping work to acceptance criteria.

## Patterns

### Specs and tickets

- **Specs local, issues on GitHub.** Publish a spec to `docs/.scratch/<feature-slug>/spec.md` and a ticket with `gh issue create`, never a GitHub issue that holds a spec or a `docs/.scratch/.../issues/` file when a GitHub remote exists. _Sources: AGENTS.md, docs/agents/issue-tracker.md_
- **One feature per directory.** Keep each feature in `docs/.scratch/<feature-slug>/`, with the spec at `spec.md` and research notes beside it. _Sources: docs/agents/issue-tracker.md_
- **Spec header lines.** Track the spec's lifecycle in `Status:`, `Glossary:`, and `History:` lines, kept apart from issue triage labels. _Sources: docs/agents/issue-tracker.md_
- **Tickets header.** List the spec's issue numbers on a `Tickets:` line, parent first, or write `none yet`. _Sources: docs/agents/issue-tracker.md_
- **Parent issue.** Title the parent after the spec heading, open its body with `Spec:`, summarise in one paragraph, list tickets in dependency order, and label it `needs-triage`. _Sources: docs/agents/issue-tracker.md_
- **Parent section in tickets.** Follow a ticket's `Spec:` line with a `## Parent` section naming `#<parent>`. _Sources: docs/agents/issue-tracker.md_

### Wayfinding and the no-remote fallback

- **Wayfinding map.** Keep `docs/.scratch/<effort>/map.md` with Notes, Decisions-so-far, and Fog sections and an ordered list of child issues. _Sources: docs/agents/issue-tracker.md_
- **Wayfinder child ticket.** Open the body with `Part of docs/.scratch/<effort>/map.md`, label it `wayfinder:<type>` (research, prototype, grilling, or task), and add it to the map in work order. _Sources: docs/agents/issue-tracker.md_
- **No-remote tickets.** Without a GitHub remote, write one file per ticket at `docs/.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never one combined file. _Sources: docs/agents/issue-tracker.md_
- **No-remote ticket fields.** Put a `Status:` line with the role string near the top and a `## Comments` heading at the bottom for history. _Sources: docs/agents/issue-tracker.md_
- **No-remote wayfinding.** Give child files `Type:`, `Status:` (`claimed` or `resolved`), and `Blocked by: NN, NN` lines, and take the lowest-numbered open, unblocked, unclaimed file as the frontier. _Sources: docs/agents/issue-tracker.md_

### Triage and the board

- **Triage roles as labels.** Speak in the five roles `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`, and set each as the GitHub label string the mapping table gives. _Sources: AGENTS.md, docs/agents/issue-tracker.md, docs/agents/triage-labels.md_
- **Role meanings.** Read `needs-triage` as waiting on a maintainer, `needs-info` as waiting on the reporter, `ready-for-agent` as fully specified for an AFK agent, `ready-for-human` as needing a human to implement, and `wontfix` as declined. _Sources: docs/agents/triage-labels.md_
- **Board status columns.** Move issues on a project board through Backlog, Ready, In progress, In review, and Done, and fall back to labels when no project exists. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **PR-as-request flag.** Leave "PRs as a request surface" at `no` unless a repo sets it to `yes`, since `/triage` reads it. _Sources: docs/agents/issue-tracker.md_
- **gh command set.** Work issues with `gh` create, view with `--comments`, list with a `--json`/`--jq` projection, comment, edit labels, and close with a comment. _Sources: docs/agents/issue-tracker.md_
- **Plan table with confirmation.** Build a table of ticket, blockers, effort (`high` or `medium`), phases, and agent or human from each sub-issue's `## Blocked by`, labels, and spec path, post it on the parent, show it to the user with at most three a/b/c questions and a recommendation, and wait for confirmation. _Sources: README.md, skills/supervise-issue/SKILL.md_

## Strategies

- **Vertical slices.** Cut work into vertical slices that each demo alone and name the pieces that block them. _Sources: docs/agents/delegation.md_
- **Work the frontier.** Walk the ordered list, keep open issues, drop any with an open blocker or an assignee, and take the first survivor. _Sources: docs/agents/delegation.md, docs/agents/issue-tracker.md_
- **Siblings own adjacent work.** Leave everything outside the criteria to sibling tickets under the same parent, even when it sits next to your change. _Sources: skills/author-ticket/SKILL.md_
- **Human or agent.** Class `ready-for-human` tickets and tickets that need a remote environment as human work, and everything else as agent work. _Sources: skills/supervise-issue/SKILL.md_

## Practices

### Working a ticket

- **Read ticket, then spec.** Before changing anything, run `gh issue view <n> --comments` for scope, acceptance criteria, `## Blocked by`, the `Spec:` path, and the parent number, then read the spec sections the ticket names and the research notes beside the spec. _Sources: docs/agents/issue-tracker.md, skills/author-ticket/SKILL.md_
- **Number the criteria.** Finish reading only when the acceptance criteria are listed and numbered. _Sources: skills/author-ticket/SKILL.md_
- **Claim as first write.** Make `gh issue edit <n> --add-assignee @me` the session's first write. _Sources: docs/agents/issue-tracker.md_
- **Sibling gaps go in the PR body.** Record a gap that belongs to a sibling ticket in the PR body and keep it out of the diff. _Sources: skills/author-ticket/SKILL.md_
- **Resolve sequence.** Comment the answer, close the issue, then append a gist and link to the map's Decisions-so-far. _Sources: docs/agents/issue-tracker.md_
- **Scope equals acceptance criteria.** Scope each piece to exactly its acceptance criteria. _Sources: docs/agents/delegation.md, skills/author-ticket/SKILL.md_

### Supervising a parent

- **Read sub-issues via GraphQL.** Fetch sub-issues through the GraphQL `subIssues` connection with body, blockers, labels, and spec path. _Sources: skills/supervise-issue/SKILL.md_
- **Exact status names.** Match project Status names exactly, such as `"In progress"`. _Sources: skills/supervise-issue/SKILL.md_
- **Move human criteria only on yes.** Propose moving a human-only criterion to the human ticket with strikethrough and a "moved to #m" note, and move it only after the user says yes. _Sources: skills/supervise-issue/SKILL.md_
- **Confirm issue closed.** Set the board to Done and check that `Closes` closed the issue, closing it yourself if not. _Sources: skills/supervise-issue/SKILL.md_
- **Hand back human tickets.** When only human tickets remain, set them to Ready, comment on the parent with merged PRs, review rounds, follow-ups, and what the human tickets carry, and stop. _Sources: README.md, skills/supervise-issue/SKILL.md_

### Tracker and spec mechanics

- **Edit specs in place.** Version specs with the code and edit them in place as the design changes. _Sources: docs/agents/issue-tracker.md_
- **Spec backlink.** Start an issue made from a spec with `Spec: docs/.scratch/<feature-slug>/spec.md` and add its number to the spec's `Tickets:` line. _Sources: docs/agents/issue-tracker.md_
- **Heredoc bodies.** Pass multi-line `gh issue create` bodies through a heredoc. _Sources: docs/agents/issue-tracker.md_
- **Native sub-issues.** Nest each ticket under its parent through the `sub_issues` API with the ticket's database id. _Sources: docs/agents/issue-tracker.md_
- **Native blocking dependencies.** Add `blocked_by` edges through the API with the blocker's database id, not `#number` or `node_id`, and treat `issue_dependencies_summary.blocked_by` as the live gate. _Sources: docs/agents/issue-tracker.md_
- **Blocked-by fallback line.** Where dependencies are unavailable, put `Blocked by: #<n>, #<n>` at the top of the body and count the issue unblocked once every blocker is closed. _Sources: docs/agents/issue-tracker.md_
- **Resolve bare numbers.** Try `gh pr view 42` for a bare `#42` and fall back to `gh issue view 42`. _Sources: docs/agents/issue-tracker.md_
- **External PR filter.** When triaging PRs, keep only `authorAssociation` values `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, and `NONE`. _Sources: docs/agents/issue-tracker.md_
- **Customise the label column.** Edit the right-hand column of the triage mapping table to match the labels the repo uses. _Sources: docs/agents/triage-labels.md_

## Where it lives

AGENTS.md carries only the spec and issue homes and the five triage labels, and points to docs/agents/issue-tracker.md and docs/agents/triage-labels.md, which hold the tracker mechanics, wayfinding, no-remote fallback, and label mapping. Vertical slices, the frontier, and scoping to criteria sit in docs/agents/delegation.md. Reading and scoping a ticket appear only in skills/author-ticket/SKILL.md, and the plan table, board handling, human-or-agent split, and hand-back appear only in skills/supervise-issue/SKILL.md and its README.md entry.
