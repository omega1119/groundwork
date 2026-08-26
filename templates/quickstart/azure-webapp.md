# Quickstart block: Azure web app

Goes in `## Deployment`, after a local quickstart. Local first, always.

---

## Deployment

Deployed to <Azure App Service / Container Apps / Static Web Apps> in
<subscription name>.

| Thing | Value |
|---|---|
| Subscription | `<subscription-id>` |
| Resource group | `<rg-name>` |
| Region | `<region>` |
| <Resource type> | `<resource-name>` |
| Live URL | <https://example.azurewebsites.net> |

Needs the Azure CLI. Check with `az version`, then:

```bash
az login
az account set --subscription <subscription-id>
```

Deploy:

```bash
azd up
```

<Or the specific commands if not using azd. If infrastructure and app deploy separately,
give the order explicitly and say why it matters.>

Watch the logs:

```bash
az webapp log tail --name <app-name> --resource-group <rg-name>
```

Tear it down. This deletes everything in the group and cannot be undone:

```bash
az group delete --name <rg-name> --yes --no-wait
```

---

## Notes for whoever fills this in

- **Real resource names, not placeholders.** This table is the section people come back
  for, six months later, when something is broken.
- **Infrastructure first, app second**, whenever the infrastructure changed. App workflows
  usually trigger on push and infra ones usually do not, so a plain `git push` runs them in
  the wrong order.
- No connection strings, no keys. Managed identity with `DefaultAzureCredential`, which
  works locally through `az login` too. Say that explicitly, because otherwise the reader
  goes looking for a key.
- Note anything that needs a second grant to work. An Entra app role that lets someone sign
  in is not the same as the data permission that lets them see anything, and having only
  the first produces 404s that read as a broken app.
- Always document the teardown. A README that creates billable resources and does not say
  how to delete them is a trap.
- The `azure-prepare`, `azure-validate` and `azure-deploy` skills do the actual work. This
  block only covers what the README has to end up saying.
