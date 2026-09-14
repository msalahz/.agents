# Import source

Glossary for the import-source skill. Ships beside `SKILL.md`.

## Language

**Source**:
One document, at a local path or a URL, that a run of the skill fetches.
_Avoid_: input, upload, original

**Imported file**:
The markdown file the skill writes for one source, word for word under a header.
_Avoid_: raw file, copy, export

**Destination**:
The directory under `docs/` that holds imported files, named by the human on each run.
_Avoid_: target, output folder, raw folder

**Questionnaire**:
A source that records a domain expert's answers to written questions. How its questions and answers are marked is set per source in the repo import doc.
_Avoid_: survey, form, Q&A doc

**Domain expert**:
The person whose answers or writing a source records.
_Avoid_: stakeholder, client, owner

**Answer marking**:
The way a source distinguishes an answer from its question and framing text, such as red text or bold.
_Avoid_: format, style, highlighting

**Supersession marker**:
A line in a questionnaire that marks an answer as replacing an earlier one it names by question and file.
_Avoid_: correction flag, override line

**Anomaly**:
Something unexpected in a source that the skill labels in the imported file: an unanswered question, an answer with no question, or an answer that contradicts itself or a neighbour.
_Avoid_: issue, error, warning

**Repo import doc**:
The file `docs/agents/import-source.md` in a repo that names its sources, each with fetch, marking, destination, and supersession instructions.
_Avoid_: config, fallback, settings
