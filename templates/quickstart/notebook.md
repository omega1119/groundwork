# Quickstart block: Jupyter notebook

---

## Quickstart

Needs Python <3.13> or newer. Check with `python3 --version`.

```bash
git clone <repo-url>
cd <repo-name>

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name <project-slug> --display-name "Python (<project>)"
```

On Windows PowerShell, replace the venv and activate lines with:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Then open the notebook:

```bash
jupyter lab <notebook.ipynb>
```

In VS Code, open `<notebook.ipynb>` and pick **Python (<project>)** from the kernel
selector at the top right instead.

Run all cells from the top. Outputs are stripped in git, so a fresh clone shows empty
cells until you run it. The <first chart> appears in <section name>, after about
<duration>.

---

## Notes for whoever fills this in

- **The `ipykernel install` line is not optional.** Without it the reader opens the
  notebook and either finds no interpreter or silently runs against a system Python that
  has none of the dependencies. That failure looks like a broken notebook, not a missing
  step.
- Name the kernel after the project. A machine collects a lot of kernels called "Python 3".
- Say where the data comes from and whether it is in the repo. If it is not, the download
  or export step belongs here, before the run step.
- Say how long a full run takes if it is more than a few seconds, and what appears when it
  worked.
- If `nbstripout` is installed, tell the reader outputs are stripped on commit so they are
  not surprised by an empty notebook or a suspiciously small diff.
- Verify the notebook runs clean from a restarted kernel before writing any of this:

  ```bash
  jupyter execute <notebook.ipynb>
  ```
