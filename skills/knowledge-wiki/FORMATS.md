# Formats

The shapes setup, ingest, and lint rely on. Read from [SKILL.md](./SKILL.md).

## Topical page

Page names are lowercase with hyphens. Connector notes are one italic sentence, placed after the citation line so lint reads them as scaffolding, and never restate a source.

```markdown
# Page Title

**Summary**: One or two sentences of navigation copy, agent-written.

**Sources**: [file.md](../raw/file.md), [other.md](../raw/other.md)

**Last updated**: YYYY-MM-DD

---

## Section heading

Verbatim block. Raw markdown carries through as it is, without an extra blockquote.

(source: [file.md](../raw/file.md))

## Related pages

- [other-page](./other-page.md)
```

## Wiki log

The `Ingested` line is the record ingest reads and lint check 3 honours. Its shape is fixed; the `skipped:` part is optional. The log records every write to the wiki. A plain ask and lint write nothing to it.

```markdown
# Wiki log

## YYYY-MM-DD

- Ingested raw/<file>.md: page-a, page-b, page-c (skipped: framing text, section X)
- Filed <question in a few words>: page-a
- Superseded <page>: "<earlier question heading>" by raw/<file>.md
- Free notes on choices made during the operation.
```

## Index

```markdown
# Wiki index

## <Group heading>

- [page-name](./page-name.md) — one line of navigation copy
```

## Repo doc stub

Written by setup at `docs/agents/knowledge-wiki.md`.

```markdown
# Knowledge wiki

Read by the knowledge-wiki skill before every operation. Only these two sections are read.

## Location

docs/knowledge/

## Supersession marker

A line starting `Supersedes:` naming the earlier question's heading and its raw file.
```

## Raw files

Any markdown file under `raw/`. The skill reads them as they are and needs nothing from their shape except the supersession marker, when present, to tell a correction from a contradiction.
