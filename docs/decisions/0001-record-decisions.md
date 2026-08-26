# 0001. Record decisions in this folder

**Date:** 2026-08-26
**Status:** Accepted

## Context

Choices made while building get forgotten, and then re-made differently, or reversed by
accident by someone who assumed there was no reason behind them. Chat history is not a
record: it is unsearchable, it is not in the repo, and it does not survive the tool that
produced it.

## Decision

Any choice that would be expensive to reverse and is not obvious from the code gets a
numbered file here. Five sentences is a normal length. Worth recording: the database, the
hosting model, the auth model, a dependency with a licence implication, and anything
chosen against the obvious default.

Never delete a decision record. Supersede it with a new one that links back, and set the
old one's status to Superseded.

## Consequences

A small ongoing cost per decision, in exchange for not re-arguing settled questions. Files
are numbered and never renumbered, so links stay valid.

Copy this file's four headings for the next one: Context, Decision, Consequences, plus the
date and status at the top.
