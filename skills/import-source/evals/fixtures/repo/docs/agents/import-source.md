# Import source

Read by the import-source skill before every run. Only the Sources section is read.

## Sources

One entry per source. Each carries: name, where it lives, how to fetch it, how questions and answers are marked, the destination under docs/, how a supersession is marked (default: a line starting `Supersedes:` naming the earlier question and its file).

### Billing questionnaire

- Lives at: `notes/billing-questionnaire.md` in this repo
- Fetch: read the file as is
- Marking: questions are plain paragraphs ending in a question mark, answers are bold text on the line below, framing text is plain prose
- Destination: `docs/sources/`
- Supersession: default
