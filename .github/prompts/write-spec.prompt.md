---
mode: agent
description: Turn a vague idea into docs/spec.md before any code is written.
---

Write `docs/spec.md` for this:

${input:idea:What is the idea?}

Load the `spec-first` skill in `.github/skills/spec-first/SKILL.md` and use
`templates/spec.template.md`.

1. Ask at most three questions, in one message, and only ones whose answer changes the
   build. Anything you can reasonably decide yourself becomes a listed assumption instead.
2. Write the spec. The sections that carry the weight are **success criteria** (checkable
   by someone else) and **non-goals** (what this deliberately will not do). A spec without
   non-goals does not survive contact with the second week.
3. State the problem without naming a solution.
4. Record rejected alternatives with the reason, specific enough that the option does not
   get re-proposed in three months.
5. Surface assumptions and open questions **before** building, not after.
6. Add an ADR in `docs/decisions/` for any choice that would be expensive to reverse and is
   not obvious from the code.

Do not write code in this turn. End by showing the assumptions and open questions and
asking whether to proceed.
