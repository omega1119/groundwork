---
mode: agent
description: Bring the README back in line with what the project actually does, verifying every command.
---

Update `README.md` so it matches reality. Load the `readme-writer` skill in
`.github/skills/readme-writer/SKILL.md`.

Establish the facts from the code, never from memory:

```bash
ls -a
python3 --version
cat requirements.txt pyproject.toml package.json 2>/dev/null
grep -rn "add_argument\|os.environ\|getenv\|uvicorn.run\|app.run\|PORT" . \
  --include=*.py --include=*.js --include=*.ts | head -40
```

Then:

1. Compare the README against `templates/README.template.md`. Add missing required
   sections, fix the order, remove sections that no longer apply.
2. Fix every command that has drifted: entry point names, script names, ports, flags, env
   var names, language versions.
3. **Run each command in Quickstart, Usage and Development.** Fix the README where it is
   wrong. If a command fails, that is a finding, not an inconvenience: either fix the
   project or document the real command.
4. Make `## Configuration` agree exactly with what the code reads and with `.env.example`.
   When they disagree, the code is right.
5. Add anything you hit while verifying to `## Troubleshooting`, with the error text.
6. Verify:

   ```bash
   python3 scripts/readme_check.py
   ```

Report which lines were wrong and why, so the drift is visible rather than quietly
patched. Do not rewrite sections you did not need to touch.
