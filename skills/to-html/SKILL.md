---
name: to-html
description: Render a report, summary, or other session deliverable as one styled self-contained HTML file in the repo. Use when the user asks for an HTML version of something, or to restyle one already produced.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# To HTML

Turn the named content into one self-contained HTML file: markup and one inline `<style>` block carry everything, so the file renders anywhere as-is.

## 1. Pin content and destination

The content is whatever the user names — usually the report or answer already produced this session. Render only what exists; a missing section stays missing.

Destination directory: the one the user names, else `docs/reports/` in the current repo (create it). Filename: `<topic-slug>-<YYYY-MM-DD>.html`.

Done when: source content, directory, and filename are fixed.

## 2. Write the file

Invoke the `frontend-design` skill and design the page under its guidance. House style, unless the user says otherwise:

- Dark theme with vivid accents; pick the palette yourself.
- Comfortable reading sizes and generous line height.
- Palette in CSS variables on `:root` with `color-scheme: dark`, so a restyle is a one-block edit.
- Severity or status gets color-coded badges with enough contrast to read.
- Structure mirrors the source: same headings, ordered lists for findings, a callout for the summary.
- Escape `<`, `>`, `&` inside code snippets.

Done when: the file opens in a browser with every section of the source present and readable.

## 3. Report

Give the path and the command to view it (`open <path>` on macOS).

Done when: the user has both.
