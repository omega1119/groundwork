# Terraform

Terraform is not installed on this machine. Homebrew reports the formula lives in a tap,
so install it before running anything here:

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform version
```

## Layout

```
infra/
  main.tf                 resources and module calls
  variables.tf            every input, with description and type
  outputs.tf              every output
  providers.tf            provider blocks and required_providers
  backend.tf              remote state, decided before the first apply
  terraform.tfvars        defaults, no secrets
  environments/
    dev.tfvars
    prod.tfvars
```

Split `main.tf` when it passes a few hundred lines, by domain (`network.tf`, `data.tf`),
not by resource type. A local `modules/` folder earns its place at the second caller, not
the first.

## Worked example

Module version checked against the registry on the day of writing. Look it up again rather
than copying `0.9.0` forward:

```bash
curl -s https://registry.terraform.io/v1/modules/Azure/avm-res-storage-storageaccount/azurerm/versions \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["modules"][0]["versions"][-1]["version"])'
```

```hcl
terraform {
  required_version = "~> 1.9"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "storage" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "0.9.0"

  name                          = var.storage_account_name
  resource_group_name           = azurerm_resource_group.this.name
  location                      = azurerm_resource_group.this.location
  account_replication_type      = "LRS"
  public_network_access_enabled = false
}
```

Variables carry a type and a description, always:

```hcl
variable "storage_account_name" {
  description = "Globally unique storage account name, 3 to 24 lowercase alphanumerics."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Must be 3 to 24 lowercase letters and digits."
  }
}
```

## State

Decide this before the first `apply`, not after.

- **Local state is single-user only.** The second person to run `apply` against local
  state recreates everything, because their state file is empty.
- Remote state goes in an Azure Storage account with versioning and soft delete on, in its
  own resource group that Terraform does not manage. Bootstrapping the backend with the
  same config that uses it is a chicken-and-egg problem, so create it by hand or in a
  separate root module.
- Never commit `terraform.tfstate` or `*.tfstate.backup`. State contains secrets in
  plaintext regardless of `sensitive = true`, which only masks CLI output.

`.gitignore` for a Terraform root:

```gitignore
.terraform/
.terraform.lock.hcl.bak
*.tfstate
*.tfstate.*
crash.log
*.tfvars.local
tfplan
```

Commit `.terraform.lock.hcl`. It pins provider hashes and is the reason two machines
resolve the same versions.

## Verification

```bash
terraform fmt -check -recursive     # formatting, fails loudly rather than reformatting
terraform init -backend=false       # resolves modules and providers, touches no state
terraform validate                  # types, references, required arguments
```

Those three need no credentials, so they belong in CI on every pull request. Then, with
credentials:

```bash
az login
terraform init
terraform plan -out=tfplan
terraform show tfplan               # read it, especially the destroy lines
terraform apply tfplan              # applies exactly what was reviewed
```

Applying a saved plan file rather than re-planning is the difference between reviewing a
change and reviewing a different change.

Teardown:

```bash
terraform destroy
```

## Conventions

- **Pin the provider with `~>`, pin modules exactly.** `~> 4.0` accepts patches and minors,
  which is right for a provider. A module pin should be a single version so an upgrade is
  a commit.
- **`sensitive = true` on secret outputs**, and understand its limit: it hides the value in
  CLI output and in nothing else.
- **No `count` where `for_each` fits.** `count` keys resources by list index, so removing
  the first element renumbers and destroys everything after it. `for_each` keys by a stable
  string.
- **One provider block, configured once.** Aliased providers for a second subscription or
  tenant, never a second unaliased block.
- **Tag everything from a single `local.tags` map** merged into each resource, so a tagging
  policy change is one edit.
- **Never use `-auto-approve` outside a pipeline** that has already shown a reviewed plan.

## Gotchas

- **`terraform init` without `-backend=false` will try to reach the backend** and fail in
  CI with a credentials error that looks like a syntax problem.
- **`azurerm` v4 made `subscription_id` required** on the provider block or via
  `ARM_SUBSCRIPTION_ID`. An upgrade from v3 fails at plan with an unhelpful message.
- **Renaming a resource in code destroys and recreates it** unless you `terraform state mv`
  or add a `moved` block first.
- **A resource changed in the portal drifts silently** until the next plan, which then
  proposes to undo the change. Plan output is the drift report; read it rather than
  skimming for the green lines.
- **Deleting a `for_each` key deletes the resource.** Reordering a map does not, which is
  exactly why `for_each` beats `count`.
