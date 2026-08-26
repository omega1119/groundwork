---
name: spec-first
description: Use when a request is vague, large, or will span more than one sitting, to turn it into docs/spec.md before any code is written. Also use when picking up work started earlier, to check the spec still matches reality.
---

# Spec first

A spec exists to make disagreement cheap. Changing a paragraph costs nothing, changing a
built system costs the build.

## When to write one

| Write a spec | Skip it |
|---|---|
| More than about three moving parts | A notebook exploring a dataset |
| Anything deployed or multi-user | A single-page landing site |
| Anything storing personal data | A throwaway script |
| The request has an unstated success criterion | The request is one sentence and unambiguous |

When skipping, say so in one line rather than silently skipping.

## Workflow

1. **Ask the questions that change the build**, at most three, in one message. Good ones:
   who uses it, how they run it (script, web, scheduled), where the data comes from,
   whether anything is private, what "done" looks like. Bad ones: anything you could
   decide yourself and note as an assumption.
2. Write `docs/spec.md` from `templates/spec.template.md`.
3. **Show the open questions and assumptions before building**, not after. Assumptions are
   decisions the reader did not get asked about, so surface them.
4. Build against the spec. When reality contradicts it, update the spec in the same commit
   as the code. A spec that lies is worse than no spec.
5. Anything discovered and deferred goes in `TASKS.md` with the reason, not just the task.

## What a good spec has

- **A problem statement that does not mention a solution.** "Users cannot tell which
  followers matter" is a problem. "Build a ranking dashboard" is a solution wearing a
  problem's clothes.
- **Success criteria that can be checked.** "Ranks 10k followers in under 5 minutes" can
  be. "Fast and reliable" cannot.
- **Explicit non-goals.** This is the section that prevents scope creep, and the one most
  often left out.
- **Constraints**: budget, rate limits, privacy, deadlines, what must not change.
- **The chosen approach, and the rejected ones with the reason.** Six months later the
  rejected options get re-proposed unless the reason is written down.
- **Open questions with an owner**, so it is clear what is blocked on whom.

## Decision records

When a choice would be expensive to reverse and is not obvious from the code, add a short
ADR in `docs/decisions/`, numbered, using `docs/decisions/0001-record-decisions.md` as the
shape. Five sentences is a normal length. Examples worth recording: the database, the
hosting model, the auth model, a dependency with a licence implication, anything chosen
against the obvious default.

Never delete an ADR. Supersede it with a new one that links back.
