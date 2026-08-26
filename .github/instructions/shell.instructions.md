---
applyTo: "**/*.sh"
---

# Shell scripts

- `#!/usr/bin/env bash` and `set -euo pipefail` at the top of every script.
- Verify before running: `bash -n script.sh`.
- Quote every expansion. `"$var"`, not `$var`.
- **Do not use bare plural nouns as variable names.** `GROUPS` is a bash special array, so
  `GROUPS=$(...)` is silently ignored and `"$GROUPS"` then reads as a group id. Same family:
  `UID`, `EUID`, `PPID`, `SECONDS`, `LINENO`, `RANDOM`, `PIPESTATUS`, `FUNCNAME`,
  `HOSTNAME`, `OSTYPE`, plus `status` and `GID` in zsh. Prefix them: `TENANT_GROUPS`.
- **`set -o pipefail` plus `| head` aborts on success.** `head` exits early, the producer
  takes SIGPIPE, the pipeline returns non-zero and `set -e` kills the script with no error
  message, so it reads like the command failed. Same for `| grep -v` matching nothing. End
  such pipelines with `|| true`.
- `command -v` fails for sbin tools (`nft`, `iptables`, `ss`) as a non-root user, because
  `/usr/sbin` is not on their PATH. Test with `sudo test -x /usr/sbin/nft` instead.
- `cd "$(dirname "$0")/.."` at the top when the script assumes a repo root, rather than
  trusting the caller's working directory.
- Anything destructive gets a confirmation or a `--dry-run` that is the default.
- Print what you are about to do before doing it. A silent script that takes a minute reads
  as hung.
- Only durable tools live in `scripts/`. Run throwaway code inline via a heredoc rather
  than leaving a one-shot script behind.
