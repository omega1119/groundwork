---
name: project-bootstrap
description: Use when starting a new project or adding a new component to this repo, whatever the size, from a single Python script or notebook or HTML landing page up to a deployed Azure web app. Picks the smallest stack that fits, creates the layout, sets up the environment, then writes and verifies the README.
---

# Project bootstrap

Turns "I want to build X" into a repo someone else can clone and run.

## Operating rules

- **Pick the smallest thing that works.** A one-file script beats a package. A single HTML
  file beats a framework. Add structure when something forces it, not in anticipation.
- **Ask at most two questions**, and only if the answer changes the stack. Otherwise pick
  a sensible default, say which default you picked and why, and carry on.
- **Never scaffold a folder you do not fill.** Empty `src/`, `tests/`, `utils/` with
  nothing in them are noise.
- **Set the environment up for real.** Actually create the venv, actually install the
  dependencies, actually run the thing once. The README is written from what happened, not
  from what should happen.
- Finish with the `readme-writer` skill. Bootstrapping is not done when the code exists,
  it is done when the README is verified.

## Workflow

### 1. Classify

Match the request to a track. When two fit, take the simpler one.

| Signal in the request | Track | Reference |
|---|---|---|
| "script", "automate", "parse", "scrape", "one-off" | Python script | `references/python-script.md` |
| "explore", "analyse", "chart", "dataset", "notebook" | Notebook | `references/notebook.md` |
| "landing page", "single page", "static", "portfolio" | Static site | `references/static-site.md` |
| "CLI", "tool", "command", "flags" | Python CLI | `references/python-cli.md` |
| "API", "endpoint", "backend", "webhook" | FastAPI service | `references/python-web.md` |
| "web app", "dashboard", "login", "users", "hosted" | Web app | `references/python-web.md` |
| "deploy", "Azure", "production", "hosting" | Add a deploy track on top | `references/azure.md` |

State the choice in one line before building: "One Python script, no package, because
there is a single entry point and no reusable API."

### 2. Spec, if it is bigger than one sitting

Anything with more than about three moving parts gets `docs/spec.md` first, via the
`spec-first` skill. A notebook or a landing page does not need one.

### 3. Scaffold

Follow the track's reference file. Common to all of them:

```
README.md            written last, from templates/README.template.md
.gitignore           populated for the stack, before the first run creates artefacts
.env.example         only if the code reads env vars
docs/spec.md         only if a spec was written
```

Do not copy `.github/skills/`, `templates/` or `scripts/readme_check.py` out of this repo
into a subfolder. They stay at the repo root and serve every project in it.

### 4. Verify

The bar is a cold clone. Minimum, before writing the README:

```bash
rm -rf .venv                    # or node_modules, or dist
# ... run the quickstart you are about to document, in order, from scratch
```

Capture the exact output of the run. Success lines go in the README so the reader can
tell whether it worked. Errors you hit go in `## Troubleshooting` with the fix.

### 5. Document

Load the `readme-writer` skill. Then:

```bash
python3 scripts/readme_check.py
```

### 6. Hand back

Report, in this order: what was built, the one command to run it, what to look at first,
and anything left undone (in `TASKS.md`, not buried in chat).

## Git

Initialise if there is no `.git`, and commit once the first verified run is done, not
before.

```bash
git init && git add -A && git commit -m "Initial scaffold"
```

Check nothing sensitive is staged first:

```bash
git status --short && git check-ignore -q .env && echo ".env ignored"
```
