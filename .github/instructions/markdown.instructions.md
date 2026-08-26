---
applyTo: "**/*.md"
---

# Markdown

- **No em dashes.** Comma, colon, full stop, parentheses, or the conjunction the dash was
  hiding. A blind swap to " - " is worse than the dash. En dashes in numeric ranges
  (`1k–4.9k`) and hyphenated compounds are fine. `scripts/readme_check.py` enforces this.
- One `#` heading per file, at the top. Then `##` sections in a sensible order.
- Language on every fenced block: `bash`, `python`, `powershell`, `json`, `mermaid`.
- Commands are copy-pasteable. No `$` prompt prefix, because it breaks copy and paste.
- Do not paste output into a command block. Describe it, or put it in its own block.
- Tables for anything with more than two attributes per row. Lists for everything else.
- Relative links between repo files, so they work on GitHub and in an editor.
- Bold is for the sentence a reader must not skip. Used on every third sentence it stops
  working.
- No marketing adjectives. "Takes about 40 seconds on a cold cache" beats "blazing fast".
- Wrap around 92 characters in prose. Do not reflow paragraphs you did not edit, it turns a
  one-line change into an unreadable diff.

## READMEs specifically

Follow `templates/README.template.md` and the `readme-writer` skill. Required sections, in
order: Requirements, Quickstart, Usage, Project layout, Configuration, Development.

Every command in a README must have been run before it was written down.

```bash
python3 scripts/readme_check.py
```
