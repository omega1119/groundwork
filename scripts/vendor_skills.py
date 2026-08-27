#!/usr/bin/env python3
"""Vendor third-party agent skills into .github/skills/ at a pinned commit.

Reads .github/skills/vendored.json, downloads each upstream repo as a tarball at the
recorded commit, and copies the named subtree in. Every vendored skill gets a
PROVENANCE.md recording where it came from, so nobody has to guess later whether a file
is ours or upstream's.

Usage:
    python3 scripts/vendor_skills.py             # fetch everything in the manifest
    python3 scripts/vendor_skills.py --check     # verify local copies match the manifest
    python3 scripts/vendor_skills.py swiftui-expert-skill

Standard library only, so it runs before any environment exists. Pinning to a commit
rather than a branch means two clones a year apart get the same files. To take an
upstream update, change the commit in the manifest and re-run.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import sys
import tarfile
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".github" / "skills" / "vendored.json"
SKILLS_DIR = ROOT / ".github" / "skills"
CODELOAD = "https://codeload.github.com/{repo}/tar.gz/{commit}"


def fetch_tarball(repo: str, commit: str) -> tarfile.TarFile:
    url = CODELOAD.format(repo=repo, commit=commit)
    print(f"  fetching {url}")
    with urllib.request.urlopen(url, timeout=120) as response:  # noqa: S310
        payload = response.read()
    print(f"  {len(payload) / 1024:.0f} KB, sha256 {hashlib.sha256(payload).hexdigest()[:12]}")
    return tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz")


def wanted(rel: str, include: list[str]) -> bool:
    return any(rel == pattern or rel.startswith(pattern) for pattern in include)


def extract(tar: tarfile.TarFile, source: str, include: list[str], dest: Path) -> list[str]:
    """Copy the wanted files out of the archive. Returns the relative paths written."""
    # The tarball wraps everything in a single <repo>-<commit> directory.
    root_prefix = tar.getnames()[0].split("/")[0]
    prefix = f"{root_prefix}/{source}/".replace("//", "/")
    written: list[str] = []

    for member in tar.getmembers():
        if not member.isfile() or not member.name.startswith(prefix):
            continue
        rel = member.name[len(prefix) :]
        if not wanted(rel, include):
            continue
        write_member(tar, member, dest, rel)
        written.append(rel)

    # MIT and the other permissive licences require the copyright notice to travel with
    # any substantial copy, and the licence sits at the repo root, outside `source`.
    for member in tar.getmembers():
        if member.isfile() and member.name == f"{root_prefix}/LICENSE":
            write_member(tar, member, dest, "LICENSE.upstream")
            written.append("LICENSE.upstream")
            break
    else:
        raise SystemExit(f"FAIL: no LICENSE at the root of {root_prefix}, refusing to vendor")

    return sorted(written)


def write_member(tar: tarfile.TarFile, member: tarfile.TarInfo, dest: Path, rel: str) -> None:
    target = (dest / rel).resolve()
    # Never let an archive path escape the destination directory.
    if not str(target).startswith(str(dest.resolve()) + "/"):
        raise ValueError(f"refusing unsafe path in archive: {member.name}")
    handle = tar.extractfile(member)
    if handle is None:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(handle.read())


def write_provenance(dest: Path, entry: dict, files: list[str]) -> None:
    total = sum((dest / f).stat().st_size for f in files)
    lines = [
        f"# Provenance: {entry['name']}",
        "",
        "This directory is vendored from another repository. Do not edit it by hand: your",
        "changes will be overwritten the next time the skill is refreshed. To change",
        "behaviour, add a rule under `.github/instructions/`, which takes precedence.",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Upstream | https://github.com/{entry['repo']} |",
        f"| Commit | `{entry['commit']}` |",
        f"| Source path | `{entry['source']}` |",
        f"| Licence | {entry['licence']}, see `LICENSE.upstream` |",
        f"| Vendored on | {date.today().isoformat()} |",
        f"| Files | {len(files)}, {total / 1024:.0f} KB |",
        "",
        "## Refresh",
        "",
        "```bash",
        f"python3 scripts/vendor_skills.py {entry['name']}",
        "```",
        "",
        "Update the `commit` field in `.github/skills/vendored.json` first, otherwise this",
        "re-fetches the same pinned revision.",
        "",
    ]
    (dest / "PROVENANCE.md").write_text("\n".join(lines), encoding="utf-8")


def vendor(entry: dict) -> None:
    dest = SKILLS_DIR / entry["name"]
    print(f"{entry['name']} <- {entry['repo']}@{entry['commit'][:12]}")
    tar = fetch_tarball(entry["repo"], entry["commit"])
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    files = extract(tar, entry["source"], entry["include"], dest)
    if not files:
        raise SystemExit(f"FAIL {entry['name']}: matched no files, check 'source' and 'include'")
    write_provenance(dest, entry, files)
    print(f"  wrote {len(files)} files to {dest.relative_to(ROOT)}")


def check(entry: dict) -> bool:
    """Confirm the vendored copy exists and records the commit the manifest asks for."""
    provenance = SKILLS_DIR / entry["name"] / "PROVENANCE.md"
    if not provenance.exists():
        print(f"FAIL {entry['name']}: not vendored yet")
        return False
    if f"`{entry['commit']}`" not in provenance.read_text(encoding="utf-8"):
        print(f"FAIL {entry['name']}: on disk copy is a different commit to the manifest")
        return False
    print(f"ok   {entry['name']}")
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="skills to vendor, default all")
    parser.add_argument("--check", action="store_true", help="verify without downloading")
    args = parser.parse_args(argv[1:])

    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["skills"]
    if args.names:
        known = {e["name"] for e in entries}
        unknown = set(args.names) - known
        if unknown:
            raise SystemExit(f"not in the manifest: {', '.join(sorted(unknown))}")
        entries = [e for e in entries if e["name"] in args.names]

    if args.check:
        return 0 if all([check(e) for e in entries]) else 1

    for entry in entries:
        vendor(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
