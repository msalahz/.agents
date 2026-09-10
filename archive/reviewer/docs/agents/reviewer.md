# Reviewer

What the `reviewer` skill reads about a project before it reviews a change. A project overrides this by adding its own `docs/agents/reviewer.md`.

## Checks

**Global default: `pnpm validate`.** Where the repository's manifest declares no `validate` script, whichever of `lint`, `typecheck`, and `test` it does declare stand in, each run and reported separately. Where it declares none of those, or has no manifest at all, no check runs and the report records the reason.

The default runs only where it needs no install: where the repository's dependencies are already installed, or where it declares none. Where a repository declares dependencies it has not installed, no check runs and the report says so. Installing is the caller's call, and a reviewer that installs has changed the machine it was asked only to read.

Where the package manager would install before running the script, reach the script another way, such as `npm run <script>` or the command the script wraps, and name on the report the command that actually ran.

A script name in the manifest is the only warrant for running a check. A lockfile entry proves a tool was wanted, not that it is installed, and a check invented from one fails for reasons the change did not cause. A command that is absent or not installed is `not run` with the reason, never a finding.

A project that wants something else lists it here, one command per line, each safe to run against a working tree without changing it:

```
pnpm validate
pnpm build
```

Commands that write to the tree, touch a remote, or need credentials do not belong here. A check that refreshes installed dependencies before it runs is fine, since package managers do that on their own. One that rewrites source, a snapshot, or a committed lockfile is not.

## Requirements

Where the agreed behaviour for a change is written down, as a path or a glob. The reviewer reads it to judge the requirements lens.

**Global default:** none. Without it the reviewer judges requirements from what the handoff states, and says so when the handoff states nothing.

## Principles

The document holding the project's durable engineering principles, if it keeps one. The reviewer reads it to judge the architecture lens.

**Global default:** none.

## Decisions and vocabulary

**Global default:** `CONTEXT.md` at the repository root for vocabulary, `docs/adr/` for recorded decisions. A project that keeps either somewhere else names the path here.
