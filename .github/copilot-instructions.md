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
4. `python3 scripts/readme_check.py` passes.
5. `.gitignore` covers whatever the run just created (`.venv/`, `__pycache__/`, data,
   secrets, build output).
6. Secrets live in `.env`, which is git-ignored, and `.env.example` lists the keys with
   dummy values.

Point 3 is the one that gets skipped. A README that documents `pip install -r
requirements.txt` against a file that does not exist is worse than no README, because the
reader blames themselves. Grep or run before you write.

## Layout

| Path | What it is |
|---|---|
| `.github/copilot-instructions.md` | This file. Always loaded. Keep it short. |
| `.github/skills/` | Loadable procedures: bootstrapping a project, writing the README, writing a spec. |
| `.github/instructions/` | Auto-applied rules, scoped by `applyTo` glob. |
| `.github/prompts/` | Slash commands: `/new-project`, `/update-readme`, `/write-spec`, `/new-infra`. |
| `.github/agents/` | Custom agent definitions. |
| `docs/spec.md` | What is being built and why. Written before the code. |
| `docs/decisions/` | Short ADRs for choices a future reader would otherwise reverse by accident. |
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

## Writing style

**Never use em dashes.** Not in prose, code comments, docstrings, commit messages,
documentation or UI copy. Use a comma, a colon, a full stop, parentheses, or the
conjunction the dash was hiding. A blind swap to " - " is worse than the dash. En dashes
in numeric ranges (`1k–4.9k`) and hyphenated compounds are fine. `readme_check.py` fails
the build on em dashes, so this is enforced, not advisory.

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
