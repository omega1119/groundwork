# Quickstart block: Python with a venv

Substitute the real values before pasting: repo URL, folder name, Python version, entry
point, and the run output. Keep both platforms.

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
```

On Windows PowerShell, the middle three lines are:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Then run it:

```bash
python <entry-point.py>
```

<What success looks like: the line it prints, or the file it writes.>

Later sessions only need the activate line:

```bash
source .venv/bin/activate
```

Leave the virtual environment with `deactivate`.

---

## Notes for whoever fills this in

- The prompt shows `(.venv)` once activated. Say so if the reader is likely new to this,
  because it is the only feedback the activate command gives.
- **Before activation use `python3` and after activation use `python`.** On macOS bare
  `python` often does not exist outside a venv, so the difference is not cosmetic.
- If PowerShell refuses the activate script with an execution policy error, the fix is
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. Put that in
  Troubleshooting, not in the main flow.
- `requirements.txt` must exist and be pinned. Generate it with `python -m pip freeze >
  requirements.txt` after installing, and never document installing a file that is not
  committed.
- If the project needs a version newer than the reader is likely to have, say how to get
  it (`brew install python@3.13`, `uv python install 3.13`, or the python.org installer).
- Using `uv` instead? Then the block is `uv sync` and `uv run <entry-point.py>`, and there
  is no activate step at all. Do not mix the two styles in one README.
