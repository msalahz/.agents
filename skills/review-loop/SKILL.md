---
name: review-loop
description: Run a review loop, a peer session reviewing work while this session fixes the findings, until both agree. Use when the user asks for a review loop, or for a peer session to review work until agreed.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.5.0"
---

# Review loop

This session is the author. A peer session started with `claude --bg` is the reviewer. A round is one message from the author and the reviewer's reply of findings ending in a verdict.

## 1. Collect the request

Collect from the request: the work under review (paths, a branch or diff, a spec, a plan), what the review should focus on, model, and effort. Defaults: model `opus` and effort `high`. Effort is one of `low`, `medium`, `high`, `xhigh`, or `max`. Any value the user names replaces its default.

Done when: work, focus, model, and effort are recorded.

## 2. Launch the reviewer

Fill the work and focus into this prompt.

```
Reply with SendMessage, copying the message's `from` attribute as your `to`.

You are the reviewer in a review loop. The author session messages you each round.

Work under review: <work>
Focus: <focus>

Each round, run the `reviewer` skill against the work as it is on disk now and reply with the report it returns, and nothing else.
```

The slug is the work's name in lowercase with hyphens: a path's basename, a branch name, or a spec title. A name already in ListAgents gets `-2`, `-3`, and so on. The prompt file below takes the same slug.

The prompt holds backticks, so write it literally, with the Write tool or a quoted heredoc (`<<'EOF'`), to `/tmp/review-<slug>-prompt.md` and pass it through `$(cat ...)`, which the shell does not rescan.

The directory is the repo root holding the work, or this session's working directory when the work is not inside one repo:

```bash
cd <dir> && claude --bg -n "review-<slug>" --model <model> --effort <effort> \
  --permission-mode auto "$(cat /tmp/review-<slug>-prompt.md)"
```

A launch that worked exits 0 and its first line starts with `backgrounded`. The session ID is the value between that line's two `·` separators, with colour codes stripped. A nonzero exit or any other first line is a failed launch; report the output verbatim and stop. The name appears in ListAgents (or `claude agents --json`) within a few seconds. When it has not appeared, carry on and address the session by ID.

Done when: the session ID is recorded.

## 3. Run the rounds

A round is one message to the reviewer, sent with SendMessage and `notify_when_idle: true`. Round 1 is `Round 1: review <work> as it is on disk now and reply with findings and a verdict.` An idle notice with no reply means the reviewer stopped.

Each reply is a `reviewer` report: a `scope:` line, one line per lens with its pass or fail, findings as `<lens> <high|medium|low> <fix|defer|ignore> <file:line or location> <what is wrong and what would fix it>`, one or more `checks:` lines, any `notes:` lines, and a closing `verdict:` line. A finding whose last field opens with `pre-existing:` names a defect the work did not cause.

On each reply:

- Fix every `fix` finding the author agrees with.
- Push back, with a reason, on every finding the author disagrees with.
- Record `defer` and `ignore` findings for the report.

Carry each finding's lens through to the report.

The next round carries, per finding from the last reply, what changed on disk or the reason the author disagrees.

When the reviewer stopped, resend the round once. A resend is the same round and does not count toward the cap. After a second stop, end the loop and report the failure to the user.

The loop ends on a reply ending `verdict: agree` with no author push-back outstanding, after 5 rounds without agreement, or on the second reviewer stop. The open findings at the cap or at a stop go to the user as disagreements.

Done when: the loop ended by agreement, round cap, or second stop, and every open finding is listed.

## 4. Hand to the user

Report in this format:

Review loop: <work>. Reviewer <name> (<id>), <model>, <effort>. <n> rounds, <agreed | round cap hit | reviewer stopped>.
Lenses: the five lens verdicts from the last reply.
Fixed: one line per finding fixed, with its lens.
Deferred: one line per finding deferred, with its lens and the reason.
Disagreed: one line per open finding, with its lens and the author's and the reviewer's position.
Please review the result.

Then stop the reviewer with `claude stop <id>` and delete the prompt file.

Done when: the report is delivered and the reviewer session is stopped.
