# Infrastructure demo script

A 15 minute walkthrough of this repo for someone who has never seen it. The story is:
**an agent writes the Bicep, but the Bicep is not "done" until it has compiled, been
previewed against the real subscription, deployed, and documented in a README that a
checker has approved.**

Every command below was run on 2026-09-14 against subscription `Pay-As-You-Go-GITC`
(`e059f707-07f9-44ef-85f2-ea39910aedad`) with Azure CLI 2.74.0 and Bicep CLI 0.41.2. The
resource group was deleted afterwards. Timings are from that run.

## What you are demonstrating

| Beat | The point your colleague should take away |
|---|---|
| 1. Fresh project from the template | The conventions arrive with the repo, not with the person. |
| 2. `/new-infra` in Copilot Chat | The agent picks Bicep or Terraform, records why, and reuses Azure Verified Modules instead of hand-writing resources. |
| 3. The gate: build, lint, what-if | Nothing is called working until it has compiled and been previewed. |
| 4. Deploy for real | About 36 seconds for a storage account. |
| 5. `readme_check.py` fails, then passes | The setup instructions are a checked artefact, not prose. |
| 6. Teardown | Infrastructure that bills and has no documented delete is a trap. |

## Before the demo

Do these the day before, not in front of the audience.

```bash
az login
az account show --query '{name:name, id:id}' -o json
az bicep version
```

If `az bicep` is missing, run `az bicep install`. If the CLI nags about a survey, run
`az survey` once to dismiss it so it does not appear mid-demo.

Warm the Bicep module cache, otherwise the first `az bicep build` in the demo pauses while
it downloads the Azure Verified Module:

```bash
curl -s https://mcr.microsoft.com/v2/bicep/avm/res/storage/storage-account/tags/list \
  | python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin)["tags"]))' \
  | sort -V | tail -3
```

That prints the three newest module versions. At the time of writing the latest is
`0.33.0`. Mention the `sort -V`: the registry returns tags in publication order, so a plain
`tail` hands you `0.9.1` and you pin a year-old module by accident.

Decide your names up front and use them everywhere:

| Thing | Value used in this script |
|---|---|
| Resource group | `rg-groundwork-demo` |
| Region | `uksouth` |
| Workload prefix | `gwdemo` |

## Step 1: start a project from the template (2 minutes)

Use the GitHub CLI if you want the audience to see a real repo appear:

```bash
gh repo create groundwork-infra-demo --template omega1119/groundwork --private --clone
cd groundwork-infra-demo
code .
```

If you would rather not create a repo live, clone locally and start the history over:

```bash
git clone https://github.com/omega1119/groundwork.git groundwork-infra-demo
cd groundwork-infra-demo
rm -rf .git && git init
code .
```

**Say this while it runs:** the interesting files are all in `.github/`.
[.github/copilot-instructions.md](../.github/copilot-instructions.md) is loaded into every
single Copilot request, which is why it is short. The long procedures sit in
`.github/skills/` and only load when they are relevant. Open
[.github/skills/iac-templating/SKILL.md](../.github/skills/iac-templating/SKILL.md) for
five seconds so they can see the table of rules, then close it.

## Step 2: ask the agent for infrastructure (4 minutes)

In Copilot Chat, type:

```text
/new-infra a storage account for demo data in uksouth, resource group rg-groundwork-demo
```

**Narrate what the agent does rather than reading its output.** It will:

1. Check whether `infra/` already exists and whether `docs/decisions/` already records a
   language choice, so it cannot introduce a second IaC language into the repo.
2. Choose Bicep, because this is Azure only, and write a short decision record into
   `docs/decisions/`.
3. Look up the current Azure Verified Module version from the registry instead of
   guessing, and pin it.
4. Write `infra/main.bicep` and `infra/main.bicepparam`.

The file it produces looks like this:

```bicep
module storage 'br/public:avm/res/storage/storage-account:0.33.0' = {
  name: 'storage-account'
  params: {
    name: storageAccountName
    location: location
    skuName: 'Standard_LRS'
    kind: 'StorageV2'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
    minimumTlsVersion: 'TLS1_2'
  }
}
```

**The line worth pausing on is `allowBlobPublicAccess: false`.** The Azure default is
already false, so setting it is redundant today. The skill requires it anyway, so that a
future change to the platform default cannot quietly open the account.

## Step 3: the gate (3 minutes)

This is the heart of the demo. Run it in the terminal so the audience sees it is real, not
something the agent claimed.

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

Both are silent on success, which takes about 2 seconds. **Point out that silence is the
pass condition**, and that a template nobody has compiled is a draft, however confident the
chat window sounded.

Then create the resource group and preview the change:

```bash
az group create --name rg-groundwork-demo --location uksouth
```

```bash
az deployment group what-if \
  --resource-group rg-groundwork-demo \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

The output ends with a summary line. On the rehearsal run it read
`Resource changes: 2 to create`, the storage account and its blob service.

**Say this:** build and lint only prove the file parses. What-if is the one that tells you
what happens to the subscription. On a real change you read the delete lines before
anything else, because that is where an afternoon goes.

## Step 4: deploy (1 minute)

```bash
az deployment group create \
  --resource-group rg-groundwork-demo \
  --template-file infra/main.bicep \
  --parameters infra/main.bicepparam
```

Took 36 seconds on the rehearsal. The template outputs the generated account name, which is
built from `uniqueString(resourceGroup().id)` so it is globally unique without anyone
inventing a name.

Confirm it exists:

```bash
az resource list --resource-group rg-groundwork-demo --query '[].name' -o table
```

## Step 5: the part people remember (3 minutes)

Ask the agent to document it:

```text
/update-readme
```

Then run the checker:

```bash
python3 scripts/readme_check.py
```

**Show it failing first if you can.** Copy the unfilled template over the README and run
the checker:

```bash
cp templates/README.template.md README.md
python3 scripts/readme_check.py README.md
```

It exits 1 and prints roughly thirty lines, each with a line number, for example
`line 14: unfilled placeholder <Python>`. That is the message: the README is not prose that
someone skims in review, it is an artefact with a pass or fail.

Restore the real README and run it again. Success is a single line:

```text
ok   README.md
```

**Say this:** the checker also fails on an install command pointing at a `requirements.txt`
that does not exist, on a notebook with no kernel registration step, on em dashes, and on
invisible Unicode characters that arrive from a web paste and turn a copied command into
"command not found" with nothing visible to blame.

The checker uses the standard library only, so it runs before any environment exists, and
it runs in CI on every push.

## Step 6: tear it down (1 minute)

Do this in front of them. It is part of the point.

```bash
az group delete --name rg-groundwork-demo --yes --no-wait
```

The README the agent wrote has this command in it, with the real group name, in a section
at the bottom. **Infrastructure that bills and has no documented delete is a trap**, so the
skill will not call the work finished without it.

## If something goes wrong live

| What you see | What to do |
|---|---|
| `az bicep build` pauses for 30 seconds | It is downloading the module. You skipped the cache warm-up. Keep talking. |
| `AuthorizationFailed` on `az group create` | Wrong subscription. `az account set --subscription <id>`. |
| The agent writes Terraform instead of Bicep | Fine, it is a valid choice. Ask it to show you the decision record it wrote. |
| The agent claims the template works without running the gate | Say so out loud and ask it to run the gate. This is the failure the repo exists to catch, and it is a good demo moment, not a bad one. |
| What-if returns an empty list | Someone already deployed this. Delete the group and start again. |

## The one sentence version

If the demo overruns and you only get to say one thing: **an agent that writes correct
Terraform and then describes how to run it from memory has not finished the job, and this
repo is the machinery that refuses to let it claim otherwise.**
