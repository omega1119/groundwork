# Quickstart block: infrastructure as code

Goes in `## Deployment`, after the local quickstart. Local first, always. Pairs with
`azure-webapp.md` when there is an app on top of the infrastructure.

Use the Bicep half or the Terraform half, not both. Delete the one you are not using.

---

## Infrastructure

Defined in `infra/`, using <Bicep / Terraform> with Azure Verified Modules. The choice is
recorded in [docs/decisions/<nnnn>-<slug>.md](docs/decisions/<nnnn>-<slug>.md).

| Thing | Value |
|---|---|
| Subscription | `<subscription-id>` |
| Resource group | `<rg-name>` |
| Region | `<region>` |
| State | `<local / azurerm backend in stterraformstate001>` |
| Entry point | `infra/main.bicep` |

### Prerequisites

```bash
az version          # <the version you tested with>
az login
az account set --subscription <subscription-id>
```

### Check the templates

<!-- Bicep -->

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

Both are silent on success. `az bicep lint` printing nothing means clean, not skipped.

<!-- Terraform -->

```bash
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra init -backend=false
terraform -chdir=infra validate
```

Expect `Success! The configuration is valid.`

### Preview the change

<!-- Bicep -->

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

<!-- Terraform -->

```bash
terraform -chdir=infra init
terraform -chdir=infra plan -out=tfplan
```

Read the delete lines before continuing.

### Apply

<!-- Bicep -->

```bash
az deployment group create \
  --resource-group <rg-name> \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

<!-- Terraform -->

```bash
terraform -chdir=infra apply tfplan
```

Takes about <n> minutes on a first run.

### Tear it down

This deletes everything in the group and cannot be undone:

```bash
az group delete --name <rg-name> --yes --no-wait
```

<!-- Terraform -->

```bash
terraform -chdir=infra destroy
```

---

## Notes for whoever fills this in

- **Real names, real subscription id, real region.** This table is what someone reads at
  2am when the thing is down.
- **State location is not optional information for Terraform.** A reader who runs `apply`
  against the wrong backend recreates production. Say where the state lives and who can
  reach it.
- **Say which module versions are pinned and where.** A reader upgrading a module wants to
  know that the pin is deliberate.
- **Never paste a parameter file containing a secret into the README.** List the secret
  parameter names and say where the values come from, for example "read from Key Vault
  `kv-example-01` at deploy time".
- Document the teardown, always, and put it last so nobody runs it by accident while
  skimming.
- The `iac-templating` skill owns the folder layout and the verification gate.
  `azure-validate` and `azure-deploy` own the deployment itself. This block only covers
  what the README has to end up saying.
