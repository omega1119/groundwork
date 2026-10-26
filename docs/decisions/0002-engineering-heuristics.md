# 0002. Engineering heuristics, and where they come from

**Date:** 2026-10-26
**Status:** Accepted

## Context

The always-loaded instructions said a lot about documentation and almost nothing about the
code itself. The only rule against over-building sat in the `shipwright` agent, which most
sessions never load. Agents left to their own defaults add options nobody asked for,
abstract after one repetition, wrap failures in `try` blocks that return `None`, and
rename or restructure things they were not asked to touch.

A list of "global coding standards" circulating on social media in 2026 (YAGNI, DRY, fail
fast, simple first, delete aggressively, semantic naming) prompted a look at older sources.
Several of the practices that suit a human directing agents were worked out at IBM in the
early 1970s, for the same problem: one person's design carried out by others who do not
share their context.

## Decision

Add a short "How to build it" section to `.github/copilot-instructions.md`, and a review
checklist at `docs/review-checklist.md`. The sources, and the changes made on the way in:

| Rule | Source | Changed on the way in |
|---|---|---|
| Skeleton first | Top-down programming with stubs, H. D. Mills, "Top down programming in large systems", 1971. Brooks, "The Whole and the Parts" | None. It is the same idea as "the code runs" applied at every step. |
| Build what the task needs, the obvious way | YAGNI (Extreme Programming, late 1990s). Brooks, "The Second-System Effect", 1975 | Merged with "simple first", which said the same thing. |
| Two copies are fine, extract on the third | The rule of three, Fowler, *Refactoring*, 1999, credited to Don Roberts | The social list said "after second duplication", which reads either way. Agents over-abstract, so the later threshold. |
| Fail loudly | Fail fast | Spelled out as the three patterns agents actually produce. |
| Delete what your change made dead | "Delete aggressively" | Narrowed. Deleting code you do not understand contradicts "no unrelated changes" and removes fixes whose reason was never written down. |
| Names say what they do | "Semantic naming" | Scoped to parameters, flags, config and public functions. A 30 character loop index helps nobody. |
| The human owns the architecture | The chief programmer team, F. T. Baker, "Chief programmer team management of production programming", *IBM Systems Journal* 11(1), 1972. Brooks, "The Surgical Team" and conceptual integrity, *The Mythical Man-Month*, 1975 | The chief programmer is the human, the agents are the team. The team's "program librarian", who kept all work in a shared record, is `TASKS.md` and this folder. |
| Review against a checklist | Inspections, M. E. Fagan, "Design and code inspections to reduce errors in program development", *IBM Systems Journal* 15(3), 1976 | Kept: a checklist of real defect types, entry and exit criteria, a reader who is not the author, defects fed back into the list. Dropped: the meeting, the moderator role and the timed sessions. |

Brooks also argued that the user manual is the external specification and should be
written first ("Passing the Word"). That is not a new rule here, it is the reason the
README contract already exists, recorded so the lineage is not lost.

Rejected: HIPO diagrams and flowchart standards from the same period, because the code and
the spec already carry that information and a diagram nobody updates drifts. The chief
programmer team's "backup programmer", because a fresh agent session fills that role at no
cost.

## Consequences

About 30 more lines in the always-loaded file, paid on every request. In exchange, the
behaviours that cost the most review time are named where every agent sees them, and the
reasoning sits here rather than in that file.

The checklist only stays useful if it grows from real defects and loses lines that a
checker now covers. If it reaches the point where nobody reads it to the end, cut it.
