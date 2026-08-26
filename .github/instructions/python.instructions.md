---
applyTo: "**/*.py"
---

# Python

- Target the version in `.python-version` or `pyproject.toml`. Check what is installed
  before writing a version anywhere: `python3 --version`.
- Standard library first. A dependency has to earn its place, and every one added must be
  pinned in `requirements.txt` and appear in the README's Requirements section.
- Type hints on function signatures. Not on every local.
- `pathlib`, not `os.path`. f-strings, not `%` or `.format`.
- `if __name__ == "__main__": main()` so the module can be imported by a test.
- Read configuration from the environment in one place, and fail at startup with a readable
  message when something required is missing. `raise SystemExit("Set API_KEY in .env")`
  beats a `KeyError` traceback.
- Never interpolate user input into SQL or a shell command. Parameterise queries, and never
  use `subprocess` with `shell=True` on anything a user supplied.
- Catch the specific exception. A bare `except:` swallows `KeyboardInterrupt` and turns a
  bug into a mystery.
- Long runs print progress. Python block-buffers stdout when piped, so use `python -u` or
  `flush=True` when the output goes through a pipe.
- Module-level mutable state is shared across every request in a web app, and across every
  import elsewhere. Treat any module-level dict or list as a bug until proven otherwise.
- Docstrings say why, not what. One line unless the function is genuinely subtle.
- **No em dashes in comments, docstrings or strings.**

## Before saying it works

```bash
python -m pytest -q            # if there are tests
python <entry-point.py>        # actually run it
```

Adding a dependency means re-freezing and re-checking the README in the same turn:

```bash
python -m pip freeze > requirements.txt
python3 scripts/readme_check.py
```
