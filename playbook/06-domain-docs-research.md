# Domain docs and research
Domain docs (CONTEXT.md, ADRs, glossary), repo doc conventions, the knowledge wiki, and verbatim research handling.

## Patterns

- **README shape.** Build a README from a title, a purpose paragraph, an annotated layout tree, inventory tables and lists grouped by ownership, a command table, a workflow walkthrough, and a "House rules" summary that points at AGENTS.md. _Sources: README.md_
- **Annotated layout tree.** Draw the layout as a `text` code block tree with a short description beside each path. _Sources: README.md_

### Agent memory and domain docs

- **Global memory with repo override.** Apply global defaults in every repo, and let a repo's own `docs/agents/*.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, or `## Agent skills` section win over them. _Sources: AGENTS.md_ _Conflicts with: Skill-owned formats_
- **Global default header.** Open a global default doc by stating that it is the global default and how a repo overrides it. _Sources: docs/agents/domain.md_
- **Single or multi-context layout.** Default to one root `CONTEXT.md` plus `docs/adr/`; a root `CONTEXT-MAP.md` makes the repo multi-context, with a `CONTEXT.md` and `docs/adr/` under each `src/<context>/`. _Sources: AGENTS.md, docs/agents/domain.md_
- **Numbered ADR filenames.** Name ADRs `docs/adr/0001-<slug>.md`. _Sources: docs/agents/domain.md_
- **Glossary with Avoid lists.** Write each glossary term as a bold name, a one-to-two sentence definition, and an italic `_Avoid_:` line listing rejected synonyms. _Sources: skills/knowledge-wiki/CONTEXT.md_

### Wiki templates

- **Repo doc configures the skill.** Let `docs/agents/knowledge-wiki.md` set the Location (default `docs/knowledge/`) and the supersession marker (default a `Supersedes:` line). _Sources: skills/knowledge-wiki/SKILL.md_
- **Repo doc stub.** Write the repo doc stub with only Location and Supersession marker sections, and state that only those two are read. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Topical page template.** Lay out a topical page as title, Summary, Sources, Last updated, a rule, sections of verbatim block plus `(source: ...)` line, then Related pages. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Index template.** Group index entries under headings, each entry in the form `[page](./page.md) — one line`. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Log template.** Write the log as dated sections of `Ingested`, `Filed`, and `Superseded` lines plus free notes. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Lint report shape.** Run every check and report findings as a numbered list, each with a suggested fix. _Sources: skills/knowledge-wiki/SKILL.md_

### Wiki glossary

- **Raw source.** Use _raw source_ for a markdown document placed by a tool outside the skill, which the skill never writes or edits. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Domain expert.** Use _domain expert_ for the person whose answers or writing a raw source records. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Topical page.** Use _topical page_ for a page about one subject holding verbatim blocks from one or more sources. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Verbatim block.** Use _verbatim block_ for a passage copied word for word and ending in a citation. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Citation.** Use _citation_ for the line under a verbatim block naming its raw source. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Connector note.** Use _connector note_ for a short agent-written sentence that points to another page or flags a contradiction without restating any source. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Supersession.** Use _supersession_ for a marked later answer becoming current while the earlier one stays in place. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Supersession marker.** Use _supersession marker_ for the line that marks a supersession, whose shape the repo knowledge doc sets. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Operation.** Use _operation_ for a named action chosen by the argument, and avoid mode, command, and subcommand. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Ingest.** Use _ingest_ for the operation that turns unprocessed raw sources into pages, index entries, and a log entry. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Repo knowledge doc.** Use _repo knowledge doc_ for `docs/agents/knowledge-wiki.md`, which sets location and supersession marking, and avoid config and settings. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Wiki log.** Use _wiki log_ for the append-only record of every write, one entry per ingested source, which ingest reads to find unprocessed sources. _Sources: skills/knowledge-wiki/CONTEXT.md_

## Strategies

- **Lazy doc creation.** Create domain docs through `/domain-modeling` only when a term or decision gets resolved. _Sources: docs/agents/domain.md_
- **Missing term is a signal.** Treat a concept missing from the glossary as either invented language to reconsider or a real gap to note for `/domain-modeling`. _Sources: docs/agents/domain.md_
- **Wiki as verbatim navigation layer.** Build the wiki as a navigation layer over raw sources that holds the experts' own words verbatim plus scaffolding and restates nothing, so a reader who trusts a page trusts the expert and lint can prove it. _Sources: skills/knowledge-wiki/SKILL.md, skills/knowledge-wiki/CONTEXT.md_
- **Ask via index.** Answer a question by reading `wiki/index.md`, then the pages it points to, and answer from verbatim blocks with citations to the pages. _Sources: skills/knowledge-wiki/SKILL.md_
- **Fallback to raw.** When no page answers, search `raw/`; answer a hit with a raw citation noting it sits on no page yet, and with no hit say no source holds the answer. _Sources: skills/knowledge-wiki/SKILL.md_

## Practices

- **Docs describe current state.** Write docs about the current state and leave fixed issues and past changes to git. _Sources: AGENTS.md_ _Conflicts with: Supersession handling_
- **Verbatim extraction.** Keep extracted or transcribed text verbatim and change only its formatting. _Sources: AGENTS.md_
- **Imported sources are read-only.** Leave imported sources, such as a knowledge wiki's `raw/` folder, unwritten; any tool may fill `raw/` with markdown files, but the wiki skill never writes there. _Sources: AGENTS.md, skills/knowledge-wiki/SKILL.md_

### Domain docs

- **Read domain docs first.** Before exploring, read `CONTEXT.md`, or `CONTEXT-MAP.md` and each relevant per-context `CONTEXT.md`. _Sources: docs/agents/domain.md_
- **Read relevant ADRs.** Read the ADRs in `docs/adr/` that touch the area, and in multi-context repos the ones in `src/<context>/docs/adr/`. _Sources: docs/agents/domain.md_
- **Read ADRs, AGENTS.md, and runbooks for a ticket.** When authoring a ticket, read `docs/adr/*.md`, `AGENTS.md`, and the runbooks the ticket points at. _Sources: skills/author-ticket/SKILL.md_
- **Proceed silently when absent.** When domain docs do not exist, carry on without flagging it or suggesting they be created. _Sources: docs/agents/domain.md_
- **Use glossary vocabulary.** Name domain concepts in issue titles, proposals, hypotheses, and test names with the `CONTEXT.md` term, and skip the synonyms the glossary lists to avoid. _Sources: docs/agents/domain.md_
- **Flag ADR conflicts.** Surface a contradiction with an ADR explicitly, in the form `_Contradicts ADR-0007 (...) — but worth reopening because…_`. _Sources: docs/agents/domain.md_

### Wiki setup

- **Skill-owned formats.** Keep page format, citations, the log, and lint checks as the skill defines them, whatever the repo doc says. _Sources: skills/knowledge-wiki/SKILL.md_ _Conflicts with: Global memory with repo override_
- **Glossary read every time.** Ship the glossary beside `SKILL.md` and read it before every operation. _Sources: skills/knowledge-wiki/CONTEXT.md_
- **Setup refuses existing wiki.** Stop and report when Location already holds `raw/` or `wiki/`. _Sources: skills/knowledge-wiki/SKILL.md_
- **Setup artefacts.** Create `raw/`, `wiki/`, `wiki/index.md`, and `wiki/log.md` with title lines, and write the repo doc stub unless a repo doc already exists. _Sources: skills/knowledge-wiki/SKILL.md_
- **Propose AGENTS.md pointer.** Propose one pointer line for the repo AGENTS.md Docs section naming the wiki as domain background, show the diff, and add it on approval. _Sources: skills/knowledge-wiki/SKILL.md_

### Wiki ingest

- **Find unprocessed files from the log.** Without an argument, list every `raw/` file that no `Ingested` line names, and stop if the list is empty. _Sources: skills/knowledge-wiki/SKILL.md_
- **Resume half-done ingests.** Extend the pages an interrupted run touched, and skip passages already on a page under the same citation. _Sources: skills/knowledge-wiki/SKILL.md_
- **One file at a time.** Take raw files one at a time and read each end to end. _Sources: skills/knowledge-wiki/SKILL.md_
- **Agree structure first.** Propose the topical pages a file touches, each about one subject, and agree the structure with the human before writing. _Sources: skills/knowledge-wiki/SKILL.md_
- **Split by topic.** Split a long source across topical pages instead of mirroring it as one page; a source touching ten or more pages is normal. _Sources: skills/knowledge-wiki/SKILL.md_
- **Keep heading text.** Keep raw heading text and change only its level to fit the page. _Sources: skills/knowledge-wiki/SKILL.md_
- **Cite every block.** End every verbatim block with its citation line, and cite both sources on a block stitched from two. _Sources: skills/knowledge-wiki/SKILL.md_
- **Scaffolding allowed.** Limit non-verbatim text to headings, wiki links, citations, connector notes, one Summary line per page, and index copy. _Sources: skills/knowledge-wiki/SKILL.md_
- **Disagreements side by side.** When sources disagree, copy both under sibling subheadings with a connector note naming the disagreement, and pick no winner. _Sources: skills/knowledge-wiki/SKILL.md_
- **Supersession handling.** When a later answer carries the marker, keep both blocks, add a note to the superseded one saying which is current, link the superseding one back, and record it in the log. _Sources: skills/knowledge-wiki/SKILL.md_ _Conflicts with: Docs describe current state_
- **Copy doubtful text as is.** Copy unclear or seemingly wrong raw text unchanged, then flag the concern in a connector note or ask the human. _Sources: skills/knowledge-wiki/SKILL.md_
- **Stop on concurrent edit.** When a page changed between reading and writing, stop and report instead of overwriting the other edit. _Sources: skills/knowledge-wiki/SKILL.md_
- **Record skipped passages.** Name the pages written on the `Ingested` line and, after `skipped:`, the passages the human chose to leave on no page. _Sources: skills/knowledge-wiki/SKILL.md_
- **Log entry last.** Finish an ingest by adding Related pages links, then adding each new page to the index with a one-line description, then appending the log entry, so an interrupted run leaves no record claiming unfinished work. _Sources: skills/knowledge-wiki/SKILL.md_

### Wiki ask

- **Ask needs a wiki.** When no wiki exists, report it, offer setup, and stop. _Sources: skills/knowledge-wiki/SKILL.md_
- **Prefer superseding block.** Answer from the superseding block and say the earlier one was superseded. _Sources: skills/knowledge-wiki/SKILL.md_
- **Mark outside-wiki content.** Mark anything in an answer that goes beyond the sources as outside the wiki. _Sources: skills/knowledge-wiki/SKILL.md_
- **Offer to file answers.** When an answer joined blocks from several pages or came from raw text on no page, offer to file it; on yes, place the blocks, update the index, and append a `Filed` log line. _Sources: skills/knowledge-wiki/SKILL.md_

### Wiki lint

- **Lint verbatim check.** Check that every verbatim block matches raw text word for word, flag paraphrase, summary, trim, and substitution, and skip scaffolding. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint orphans.** Flag topical pages with no inbound link from the index or another page. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint coverage.** Flag raw content that sits on no page, except passages listed after `skipped:`. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint links.** Check that every `(source: ...)` link resolves. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint headers.** Check that every topical page has the Summary, Sources, and Last updated header, skipping `index.md` and `log.md`. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint log completeness.** Check that every raw file has an `Ingested` line and every page a log line names exists. _Sources: skills/knowledge-wiki/SKILL.md_
- **Lint supersession notes.** Check that every superseded block carries a connector note pointing at its superseding block. _Sources: skills/knowledge-wiki/SKILL.md_

### Wiki formats

- **Page names.** Name pages in lowercase with hyphens. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Connector note placement.** Write a connector note as one italic sentence after the citation line, so lint reads it as scaffolding. _Sources: skills/knowledge-wiki/FORMATS.md_
- **No extra blockquote.** Carry raw markdown through as it is, without wrapping it in a blockquote. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Fixed Ingested shape.** Keep the `Ingested` line in its fixed shape with an optional `skipped:`, and write nothing to the log during a plain ask or lint. _Sources: skills/knowledge-wiki/FORMATS.md_
- **Raw shape-agnostic.** Require nothing of a raw file's shape except the optional supersession marker, which tells a correction from a contradiction. _Sources: skills/knowledge-wiki/FORMATS.md_

## Where it lives

AGENTS.md holds the global rules here: repo override of global memory, the single-context default, docs describing current state, verbatim extraction, and read-only imported sources. docs/agents/domain.md holds the domain doc rules (reading CONTEXT.md and ADRs, layouts, ADR naming, glossary vocabulary, ADR conflict flags, lazy creation), and README.md is the source of the README shape. Everything about the knowledge wiki except finding the repo root lives only in skills/knowledge-wiki (SKILL.md, CONTEXT.md, FORMATS.md), and the ticket-time reading of ADRs and runbooks lives only in skills/author-ticket/SKILL.md.
