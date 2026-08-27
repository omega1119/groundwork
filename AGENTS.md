# Agent instructions

The project conventions live in [.github/copilot-instructions.md](.github/copilot-instructions.md).
Read that file first. It is the source of truth for every agent working in this repo,
whatever tool you are running under.

Procedures that are too long to keep loaded are in `.github/skills/<name>/SKILL.md`:

| Skill | Load it when |
|---|---|
| `project-bootstrap` | Starting a new project or adding a new component. |
| `readme-writer` | Creating a README, or changing how the project is set up or run. |
| `spec-first` | The request is vague, or the work is bigger than one sitting. |
| `iac-templating` | Writing or reviewing Bicep or Terraform under `infra/`. |

Two more are vendored from other repositories, pinned in `.github/skills/vendored.json`.
They carry a `PROVENANCE.md` and the upstream MIT licence. Do not edit them by hand.

| Skill | Load it when | Upstream |
|---|---|---|
| `design-taste-frontend` | Building a landing page, portfolio or redesign. | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) |
| `swiftui-expert-skill` | Writing or reviewing SwiftUI. | [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) |

```bash
python3 scripts/vendor_skills.py --check
```

Short version, if you read nothing else:

1. Write `docs/spec.md` before the code when the task is bigger than a single file.
2. Build the thing.
3. Rewrite `README.md` from `templates/README.template.md` with real values.
4. **Run every command you wrote in the README.** Fix the README, not your memory of it.
5. `python3 scripts/readme_check.py` must pass.
6. Never use em dashes.
