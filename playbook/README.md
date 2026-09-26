# Playbook

This folder holds every pattern, strategy, and practice extracted from AGENTS.md, docs/agents, and the personal skills under skills/, with each bullet traced to its sources. A pattern is a reusable shape, a strategy is a decision rule, and a practice is a habit applied every time.
Plugin skills are excluded.
File 11 is a cross-cutting view, and every bullet in it duplicates one in files 01 to 10.

| File | Scope | Bullets |
| --- | --- | --- |
| [00-index.md](00-index.md) | Alphabetical list of every bullet short name in files 01 to 10 and the file that holds it. | 697 |
| [01-writing-and-responses.md](01-writing-and-responses.md) | Prose style (unslop), doc shape, and how to answer and ask the user: question budget, lettered options, approvals, settled answers. | 68 |
| [02-delegation-and-sessions.md](02-delegation-and-sessions.md) | Splitting work and launching subagents and peer sessions; coordinator and supervisor roles; briefs, handoffs, work logs, report lines; session naming, phases, idle handling, and cleanup. | 102 |
| [03-review-process.md](03-review-process.md) | How reviews, review loops, PR reviews, and arbitration run: roles, rounds, confidence scoring, finding and verdict format, review records. | 57 |
| [04-review-checklists.md](04-review-checklists.md) | Stack-specific code review checks for Drizzle, React, TanStack Start, and TypeScript, plus the shape of a stack check file. | 147 |
| [05-tickets-planning.md](05-tickets-planning.md) | Issue tracker, specs, tickets, triage labels, board status, plan tables, and scoping work to acceptance criteria. | 41 |
| [06-domain-docs-research.md](06-domain-docs-research.md) | Domain docs (CONTEXT.md, ADRs, glossary), repo doc conventions, the knowledge wiki, and verbatim research handling. | 74 |
| [07-git-safety-tooling.md](07-git-safety-tooling.md) | Branches, worktrees, commits, PRs, merges and rebases; human-only and remote actions, permission modes; gh, shell scripts, and human-run wizards. | 51 |
| [08-engineering-practice.md](08-engineering-practice.md) | Coding rules, validation gates and CI, UI checks in the browser, and the favicon generator. | 34 |
| [09-skill-structure.md](09-skill-structure.md) | The shape of a skill: frontmatter, openai.yaml metadata and invocation policy, step sections, descriptions, minimal and composite skills. | 23 |
| [10-skill-lifecycle.md](10-skill-lifecycle.md) | The skill home and linking model, and installing, uninstalling, updating, writing, archiving, and evaluating skills. | 100 |
| [11-agent-instructions.md](11-agent-instructions.md) | Cross-cutting view of the bullets in 01 to 10 that tell an agent how to behave: reading requests, asking, reporting, working with humans and agents, limits, context, coding, reviewing, and writing. | 93 |
| [99-conflicts-and-gaps.md](99-conflicts-and-gaps.md) | Pairs of bullets in files 01 to 10 that give different rules for the same situation, and the rules that exist only inside a skill. | 22 |

## Regenerating

1. Extract every pattern, strategy, and practice from each source file, with its source path.
2. Classify the extracted bullets into one bucket per category and record conflicting pairs.
3. Write one category file per bucket, then rebuild the index, the conflicts file, and this README.
