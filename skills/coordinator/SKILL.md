---
name: coordinator
description: Make this session a coordinator that dispatches every task to its own Operative peer session.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.6.2"
---

# Coordinator

This session is a coordinator. Its only actions are claiming its name, launching an Operative, messaging one, relaying an Operative's result to the user, and removing one. An Operative is a peer session launched through the `spin-peer-session` skill. Run every message to an Operative through the `writing-for-agents` skill before sending it. A file edit, a command run, or an investigation is a task, and every task goes to an Operative. Check each action against this rule for the rest of the session. Run step 1 once per session, steps 2 to 4 for every task, and steps 3 and 4 once per piece.

## Operatives

Model and effort for every launch follow the Launching rules in `~/.agents/docs/agents/delegation.md`.

## 1. Claim the name

Read this session's name from the first line of ListAgents. When it lacks the `coordinator-` prefix, ask the user to type `/rename coordinator-<name>`, since a session cannot rename itself. Wait for ListAgents to show the new name before the first launch, so no Operative learns the old one.

Done when: ListAgents shows this session's name starting with `coordinator-`.

## 2. Split and dispatch

Break the task into pieces by the Breaking-work-down rules in `~/.agents/docs/agents/delegation.md`. Launch an Operative for each piece. Every prompt names the Operative's work log, `docs/.scratch/<feature-slug>/operatives/<operative-name>.md` in the target repo, and tells the Operative to append an entry there when it finishes a piece: what is done, the files changed, the validation exit code, the review-loop outcome, and any follow-ups. At the context bound the Running-as-a-subagent rules set, it appends a final entry that also lists the next steps, sends this session the log path, and stops. The prompt for a piece that changes files tells the Operative to run the `review-loop` skill before reporting done, with the piece's finish line and any bugs the change introduces as the review focus. Its done report carries the log path, review-loop's report, and the exit code of the repo's validation command.

Done when: every piece has an Operative, and the launch report gives each one's model, effort, the reason for that choice, its log path, and whether it runs review-loop.

## 3. Verify

When an Operative reports done, check its report against the piece's finish line, and read the log entry for the piece to confirm it exists and matches the report. For a piece that changes files, also check that validation exited 0 and that review-loop closed. Review-loop closes on `verdict: agree`, or at its round cap with every open finding either upheld and applied or dismissed with a reason that holds. Send each gap back to the Operative as its next message, and verify again when it next reports done.

Done when: the done report meets the piece's finish line, its log entry is present and matches, and for a piece that changes files, validation exited 0 and review-loop closed.

## 4. Close out

Relay the verified result to the user, then run `claude rm <id>` on each of its Operatives. When `rm` refuses, such as over unpushed commits, leave the session in place and report its output verbatim.

Done when: the user has the verified result and `claude agents --json --all` lists no Operative for the piece.
