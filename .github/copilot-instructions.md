# Groundwork

This repo is a **template**. It ships the conventions, skills and templates that make an
agent-built project land with working setup instructions on the first try.

If this file still says "Groundwork" and the repo has real code in it, the template was
cloned and never adapted. Run `/new-project` (or load the `project-bootstrap` skill) and
rewrite this file for the actual project before doing anything else.

## The one rule that matters

**A project is not finished until someone who has never seen it can clone it and run it
from the README alone.** Working code with a stale README is an unfinished task, not a
finished one with a documentation debt.

Every change that affects how the project is installed, configured or run updates the
README in the same turn. Not "later", not in a follow-up.

## Definition of done

For any build task, all of these, every time:

1. The code runs.
2. `README.md` matches `templates/README.template.md`: same section order, every
   placeholder replaced with a real value.
3. Every command in the README was **actually executed** in the terminal, and the README
   records what it printed where that is useful. No invented flags, no invented script
   names, no invented package names.
4. `python3 scripts/readme_check.py` passes, and so does
   `python3 scripts/readme_check.py --text-only`, which scans every markdown file.
5. `.gitignore` covers whatever the run just created (`.venv/`, `__pycache__/`, data,
   secrets, build output).
6. Secrets live in `.env`, which is git-ignored, and `.env.example` lists the keys with
   dummy values.

Point 3 is the one that gets skipped. A README that documents `pip install -r
requirements.txt` against a file that does not exist is worse than no README, because the
reader blames themselves. Grep or run before you write.

## How to build it

Rules for the code itself. Where they come from, and what was left out on purpose, is in
`docs/decisions/0002-engineering-heuristics.md`.

- **Skeleton first.** Get the thinnest end-to-end path running (entry point, one real input,
  one real output) before filling anything in. Stub the rest. It runs at every step, not
  only at the end.
- **Build what the task needs, the obvious way.** No option, layer, config switch or
  abstraction for a case nobody asked for. Optimise only after measuring a problem.
- **Two copies are fine, extract on the third.** The wrong abstraction costs more than a
  duplicated block.
- **Fail loudly.** No `except` that returns `None`, no default that hides a missing setting,
  no retry loop that ends in silence. Put the offending value in the error message.
- **Delete what your change made dead:** imports, helpers, flags, files. Leave code you did
  not touch and do not understand, and ask before removing it.
- **Names say what they do.** Parameters, flags, config keys and public functions get the
  long name: `wait_until_saved=True`, not `wait=True`. Loop indices can stay short.
- **The human owns the architecture.** Do not change the stack, data model, public
  interface or folder layout on your own initiative. Propose it, say why, wait. Once
  agreed, record it in `docs/decisions/`.
- **Review against the checklist, not from memory.** Before reporting done, walk the diff
  through `docs/review-checklist.md`, in a fresh context or a second agent where you can.
  When a defect gets past it, add a line.

## Layout

| Path | What it is |
|---|---|
| `.github/copilot-instructions.md` | This file. Always loaded. Keep it short. |
| `AGENTS.md`, `CLAUDE.md` | Pointers to this file for other agent tools. `CLAUDE.md` imports both. |
| `.github/skills/` | Loadable procedures: bootstrapping a project, writing the README, writing a spec. Third-party skills are vendored here, pinned by `vendored.json`. |
| `.github/instructions/` | Auto-applied rules, scoped by `applyTo` glob. |
| `.github/prompts/` | Slash commands: `/new-project`, `/update-readme`, `/write-spec`, `/new-infra`. |
| `.github/agents/` | Custom agent definitions. |
| `docs/spec.md` | What is being built and why. Written before the code. |
| `docs/decisions/` | Short ADRs for choices a future reader would otherwise reverse by accident. |
| `docs/review-checklist.md` | Questions to put to a diff before calling it done, one per defect that has actually happened. |
| `templates/` | The README, spec and changelog templates, plus per-stack quickstart blocks. |
| `scripts/` | Durable tools only. Run throwaway code inline via a heredoc, do not leave one-shot scripts behind. |
| `TASKS.md` | Working task list with the reasoning, not just the checkboxes. |

## Skills

Load these rather than improvising. Each is in `.github/skills/<name>/SKILL.md`.

- **`project-bootstrap`**: starting anything new, from a one-file script to an Azure web
  app. Picks the stack, creates the layout, writes the README, verifies it.
- **`readme-writer`**: any time the README is created or the setup/run story changes.
  Owns the README contract and the per-stack quickstart blocks.
- **`spec-first`**: turning a vague request into `docs/spec.md` before writing code.
- **`iac-templating`**: writing or reviewing Bicep or Terraform. Owns the `infra/` layout,
  Azure Verified Module reuse, and the build/lint/what-if gate.

### Vendored skills

These come from other repositories, pinned to a commit in `.github/skills/vendored.json`
and fetched by `scripts/vendor_skills.py`. Each has a `PROVENANCE.md` and the upstream
licence. **Never edit them by hand**, a refresh overwrites the directory. To change how
they behave, add a rule under `.github/instructions/`, which wins.

- **`design-taste-frontend`**: landing pages, portfolios and redesigns that should not
  look templated. From `Leonxlnx/taste-skill`. Big file, roughly 87 KB, so it costs real
  context when it loads. Its Tailwind default agrees with our rule, but its design system
  step can drift toward Material or Carbon, and `webui.instructions.md` overrides that.
- **`swiftui-expert-skill`**: SwiftUI state and `@Observable` data flow, view
  composition, performance, and migration onto the iOS 26 and 27 APIs, including Liquid
  Glass, toolbars, Document and WebKit integration. From `AvdLee/SwiftUI-Agent-Skill`.
  10 KB entry point with 32 on-demand files under `references/`, so it is cheap to load.

```bash
python3 scripts/vendor_skills.py --check
```

## Writing style

**Never use em dashes.** Not in prose, code comments, docstrings, commit messages,
documentation or UI copy. Use a comma, a colon, a full stop, parentheses, or the
conjunction the dash was hiding. A blind swap to " - " is worse than the dash. En dashes
in numeric ranges (`1k–4.9k`) and hyphenated compounds are fine. `readme_check.py` fails
the build on em dashes in any markdown file outside the vendored skills, so this is
enforced, not advisory.

It also fails on invisible characters: zero width spaces, non-breaking spaces, bidi
controls and Unicode tag characters. These arrive from web paste and from tools that hide
markers between letters. A zero width space inside a command block gives the reader
"command not found" with nothing visible to blame.

Comments state what the code cannot show on its own, in one line. Do not restate the next
line and do not explain the change to a reviewer.

Prose is plain and specific. Prefer "takes about 40 seconds on a cold cache" to "is
performant". No marketing adjectives in a README.

## Conventions that bite

- **Python: always a `.venv` in the project root**, created with the version the README
  claims. Check what you actually have with `python3 --version` before writing a version
  number down. Never document `python` when the machine only has `python3`.
- **Activate commands differ per shell and per OS.** The README quickstart gives macOS and
  Linux first, then Windows PowerShell. Both, always. See
  `templates/quickstart/python-venv.md`.
- **Notebooks: the venv needs a registered kernel**, or the reader opens the notebook and
  finds no interpreter. Document the `ipykernel install` line.
- **Never commit notebook output.** Set up `nbstripout` or document the manual clear.
- **Do not invent a project name in a command.** If the entry point is `main.py`, the
  README says `python main.py`, not `python app.py`.
- **Pin what you install.** Freeze after installing, or the reader gets a different
  dependency tree in six months.
- One project per repo unless there is a reason. If there are several, each subfolder gets
  its own README and the root README links to them with a status column.
- **Web UI is Tailwind.** Check the installed major version in `package.json` before
  writing a class, because v3 and v4 configure differently. See
  `.github/instructions/webui.instructions.md`.
