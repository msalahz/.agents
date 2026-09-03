---
name: review-loop
description: Run a review loop, a peer session reviewing work while this session fixes the findings, until both agree. Use when the user asks for a review loop, or for a peer session to review work until agreed, with Claude or Codex as the reviewer.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Review loop

This session is the author. A peer session is the reviewer: a Claude session started with `claude --bg`, or a Codex thread started with `codex_peer.py` from the `spin-peer-codex-session` skill. A round is one message from the author and the reviewer's reply of findings ending in a verdict.

## 1. Collect the request

Collect from the request: the work under review (paths, a branch or diff, a spec, a plan), what the review should focus on, the reviewer (`claude` or `codex`), model, and effort. Defaults: reviewer `claude`; with `claude`, model `opus` and effort `high`; with `codex`, the model and effort in `~/.codex/config.toml`. Any value the user names replaces its default.

Done when: work, focus, reviewer, model, and effort are recorded.

## 2. Launch the reviewer

Fill the work and focus into this prompt. The first line is the reply rule; pick it by reviewer.

```
<reply rule>

You are the reviewer in a review loop. The author session messages you each round.

Work under review: <work>
Focus: <focus>

Each round, read the work as it is on disk now, then reply with one finding per line in the form `<high|medium|low> <fix|defer|ignore> <file:line or location> <what is wrong and what would fix it>`, ordered by risk. When the author pushes back on a finding, withdraw it or say why it stands. End every reply with `verdict: agree` when no finding you recommend fixing remains, otherwise `verdict: findings`.
```

Reply rule for `claude`: Reply with SendMessage, copying the message's `from` attribute as your `to`.
Reply rule for `codex`: Each message you receive is one round, and your answer to it is the reply.

The name is `review-<slug of the work>`. Launch from the directory holding the work.

With `claude`:

```bash
cd <dir> && claude --bg -n "review-<slug>" --model <model> --effort <effort> \
  --permission-mode auto "<prompt>"
```

The launch prints the session ID. The name then appears in ListAgents (or `claude agents --json`). A missing name means the launch failed; report its output verbatim and stop.

With `codex`, run as a background command, since `new` blocks until the first turn ends:

```bash
python3 ~/.claude/skills/spin-peer-codex-session/scripts/codex_peer.py new \
  --name "review-<slug>" --cwd "<dir>" --model <model> --effort <effort> \
  --sandbox read-only --approval never "<prompt>"
```

Omit `--model` and `--effort` when the user named none. The output opens with a `thread_id` line; record it. The first turn is round 1, so the output's reply is the round 1 reply. Exit 2 means the turn is still running; handle it as in step 3. Any other non-zero exit is a failed launch; report its output verbatim and stop.

Done when: the session ID or thread ID is recorded, and with `claude` the name is listed.

## 3. Run the rounds

A round is one message to the reviewer. With `claude`, round 1 asks for the first review. With `codex`, the launch prompt was round 1, so start from its reply.

With `claude`, send it with SendMessage and `notify_when_idle: true`. An idle notice with no reply means the reviewer stopped.

With `codex`, send it as a background command:

```bash
python3 ~/.claude/skills/spin-peer-codex-session/scripts/codex_peer.py send <thread_id> "<message>"
```

Exit 0 prints the reply. Exit 2 means the turn outlived the timeout and is still running; poll `codex_peer.py read <thread_id>` until it shows the turn ended, and take its message as the reply. Exit 1 means the reviewer stopped.

On each reply:

- Fix every `fix` finding the author agrees with.
- Push back, with a reason, on every finding the author disagrees with.
- Record `defer` and `ignore` findings for the report.

The next round carries, per finding from the last reply, what changed on disk or the reason the author disagrees.

When the reviewer stopped, resend the round once; after a second stop, stop and report the failure to the user.

The loop ends on a reply ending `verdict: agree` with no author push-back outstanding, or after 5 rounds without agreement. The open findings at the cap go to the user as disagreements.

Done when: the reviewer agreed, or the round cap was hit and every open finding is listed.

## 4. Hand to the user

Report in this format:

Review loop: <work>. Reviewer <name> (<id>), <claude | codex>, <model>, <effort>. <n> rounds, <agreed | round cap hit>.
Fixed: one line per finding fixed.
Deferred: one line per finding deferred, with the reason.
Disagreed: one line per open finding, with the author's and the reviewer's position.
Please review the agreed result.

Done when: the report is delivered.
