---
name: review-loop
description: Run a review loop, a peer session reviewing work while this session fixes the findings, until both agree. Use when the user asks for a review loop, or for a peer session to review work until agreed.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Review loop

This session is the author. A peer session launched with `spin-peer-claude-session` is the reviewer. A round is one message from the author and the reviewer's reply of findings ending in a verdict.

## 1. Collect the request

Collect from the request: the work under review (paths, a branch or diff, a spec, a plan), what the review should focus on, model, and effort. Defaults: model `opus`, effort `high`. Any model or effort the user names replaces its default.

Done when: work, focus, model, and effort are recorded.

## 2. Launch the reviewer

Invoke `spin-peer-claude-session` with name `review-<slug of the work>`, the model and effort from step 1, and this prompt with the work and focus filled in:

```
You are the reviewer in a review loop. The author session messages you each round; reply with SendMessage, copying the message's `from` attribute as your `to`.

Work under review: <work>
Focus: <focus>

Each round, read the work as it is on disk now, then reply with one finding per line in the form `<high|medium|low> <fix|defer|ignore> <file:line or location> <what is wrong and what would fix it>`, ordered by risk. When the author pushes back on a finding, withdraw it or say why it stands. End every reply with `verdict: agree` when no finding you recommend fixing remains, otherwise `verdict: findings`.
```

Done when: `spin-peer-claude-session` has delivered its one-line report.

## 3. Run the rounds

Every round is one SendMessage to the reviewer, sent with `notify_when_idle: true`; its text goes through `unslop-writing-for-agents` first. Round 1 asks for the first review.

On each reply:

- Fix every `fix` finding the author agrees with.
- Push back, with a reason, on every finding the author disagrees with.
- Record `defer` and `ignore` findings for the report.

The next round carries, per finding from the last reply, what changed on disk or the reason the author disagrees.

An idle notice with no reply means the reviewer stopped. Resend the round once; after a second silence, stop and report the failure to the user.

The loop ends on a reply ending `verdict: agree` with no author push-back outstanding, or after 5 rounds without agreement. The open findings at the cap go to the user as disagreements.

Done when: the reviewer agreed, or the round cap was hit and every open finding is listed.

## 4. Hand to the user

Report in this format:

Review loop: <work>. Reviewer <name> (<id>), <model>, <effort>. <n> rounds, <agreed | round cap hit>.
Fixed: one line per finding fixed.
Deferred: one line per finding deferred, with the reason.
Disagreed: one line per open finding, with the author's and the reviewer's position.
Please review the agreed result.

Done when: the report is delivered.
