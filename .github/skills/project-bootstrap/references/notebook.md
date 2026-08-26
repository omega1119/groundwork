# Track: Notebook

Exploration and analysis, read top to bottom. The failure mode is a notebook that only
runs on the machine it was written on.

## Layout

```
analysis.ipynb        named for the question it answers, not "Untitled"
requirements.txt
data/                 git-ignored if the data is real or large
outputs/              charts and exports, git-ignored
README.md
.gitignore
```

## Setup, actually run these

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyterlab ipykernel pandas matplotlib
python -m ipykernel install --user --name <project-slug> --display-name "Python (<project>)"
python -m pip freeze > requirements.txt
```

**The kernel registration line is the one everybody forgets.** Without it the reader opens
the notebook and finds no interpreter, or silently runs against a system Python that has
none of the dependencies. It goes in the README quickstart, not in a comment.

## Conventions

- First cell is markdown: the question, the data source, the date, and any assumption a
  reader would otherwise have to infer.
- Second cell is imports and paths. Every path relative to the notebook, never absolute,
  never `/Users/...`.
- The notebook must run clean from a restarted kernel, top to bottom. Verify it, do not
  assume it:

  ```bash
  python -m pip install nbclient
  jupyter execute analysis.ipynb
  ```

- **Never commit outputs.** They bloat diffs and they leak data.

  ```bash
  python -m pip install nbstripout
  nbstripout --install          # installs a git filter in this repo
  ```

  Document that the reader's first run will show empty outputs, which is expected.
- Secrets never appear in a cell. Read them from `.env` with `python-dotenv`.
- When a notebook grows a function used more than twice, move it to a `helpers.py` next to
  it and import it. Notebooks are for narrative, not for library code.

## .gitignore

```gitignore
.venv/
.ipynb_checkpoints/
__pycache__/
.env
data/
outputs/
.DS_Store
```

## README notes

Quickstart block: `templates/quickstart/notebook.md`.

Add a `## Data` section describing where the input comes from, whether it is in the repo,
and how to obtain it if it is not. A notebook whose data source is undocumented is a
screenshot.
