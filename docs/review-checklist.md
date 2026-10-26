# Review checklist

Questions to put to a diff before calling it done. Each line comes from a trap already
recorded in this repo's rules and instructions, not from a list of things that might go
wrong in theory, because a theoretical checklist gets skimmed. Why it works this way is in
[ADR 0002](decisions/0002-engineering-heuristics.md).

## Before you start

Do not review something that is not ready. These must already hold:

- The code runs, and you ran it in this session.
- `python3 scripts/readme_check.py` and `python3 scripts/readme_check.py --text-only` pass.

Review in a fresh context, or hand it to a second agent, where you can. The author reads
what they meant to write.

## Setup and README

- [ ] Was every command in the README run in this session, as written? No invented flag,
      script name, package name or port.
- [ ] Does every file the Quickstart mentions exist (`requirements.txt`, `.env.example`)?
- [ ] Does the README say `python3` or `python` to match the machine, and does the version
      it claims match `python3 --version`?
- [ ] Is there a Windows PowerShell line next to every macOS and Linux one?
- [ ] Notebooks: is the `ipykernel install` step documented, and is output stripped?
- [ ] Is every new dependency pinned and listed under Requirements?
- [ ] Is every new environment variable in `.env.example` and the Configuration table?
- [ ] Does `.gitignore` cover everything this run created?

## Code

- [ ] Does any `except` swallow the error, return `None`, or catch more than it names?
- [ ] Does a missing required setting stop startup with a message that names it?
- [ ] Does user input reach SQL or a shell command without parameterising?
- [ ] Web apps: is there module-level mutable state shared across requests?
- [ ] Shell: any bash special variable used as a name (`GROUPS`, `UID`, `SECONDS`), or a
      `| head` under `pipefail` without `|| true`?
- [ ] Did this change leave anything dead: an import, a helper, a flag, a file?
- [ ] Is there an abstraction with one caller, or an option nobody asked for?
- [ ] Did the stack, data model, public interface or layout change without agreement and
      an ADR?

## Done when

Every box is ticked or marked n/a. Anything that cannot be fixed now goes in `TASKS.md`
with the reason, in the same turn.

## Growing the list

When a defect reaches a reader, add the question that would have caught it, under the
heading it belongs to. When a question has not caught anything in a long time and a
checker now covers it, delete it. A short list that gets read beats a long one that does
not.
