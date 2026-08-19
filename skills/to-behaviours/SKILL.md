---
name: to-behaviours
description: Extract product behaviour from the codebase into a durable, language-neutral behaviour catalogue. A description of what to extract names the source — a domain, term, path, branch or area; with no description, the whole source tree. Ask it to lint or audit and it checks the existing catalogue instead. Presents a pick-list and writes nothing until the human approves.
disable-model-invocation: true
---

# To Behaviours

Maintain the **behaviour catalogue** — numbered statements of what the product does, written to survive a rewrite in another language. Specs cite its IDs; statements with no spec are the visible backlog.

**Never write to the catalogue without explicit human approval.**

Every ask — scope, vocabulary, picks, confirmations — offers a recommended option plus free-form; never guess.

## Where

`docs/behaviours/<domain>.md`, one file per domain. If `docs/agents/behaviours.md` exists, it overrides this location and these conventions.

Vocabulary comes from the repo's domain docs — `CONTEXT.md`, or the contexts in `CONTEXT-MAP.md`. If neither exists, ask for the vocabulary source before proceeding.

## Statement rules

<statement-rules>

A candidate qualifies only if **all** hold:

- **Product-observable** — a URL, accessible name, visible text, or domain outcome. Never a function, file, prop, or config key.
- **Domain vocabulary** — nouns, roles and states verbatim from the domain docs, never the identifier in code.
- **Rewrite-proof** — rebuild the product in another language and the statement is unchanged.
- **One fact, one line** — declarative present tense; two facts on one line are two statements.
- **A person is the subject** — never a session, request, record or field. A limit is written as what the person who breaks it observes.
- **Falsifiable** — never "gracefully", "correctly", "properly", "as expected".
- **Level-neutral** — never says how it is proven.

</statement-rules>

Never in the catalogue: rationale, history, implementation detail, mechanism, coverage numbers, Gherkin, or any record of what the human declined. A change that alters no observable behaviour yields **zero** statements — say so; never pad.

## Scope

The invocation's description names the source: a domain, term, path, branch or commit range, or an area in prose. Resolve it however the words fit; if ambiguous, ask before scanning. With no description, the whole tree — one domain at a time: present, pick, write, then the next. A request to lint or audit goes to [Lint](#lint) instead.

## Process

1. **Read first** — every existing `docs/behaviours/*.md` and the relevant domain docs.
2. **Extract.** Ask what a person can observe; discard everything that fails `<statement-rules>`. Read past mechanism to the behaviour it carries — a permission table's capabilities, a library's defaults.
3. **Reconcile** into buckets: **New**, **Changed** (code contradicts a recorded statement), **Removed** (recorded behaviour the code no longer has), **Dropped**. A candidate that contradicts the domain docs, or decides a case they leave open, is a **conflict** — flag it with the conflicting section, never write it. A concept the docs never name is a gap in the domain docs, not a new statement. If the domain docs disagree with each other, report both sections — never pick a winner.
4. **Present** the buckets; write nothing yet. Pick-list numbers are ephemeral selection handles — IDs are allocated only on write. Always show Dropped so a bad drop can be caught. **Changed and Removed are confirmed one at a time** — show recorded vs. code and ask if the change was intended; if it wasn't, the code has a bug: report it and leave the catalogue untouched.
5. **Write** only what was picked.
6. **Report** what landed, plus unresolved conflicts and vocabulary drift (code identifier ≠ domain term) as notes to the human.

<pick-list-format>

```
New — docs/behaviours/access.md

  1  An Accountant may read Service Categories and may not create, update or delete them.
  2  A Part-timer may not read Service Categories.
  3  A Client may read Service Categories.        ⚠ conflicts with CONTEXT.md § Client

Dropped
  · the access-control object and plugin registration — mechanism, not behaviour

Reply: numbers to add (1,3), `all`, `none`, or tell me what to change.
```

</pick-list-format>

## IDs and file shape

- `DOMAIN-NNN`, zero-padded, prefix matching the file name. Next ID = highest ever seen in the file, live or retired, + 1. Never renumbered, never reused — specs cite it by name.
- Retiring deletes the statement's line and appends its ID to the file's retired comment.

<catalogue-file-template>

```md
# Access

- **ACCESS-001** An Owner may create, read, update and delete Service Categories.
- **ACCESS-003** An Accountant may read Service Categories and may not create, update or delete them.

<!-- retired: ACCESS-002 -->
```

</catalogue-file-template>

One `#` heading, statements in ID order, one bullet each with the ID bold, at most one retired comment. Nothing else.

## Lint

Check the catalogue, not the code — `docs/behaviours/*.md`, the domain docs, and whatever cites an ID. Whether the code still matches a statement is a normal run, not a lint.

Find: statements failing `<statement-rules>` or carrying forbidden content, vocabulary absent from or contradicting the domain docs, malformed, duplicate, or live-and-retired IDs, misfiled or duplicate statements, and citations of retired or unknown IDs. Uncited statements are the backlog, not a defect — list them last.

Report findings as a numbered list — file, ID, the fix — then stop. Fix only what the human picks, under the same write rules; retirements and rewordings are confirmed one at a time.
