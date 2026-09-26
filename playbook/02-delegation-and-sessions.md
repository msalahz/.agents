# Delegation and sessions

Splitting work and launching subagents and peer sessions; coordinator and supervisor roles; briefs, handoffs, work logs, report lines; session naming, phases, idle handling, and cleanup.

## Patterns

- **Brief.** Shape every instruction written for a subagent, peer session, or human as a brief. _Sources: docs/agents/briefs.md_

### Roles and flows

- **Supervised issue hierarchy.** Run `supervisor-<parent>` over `author-<n>` sessions, each launching a read-only `reviewer-<n>`, and add `arbiter-<n>` only after 3 unresolved rounds. _Sources: README.md_
- **Operative.** Launch each coordinator Operative as a peer session through the `spin-peer-session` skill. _Sources: skills/coordinator/SKILL.md_
- **Managed subagent.** Launch a background subagent with the Agent tool; it reports through a task notification and takes follow-ups over SendMessage. _Sources: skills/spin-bg-agent/SKILL.md_
- **Peer session.** Start an independent session with `claude --bg`; it registers as a peer, keeps its own context and lifecycle, and reports to no parent. _Sources: skills/spin-peer-session/SKILL.md_
- **Reviewer session.** Run `reviewer-<n>` inside the PR's worktree, report over SendMessage, and wait for re-review requests, up to three rounds. _Sources: skills/review-pr/SKILL.md_
- **Three default phases.** Split an author's work into `implement` (steps 1-3 plus commits), `pr` (browser checks, push, PR, report), and `review` (steps 5-6). _Sources: skills/supervise-issue/SKILL.md_
- **Phase line.** When the launch prompt has `Phase <phase>: <steps>. Run only these.`, run only those steps, write the handoff file, message the supervisor, and stop; with no phase line, run every step. _Sources: skills/author-ticket/SKILL.md_
- **Same name across phases.** Launch each phase as a fresh session under the same name `author-<n>` so the reviewer still reaches it. _Sources: skills/supervise-issue/SKILL.md_

### Launch and naming

- **Session naming.** Name sessions `<role>-<n>` and add the lowest free number suffix on collision, so SendMessage reaches a session by name alone. _Sources: docs/agents/delegation.md, skills/review-loop/SKILL.md_
- **Exact role names.** Use exactly `author-<n>`, `reviewer-<n>`, and `arbiter-<n>`; the supervisor sets `author-<n>` at launch and the arbiter runs from the PR's worktree. _Sources: skills/supervise-issue/SKILL.md, skills/author-ticket/SKILL.md, skills/arbitrate-review/SKILL.md_
- **Review-loop reviewer name.** Name the review-loop reviewer `review-<author>`, taking this session's name from ListAgents' first line. _Sources: skills/review-loop/SKILL.md_
- **Wave launch recipe.** For each wave ticket, fetch, add a worktree on branch `<n>-<slug>` from `origin/<default>`, launch `claude --bg --name author-<n> --model opus --effort <effort> --permission-mode auto` running `/author-ticket`, and set the board to In progress. _Sources: skills/supervise-issue/SKILL.md, README.md_
- **Author prompt lines.** Put `/author-ticket <n> <n>-<slug> <supervisor-name>`, the phase line, and the handoff block on separate lines of the author prompt. _Sources: skills/supervise-issue/SKILL.md_
- **Peer launch command.** Launch a peer with `cd <dir> && claude --bg -n "<name>" --model <model> --effort <level> --permission-mode auto "<prompt>"`. _Sources: skills/spin-peer-session/SKILL.md_
- **Newest session by name and cwd.** Filter `claude agents --json --all` to background sessions by name and optional normalised cwd, and print the newest `sessionId`. _Sources: skills/supervise-issue/scripts/session-uuid.sh_

### Report lines

- **First-line dispatch.** Have the supervisor match each worker's fixed first line (`PR #<pr> opened for #<n>`, `approved ... after round <k>`, `rebased and approved`, `unresolved ... after 3 rounds`, `arbitrated`) to board changes, merges, and launches. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **Supervisor hears only fixed lines.** Let the author run the review loop itself so the supervisor hears only fixed report lines. _Sources: skills/supervise-issue/SKILL.md_
- **PR-opened line.** Report to the supervisor with first line `PR #<pr> opened for #<n>`, then the URL and any human-only criteria. _Sources: skills/author-ticket/SKILL.md_
- **Final review lines.** Send one of `PR #<pr> approved for #<n> after round <k>`, `PR #<pr> rebased and approved`, or `PR #<pr> unresolved for #<n> after 3 rounds`, then the detail. _Sources: skills/author-ticket/SKILL.md_
- **Arbitration line.** Open the arbiter report with `PR #<pr> arbitrated for #<n>`, then one line per finding with decision, reason, and the applying commit or resulting follow-up. _Sources: skills/arbitrate-review/SKILL.md_
- **Handoff message lines.** After writing a handoff, message the supervisor with `Handoff written for #<n>` on the first line and the path on the second, then stop. _Sources: skills/supervise-issue/SKILL.md_
- **Report tail headings.** End a done report with `Blocked on me` (every human step, listed only there), `Changed` (per-criterion status, files, validation exit code), and `Found` (review outcome and follow-ups). _Sources: docs/agents/delegation.md_
- **Operative done report.** Put the log path, review-loop's report, and the validation exit code in an Operative's done report. _Sources: skills/coordinator/SKILL.md_
- **Coordinator launch report.** Give each Operative's model, effort, reason for the choice, log path, and whether it runs review-loop. _Sources: skills/coordinator/SKILL.md_
- **Subagent one-line report.** Report `Subagent: <name> — type: <agent type> — <model>, <effort>, agent prompt: <prompt>`, with `default` for unset values. _Sources: skills/spin-bg-agent/SKILL.md_
- **Peer session one-line report.** Report `Session Title: <name> — ID: <id> — <model>, <effort>, <permission mode> permission mode, agent prompt: <prompt>`, with `default` for unset values and the short ID. _Sources: skills/spin-peer-session/SKILL.md_

### Handoffs, logs, and state

- **Context-limit handoff.** Near 110k tokens, write a handoff of at most 100 lines with sections done, changed, verified, machine state, next steps, gotchas, and follow-ups, send the parent the path, and stop. _Sources: docs/agents/delegation.md_
- **Handoff block in every prompt.** Put a fixed handoff block naming an absolute handoff file path per role in every supervisor launch prompt. _Sources: skills/supervise-issue/SKILL.md_
- **Handoff file naming.** Name handoff files `handoff-<n>.md` for the author, `handoff-<n>-reviewer.md` for the reviewer, and `handoff-<n>-arbiter.md` for the arbiter. _Sources: skills/supervise-issue/SKILL.md_
- **Successor launch.** On a handoff, read the file, stop the sender, and relaunch under the same name with a skill line, phase line, `Read <file> first...`, and the handoff block. _Sources: skills/supervise-issue/SKILL.md_
- **Operative work log path.** Name the work log `docs/.scratch/<feature-slug>/operatives/<operative-name>.md` in the target repo in every Operative prompt. _Sources: skills/coordinator/SKILL.md_
- **Work log entry.** On finishing a piece, append what is done, files changed, validation exit code, review-loop outcome, and follow-ups to the work log. _Sources: skills/coordinator/SKILL.md_
- **Resumable state file.** Keep supervisor state current at `~/.agents/.scratch/<repo>-issue-<n>/state.md` as a table of ticket, worktree, branch, phase, author ids per phase, reviewer id, PR, and status, plus launch and cleanup recipes, so a resumed supervisor carries on from it. _Sources: README.md, skills/supervise-issue/SKILL.md_

## Strategies

- **Launch message as sole source.** Put both session names and the author's unresolved report verbatim in the arbiter's launch message, since nothing about the dispute exists on GitHub. _Sources: skills/arbitrate-review/SKILL.md_
- **Default model and effort.** Default launches to `opus` at `medium`, and use `high` for hard design, scripts, or work touching more than one domain. _Sources: docs/agents/delegation.md, skills/coordinator/SKILL.md, skills/supervise-issue/SKILL.md_
- **Reviewer model.** Launch a reviewer on `fable` at `medium` or `high`, else `opus` at `medium` or `high`. _Sources: docs/agents/delegation.md_
- **Depth via effort level.** Set depth with the effort level, because brief wording does not change it. _Sources: docs/agents/briefs.md_
- **Agent type by effort.** Use agent type `bg-<effort>` when the user named an effort, otherwise `general-purpose`. _Sources: skills/spin-bg-agent/SKILL.md_
- **Relay or decide subagent questions.** Relay a subagent's question to the user when present; when the user is away, decide and tell the subagent the decision and reason. _Sources: docs/agents/delegation.md_
- **Ask and keep working.** As a subagent, send a question to the parent and keep working on what does not depend on it, stopping only when everything left is gated. _Sources: docs/agents/delegation.md_
- **No polling.** Take only author messages and idle notices as supervisor inputs, because CronCreate is refused. _Sources: skills/supervise-issue/SKILL.md_

### Splitting and phasing

- **Waves.** Launch as a wave every agent ticket whose blockers have all merged. _Sources: README.md, skills/supervise-issue/SKILL.md_
- **Split by the breaking-work-down rules.** Break a coordinator task into pieces by the Breaking-work-down rules in `delegation.md`, one Operative per piece. _Sources: skills/coordinator/SKILL.md_
- **Phase tickets by bound.** Break each ticket into phases by the Breaking-work-down rules and size every launch against that bound. _Sources: skills/supervise-issue/SKILL.md_
- **Isolate screenshot-heavy work.** Give screenshot-heavy checks their own piece or phase, such as the standalone `pr` phase, because images fill context fast. _Sources: docs/agents/delegation.md, skills/supervise-issue/SKILL.md_
- **Merge small phases.** Merge two phases of a small ticket, as `implement+pr`, when one session fits the work in the same bound. _Sources: skills/supervise-issue/SKILL.md_
- **Same phase or next phase.** Continue the same phase after a context-bound handoff, and move to the next planned phase otherwise. _Sources: skills/supervise-issue/SKILL.md_
- **Expand, migrate, contract.** Sequence a wide refactor as expand, migrate in batches, then contract. _Sources: docs/agents/delegation.md_

## Practices

### Before starting

- **Read the briefs doc first.** Read `~/.agents/docs/agents/briefs.md` before writing a brief for a subagent, peer session, or human. _Sources: AGENTS.md_
- **Read the delegation doc first.** Read `~/.agents/docs/agents/delegation.md` before splitting work or launching a subagent or peer session. _Sources: AGENTS.md_
- **Subagent reads its section.** As a subagent or background session, read the "Running as a subagent" section of `delegation.md` before the first tool call. _Sources: AGENTS.md_
- **Read the handoff first.** When the brief or launch prompt names a handoff file, read it before anything else and skip what it settles. _Sources: docs/agents/delegation.md, skills/author-ticket/SKILL.md_
- **Skill steps stay local.** Run the running skill's steps in this session unless the skill says to delegate them. _Sources: docs/agents/delegation.md_
- **Required skills resolve by path.** In preflight, check that skills an author reads by path, such as implement and resolving-merge-conflicts, resolve. _Sources: skills/supervise-issue/SKILL.md_

### Briefs

- **Polish every brief.** Run each brief, Operative message, or launch prompt through `unslop-writing-for-agents` and apply every fix before sending. _Sources: docs/agents/briefs.md, skills/coordinator/SKILL.md, skills/spin-bg-agent/SKILL.md, skills/spin-peer-session/SKILL.md_
- **State the finish line.** Say what done looks like and when to stop asking. _Sources: docs/agents/briefs.md_
- **Name the skills.** Name the skills the reader should use, since a subagent inherits none. _Sources: docs/agents/briefs.md_
- **Answer directly.** Write "Answer directly" in a brief that asks a simple question. _Sources: docs/agents/briefs.md_
- **Ask for reasons.** Ask for reasons in the reply, in the form "Explain in three sentences why you chose this". _Sources: docs/agents/briefs.md_
- **Pass visuals as files.** Pass a chart, screenshot, or diagram as the file itself. _Sources: docs/agents/briefs.md_
- **Name patterns to avoid in design briefs.** Name concrete patterns to avoid, such as "no cream backgrounds, no pill-shaped buttons", because "avoid a generic look" says nothing. _Sources: docs/agents/briefs.md_
- **Pass the reviewer handoff verbatim.** Append the reviewer copy of the handoff block verbatim on its own line after the `/review-pr` command. _Sources: skills/author-ticket/SKILL.md_

### Launching

- **Context-sized pieces.** Size each piece to finish well inside a 140k-token context. _Sources: docs/agents/delegation.md_
- **One worktree and session pair per sub-issue.** Give every sub-issue its own worktree, author session, and reviewer session. _Sources: README.md_
- **State launch parameters.** State model, effort, and the reason at every launch. _Sources: docs/agents/delegation.md_
- **Collect launch options with defaults.** Require the instructions and take any named short name, model, effort, worktree, permission mode, and directory, defaulting the name to one derived from the task, a peer's permission mode to `auto` and directory to the current one, and everything else to session or CLI defaults. _Sources: skills/spin-bg-agent/SKILL.md, skills/spin-peer-session/SKILL.md_
- **Pass only named options.** Pass model, effort, or a worktree only when the user named it. _Sources: skills/spin-bg-agent/SKILL.md, skills/spin-peer-session/SKILL.md_
- **Confirm registration.** Call a launch done when ListAgents or `claude agents --json` shows the name, otherwise report the launch output or error verbatim. _Sources: skills/spin-bg-agent/SKILL.md, skills/spin-peer-session/SKILL.md_
- **Omit the agent ID.** Leave the agent ID out of a subagent launch report. _Sources: skills/spin-bg-agent/SKILL.md_
- **File-changing pieces run review-loop.** Have a piece that changes files run `review-loop` before reporting done, focused on the finish line and introduced bugs. _Sources: skills/coordinator/SKILL.md_

### Session names and idle handling

- **Rename before launch.** Read this session's name from ListAgents' first line and, if it lacks the role prefix, ask the user to type `/rename <role>-<n>` (such as `coordinator-<name>` or `supervisor-<n>`) and wait for ListAgents to show it before the first launch, since a session cannot rename itself. _Sources: docs/agents/delegation.md, skills/coordinator/SKILL.md, skills/supervise-issue/SKILL.md_
- **Record your own name for workers.** Run ListAgents once and record the session name that goes to every author. _Sources: skills/supervise-issue/SKILL.md_
- **Address by name.** Send to a session by name over SendMessage and tell workers to reply by name, because a `from` address is a process socket that goes stale; on failure use the ListAgents row whose name starts with the role, such as `supervisor` or `author-<n>`. _Sources: docs/agents/delegation.md, skills/review-loop/SKILL.md, skills/arbitrate-review/SKILL.md, skills/author-ticket/SKILL.md, skills/review-pr/SKILL.md_
- **Subscribe to idle.** Record the author's short id and phase, then send `author-<n>` a SendMessage with `notify_when_idle: true` and no message. _Sources: skills/supervise-issue/SKILL.md_
- **Ignore repeat idle notices.** Treat a repeated idle notice with the same timestamp, or one saying the author waits on its reviewer, as a no-op apart from renewing the subscription. _Sources: skills/supervise-issue/SKILL.md_
- **Nudge a stalled author.** For an idle author with no report and no reviewer, read `claude logs <id>` and message it on what is missing. _Sources: skills/supervise-issue/SKILL.md_
- **Resume by full id.** Resume an exited author with `claude --bg --resume $(scripts/session-uuid.sh ...)`, because the short id opens a picker and hangs. _Sources: skills/supervise-issue/SKILL.md_
- **Relaunch held-message peers.** When a cross-session notice says a message was held, relaunch the peer with `--permission-mode auto`. _Sources: skills/supervise-issue/SKILL.md_

### Working as a worker

- **Author flow.** Read the ticket, spec, ADRs, and prior art, implement through `implement`, run the repo's gates, and open the PR. _Sources: README.md_
- **No parent means decide.** With no parent session, decide yourself and record the decision and reason in the report. _Sources: docs/agents/delegation.md_
- **Sibling gaps go to the report.** Put a gap that belongs to a sibling piece in the report, not the diff. _Sources: docs/agents/delegation.md_
- **Fixed first line.** Open a report with the fixed first line the brief names. _Sources: docs/agents/delegation.md_
- **Unresolved report lists both positions.** Put each open finding on one line with both positions. _Sources: skills/author-ticket/SKILL.md_
- **Handoff at phase end too.** Write the handoff at the context bound and also when the phase is done and a later phase remains. _Sources: skills/supervise-issue/SKILL.md_
- **Handoffs beside state.** Keep handoff files beside the supervisor's state file. _Sources: skills/supervise-issue/SKILL.md_
- **Context-bound log entry.** At the context bound, append a final work log entry with next steps, send the log path, and stop. _Sources: skills/coordinator/SKILL.md_
- **Stop and wait after reporting.** After the report, or after the third verdict or `verdict: agree`, stop, wait for messages, and start nothing else. _Sources: skills/arbitrate-review/SKILL.md, skills/author-ticket/SKILL.md, skills/review-pr/SKILL.md_

### Orchestrating

- **Orchestrator role limits.** Limit an orchestrator to planning, launching, messaging, verifying, and cleaning up. _Sources: docs/agents/delegation.md_ _Conflicts with: Supervisor writes no code_
- **Supervisor writes no code.** Keep the supervisor to planning, launching author sessions per phase, watching reports, merging approved PRs, moving the project board, and handing human-only tickets back. _Sources: README.md, skills/supervise-issue/SKILL.md_ _Conflicts with: Orchestrator role limits_
- **Coordinator delegates every task.** Treat every file edit, command run, or investigation as a task and send it to an Operative; the coordinator only claims its name, launches, messages, relays results, and removes Operatives. _Sources: skills/coordinator/SKILL.md_
- **Self-check each action.** Check each coordinator action against the delegate-everything rule for the rest of the session. _Sources: skills/coordinator/SKILL.md_
- **Additions as follow-ups.** Send an addition to a running piece as a follow-up message. _Sources: docs/agents/delegation.md_
- **Persistent task list.** Keep a long run's task list in a file the run updates, such as `TASKS.md` or the skill's work log. _Sources: docs/agents/delegation.md_
- **Verify reports.** Check each done report against the piece's finish line, its log entry or handoff, a validation exit code of 0, and a closed review for file-changing pieces. _Sources: docs/agents/delegation.md, skills/coordinator/SKILL.md_
- **Gaps as the next message.** Send each gap back as the next message and verify again at the next done report. _Sources: docs/agents/delegation.md, skills/coordinator/SKILL.md_

### Cleanup

- **Relay then remove.** Relay the verified result to the user, then run `claude rm <id>` on each Operative. _Sources: skills/coordinator/SKILL.md_
- **Report rm refusal verbatim.** When `rm` refuses, such as over unpushed commits, leave the session and report its output verbatim. _Sources: skills/coordinator/SKILL.md_
- **Confirm cleanup.** Call close-out done when `claude agents --json --all` lists no Operative for the piece. _Sources: skills/coordinator/SKILL.md_
- **Stop the reviewer.** Stop the review-loop reviewer with `claude stop <id>`. _Sources: skills/review-loop/SKILL.md_
- **Stop before removing a worktree.** Run `claude stop` on the author, reviewer, and arbiter before removing the worktree, and keep `claude rm` for final cleanup. _Sources: skills/supervise-issue/SKILL.md_
- **Close on the user's word.** When the user says the parent is complete, `claude rm` every session, close the parent issue, and delete the state directory. _Sources: README.md, skills/supervise-issue/SKILL.md_

## Where it lives

AGENTS.md holds only the three read-first pointers. The brief rules, launch defaults, naming, addressing, subagent conduct, handoff and report shapes, and report verification live in `docs/agents/briefs.md` and `docs/agents/delegation.md`. Everything else, including the supervisor, author, reviewer, and arbiter flows, phases, idle handling, work logs, Operatives, launch recipes, one-line launch reports, and cleanup, appears only in the SKILL.md files of `supervise-issue`, `author-ticket`, `review-pr`, `arbitrate-review`, `review-loop`, `coordinator`, `spin-bg-agent`, and `spin-peer-session` and in supervise-issue's `session-uuid.sh`, with an overview in README.md.
