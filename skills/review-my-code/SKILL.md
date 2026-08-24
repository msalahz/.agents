---
name: review-my-code
description: Senior-engineer review of changed code for logic, readability, performance, and safety, with stack-specific checks loaded per repo. Use when the user asks to review their changes, a branch, a PR, the working tree, or "review since X".
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.3.0"
---

# Review my code

Review the changed code as a senior engineer would: find the bug, the slow path, and the line the next developer will misread, and say what to change. Three reviewers run in parallel, one per aspect group; the skill merges their findings into one report the user applies by ID.

Steps 1 through 4 print nothing. The report in step 5 is the run's entire output.

Arguments, in any order, both optional: a fixed point (commit, branch, tag, `HEAD~3`) and `scope=a|b|c`.

## 1. Pin the range

Resolve the fixed point:

- The argument, when given.
- Otherwise the working tree against `HEAD` when `git status --porcelain` prints anything. Untracked files count as added.
- Otherwise the merge-base with the default branch (`origin/HEAD`, falling back to `main`).

Check the ref resolves with `git rev-parse` and the diff is non-empty. A bad ref or an empty diff stops the run here with the reason.

Record the diff command (`git diff <fixed-point>...HEAD` for a ref, `git diff HEAD` plus untracked files for the working tree) and the commit list from `git log <fixed-point>..HEAD --oneline`.

Done when: the diff command is recorded.

## 2. Choose the scope

Read `scope=` from the arguments. When absent, ask the user to pick one of the three below, naming b as the default. Use b when the run is unattended.

- **a. Changed lines.** Findings only on lines in the diff. Surrounding code is read for judgement.
- **b. Touched units.** Findings on any function, component, or module the diff touches, including its unchanged lines.
- **c. Blast radius.** b plus every caller of and callee from the touched units.

Scope a keeps the recorded diff command; b and c rewrite it with `-U0`, since those scopes read surrounding code straight from the files.

Done when: one scope letter is recorded.

## 3. Load the checks

Checks live in markdown files, each with one `## <Aspect>` heading per aspect it translates for a stack. Two directories:

- Global: `~/.agents/docs/agents/code-review/`.
- Repo: `docs/agents/code-review/` at the repo root.

A file loads when its frontmatter `detect:` list has at least one match against the repo, or when it has no `detect:` at all. A `dep:<name>` item matches a key in `dependencies` or `devDependencies` of the root `package.json`; a `file:<glob>` item matches a path from the repo root. Load matching global files first, then repo files. A repo file with the same name as a global one replaces it; other repo files load alongside.

Done when: the loaded file list is recorded, in load order, with each replacement noted.

## 4. Run the three reviewers

List the touched units; scope c extends the list with their callers and callees. Dispatch three sub-agents in parallel, one per group in the aspects table below. Build each prompt with the `unslop-writing-for-agents` skill from the parts below:

- The diff command, the commit list, the scope letter with its definition from step 2, and the touched-unit paths.
- The group's aspects with their definitions from the table.
- Every `## <Aspect>` section belonging to the group, from every loaded file, pasted in full and labelled with its source file.
- The finding contract and the report rules below, pasted in full.
- The brief: "Review as a senior engineer whose job is to make this code correct, readable, and fast. Read each touched unit in full before judging the diff. Return your top eight findings by risk. Report only what you can point at with `path:line`. Skip anything the repo's lint, typecheck, or formatter already enforces."

Done when: three reports are back.

## 5. Merge and report

Print the report in this order:

1. Header: the resolved range, the scope letter, the loaded check files.
2. One section per group, in table order. Each section opens with a line giving the finding count and the worst risk, then the findings.
3. Footer: total findings, findings dropped by the cap per group.

When two groups report the same `path:line`, keep the finding with the higher risk, add the other finding's aspect name and ID to it, and list the absorbed IDs at the end of their own group's section. IDs stay as the reviewers assigned them. Keep everything else verbatim.

Done when: the report is printed and every finding has an ID.

## 6. Apply by ID

Ask which IDs to apply. Apply those, run the repo's `validate` script (`pnpm validate` when present; otherwise typecheck, lint, and test in turn), and report anything that fails with its output. Stop after the report when the user picks none.

Done when: every chosen ID is applied and the validate result is reported, or the user chose none.

## Aspects

| Group | ID prefix | Aspect | The reviewer asks |
| --- | --- | --- | --- |
| Structure and Health | S | Idiomatic | Does this use the modern, native patterns of the language and framework? |
| Structure and Health | S | Maintainable | Can the next developer change this safely without reading the whole module? |
| Structure and Health | S | Cognitive Load | Is any logic harder to follow than the problem requires? |
| Structure and Health | S | Edge Cases | What input, state, or timing breaks this: null, empty, duplicate, out of order, partial failure? |
| Performance and Architecture | P | Complexity | Where is the time or space cost superlinear, and what is the bottleneck under real data sizes? |
| Performance and Architecture | P | Idempotent | Does repeating this action produce the same result and no extra side effects? |
| Performance and Architecture | P | Scalable | Does the logic hold at ten times the rows, users, or requests? |
| Security and Safety | X | Sanitization | Can any input reach a query, a command, the DOM, or a URL without validation or escaping? |
| Security and Safety | X | Thread-safe | What happens when two of these run at once: double submit, concurrent writes, stale reads? |

A check file translates an aspect into concrete checks for a stack. The report always carries all nine names.

## Finding contract

Every finding opens with one header line, then a body:

```
**S1** `path:line` | Aspect | risk | recommendation | unchanged line
```

- ID: group prefix plus a number, `S1`, `P2`, `X3`, numbered per group in report order.
- `path:line`. A finding without one is dropped.
- Aspect name from the table.
- Risk: high, medium, or low.
- Recommendation: fix, defer, or ignore.
- `unchanged line` only when the line is outside the diff (scope b or c).
- Body: high and medium risk get at most two sentences, what breaks then why. Low risk stops at the header line.
- Snippet: the proposed change in at most 8 lines, changed lines only, `...` marking each gap. Include one when the recommendation alone cannot carry the fix. Larger changes get one sentence naming the steps.

## Report rules

- A reviewer's report opens with one line giving its finding count and worst risk, then the findings, nothing else.
- At most 8 findings per group. Over the cap, drop the lowest risk first and state how many were dropped.
- One finding per root cause. The same bug in three call sites is one finding listing three lines.
- Risk follows consequence, not aspect: a cognitive-load finding that hides a data leak is high.
