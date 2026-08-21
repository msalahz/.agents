---
name: to-scoped-tickets
description: Break an approved feature spec into implementation tickets grouped by user-named scopes, published as a blocking chain in scope order.
disable-model-invocation: true
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.2.0"
---

# To scoped tickets

Break an approved spec into a blocking chain of tickets, one per user-named **scope**, by following `to-tickets` (`~/.agents/skills/to-tickets/SKILL.md`) with the amendments below. Where the two disagree, this file wins.

Input: the spec path, and the ordered list of scopes with the directories each one covers. Missing either, ask before anything else. The chain always starts with two default scopes, prepended in this order when the user's list lacks them: **integrations**, covering work under each vendor folder in `src/integrations/`, then **core**, covering anything under `src/core/`. Every scope is optional: it produces a ticket only when the spec demands work in its directories (the empty-scope bin below).

## 1. Survey per scope

This survey replaces to-tickets' optional exploration. For each scope in order, read the directories it names and work out what the spec demands there. Sort every finding into three bins:

- **Scope work.** What the scope's ticket will deliver.
- **Empty scope.** The spec demands nothing in its directories. It gets no ticket and no placeholder; it appears in step 2's report and the chain skips over it.
- **Unscoped work.** The spec requires it and no scope's directories hold it. Draft a proposed home: its own ticket, or folded into the nearest scope's ticket.

Done when: every spec requirement sits in exactly one bin, and every scope is either loaded with work or marked empty.

## 2. Quiz the user

Scope grouping replaces to-tickets' free-form slicing: one ticket per non-empty scope, in the given order, each blocked by the previous non-empty scope's ticket. Run to-tickets' quiz on that breakdown, adding:

- Each empty scope.
- Each piece of unscoped work with its proposed home, put as a question.

Done when: the user has approved the breakdown.

## 3. Publish

Publish as to-tickets' local files, with two amendments:

- The path is `docs/scratch/<feature-slug>/issues/NN-<slug>.md`, not `.scratch/`.
- A `**Scope:** <scope name> — <its directories>` line sits between "What to build" and "Blocked by", and file paths appear there and nowhere else in the body.

Done when: every approved ticket is on disk and matches the amended template.

## 4. Sync the spec

A decision that changed during the breakdown (a rename, a scope shift) goes into the spec in the same pass, so spec and tickets never diverge.

Done when: the spec states every decision the tickets assume.
