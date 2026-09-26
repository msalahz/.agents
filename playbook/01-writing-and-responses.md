# Writing and responses
Prose style (unslop), doc shape, and how to answer and ask the user: question budget, lettered options, approvals, settled answers.

## Patterns

- **Scan, rewrite, add soul.** Edit prose in three passes: scan for AI patterns, rewrite while keeping meaning and tone, then add voice. _Sources: skills/unslop/SKILL.md_
- **Lettered options with a recommendation.** Label a question's options `a`, `b`, `c` and mark the one you recommend. _Sources: AGENTS.md_

### Doc shapes

- **Rules grouped by domain.** Write global memory as short H2 sections by domain, each a flat list of one-line imperative rules in the first person. _Sources: AGENTS.md_
- **Pointer to a lazy-loaded doc.** Keep a one-line "Before X, read Y" trigger in AGENTS.md and put the detail in a separate file under `docs/agents/`. _Sources: AGENTS.md_
- **House rules summary.** Restate AGENTS.md's key rules briefly in the README and name AGENTS.md as the source of truth. _Sources: README.md_
- **Definition then rules.** Open a doc with a one-line definition and follow it with a flat list of imperative rules. _Sources: docs/agents/briefs.md_
- **Sections per role.** Split a doc into one section per role the reader plays, such as Reviewing, Answering, Arbitrating, and Reporting to a human. _Sources: docs/agents/code-review.md_
- **Sections per lifecycle stage.** Split a doc into one section per stage, such as Breaking work down, Launching, Running as a subagent, and Verifying a report, each a flat list of imperative bullets. _Sources: docs/agents/delegation.md_
- **Numbered catalogue with fixes.** Write a style guide as a numbered catalogue grouped under category headings, each entry a bold name, examples, and a one-line fix. _Sources: skills/unslop/SKILL.md_
- **Reason beside each command rule.** Give every command-level rule its reason, such as a classifier refusal or a hang. _Sources: skills/supervise-issue/SKILL.md_

## Strategies

- **Sterile is also a tell.** Treat removing AI patterns as half the job, because voiceless writing reads as machine-made too. _Sources: skills/unslop/SKILL.md_
- **Caller decides approval.** Apply fixes at once and report them when another skill asked, and wait for approval when the user asked. _Sources: skills/unslop-writing-for-agents/SKILL.md_

## Practices

### Answering and asking

- **Questions are not change requests.** In an interactive session, answer a question about code or a plan and change nothing until the user says to act. _Sources: AGENTS.md_
- **A question that names the change is a request.** Act on a question that names the change to make. _Sources: AGENTS.md_
- **Answer without changing anything.** In reply mode, answer in plain text, read and run what the answer needs, and make no file edits or state-altering commands. _Sources: skills/reply/SKILL.md_
- **Narrow approval.** Take "go" or "apply" as approval for the item just discussed and nothing else. _Sources: AGENTS.md_
- **Flag then comply.** Say in one sentence when a request looks mistaken or a better approach exists, then do what was asked. _Sources: AGENTS.md_
- **Settled answers.** Treat an earlier answer in the thread as settled unless the user reopens it. _Sources: AGENTS.md_
- **Self-reopen in analysis.** In analysis work, reopen an earlier answer yourself when a later step shows it was wrong. _Sources: AGENTS.md_
- **Label unverified claims.** Mark unverified claims `unverified` and say when you do not know. _Sources: AGENTS.md_ _Conflicts with: Cutoff disclaimers_
- **Question budget.** Ask at most three questions per round. _Sources: AGENTS.md, skills/favicon-generator/SKILL.md_
- **Ask with a recommended option.** When details are missing, ask and offer a recommended option instead of guessing. _Sources: skills/knowledge-wiki/SKILL.md_
- **Ask only what changes the work.** Limit questions to what changes the outcome, which for supervise-issue means status tracking without a project, effort overrides, and human-only criteria in agent tickets. _Sources: skills/supervise-issue/SKILL.md_

### Writing artifacts

- **Scope rules by task kind.** Apply each rule only to the kind of task it names. _Sources: AGENTS.md_
- **Unslop artifacts, not chat.** Run `unslop` on docs, specs, commit messages, and PR bodies you write, and skip chat replies unless asked. _Sources: AGENTS.md, skills/unslop/SKILL.md_
- **Plain and specific PR body.** Write the PR body plainly and specifically. _Sources: skills/author-ticket/SKILL.md_
- **Collect every finding.** Review the text against both skills until every finding is collected. _Sources: skills/unslop-writing-for-agents/SKILL.md_
- **Fix all and diff.** Fix every finding and show the result as a unified diff against the original. _Sources: skills/unslop-writing-for-agents/SKILL.md_
- **Combined review pass.** Polish agent-facing text by running it past both writing-for-agents and unslop, then apply every fix. _Sources: skills/unslop-writing-for-agents/SKILL.md_

### Voice

- **Have opinions.** React to facts instead of listing pros and cons neutrally. _Sources: skills/unslop/SKILL.md_
- **Vary rhythm.** Mix short sentences with longer ones. _Sources: skills/unslop/SKILL.md_
- **Acknowledge complexity.** Give a mixed reaction where one exists instead of a single flat adjective. _Sources: skills/unslop/SKILL.md_
- **Use "I" when it fits.** Write in the first person where it reads naturally. _Sources: skills/unslop/SKILL.md_
- **Let some mess in.** Leave some structure imperfect, since perfect structure looks machine-made. _Sources: skills/unslop/SKILL.md_
- **Be specific.** Replace vague reactions with concrete detail. _Sources: skills/unslop/SKILL.md_

### Content and word choice

- **Puffery.** Cut phrases like "pivotal moment" and "testament to" and state what happened. _Sources: skills/unslop/SKILL.md_
- **Name-dropping.** Pick one outlet and say what it said instead of listing outlets without context. _Sources: skills/unslop/SKILL.md_
- **Superficial -ing phrases.** Delete phrases like "highlighting..." and "ensuring...", or back them with real sources. _Sources: skills/unslop/SKILL.md_
- **Promotional language.** Swap words like "vibrant" and "groundbreaking" for neutral descriptions. _Sources: skills/unslop/SKILL.md_
- **Vague attributions.** Name the source behind "experts believe" claims or delete them. _Sources: skills/unslop/SKILL.md_
- **Formulaic challenges.** Replace "despite challenges, it continues to thrive" with specific facts. _Sources: skills/unslop/SKILL.md_
- **Cutoff disclaimers.** Find sources or delete disclaimers like "while specific details are limited". _Sources: skills/unslop/SKILL.md_ _Conflicts with: Label unverified claims_
- **AI vocabulary.** Swap words like delve, crucial, pivotal, tapestry, and underscore for plain ones. _Sources: skills/unslop/SKILL.md_
- **Plain word.** Write "use" for utilize and leverage, "help" for facilitate, and "many" for numerous. _Sources: skills/unslop/SKILL.md_
- **Just say "is".** Write "is" or "has" instead of "serves as", "stands as", "boasts", or "features". _Sources: skills/unslop/SKILL.md_
- **Abstract metaphor nouns.** Replace substrate, wedge, vector, surface, north star, flywheel, and similar nouns with the concrete word. _Sources: skills/unslop/SKILL.md_
- **Not just X but Y.** State the point directly. _Sources: skills/unslop/SKILL.md_
- **Rule of three.** List the natural number of items instead of forcing three. _Sources: skills/unslop/SKILL.md_
- **Synonym cycling.** Pick one name for a thing and repeat it. _Sources: skills/unslop/SKILL.md_
- **False ranges.** List topics directly instead of "from X to Y" when X and Y share no scale. _Sources: skills/unslop/SKILL.md_
- **Chatbot phrases.** Delete "I hope this helps!", "Certainly!", and similar. _Sources: skills/unslop/SKILL.md_
- **No sycophancy.** Answer directly instead of opening with "Great question!". _Sources: skills/unslop/SKILL.md_
- **Filler phrases.** Write "to" for "in order to" and "because" for "due to the fact that", and delete "it is important to note that". _Sources: skills/unslop/SKILL.md_
- **Excessive hedging.** Collapse stacked hedges into one word like "may". _Sources: skills/unslop/SKILL.md_
- **Generic conclusions.** End on specific plans or facts instead of "the future looks bright". _Sources: skills/unslop/SKILL.md_

### Plain speech

- **Say what it does.** Name the mechanism or a number instead of how something feels. _Sources: skills/unslop/SKILL.md_
- **Restate or cut.** Cut any sentence you cannot restate as a concrete instruction, fact, or number. _Sources: skills/unslop/SKILL.md_
- **Portability test.** Cut any sentence that could appear unchanged in another project's docs. _Sources: skills/unslop/SKILL.md_
- **One idea per sentence.** Shorten or split any sentence the reader has to backtrack to parse. _Sources: skills/unslop/SKILL.md_
- **Active voice.** Name the actor instead of writing "is/are + past participle", unless the actor is unknown or irrelevant. _Sources: skills/unslop/SKILL.md_
- **Cut adverbs.** Replace an adverb propping up a weak verb with a stronger verb or the measured number. _Sources: skills/unslop/SKILL.md_

### Punctuation and formatting

- **No em dashes.** Use periods or commas in place of em dashes, and skip parentheses, en dashes, and hyphen-as-dash substitutes too. _Sources: skills/unslop/SKILL.md_
- **Colon limits.** Use a colon only before a list or example, never as a mid-sentence connector. _Sources: skills/unslop/SKILL.md_
- **Boldface restraint.** Leave proper nouns and acronyms unbolded. _Sources: skills/unslop/SKILL.md_
- **Inline-header lists.** Turn a bold label and colon that restates its line into prose, and keep a bold lead-in that ends in a period and precedes new detail. _Sources: skills/unslop/SKILL.md_
- **Sentence case headings.** Write headings in sentence case. _Sources: skills/unslop/SKILL.md_
- **No decorative emojis.** Remove emojis from headings and bullets. _Sources: skills/unslop/SKILL.md_
- **Straight quotes.** Replace curly quotes with straight ones. _Sources: skills/unslop/SKILL.md_

## Where it lives

AGENTS.md holds the answering and approval rules, the question budget, lettered options, the unverified label, task-kind scoping, the pointer-to-doc pattern, and the rule to run unslop on artifacts. The docs/agents files show the doc shapes for briefs, code review, and delegation, and the README repeats the house rules. The unslop catalogue, the combined review pass, reply's no-edit mode, supervise-issue's question list and command reasons, author-ticket's PR body rule, and knowledge-wiki's recommended option live only in their skills, and favicon-generator repeats the three-question budget.
