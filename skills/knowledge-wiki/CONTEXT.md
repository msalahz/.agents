# Knowledge wiki

Glossary for the knowledge-wiki skill. Ships beside `SKILL.md` and is read before every operation.

## Language

**Knowledge wiki**:
A set of pages in a repo that hold verbatim excerpts of raw sources and the links, citations, and index needed to navigate them. It never restates a source in its own words.
_Avoid_: knowledge base, digest, summary, knowl, knowledge dir

**Raw source**:
A markdown document in the wiki's raw folder, placed there by a tool outside this skill. The skill never writes there and never edits one.
_Avoid_: original, upload, input, import

**Domain expert**:
The person whose answers or writing a raw source records.
_Avoid_: stakeholder, client, owner

**Topical page**:
A wiki page about one subject, term, or concept, holding verbatim blocks from one or more raw sources.
_Avoid_: article, mirror page, source page

**Verbatim block**:
A passage copied word for word from a raw source, ending in a citation.
_Avoid_: quote, excerpt, snippet

**Citation**:
The line under a verbatim block naming the raw source it came from.
_Avoid_: reference, attribution

**Connector note**:
A short agent-written sentence between verbatim blocks that points the reader to another page or flags a contradiction, without restating any source.
_Avoid_: commentary, summary, annotation

**Supersession**:
A correction in which a later answer, marked as superseding an earlier one it names by question and raw source, becomes the current answer while the earlier one stays in place.
_Avoid_: contradiction, override, update

**Supersession marker**:
The line in a raw source that marks an answer as a supersession. Its shape is set in the repo knowledge doc.
_Avoid_: correction flag, override line

**Operation**:
A named action the knowledge-wiki skill performs, chosen by its argument.
_Avoid_: mode, command, subcommand

**Ingest**:
The operation that turns raw sources not yet on any page into topical pages, index entries, and a log entry.
_Avoid_: import, digest, process, mirror

**Repo knowledge doc**:
The file `docs/agents/knowledge-wiki.md` in a repo that sets where the wiki lives and how a supersession is marked.
_Avoid_: config, fallback, settings

**Wiki log**:
The append-only record of every write to the wiki, one entry per ingested raw source naming the pages it produced. Ingest reads it to find raw sources with no entry.
_Avoid_: changelog, history, manifest
