---
mode: agent
description: Start a new project in this repo, from a one-file script to a deployed web app, and finish with a verified README.
---

Start a new project. The request follows, or ask for it if it is missing:

${input:idea:What do you want to build?}

Load the `project-bootstrap` skill in `.github/skills/project-bootstrap/SKILL.md` and
follow it. In short:

1. **Classify** the request against the track table and say in one line which track you
   picked and why. Prefer the simpler track when two fit.
2. **Ask at most two questions**, and only if the answer changes the stack. Otherwise pick
   a default, name it as a default, and continue.
3. Write `docs/spec.md` first if this is bigger than one sitting. Skip it for a notebook or
   a landing page, and say that you are skipping it.
4. **Scaffold, then actually set the environment up and run it.** Create the venv, install
   the dependencies, execute the entry point. Do not describe steps you have not run.
5. Write `.gitignore` before the first run creates artefacts.
6. Write `README.md` from `templates/README.template.md` using the `readme-writer` skill,
   with the matching block from `templates/quickstart/` and real values throughout.
7. Verify:

   ```bash
   python3 scripts/readme_check.py
   ```

8. Report: what was built, the single command to run it, what to look at first, and
   anything deferred (write those to `TASKS.md`).

Rules that are not negotiable: every command in the README has been executed, no
placeholders survive, no em dashes anywhere.
