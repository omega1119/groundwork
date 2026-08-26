#!/usr/bin/env python3
"""Check a README against the contract in templates/README.template.md.

Usage:
    python3 scripts/readme_check.py                 # checks ./README.md
    python3 scripts/readme_check.py path/to/README.md ...

Exit code 0 if every file passes, 1 otherwise. Runs on the standard library alone so it
works before any environment has been set up.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "Requirements",
    "Quickstart",
    "Usage",
    "Project layout",
    "Configuration",
    "Development",
]

PLACEHOLDER = re.compile(r"<([^<>\n]{1,80})>")
BRACES = re.compile(r"\{\{[^}]{1,80}\}\}")
LEFTOVERS = re.compile(r"\b(TODO|FIXME|TBD|Lorem ipsum|coming soon)\b", re.IGNORECASE)
HEADING = re.compile(r"^##\s+(.*?)\s*$")

# Deliberately a whitelist. A loose pattern reads "<Project name>" as markup and lets the
# placeholder through, which is the failure this whole script exists to prevent.
HTML_TAG = re.compile(
    r"^/?(a|b|br|code|details|div|em|h[1-6]|hr|i|img|kbd|li|ol|p|pre|s|small|span"
    r"|strong|sub|sup|summary|table|tbody|td|th|thead|tr|ul)(\s[^<>]*)?/?$",
    re.IGNORECASE,
)


def split_fences(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """Return (prose_lines, all_lines) as (line_number, line) pairs.

    Prose excludes fenced code blocks, because <angle-bracket> arguments are legitimate
    inside a command example.
    """
    prose: list[tuple[int, str]] = []
    every: list[tuple[int, str]] = []
    in_fence = False
    for n, line in enumerate(text.splitlines(), start=1):
        every.append((n, line))
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            prose.append((n, line))
    return prose, every


def is_placeholder(inner: str) -> bool:
    lowered = inner.strip().lower()
    if lowered.startswith(("http://", "https://", "mailto:", "!--")) or "@" in lowered:
        return False
    return not HTML_TAG.match(lowered)


def check(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    prose, every = split_fences(text)
    lines = text.splitlines()

    body = [line for line in lines if line.strip()]
    if not body:
        return ["file is empty"]

    if not body[0].startswith("# "):
        problems.append("line 1 must be the project name as an H1, for example '# Thing'")
    elif len(body) < 2 or body[1].startswith("#"):
        problems.append("the H1 must be followed by a one-paragraph summary before the first '##'")

    found = [m.group(1) for _, line in prose if (m := HEADING.match(line))]
    missing = [s for s in REQUIRED if s not in found]
    if missing:
        problems.append("missing required sections: " + ", ".join(missing))

    present = [s for s in REQUIRED if s in found]
    order = [found.index(s) for s in present]
    if order != sorted(order):
        problems.append("required sections are out of order, expected: " + " then ".join(REQUIRED))

    for n, line in prose:
        for match in PLACEHOLDER.finditer(line):
            if is_placeholder(match.group(1)):
                problems.append(f"line {n}: unfilled placeholder <{match.group(1)}>")
        stripped = line.lstrip("-* ").strip()
        if stripped.startswith("<") and ">" not in stripped and is_placeholder(stripped[1:]):
            problems.append(f"line {n}: unfilled placeholder block starting '{stripped[:40]}...'")
        if BRACES.search(line):
            problems.append(f"line {n}: unfilled placeholder {BRACES.search(line).group(0)}")
        if match := LEFTOVERS.search(line):
            problems.append(f"line {n}: leftover '{match.group(0)}' from the template")

    for n, line in every:
        if "\u2014" in line:
            problems.append(f"line {n}: em dash. Use a comma, colon, full stop or parentheses")

    quickstart = section_body(lines, "Quickstart")
    if quickstart is None:
        pass  # already reported as missing
    elif "```" not in "\n".join(quickstart):
        problems.append("Quickstart has no command block. It must be copy-pasteable")
    else:
        problems.extend(check_quickstart(path, "\n".join(quickstart)))

    return problems


def section_body(lines: list[str], name: str) -> list[str] | None:
    start = None
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m and m.group(1) == name:
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return lines[start:end]


def check_quickstart(path: Path, block: str) -> list[str]:
    """Cross-check the documented setup against what the project actually contains."""
    problems: list[str] = []
    root = path.parent

    has_python = any(
        (root / f).exists() for f in ("requirements.txt", "pyproject.toml", "environment.yml")
    ) or any(root.glob("*.py"))
    if has_python:
        if "venv" not in block and "uv " not in block and "conda" not in block:
            problems.append("Quickstart never creates an environment, but this is a Python project")
        if "Activate.ps1" not in block and "uv " not in block:
            problems.append("Quickstart has no Windows PowerShell activation line")
        if "requirements.txt" in block and not (root / "requirements.txt").exists():
            problems.append(
                "Quickstart installs requirements.txt, which does not exist in this folder"
            )

    if (root / "package.json").exists() and "npm" not in block and "pnpm" not in block:
        problems.append("package.json exists but Quickstart never installs dependencies")

    if any(root.glob("*.ipynb")) and "ipykernel" not in block:
        problems.append(
            "notebook project with no 'ipykernel install' step, so the reader gets no kernel"
        )

    if (root / ".env.example").exists() and ".env" not in block:
        problems.append(".env.example exists but Quickstart never tells the reader to copy it")

    return problems


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv[1:]] or [Path("README.md")]
    failed = False

    for path in targets:
        if not path.exists():
            print(f"FAIL {path}: does not exist")
            failed = True
            continue
        problems = check(path)
        if problems:
            failed = True
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"ok   {path}")

    if failed:
        print("\nSee templates/README.template.md and the readme-writer skill.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
