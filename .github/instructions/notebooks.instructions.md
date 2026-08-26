---
applyTo: "**/*.ipynb"
---

# Notebooks

- **Never commit outputs.** They bloat diffs and they leak data. Install the git filter
  once per clone:

  ```bash
  python -m pip install nbstripout && nbstripout --install
  ```

- First cell is markdown: the question the notebook answers, the data source, the date, and
  any assumption a reader would otherwise have to infer.
- Second cell is imports and paths. Every path relative to the notebook. Never absolute,
  never `/Users/...`.
- The notebook must run clean from a restarted kernel, top to bottom. Verify it rather than
  assuming it:

  ```bash
  jupyter execute <notebook>.ipynb
  ```

- The venv needs a registered kernel, and the README quickstart must contain that line:

  ```bash
  python -m ipykernel install --user --name <slug> --display-name "Python (<project>)"
  ```

- No secrets in cells. Read them from `.env` with `python-dotenv`.
- A function used more than twice moves to a `helpers.py` beside the notebook and gets
  imported. Notebooks are for narrative, not for library code.
- Markdown between sections says what the next cells show and what to conclude. A notebook
  of bare code cells is a script with worse ergonomics.
- Charts get axis labels and units. Every one.
- **Averaging engagement-style or long-tailed metrics is a defect, not a style choice.**
  One viral row drags the mean orders of magnitude above the median. Use the median and say
  why. Similarly, a `0` from an API often means "hidden", not "zero", so check before it
  enters an average.
