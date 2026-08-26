# Track: Python CLI

A tool run repeatedly with different arguments, by someone other than the author.

## Layout

```
cli.py                or a package folder once there is more than one module
requirements.txt
pyproject.toml        only when it needs installing as a command
tests/test_cli.py
README.md
```

## Conventions

- `argparse` with `description=` and `help=` on every argument. Those strings become the
  README's Usage section, so write them for a stranger.
- Subcommands via `add_subparsers(dest="command", required=True)` once there is more than
  one verb.
- Exit codes mean something: `0` success, `1` expected failure with a readable message,
  `2` bad usage (argparse does this itself). Never traceback at a user for bad input.
- `--dry-run` on anything that writes, deletes or spends money. Make it the safe default
  when the action is destructive.
- `--verbose` toggles `logging` level, it does not sprinkle `print`.
- Progress on anything slow, and remember Python block-buffers stdout when piped.

## Installing as a command

Only when the user will run it by name from anywhere. Otherwise `python cli.py` is fine
and simpler to document.

```toml
# pyproject.toml
[project]
name = "toolname"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["click>=8.1"]

[project.scripts]
toolname = "toolname.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```bash
python -m pip install -e .
toolname --help
```

The README then documents `toolname --help`, and must mention the editable install, or the
command does not exist for the reader.

## README notes

Quickstart block: `templates/quickstart/python-venv.md`.

Usage section is the real `--help` output, pasted, plus one worked example per subcommand.
Regenerate it whenever an argument changes:

```bash
python cli.py --help
```
