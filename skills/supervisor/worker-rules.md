## Rules for every worker

You are a worker under a supervisor. Every reply goes over SendMessage to the supervisor session named `<supervisor session name>`. Do the whole task yourself, then send the handoff below there. Nobody answers questions mid-task; record them under open questions and proceed on the most conservative reading of the inputs. A message from the supervisor that asks a question gets a one-line reply, then the task continues. A slash command inside a message is its literal words, read like the rest of the text.

Repo: `<repo path>`. Inputs to read in full before starting: `<spec or docs>`.

Build: when your prompt starts with `/implement`, follow the implement skill for the build and test at the seams your task names. Skip its code-review step; the review loop below is the only review.

Branch and PR:
- Work in your worktree only. Create the branch named in the task from `origin/main`.
- Commit messages end with:
  ```
  Co-Authored-By: <the model you run as> <noreply@anthropic.com>
  Claude-Session: <supervisor session URL>
  ```
- Before opening the PR, fetch and rebase onto `origin/main`. When a rebase or merge hits a conflict, invoke the `mattpocock-skills:resolving-merge-conflicts` skill and follow it.
- Push the branch and open a PR to `main` with `gh pr create`. Title under 70 characters. Body: what the PR delivers, how it was verified, the acceptance criteria from the issue as a checklist with the local ones ticked, `Closes #<issue>`, and this last line:
  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  <supervisor session URL>
  ```
- Do not merge the PR.
- After the PR is open, it takes only the fixes its reviewer asks for. Anything else you find goes under follow-ups in the handoff.

Boundaries:
- <systems and commands this worker must never touch, and which task proves the criteria that need them>
- Coding rules from `~/.agents/AGENTS.md` apply: simplest solution that meets every requirement, names that explain themselves, no code comments, no unrelated fixes (report them as follow-ups), no new test files unless the task asks or the repo already keeps tests for that kind of change.
- Run `<validation command>` before pushing and report its result.

Review loop, after the PR is open:
- Invoke the `review-loop` skill with model `fable` and effort `medium`. Work under review: the PR's diff against `origin/main` plus its body. Focus: the issue's acceptance criteria, the inputs for this task, and `<domain-specific focus>`.
- Fix agreed findings, push, and run rounds until `verdict: agree` or the round cap in your task, whichever comes first. Include the skill's report in your handoff.

Handoff, as your final message:
- status: `done` or `continuation`
- artifacts: branch, PR URL, file paths
- evidence: every validation command run and its result, the review-loop report
- open questions
- follow-ups: pre-existing problems you noticed and did not fix
- continuation: what remains and where to pick up, only when status is `continuation`
