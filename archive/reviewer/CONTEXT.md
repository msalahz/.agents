# Agent skills

The one inventory of every agent skill on this machine, plus the shared configuration those skills read. Terms here are the vocabulary skills use when they talk to each other or to a person.

## Review

**Reviewer**:
The role that judges a change and returns a verdict. It never edits the work it judges.
_Avoid_: Critic, checker

**Author**:
The role that produced the change under review and acts on what the reviewer returns.
_Avoid_: Worker, implementer

**Lens**:
One of the five fixed angles a review is judged from: requirements, architecture, simplicity, testing, maintainability. Each carries its own pass or fail.
_Avoid_: Concern, dimension, axis, category

**Handoff**:
What an author gives a reviewer to establish context: the reference to review, the base to compare against, the agreed requirements, what was deliberately left out, what is already known to be failing, and on later rounds what moved since the last one.
_Avoid_: Packet, bundle, brief, context dump

**Round**:
One exchange: an author's handoff and the reviewer's report answering it.
_Avoid_: Iteration, pass, cycle

**Finding**:
One reported defect, carrying the lens it falls under, a risk, a recommendation, a location, and what is wrong.
_Avoid_: Issue, problem, comment, nit

**Risk**:
How much a finding matters: high, medium, or low.
_Avoid_: Severity, priority

**Recommendation**:
What the author should do with a finding: fix, defer, or ignore.
_Avoid_: Action, disposition

**Verdict**:
The reviewer's single terminating signal for a round, stating whether every lens passed.
_Avoid_: Approval, sign-off, decision

**Pre-existing finding**:
A finding in code the change did not cause. Always recommended for deferring, never blocking a lens.
_Avoid_: Legacy issue, drive-by

**Review scope**:
What the reviewer resolved to judge, and the base it compared against, stated at the top of every report.
_Avoid_: Target, subject
