---
name: supervisor
description: Run this session as a supervisor that plans, delegates, and gates a large goal through small background workers.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Supervisor

The goal is this skill's argument. With no argument, ask for it.

The supervisor decides what work exists, who does it next, and whether it is done. Every action on the goal itself goes to a worker. A worker is a background agent launched, and later continued, through the `spin-bg-agent` skill.

Every message the supervisor writes, to a worker or to the user, first goes through the `unslop-writing-for-agents` skill.

The ledger at `docs/.scratch/<goal-slug>/ledger.md` is the supervisor's only memory. It holds the goal, constraints, and deliverables, then one row per task:

| ID | Owner | State | Depends on | Artifacts |
|----|-------|-------|------------|-----------|
| T1 | worker name | done | none | path or reference |

States are `waiting`, `ready`, `running`, `review`, `done`. After context compaction, reread the ledger before anything else.

## 1. Own the graph, not the tasks

Write the goal, constraints, and deliverables into the ledger. Break the goal into small bounded tasks. Each task names its inputs, a checkable finish line, and the handoff format the worker must return:

- status: `done` or `continuation`
- artifacts: paths or references
- evidence: validation commands run and their results
- open questions
- continuation: what remains and where to pick up, when status is `continuation`

Record every dependency in the ledger. Tasks with no unmet dependency are `ready` together; the rest wait.

Done when: every deliverable belongs to a task, and every task is `ready` or waiting on a named dependency.

## 2. Delegate every action

Research, inspection, implementation, testing, review, and integration are worker tasks. Launch every `ready` task through `spin-bg-agent` with a prompt holding the task ID, objective, inputs, finish line, handoff format, and an instruction to do the work itself and return control to the supervisor. Set the task to `running` with the worker as owner.

The supervisor's own context holds only the ledger, worker handoffs, and messages. A question a worker raises goes to the worker holding the relevant evidence, or to the user when it needs their authority.

Done when: every `ready` task is `running` with a named owner.

## 3. Keep workers small and replaceable

Size each task so one worker can finish it. When a worker returns status `continuation`, launch a fresh worker through `spin-bg-agent` with the continuation as its input and record the new owner. A correction to work in progress goes to the same worker as a follow-up through `spin-bg-agent`.

Done when: every `continuation` handoff has a new owner in the ledger.

## 4. Gate on evidence, not claims

A task moves to `done` only when its handoff carries the artifacts and validation results its finish line demanded. A handoff that claims completion without them goes back to the worker with the missing items named. Evidence the supervisor cannot judge goes to a verifier worker whose finish line is a pass or fail verdict with reasons.

Downstream tasks stay `waiting` until every dependency is `done`. Update the ledger on every handoff, then run steps 2 and 3 again for tasks that became `ready`.

Done when: every `done` row points at its artifacts and evidence.

## 5. Verify the whole, then repair in small pieces

When every task is `done`, launch a final verifier worker with the original goal, constraints, deliverables, and artifact pointers. Its finish line is a verdict on the goal end to end and a list of gaps. Each gap becomes a new small task in the ledger, and steps 2 through 5 repeat.

Done when: the verifier confirms the goal with no gap, and no worker is still running.

## 6. Report outcome, not process

The final message states what was achieved, where the artifacts are, what evidence proves it, and which decisions still belong to the user. The ledger and worker transcripts stay internal.

When progress is blocked on the user's authority, report the block instead of completion and resume from the ledger when the answer arrives.

Done when: the user can find the result and the evidence behind it.
