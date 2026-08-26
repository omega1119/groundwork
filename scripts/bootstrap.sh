#!/usr/bin/env bash
# Create a Python virtual environment and install dependencies.
# Prints the exact commands the README should document, so the two cannot drift.
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "No $PYTHON on PATH. Install Python 3.11 or newer first." >&2
  exit 1
fi

VERSION="$("$PYTHON" --version)"
echo "Using $VERSION"

if [[ -d .venv ]]; then
  echo ".venv already exists, reusing it. Delete it to start clean."
else
  "$PYTHON" -m venv .venv
  echo "Created .venv"
fi

.venv/bin/python -m pip install --upgrade pip --quiet

if [[ -f requirements.txt ]]; then
  .venv/bin/python -m pip install -r requirements.txt
  echo "Installed from requirements.txt"
elif [[ -f pyproject.toml ]]; then
  .venv/bin/python -m pip install -e .
  echo "Installed this project in editable mode"
else
  echo "No requirements.txt or pyproject.toml, nothing to install."
fi

if [[ -f .env.example && ! -f .env ]]; then
  cp .env.example .env
  echo "Copied .env.example to .env. Fill in the values before running."
fi

cat <<'EOF'

Done. The README should document exactly this:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

and on Windows PowerShell:

    py -3 -m venv .venv
    .\.venv\Scripts\Activate.ps1

Activate this shell with:

    source .venv/bin/activate
EOF
