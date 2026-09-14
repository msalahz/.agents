---
name: knowledge-wiki
description: Keep a verbatim wiki of domain expert answers inside a repo. Operations are setup, ingest, ask, and lint.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Knowledge wiki

Keep a wiki that is a navigation layer over raw sources written by domain experts. Pages hold the sources' own words, copied verbatim, plus the scaffolding needed to find them: headings, wiki links, citations, connector notes, one Summary line per page, and index copy. Verbatim means word for word. The wiki restates nothing, so a reader who trusts a page trusts the expert, and lint can prove it.

The argument is `<operation> [argument]`: `setup`, `ingest [raw-file]`, `ask <question>`, or `lint`. With no operation, list the four and stop. The terms this skill uses are defined in [CONTEXT.md](./CONTEXT.md); the page, log, and repo doc shapes are in [FORMATS.md](./FORMATS.md).

Two rules hold across every operation that writes. Append the log entry last, after every page and the index are written, so an interrupted run leaves no record claiming work it did not finish. When a page changed between reading it and writing it, stop and report instead of writing over someone else's edit.

## 1. Read the repo doc

Find the repo root with `git rev-parse --show-toplevel`, or use the current directory outside git. Read `docs/agents/knowledge-wiki.md` there when it exists. Two sections carry meaning.

- Location: the wiki directory relative to the root. Default `docs/knowledge/`.
- Supersession marker: how a raw source marks one answer as replacing an earlier one. Default a line starting `Supersedes:` followed by the earlier question's heading and its raw file name.

Page format, citations, the log, and lint checks are this skill's own, whatever else the doc says.

Then run only the section below that matches the operation.

Done when: Location and the supersession marker are resolved and the operation is chosen.

## 2. Setup

Stop and report when Location already holds `raw/` or `wiki/`.

Create `raw/`, `wiki/`, `wiki/index.md` holding its title line, and `wiki/log.md` holding its title line. Write the repo doc stub from FORMATS.md with the Location filled in, leaving an existing doc untouched and reporting the Location it sets. Propose one pointer line for the repo AGENTS.md Docs section naming `<Location>/wiki/` as domain background, show the diff, and add it on approval.

Report that `raw/` is empty and that any tool may fill it with markdown files. This skill never writes there.

Done when: the repo doc, `index.md`, and `log.md` exist with the two folders, and the human has answered on the AGENTS.md line.

## 3. Ingest

With an argument, take that raw file. Without one, read `wiki/log.md` and list every file under `raw/` that no `Ingested` line names. Stop and say so when the list is empty. A file an interrupted run left half done is on this list because its `Ingested` line was never written. Extend the pages it already touched, and skip a passage that already sits on a page under the same citation.

Take the files one at a time. Read the file end to end, propose the topical pages it touches, each about one subject, and agree the structure with the human before writing. A single source touching ten or more pages is normal. Split a long source across topical pages rather than mirroring it as one page.

Copy the relevant passages verbatim onto each topical page, creating or extending pages in the shape FORMATS.md gives. Keep raw heading text, changing only the level to fit the page. End every verbatim block with its citation line; a block stitched from two sources cites both. When two sources disagree, copy both under sibling subheadings with a connector note naming the disagreement and pick no winner. When the later answer carries the supersession marker naming the earlier question, it is a correction: both blocks stay, the superseded block gets a connector note saying which block is current, the superseding block gets one linking back, and the log records the supersession. Copy raw text that is unclear or seems wrong as it is, then flag the concern in a connector note or ask the human.

Add Related pages links, add each new page to `wiki/index.md` with a one-line navigation description, then append the log entry. The `Ingested` line names the pages written and, after `skipped:`, any passages the human chose to leave on no page.

Done when: every agreed page is written, the index lists each one, and the log carries one `Ingested` line per raw file processed.

## 4. Ask

When no wiki exists at Location, report that, offer setup, and stop there.

Read `wiki/index.md`, then the pages it points to for the question. Answer from their verbatim blocks and cite the pages. Where a page holds a superseded block, answer from the superseding block and say the earlier one was superseded. When the pages do not answer, search `raw/` for the question's terms. Answer a hit from the raw text with a raw citation and a note that it sits on no page yet. With no hit, say the answer is in no source, and mark anything further as outside the wiki. When details are missing, ask with a recommended option rather than guess.

When the answer joined blocks from several pages, or came from raw text on no page, offer to file it. On yes, place those verbatim blocks on the fitting topical page with links, update the index, and append a `Filed` line to the log.

Done when: the answer is delivered with citations and the filing offer, if any, has been answered.

## 5. Lint

Run every check and report findings as a numbered list, each with a suggested fix.

1. Every verbatim block in a topical page, the text between a section heading and its citation line, matches the raw text word for word. Flag paraphrase, summary, trim, and substitution. Scaffolding is skipped: Summary lines, connector notes, Related pages, and index copy.
2. Topical pages with no inbound link from `index.md` or another page.
3. Raw content on no page, except passages an `Ingested` line lists after `skipped:`.
4. Every `(source: ...)` link resolves.
5. Every topical page has the Summary, Sources, Last updated header. This covers topical pages only, so `index.md` and `log.md` are skipped.
6. Every raw file has an `Ingested` line in the log.
7. Every page a log line names exists.
8. Every superseded block carries a connector note pointing at its superseding block.

Done when: all eight checks have run and the numbered report is delivered.
