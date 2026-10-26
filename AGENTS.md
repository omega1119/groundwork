# Agent instructions

The project conventions live in [.github/copilot-instructions.md](.github/copilot-instructions.md).
Read that file first, all of it. It is the source of truth for every agent working in this
repo, whatever tool you are running under. The definition of done and the rules for how to
build are there, and are deliberately not copied here, because two copies drift.

Procedures that are too long to keep loaded are in `.github/skills/<name>/SKILL.md`:

| Skill | Load it when |
|---|---|
| `project-bootstrap` | Starting a new project or adding a new component. |
| `readme-writer` | Creating a README, or changing how the project is set up or run. |
| `spec-first` | The request is vague, or the work is bigger than one sitting. |
| `iac-templating` | Writing or reviewing Bicep or Terraform under `infra/`. |

These are vendored from other repositories, pinned in `.github/skills/vendored.json`. Each
carries a `PROVENANCE.md` and the upstream licence. Do not edit them by hand.

| Skill | Load it when | Upstream |
|---|---|---|
| `design-taste-frontend` | Building a landing page, portfolio or redesign. | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) |
| `swiftui-expert-skill` | Writing or reviewing SwiftUI. | [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) |

Copilot exposes two more kinds of file through its UI. Other tools can read them as plain
procedures:

| Path | What it is |
|---|---|
| `.github/prompts/*.prompt.md` | Step lists behind `/new-project`, `/update-readme`, `/write-spec` and `/new-infra`. When asked for one of those, follow the file. |
| `.github/agents/shipwright.agent.md` | A build-and-verify persona: build the smallest thing, run it, document from the transcript. |
| `.github/instructions/*.instructions.md` | Rules for a file type, scoped by the `applyTo` glob in each header. Read the matching one before editing that kind of file. |
| `docs/review-checklist.md` | Walk the diff through it before reporting done. |

Before reporting done:

```bash
python3 scripts/readme_check.py
python3 scripts/readme_check.py --text-only
python3 scripts/vendor_skills.py --check
```
