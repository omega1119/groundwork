# Bicep

## Layout

```
infra/
  main.bicep              entry point, one target scope, no resources of its own
  main.bicepparam         default parameters
  main.dev.bicepparam     one per environment, only where they differ
  main.prod.bicepparam
  core/                   only once a second caller exists
    monitoring.bicep
  bicepconfig.json        linter rules, optional but recommended
```

`main.bicep` orchestrates. It declares parameters, calls modules, and emits outputs. If it
declares a `resource` directly, that is usually a sign the resource belongs in a module or
should have been an AVM call.

## Worked example

This compiles and lints clean as written. Verified with Bicep CLI 0.41.2 via
`az bicep`, module version checked against the registry on the day of writing. Look the
version up again rather than copying `0.33.0` forward.

```bicep
targetScope = 'resourceGroup'

@description('Deployment location. Defaults to the resource group location.')
param location string = resourceGroup().location

@description('Globally unique storage account name.')
@minLength(3)
@maxLength(24)
param storageAccountName string

module storage 'br/public:avm/res/storage/storage-account:0.33.0' = {
  name: 'storage-deployment'
  params: {
    name: storageAccountName
    location: location
    skuName: 'Standard_LRS'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
  }
}

output storageAccountId string = storage.outputs.resourceId
```

Parameters go in a `.bicepparam`, not a JSON parameters file, unless `azd` requires
otherwise:

```bicep
using 'main.bicep'

param storageAccountName = 'stexample001'
```

## Verification

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
az bicep build-params --file infra/main.bicepparam --stdout > /dev/null
```

`az bicep lint` prints nothing and exits 0 when there is nothing to report. It is easy to
mistake that for the command not running, so check `echo $?` the first time.

Then, against a real subscription:

```bash
az login
az account set --subscription <subscription-id>
az deployment group what-if \
  --resource-group <rg> \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

Read the `Delete` and `Modify` lines out loud before answering the prompt. What-if is the
only step that tells you what the deploy will do to resources that already exist.

Keep the Bicep CLI current, since module features track it:

```bash
az bicep upgrade
```

## Conventions

- **Every `param` gets `@description`.** It becomes the parameter documentation and shows
  up in the portal for a template deployment.
- **Constrain what you can.** `@allowed`, `@minLength`, `@maxLength`, `@minValue`. Failing
  at compile time beats failing halfway through a deploy.
- **`@secure()` on anything secret**, including connection strings and admin passwords.
  It keeps the value out of deployment history.
- **Names come from a single expression**, not repeated string literals. A `uniqueString`
  seed off `resourceGroup().id` gives a name that is stable per group and unique across
  them.
- **`targetScope` is explicit** at the top of every file, even `resourceGroup`, which is
  the default.
- **Outputs are never secrets.** Deployment outputs are readable by anyone with reader on
  the resource group. Output the Key Vault URI, not the value in it.
- **Symbolic name matches purpose, not resource type.** `module telemetry ...` beats
  `module appInsights ...` when there is only one of them.

## bicepconfig.json

Turning the linter up costs nothing and catches the boring class of mistake:

```json
{
  "analyzers": {
    "core": {
      "enabled": true,
      "rules": {
        "no-hardcoded-env-urls": { "level": "error" },
        "no-unused-params": { "level": "error" },
        "no-unused-vars": { "level": "error" },
        "outputs-should-not-contain-secrets": { "level": "error" },
        "secure-parameter-default": { "level": "error" },
        "use-recent-api-versions": { "level": "warning" }
      }
    }
  }
}
```

## Gotchas

- **Module versions are not sorted in the registry tag list.** `tail` gives you an old
  version. Always `sort -V`.
- **`az bicep build` restores remote modules on first use** and needs network access.
  A CI runner behind a proxy fails here with a registry error, not a syntax error.
- **Changing a parameter that feeds a resource name replaces the resource.** For a storage
  account or a database, that is data loss. What-if shows this as delete plus create.
- **`existing` references do not create anything.** If the resource is not there, the
  deploy fails at runtime with a not-found, having already created everything before it.
- **Deployment names collide.** Two deploys with the same `name` in the same scope
  overwrite each other's history. Suffix with `utcNow()` at the top level if you care.
