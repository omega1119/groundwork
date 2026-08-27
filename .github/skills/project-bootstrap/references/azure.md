# Track: deploying to Azure

Layered on top of an app track, never on its own. Get it running locally and documented
first, then deploy. A deploy that has never run locally has two sets of unknowns.

## Before writing any infrastructure

The environment already carries deep Azure skills. Use them rather than improvising:

| Need | Skill |
|---|---|
| Scaffold infra, `azure.yaml`, Bicep or Terraform | `azure-prepare` |
| `infra/` layout, module reuse, the build/lint/what-if gate | `iac-templating` |
| Pre-deployment checks, RBAC, what-if | `azure-validate` |
| Run the deploy, recover from errors | `azure-deploy` |
| Pick the right role, least privilege | `azure-rbac` |
| Diagnose a broken deploy | `azure-diagnostics` |

This file only covers what those skills do not: what the README must say afterwards.

## Hosting choice

| Shape | Target |
|---|---|
| Static HTML/CSS/JS | Static Web Apps |
| Python or Node web app, no container | App Service (Linux) |
| Containerised, scale to zero | Container Apps |
| Event or timer triggered, short runs | Functions |

Pick one, say why in one line, and record it in `docs/decisions/`.

## Rules that cost time when broken

- **Managed identity, not connection strings.** `DefaultAzureCredential` locally and in
  the cloud. If a key ends up in an app setting, that is a finding, not a shortcut.
- **Never write a built-in role definition GUID from memory.** They look plausible and
  fail at deploy with `RoleDefinitionDoesNotExist`. Verify:

  ```bash
  az role definition list --name "Storage Blob Data Reader" --query '[0].name' -o tsv
  ```

  Same discipline for API versions and SKU names in Bicep.
- **Infrastructure first, app second**, whenever the infrastructure changed. App workflows
  usually trigger on push and infra ones usually do not, so a plain `git push` runs them
  in the wrong order.
- Data-plane permission and control-plane RBAC are different systems. Cosmos
  `sqlRoleAssignments` do not show up in `az role assignment list`. Granting one and not
  the other produces a signed-in user who gets 404 everywhere, which reads as a broken app
  rather than a missing permission.
- Validate before deploying:

  ```bash
  az bicep build --file infra/main.bicep
  ```

- Deployment identity uses OIDC federated credentials in GitHub Actions. No client secrets
  in repository secrets.

## What the README must say

A `## Deployment` section with:

1. Prerequisites: `az` version, the subscription, and how to log in.
2. A resource table: subscription, resource group, region, and every resource name. Real
   values, not placeholders. This is the section people come back for.
3. The first-run order, explicitly, when infra and app deploy separately.
4. The deployed URL.
5. How to see logs, with the actual command:

   ```bash
   az webapp log tail --name <app-name> --resource-group <rg>
   ```

6. How to tear it down. A template that creates billable resources and does not document
   deletion is a trap.

   ```bash
   az group delete --name <rg> --yes --no-wait
   ```
