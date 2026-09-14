---
name: import-source
description: Fetch one document from a local path or URL and write it word for word as one markdown file under a directory in docs/, headed by Source, Retrieved, and Formatting convention lines. Runs only when the human types /import-source <path|url>.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Import source

Source: $ARGUMENTS

Write the source, a local path or a URL, word for word as one markdown file under a directory in `docs/` that the human names. With no argument, ask for one before anything else. `CONTEXT.md` beside this file defines the terms used below.

The imported file keeps every word of the source in the source's order. Render the source's markup (colour, weight, headings) into the markdown markings the Sources entry names. Add only the header and the anomaly labels, both of which read as visibly not source text. Drop only rendering artifacts such as duplicated list items and empty placeholders. A file an earlier run wrote stays as it is. A changed source becomes a new file beside it.

## 1. Match the source

Read the Sources section of `docs/agents/import-source.md` when the repo has one. An entry whose location matches the argument supplies the fetch method, the answer marking, the destination, and the supersession marker. With no matching entry, fetch the path or URL as is.

Done when: the fetch method, markings, and recommended destination are recorded, or their absence is.

## 2. Pick the destination

Ask for the destination directory under `docs/`. Recommend the first of these that exists: the entry's destination, a directory under `docs/` that already holds a file with this skill's header, then `docs/sources/`. Create the directory when it is missing.

Done when: the destination directory exists.

## 3. Check for an earlier import

Look in the destination for a file whose `**Source:**` line carries the same path or link. When the content matches, report the source as already imported and stop. When it differs, report what changed and ask before writing. On approval the changed source becomes a new file and the earlier file stays.

Done when: no earlier import exists, or the human has approved a new file.

## 4. Fetch

Fetch the source as rendered content so colour and weight survive. Fetch a Google Doc through its `mobilebasic` view, `https://docs.google.com/document/d/<id>/mobilebasic`. Read a local file as is.

When the source reads as a questionnaire and no entry names its answer marking, ask how answers are marked before writing anything.

Done when: the full source text is in hand with its markup, and the answer marking is known for a questionnaire.

## 5. Write the file

Write `<destination>/<slug>.md`, the slug taken from the source title, with this header and then the content word for word.

```markdown
# Title

**Source:** title, tab or section, and the path or link
**Retrieved:** YYYY-MM-DD
**Formatting convention:** one line on how questions, answers, and framing text are marked below

---
```

Done when: the file holds the header and every word of the source in order.

## 6. Render a questionnaire

When the Sources entry marks the source as a questionnaire, questions become `###` headings, answers become `> **Answer:**` blockquotes keeping any name prefix, framing text stays as prose, and a supersession marker sits directly above its answer. The marker defaults to a line starting `Supersedes:` naming the earlier question's heading and its file name.

```markdown
### Question heading as written in the source

> **Answer:** Name prefix if present: answer text as written.

### A question that revisits an earlier one

**Supersedes:** "Earlier question heading" in earlier-file.md

> **Answer:** the current answer.

### A question the expert skipped

> **Unanswered in source.**
```

Done when: every question, answer, and framing passage carries the markings above.

## 7. Label anomalies

- A question with no answer gets `> **Unanswered in source.**` where the answer would sit.
- An answer with no question goes word for word under a `### (No question in source)` heading.
- An answer that contradicts itself, its question, or a neighbour stays as written, followed by a one-line note labelled `unconfirmed` naming the contradiction.

Done when: every anomaly in the source carries its label in the file.

## 8. Report

Report the file written, the destination, and every anomaly. An empty anomaly list is stated as such.

Done when: the report is delivered.
