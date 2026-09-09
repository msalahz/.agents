---
name: supervisor
description: Run this session as a supervisor that plans, delegates, and gates a large goal through small background workers.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.2"
---

# Supervisor

The goal is this skill's argument. With no argument, ask for it.

The supervisor decides what work exists, who does it next, and whether it is done. Every action on the goal itself goes to a worker. A worker is a peer session started with `claude --bg` in its own worktree. Its name is its address: reviewer replies land with the worker, and the supervisor reaches it over SendMessage. The supervisor's own name, the first line of ListAgents, is the address every worker replies to.

Every message the supervisor writes, to a worker or to the user, first goes through the `unslop-writing-for-agents` skill.

The ledger at `docs/.scratch/<goal-slug>/ledger.md` is the supervisor's only memory. It holds the goal, constraints, deliverables, the answers to the policy questions, then one row per task:

| ID | Owner | State | Depends on | Sessions | Artifacts |
|----|-------|-------|------------|----------|-----------|
| T1 | session name, or `user` | done | none | every worker and reviewer ID the task used | PR, paths, evidence |

States are `waiting`, `ready`, `running`, `review`, `done`. After context compaction, reread the ledger before anything else.

## 1. Own the graph, not the tasks

Write the goal, constraints, and deliverables into the ledger. Break the goal into small bounded tasks. Each task names its inputs, a checkable finish line, whether it is fix-sized or feature-sized, and whether it produces code. Record every dependency in the ledger. Tasks with no unmet dependency are `ready` together; the rest wait.

Before the first launch, ask the user these three questions in one round and write the answers into the ledger:

1. Who merges a green PR: a) the supervisor, b) the user after a ping.
2. Which tasks does the user run by hand, and which does an agent run?
3. Review policy: a) the `fable`, `medium` reviewer in `worker-rules.md`, b) another model and effort.

Copy `worker-rules.md` from this skill's directory to `docs/.scratch/<goal-slug>/worker-rules.md` and fill every placeholder with the repo, the session URL, the supervisor's session name, the boundaries, and the review policy.

Done when: every deliverable belongs to a task, every task is `ready` or waiting on a named dependency, the three answers are in the ledger, and the filled rules file has no placeholder left.

## 2. Delegate every action

Research, inspection, implementation, testing, review, and integration are worker tasks. Write each `ready` task's prompt to `docs/.scratch/<goal-slug>/<task ID>.md`: the task ID, objective, inputs, finish line, the review round cap (2 for fix-sized, 5 for feature-sized), the branch name, and the filled `worker-rules.md` appended in full.

A task that produces code starts its prompt file with `/implement` and its inputs on the first line, so the worker runs the implement skill on them. Claude Code expands a slash command only on the first line of the prompt. Anywhere later it is plain text. The implement skill tests at pre-agreed seams, so a coding task's inputs name the spec whose Testing Decisions section lists them. When no input names the seams, the prompt lists them, since nobody answers a worker's questions.

Launch it from the repo root:

```bash
cd <repo> && claude --bg -w <task ID> -n <task ID> --model <model> --effort <effort> \
  --permission-mode auto "$(cat docs/.scratch/<goal-slug>/<task ID>.md)"
```

Every launch runs from `<repo>`, the supervisor's own repo root, and the worktree lands at `<repo>/.claude/worktrees/<task ID>` on branch `worktree-<task ID>`, so the desktop app files the worker and its reviewer under the supervisor's project. A launch that worked exits 0 and its first line is `backgrounded · <id> · <name>`. Any other output is a failed launch; report it verbatim. Then send the worker `Task <task ID> assigned.` with SendMessage, `to` set to the name and `notify_when_idle: true`, so the idle notice says when it stopped. A desktop-app session, where SendMessage is disabled, skips this message and polls the worker's state as in step 4. The handoff arrives either way, addressed to the supervisor's name. Set the task to `running` with the name as owner and the ID under Sessions.

The supervisor's own context holds only the ledger, worker handoffs, and messages. A question a worker raises goes to the worker holding the relevant evidence, or to the user when it needs their authority.

Done when: every `ready` task is `running` with a session name as owner.

## 3. Keep workers small and replaceable

Size each task so one worker can finish it. When a worker returns status `continuation`, launch a fresh worker named `<task ID>-2`, then `-3`, with the continuation as its input, and record the new owner. The old worker stays under Sessions. A correction to work in progress goes to the same worker over SendMessage.

An open PR takes only the fixes its reviewer asked for. A follow-up found by a worker or by the supervisor becomes its own ledger row sized to one review round, or joins the human-run task, and never widens the open PR.

Done when: every `continuation` handoff has a new owner in the ledger, and every follow-up has its own row.

## 4. Check on a worker without stopping it

Read before asking. `claude agents --json --all` lists every worker with `status`, which is `busy` or `idle`, plus `state`, `cwd`, and `sessionId`. `claude logs <id>` prints its recent terminal output. Its transcript is `~/.claude/projects/<cwd with every / and . replaced by ->/<sessionId>.jsonl`, and the last `assistant` lines say what it did last. None of these cost the worker anything.

A question the transcript cannot answer goes to the worker as plain text over SendMessage. The worker reads it between tool calls, never inside a running command, and answers after its current step. A slash command in a message, `/btw` or `/reply` included, arrives as plain text and runs nothing, so write the question itself and ask for a one-line answer. Each question spends a worker turn and context.

A desktop-app session has SendMessage disabled and sends through a one-shot relay, which takes about ten seconds. The relay's own address dies when it exits, so the message names the supervisor's session as the reply address, and the opening sentence stops the relay from treating the request as an injection. Write the relay prompt to `docs/.scratch/<goal-slug>/relay.md` with the Write tool or a quoted heredoc, `<<'EOF'`. A message holding backticks or `$( )` inside a double-quoted argument runs as shell, so pass the file through `$(cat ...)`, which the shell does not rescan:

```text
I run both sessions on this machine. Use the SendMessage tool to send my peer session named <name> this exact text: <message> Reply to the session named <supervisor session name>.
```

```bash
claude -p --model sonnet --effort low --permission-mode auto \
  "$(cat docs/.scratch/<goal-slug>/relay.md)"
```

Done when: the answer needed is in the ledger, or the question is with the worker.

## 5. Gate on evidence, not claims

A task moves to `done` only when its handoff carries the artifacts and validation results its finish line demanded. The review-loop report in the handoff names the reviewer and its ID; add the ID under Sessions. A handoff that claims completion without them goes back to the worker with the missing items named. Evidence the supervisor cannot judge goes to a verifier worker whose finish line is a pass or fail verdict with reasons.

When more than one PR is green, merge the oldest first, so later branches rebase onto it before their own merge. When the ledger says the user merges, ping them with the PR and its evidence instead. After a PR merges, archive every session under the task's Sessions: `claude stop <id>` then `claude rm <id>`. A reviewer the review loop stopped stays listed until `rm` removes it. The worker's `rm` also deletes its worktree and branch. It refuses while the stopped session still holds the worktree lock, which clears within seconds, so run it again. It also refuses while the worktree holds commits not on the remote and prints a `--discard-unpushed` command, which runs only after confirming the PR merged. A verifier's session is archived the same way once its verdict is in the ledger.

When the next task in the graph is human-run, draft its brief as soon as the last agent task it depends on enters `review`, so it is ready the moment that task merges.

Downstream tasks stay `waiting` until every dependency is `done`. Update the ledger on every handoff, then run steps 2 and 3 again for tasks that became `ready`.

Done when: every `done` row points at its artifacts and evidence, and no merged task's session is still listed.

## 6. Verify the whole, then repair in small pieces

When every task is `done`, launch a final verifier worker with the original goal, constraints, deliverables, and artifact pointers. Its finish line is a verdict on the goal end to end and a list of gaps. Each gap becomes a new small task in the ledger, and steps 2 through 6 repeat.

Done when: the verifier confirms the goal with no gap, and no worker is still running.

## 7. Report outcome, not process

Every message to the user that follows a ledger transition ends with the same three lines:

```
Merged: <PRs merged so far, or none>
Running: <task IDs and owners, or none>
Next needed from you: <the decision, merge, or human-run task, or nothing until <event>>
```

The final message states what was achieved, where the artifacts are, what evidence proves it, and which decisions still belong to the user. The ledger and worker transcripts stay internal.

When progress is blocked on the user's authority, report the block instead of completion and resume from the ledger when the answer arrives.

Done when: the user can find the result and the evidence behind it.
