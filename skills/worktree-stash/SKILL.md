---
name: worktree-stash
description: Work a code task inside a git worktree, then stash every change under a named stash and report the name. Use when the user asks to work in a worktree or to hand changes back as a stash.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.5.0"
---

# Worktree stash

Enter a worktree with `EnterWorktree` and make every change for the task there.

Name the stash after the ticket the task came from. A GitHub issue gives `issue-<number>-<slug>`, slugging the issue title. A local-markdown ticket at `docs/.scratch/<feature>/issues/<NN>-<slug>.md` gives `<feature>/<NN>-<slug>`; every feature numbers its tickets from `01`, so the feature prefix is what keeps two `02-` stashes apart and groups a feature's stashes together in `git stash list`. A task that came without a ticket takes a slug of the task itself.

Read `git stash list` before stashing. When the name is already taken, add the next free `-2`, `-3` so each run of the same ticket keeps its own name.

When the task is done, run `git stash push -u -m "<name>"` inside the worktree, then leave it with `ExitWorktree` `action: "remove"`.

Report the name and its `stash@{N}` line from `git stash list`; the stash is visible from the main checkout.
