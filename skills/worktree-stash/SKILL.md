---
name: worktree-stash
description: Work a code task inside a git worktree, then stash every change under a named stash and report the name. Use when the user asks to work in a worktree or to hand changes back as a stash.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.4.0"
---

# Worktree stash

Enter a worktree with `EnterWorktree` and make every change for the task there.

Name the stash after the ticket the task came from, prefixed by the feature that owns it: a ticket at `docs/.scratch/<feature>/issues/<NN>-<slug>.md` gives the name `<feature>/<NN>-<slug>`. Every feature numbers its tickets from `01`, so the prefix is what keeps two `02-` stashes apart, and `git stash list` groups a feature's stashes together. A task that came without a ticket takes a slug of the task itself.

Read `git stash list` before stashing. When the name is already taken, add the next free `-2`, `-3` so each run of the same ticket keeps its own name.

When the task is done, run `git stash push -u -m "<name>"` inside the worktree, then leave it with `ExitWorktree` `action: "remove"`.

Report the name and its `stash@{N}` line from `git stash list`; the stash is visible from the main checkout.
