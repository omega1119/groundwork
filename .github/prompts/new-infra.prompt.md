---
mode: agent
description: Create or review an infra/ folder in Bicep or Terraform, with Azure Verified Modules and a verification gate that actually runs.
---

Work on infrastructure as code. The request follows, or ask for it if it is missing:

${input:request:What infrastructure do you need, or what should be reviewed?}

Load the `iac-templating` skill in `.github/skills/iac-templating/SKILL.md` and follow it.
In short:

1. **Check what already exists.** `ls infra/`, read `docs/decisions/` for a prior language
   choice. Do not introduce a second IaC language into a repo that already has one.
2. **Pick Bicep or Terraform** against the decision table, say why in one line, and write
   an ADR into `docs/decisions/` if there is not one already.
3. **Look for an Azure Verified Module before writing any resource block.** Get the
   current version from the registry with the `curl` commands in the skill, and pin it.
   Sort Bicep tags with `sort -V`, the registry does not return them in version order.
4. **Look up every magic constant.** Role definition GUIDs, API versions, SKU names and
   region names, using the commands in the skill. Never write one from memory.
5. **Run the gate and paste what it printed.** `az bicep build` and `az bicep lint`, or
   `terraform fmt -check` / `init -backend=false` / `validate`. Then `what-if` or `plan`
   against the real subscription if credentials are available, and read the delete lines.
6. **Update the README** with the block in `templates/quickstart/iac.md`, real values
   throughout, including the teardown command.
7. Verify:

   ```bash
   python3 scripts/readme_check.py
   ```

Rules that are not negotiable: nothing is reported as working until it has compiled, no
secrets in parameter or tfvars files, every module and provider version pinned, teardown
documented, no em dashes.
