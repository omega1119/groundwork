---
name: readme-writer
description: Use when creating or updating a README, or whenever a change affects how a project is installed, configured, run, tested or deployed. Owns the README contract, the per-stack quickstart blocks (Python venv, notebooks, Node, static site, Azure web app, Docker) and the rule that every documented command must be executed before it is written down.
---

# README writer

A README is a contract with a stranger holding a fresh clone and no context. It succeeds
only if they get to a running project without asking a question.

## Operating rules

1. **Start from `templates/README.template.md`.** Same sections, same order. Do not
   improvise a structure.
2. **Every placeholder gets a real value.** No `<project name>`, no `TODO`, no "coming
   soon". If a section does not apply, write one line saying so and why, for example
   "No configuration. The script takes everything from the command line."
3. **Run the commands.** Every line in Quickstart, Usage and Development gets executed in
   the terminal before it goes in the file. This is the whole point of the skill.
4. **Read the code for the real values.** Entry point filename, the actual CLI flags from
   the argparse block, the env vars the code reads, the port the server binds, the Python
   version in `.python-version` or `pyproject.toml`. Never write these from memory.
5. **Both platforms for activation.** macOS/Linux and Windows PowerShell, always.
6. Keep it short. A single-script project has a README of about 40 lines. Length is not
   thoroughness.
7. No em dashes.

## Workflow

### Creating a README

1. Establish the facts. Do not guess any of them:

   ```bash
   python3 --version
   node --version 2>/dev/null
   ls -a                                   # what is actually in the root
   cat pyproject.toml requirements.txt package.json 2>/dev/null
   grep -n "argparse\|add_argument\|os.environ\|getenv" -r . --include=*.py | head -30
   ```

2. Copy `templates/README.template.md` to `README.md`.
3. Paste the matching block from `templates/quickstart/` into the Quickstart section, then
   substitute the real values into it.
4. Fill the rest of the sections. Delete optional sections that do not apply rather than
   leaving them empty.
5. Verify, from a clean state, in the terminal:

   ```bash
   python3 scripts/readme_check.py
   ```

6. Then actually walk it. The high-value check is deleting `.venv/` and running the
   quickstart start to finish. Do it whenever the setup story changed.

### Updating a README

Triggered by: a new dependency, a new env var, a renamed entry point, a new test command,
a changed port, a new deploy step, a bumped language version.

Change the affected lines and re-run them. Do not rewrite sections you did not touch.

## The contract

Required sections, in this order:

| Section | Must contain |
|---|---|
| `# Name` | Then one paragraph, plain English, what it does and for whom. No preamble. |
| `## Requirements` | Exact versions, and how to check each one. |
| `## Quickstart` | Clone to running, copy-pasteable, both platforms. Ends with what success looks like. |
| `## Usage` | The real invocations with real arguments, and the output shape. |
| `## Project layout` | A table or tree of the files that matter. Not every file. |
| `## Configuration` | Every env var: name, what it does, default, required or not. Or "None". |
| `## Development` | Tests, lint, formatting. The exact commands. |

Optional, in this order after the above: `## Deployment`, `## How it works`,
`## Troubleshooting`, `## Roadmap`, `## License`.

`## Troubleshooting` earns its place the moment you hit an error while verifying. If the
setup broke for you, it will break for them. Write down the error text and the fix.

## Quickstart quality bar

A quickstart passes if all of these hold:

- It starts from `git clone` and ends with something observable: a URL, a printed line, a
  written file.
- Every command can be pasted without editing, except values that are genuinely per-user
  (an API key, a subscription ID). Those are visibly marked and explained in Configuration.
- The interpreter or runtime version is stated, and the command to install or check it is
  given.
- Environment setup is separated from running, so a returning reader can skip to the run.
- It tells the reader what success looks like: "prints `Ready on http://127.0.0.1:8000`".

## Per-stack blocks

Copy from `templates/quickstart/`:

| File | Use for |
|---|---|
| `python-venv.md` | Any Python script, CLI or library. |
| `notebook.md` | Jupyter, including kernel registration and output stripping. |
| `static-site.md` | A single HTML page or a plain HTML/CSS/JS site. |
| `node-web.md` | Node, Vite, Next, anything with `package.json`. |
| `docker.md` | Anything containerised. |
| `azure-webapp.md` | Deployed to Azure App Service or Container Apps. |

## Failure modes seen in the wild

- Documenting `pip install -r requirements.txt` when the file does not exist. Create the
  file or change the line.
- `source .venv/bin/activate` on a repo whose venv is at `env/`. Match reality.
- `python` instead of `python3` on macOS, where bare `python` is often missing.
- A port number that came from a different project.
- A `## Configuration` table listing env vars the code never reads, or missing one it
  requires and crashes without.
- Notebook instructions with no kernel step, so the reader opens a notebook that cannot
  execute.
- An `npm run dev` that is not in `package.json` scripts.
