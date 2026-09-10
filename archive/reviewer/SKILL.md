---
name: reviewer
description: Review a change against five lenses and return one report with a verdict per lens. Use when asked to review a change, or when a review loop needs a reviewer.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Reviewer

Judge a change against five lenses and return one report.

This session is read-only on the work under review. It reads, and it runs the checks a project declares. It writes no file, stages nothing, commits nothing, and pushes nothing. A declared check may refresh what the project installs before it runs; nothing else moves.

A person, an agent mid-task, and a review loop running this in a separate session all get the same procedure and the same report.

## 1. Collect the handoff

The handoff is what the caller supplies about the work:

- The reference to review, and the base to compare against.
- The agreed requirements, or a path to them.
- What the author deliberately left out.
- What is already known to be failing.
- On a later round, what moved since the last report, per finding.

Every part is optional. Resolve what is missing in the steps below.

Done when: what the caller supplied is recorded, and what is absent is named.

## 2. Resolve the review scope

Take the first of these that applies:

1. A reference the handoff supplied. Use it as given.
2. The branch's own commits and the uncommitted work, together, taking whichever of the two exists.

The branch's own commits are what `HEAD` holds that its base does not. Resolve the base from `git symbolic-ref --quiet --short refs/remotes/origin/HEAD`; when that prints nothing, try `origin/main` then `origin/master` with `git rev-parse --verify --quiet`. Compare `git merge-base HEAD <base>` against `HEAD`.

The uncommitted work is what `git diff HEAD --name-status` prints for tracked changes, staged or not, plus what `git ls-files --others --exclude-standard` prints for files git does not track yet.

A branch waiting on a pull request usually holds both. Review the union, and let the `scope:` line name each part that is present.

When neither exists, report that there is nothing to review and stop.

Done when: the scope and its base are resolved and ready for the report's first line.

## 3. Load the review configuration

Read `docs/agents/reviewer.md` in the repository under review, or `~/.agents/docs/agents/reviewer.md` when the repository has none. It names the checks that exist and are safe to run, where agreed requirements live, and which document holds the project's principles.

Run only the checks that file lists, and only through script names the repository's own manifest declares. A lockfile entry proves a tool was wanted, not that it is installed, and a check invented from one fails for reasons the change did not cause. When neither file exists, run no checks and say so in the report.

Done when: the checks to run and the paths to read are known, or their absence is recorded.

## 4. Read the change and its context

Read the diff in full, then the code around it far enough to judge whether the change fits what is already there. Read the agreed requirements, the project's principles document, and its glossary when the configuration names them.

Where the repository's vocabulary has a word for a concept, use that word in the findings.

Done when: the diff, its surrounding code, and the named documents have been read.

## 5. Run the checks

Run each check the configuration names. Record each as passed, failed, or not run.

A check that runs and fails because of the change is a finding under the testing lens at high risk.

A check that is not installed, or that errors for reasons the change did not cause, gets a `checks:` line of its own reading `not run` with the reason. The same goes for anything the handoff named as already failing. Absent tooling is a fact about the project, and a fact about the project is never a finding.

Done when: every named check has a result, and every failure is attributed to the change or to the project.

## 6. Judge the five lenses

A defect belongs to the first lens below that covers it. Report it once, under that lens only.

**Requirements.** Whether the change does what was agreed, including the edge cases the requirements name; behaviour the requirements demand that is missing; behaviour present that nobody asked for. Not whether the requirements are themselves good, not how the behaviour is built, not the tests.

**Architecture.** Whether the change respects the boundaries, layering, and dependency direction already in the codebase; whether it contradicts a recorded decision; whether new code sits where its kind of code lives. Not the amount of machinery, not the naming.

**Simplicity.** Machinery not earning its place: an abstraction with one caller, configuration nothing varies, indirection with no second implementation, state that could be derived, a dependency added for what the platform already does. Not whether the design fits what surrounds it, not whether names read well.

**Testing.** Whether the tests assert behaviour rather than implementation; whether a plausible mistake would fail them; branches the change introduces that nothing covers; tests that pass whatever the code does. Checks that failed because of the change belong here. Judge the change against the harness the project has: where it has none, this lens has nothing to judge, so pass it and record the absence as a `notes:` line.

**Maintainability.** Names that mislead or need a comment to survive; structure that hides where behaviour lives; coupling that makes the next change expensive; a dependency someone will have to live with. Not whether the change is too complex, not whether it sits in the right module.

A defect in code the change did not cause is a pre-existing finding: report it, recommend `defer`, and open the last field, the one after the location, with `pre-existing:`. It never blocks a lens.

A lens passes when no finding under it recommends `fix`.

Done when: each of the five lenses has a pass or fail, and every finding sits under exactly one.

## 7. Report

Return this and nothing else:

```
scope: <what was reviewed> against <base>
requirements: <pass|fail>
architecture: <pass|fail>
simplicity: <pass|fail>
testing: <pass|fail>
maintainability: <pass|fail>

<lens> <high|medium|low> <fix|defer|ignore> <file:line> <what is wrong and what would fix it>
<lens> <high|medium|low> defer <file:line> pre-existing: <what is wrong and what would fix it>

checks: <command> <passed|failed|not run: reason>
notes: <one fact about the project that the change did not cause>
verdict: <agree|findings>
```

Every line carries one item. One finding per line, ordered by risk, highest first. One `checks:` line per command that ran or was meant to run. Where nothing was meant to run, the report still carries one `checks:` line, reading `none` and the reason. Every report has at least one. One `notes:` line per fact about the project the review had to work around: an absent test harness, an absent requirements document, a glossary the configuration named that is not there. A `notes:` line states one fact and stops. Where there are two facts, write two lines.

The verdict is `agree` when all five lenses pass, otherwise `findings`.

When the caller pushes back on a finding, withdraw it or say why it stands. A finding recommending `fix` that is still outstanding keeps the verdict at `findings`.

Done when: the report is returned in this format and the work under review is byte-for-byte as it was found.
