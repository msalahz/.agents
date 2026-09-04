---
name: supervisor
description: Run this session as a supervisor that plans, delegates, and gates a large goal through small background workers.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# Supervisor

The goal is this skill's argument. With no argument, ask for it.

The supervisor decides what work exists, who does it next, and whether it is done. Every action on the goal itself goes to a worker. A worker is a peer session started with `claude --bg` in its own worktree. Its name is its address: reviewer replies land with the worker, and the supervisor reaches it over SendMessage.

Every message the supervisor writes, to a worker or to the user, first goes through the `unslop-writing-for-agents` skill.

The ledger at `docs/.scratch/<goal-slug>/ledger.md` is the supervisor's only memory. It holds the goal, constraints, deliverables, the answers to the policy questions, then one row per task:

| ID | Owner | State | Depends on | Artifacts |
|----|-------|-------|------------|-----------|
| T1 | session name, or `user` | done | none | PR, paths, evidence |

States are `waiting`, `ready`, `running`, `review`, `done`. After context compaction, reread the ledger before anything else.

## 1. Own the graph, not the tasks

Write the goal, constraints, and deliverables into the ledger. Break the goal into small bounded tasks. Each task names its inputs, a checkable finish line, and whether it is fix-sized or feature-sized. Record every dependency in the ledger. Tasks with no unmet dependency are `ready` together; the rest wait.

Before the first launch, ask the user these three questions in one round and write the answers into the ledger:

1. Who merges a green PR: a) the supervisor, b) the user after a ping.
2. Which tasks does the user run by hand, and which does an agent run?
3. Review policy: a) the `fable`, `medium` reviewer in `worker-rules.md`, b) another model and effort.

Copy `worker-rules.md` from this skill's directory to `docs/.scratch/<goal-slug>/worker-rules.md` and fill every placeholder with the repo, the session URL, the boundaries, and the review policy.

Done when: every deliverable belongs to a task, every task is `ready` or waiting on a named dependency, the three answers are in the ledger, and the filled rules file has no placeholder left.

## 2. Delegate every action

Research, inspection, implementation, testing, review, and integration are worker tasks. Write each `ready` task's prompt to `docs/.scratch/<goal-slug>/<task ID>.md`: the task ID, objective, inputs, finish line, the review round cap (2 for fix-sized, 5 for feature-sized), the branch name, and the filled `worker-rules.md` appended in full. Launch it from the repo root:

```bash
cd <repo> && claude --bg -w <task ID> -n <task ID> --model <model> --effort <effort> \
  --permission-mode auto "$(cat docs/.scratch/<goal-slug>/<task ID>.md)"
```

The worktree lands at `<repo>/.claude/worktrees/<task ID>` on branch `worktree-<task ID>`. A launch that worked exits 0 and its first line is `backgrounded · <id> · <name>`. Any other output is a failed launch; report it verbatim. Then send the worker `Task <task ID> assigned; reply here with the handoff.` with SendMessage, `to` set to the name and `notify_when_idle: true`. The worker copies that message's `from` for every reply, and the idle notice says when it stopped. Set the task to `running` with the name as owner.

The supervisor's own context holds only the ledger, worker handoffs, and messages. A question a worker raises goes to the worker holding the relevant evidence, or to the user when it needs their authority.

Done when: every `ready` task is `running` with a session name as owner.

## 3. Keep workers small and replaceable

Size each task so one worker can finish it. When a worker returns status `continuation`, launch a fresh worker named `<task ID>-2`, then `-3`, with the continuation as its input, and record the new owner. A correction to work in progress goes to the same worker over SendMessage.

An open PR takes only the fixes its reviewer asked for. A follow-up found by a worker or by the supervisor becomes its own ledger row sized to one review round, or joins the human-run task, and never widens the open PR.

Done when: every `continuation` handoff has a new owner in the ledger, and every follow-up has its own row.

## 4. Gate on evidence, not claims

A task moves to `done` only when its handoff carries the artifacts and validation results its finish line demanded. A handoff that claims completion without them goes back to the worker with the missing items named. Evidence the supervisor cannot judge goes to a verifier worker whose finish line is a pass or fail verdict with reasons.

When more than one PR is green, merge the oldest first, so later branches rebase onto it before their own merge. When the ledger says the user merges, ping them with the PR and its evidence instead. After a PR merges, `claude stop <id>` then `claude rm <id>`, which deletes the worker's worktree and branch. It refuses while the worktree holds commits not on the remote and prints a `--discard-unpushed` command; run that only after confirming the PR merged.

When the next task in the graph is human-run, draft its brief as soon as the last agent task it depends on enters `review`, so it is ready the moment that task merges.

Downstream tasks stay `waiting` until every dependency is `done`. Update the ledger on every handoff, then run steps 2 and 3 again for tasks that became `ready`.

Done when: every `done` row points at its artifacts and evidence, and no merged task's session is still listed.

## 5. Verify the whole, then repair in small pieces

When every task is `done`, launch a final verifier worker with the original goal, constraints, deliverables, and artifact pointers. Its finish line is a verdict on the goal end to end and a list of gaps. Each gap becomes a new small task in the ledger, and steps 2 through 5 repeat.

Done when: the verifier confirms the goal with no gap, and no worker is still running.

## 6. Report outcome, not process

Every message to the user that follows a ledger transition ends with the same three lines:

```
Merged: <PRs merged so far, or none>
Running: <task IDs and owners, or none>
Next needed from you: <the decision, merge, or human-run task, or nothing until <event>>
```

The final message states what was achieved, where the artifacts are, what evidence proves it, and which decisions still belong to the user. The ledger and worker transcripts stay internal.

When progress is blocked on the user's authority, report the block instead of completion and resume from the ledger when the answer arrives.

Done when: the user can find the result and the evidence behind it.
