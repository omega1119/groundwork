# Track: Python script

One entry point, run by a human on demand. No package, no `src/`, no `__init__.py`.

## Layout

```
main.py               or a name that says what it does: fetch_prices.py
requirements.txt      pinned, even for one dependency
.env.example          only if the script reads env vars
.gitignore
README.md
data/                 only if it reads or writes files, and git-ignored if the data is real
```

Add `tests/test_main.py` the moment there is logic worth protecting, which usually means
any parsing or arithmetic. A script that only calls an API and prints does not need one.

## Setup, actually run these

```bash
python3 --version                      # record what this prints, it goes in the README
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests         # whatever is genuinely needed
python -m pip freeze > requirements.txt
```

Inside an activated venv, `python` and `pip` are correct. Outside it, use `python3`. The
README quickstart must respect that distinction line by line.

## Conventions

- `if __name__ == "__main__": main()` even for a small script, so it can be imported by a
  test.
- Read configuration from `os.environ` with an explicit failure when a required key is
  missing. A `KeyError` traceback is a worse message than
  `raise SystemExit("Set API_KEY in .env")`.
- Use `argparse` as soon as there is more than one input. Then the README's Usage section
  is a transcript of `--help`, which cannot drift.
- Long runs print progress. A silent script that takes four minutes reads as hung. Note
  that Python block-buffers stdout when piped, so run with `python -u` when piping.
- Write output to a path passed in, not a hardcoded one.

## .gitignore

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
data/
output/
.DS_Store
```

If `data/` holds real personal data, keep the ignore by extension too (`*.csv`, `*.json`)
so a new folder cannot leak by accident.

## README notes

Quickstart block: `templates/quickstart/python-venv.md`.

Usage section: paste the real `--help` output, then one worked example with real-looking
arguments and a line describing what it writes or prints.
