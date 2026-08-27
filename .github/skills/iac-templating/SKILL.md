---
name: iac-templating
description: Use when creating, reviewing or restructuring Azure infrastructure as code in Bicep or Terraform. Picks one language and records why, reuses Azure Verified Modules instead of hand-writing resources, enforces a build/lint/what-if gate before anything is deployed, and defines what the README must say about infrastructure.
---

# IaC templating

Owns the **shape** of an `infra/` folder and the **gate** it has to pass. It does not own
the deploy itself, and it does not try to replace the deep Azure skills already in the
environment.

| Need | Where it lives |
|---|---|
| Layout, language choice, module reuse, verification gate, README contract | This skill |
| Scaffold an azd project, `azure.yaml`, first-cut infra | `azure-prepare` |
| Enterprise topology: hub and spoke, landing zones, private endpoints | `azure-enterprise-infra-planner` |
| Preflight, RBAC review, what-if analysis | `azure-validate` |
| Run the deploy and recover from errors | `azure-deploy` |
| Pick a role, least privilege | `azure-rbac` |
| Reverse engineer IaC from resources that already exist | `Azure IaC Exporter` agent |

If the request is "stand up a new app on Azure", start with `azure-prepare` and use this
skill to review what it produced. If the request is "our infra folder is a mess" or "write
me a module for X", start here.

## Operating rules

1. **One language per repo.** Bicep or Terraform, chosen once, recorded in
   `docs/decisions/`. A repo with both is a repo where nobody knows which one is true.
2. **Reuse before authoring.** Check for an Azure Verified Module first. Hand-written
   resource blocks are the exception and need a one-line reason in the file.
3. **Pin every version.** Module versions, provider versions, API versions. An unpinned
   module is a deployment that changes without a commit.
4. **Never write a magic constant from memory.** Role definition GUIDs, API versions, SKU
   names and module versions all look plausible when wrong and fail only at deploy time.
   Look each one up. See [Constants you must look up](#constants-you-must-look-up).
5. **The gate runs before you claim it works.** Build, lint, then what-if or plan. A
   template that has never been compiled is a draft.
6. **No secrets in parameter files.** `@secure()` in Bicep, `sensitive = true` in
   Terraform, values from Key Vault or the deployment environment. A secret in a
   `.bicepparam` or `.tfvars` committed to git is a rotation job, not a typo.
7. **Document the teardown.** Infrastructure that bills and has no documented delete is a
   trap.

## Workflow

### 1. Choose the language

Ask once, then stop asking.

| Signal | Choose |
|---|---|
| Azure only, and the team is Microsoft-shop | Bicep |
| `azd` is in play, or the template came from `awesome-azd` | Bicep |
| Deploying to more than one cloud, or alongside Cloudflare, GitHub, Datadog | Terraform |
| A state file and a plan/apply review step are wanted | Terraform |
| Nobody has an opinion and it is Azure only | Bicep, because there is no state to manage |

Write the choice into `docs/decisions/` as a short ADR. Two sentences of reasoning is
enough. The point is that the next person does not silently reverse it.

### 2. Find the module before writing the resource

Azure Verified Modules (AVM) are Microsoft-maintained, tested and versioned for both
languages. Browse at <https://azure.github.io/Azure-Verified-Modules/> and search the
index at <https://azure.github.io/Azure-Verified-Modules/indexes/>.

Get the current version. **Sort the Bicep tags with `sort -V`**: the registry returns them
in publication order, so a plain `tail` hands you `0.9.1` when the latest is `0.33.0`.

```bash
# Bicep, from the Microsoft Container Registry
curl -s https://mcr.microsoft.com/v2/bicep/avm/res/storage/storage-account/tags/list \
  | python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin)["tags"]))' \
  | sort -V | tail -3
```

```bash
# Terraform, from the public registry
curl -s https://registry.terraform.io/v1/modules/Azure/avm-res-storage-storageaccount/azurerm/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["modules"][0]["versions"][-1]["version"])'
```

Swap the resource segment for the one you need: `avm/res/<provider>/<resource>` for Bicep,
`avm-res-<provider>-<resource>` for Terraform.

Write a hand-rolled resource only when no module exists or the module cannot express what
is needed. Say which, in a comment, on the resource.

### 3. Lay the folder out

Details per language:

- Bicep: `references/bicep.md`
- Terraform: `references/terraform.md`

Both follow the same principle: one entry point, one file per logical grouping, parameters
separated from templates, one file per environment. Do not create a `modules/` folder until
there is a second caller.

### 4. Run the gate

Nothing is "done" until this passes. Run it, paste what it printed.

**Bicep**, needs the Azure CLI only:

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null   # compiles
az bicep lint --file infra/main.bicep                         # silent means clean
az deployment group what-if \
  --resource-group <rg> \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

**Terraform**:

```bash
terraform fmt -check -recursive
terraform init -backend=false     # syntax and module resolution, no state touched
terraform validate
terraform plan -out=tfplan        # needs credentials and a backend
```

`what-if` and `plan` are the ones that matter. Build and lint prove the file parses; only
what-if and plan tell you what will happen to the subscription. Read the delete lines.

### 5. Write the README section

Copy `templates/quickstart/iac.md` into the README and fill it with real values. The
`readme-writer` skill owns the rest of the file.

## Constants you must look up

These fail at deploy, not at build, which is the expensive place to find out.

| Constant | How to check |
|---|---|
| Role definition GUID | `az role definition list --name "Storage Blob Data Reader" --query '[0].name' -o tsv` |
| Resource API version | `az provider show --namespace Microsoft.Storage --query "resourceTypes[?resourceType=='storageAccounts'].apiVersions[0]" -o tsv` |
| SKU name and regional availability | `az vm list-skus --location uksouth --size Standard_D2 -o table` (or the service equivalent) |
| Region name | `az account list-locations --query "[].name" -o tsv` |
| AVM module version | The two `curl` commands above |

## Failure modes seen in the wild

- A `main.bicep` that was never compiled, committed alongside a README claiming it
  deploys.
- Terraform state left as a local file, so the second person to run `apply` recreates
  everything the first person made.
- An AVM module pinned to `latest`, or not pinned at all, so a deploy that worked in March
  breaks in April with no commit in between.
- `allowBlobPublicAccess` left at its default because nobody set it. Set the security
  properties explicitly even when the default is already correct, so a default change does
  not silently open the account.
- Control-plane RBAC granted, data-plane permission forgotten. Cosmos
  `sqlRoleAssignments` do not appear in `az role assignment list`, and the app returns 404
  rather than 403, which reads as broken code.
- A parameter file per environment that drifted, so prod has a parameter dev does not.
  Diff them as part of review.
- Terraform `azurerm` provider left unpinned, picking up a major version bump on the next
  `init`.
