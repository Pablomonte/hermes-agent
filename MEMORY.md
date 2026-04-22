# Project Memory — nicoechaniz/hermes-agent fork

## Fork Setup (done once)

- Active install lives at `~/.hermes/hermes-agent` — actual dir, never symlink (Python hardcodes venv paths in `~/.local/bin/hermes`).
- `origin` remote points to `git@github.com:nicoechaniz/hermes-agent.git` (fork) — `hermes update` pulls from here.
- `upstream` remote points to `https://github.com/NousResearch/hermes-agent.git`.
- Clean rebase workspace at `~/Projects/hermes-agent`.

## Updating Hermes (`hermes update`)

1. `hermes update` in any terminal pulls from `origin` (the fork) because `hermes_cli/main.py` hardcodes `branch = "main"`.
2. To sync fork with upstream: use `~/Projects/hermes-agent` workspace, rebase `main` onto `upstream/main`, force-push to fork, then run `hermes update`.

## Rebasing a Feature Branch

1. `cd ~/Projects/hermes-agent`
2. `git fetch upstream`
3. `git checkout feat/branch-name`
4. `git rebase upstream/main`
5. Resolve conflicts if any, then `git push --force-with-lease origin feat/branch-name`
6. Merge into `main` in the workspace, push `main`, then fast-forward `~/.hermes/hermes-agent` via its `local-project` remote.

## Creating a New Fix / Feature

1. Start from `upstream/main` in `~/Projects/hermes-agent`.
2. `git checkout -b fix/descriptive-name` or `feat/descriptive-name`.
3. Make changes, commit.
4. Push to fork: `git push -u origin fix/descriptive-name`.
5. Rebase onto latest upstream when ready, merge into workspace `main`, push `main`, then update active install.

## Testing Before Pushing

- Always use `scripts/run_tests.sh` — never call `pytest` directly. The wrapper enforces CI parity (unsets API keys, TZ=UTC, LANG=C.UTF-8, `-n 4`).
- Direct pytest diverges on API key presence, HOME path, timezone, locale, and worker count.

## Kimi OAuth Integration

- Credentials are read from `~/.kimi/credentials/kimi-code.json` (installed by `kimi login`).
- `resolve_kimi_coding_runtime_credentials()` in `hermes_cli/auth.py` returns the OAuth token.
- `kimi_coding_default_headers()` generates the mandatory `X-Msh-*` headers and `User-Agent`.
- `kimi_coding_required_temperature()` in `hermes_cli/models.py` pins temperature to `0.6` for `kimi-k2.6` on the coding endpoint.
- Both `run_agent.py` and `agent/auxiliary_client.py` integrate these helpers.
- `hermes auth kimi` prints a safe Kimi CLI OAuth diagnostic summary (token file path, presence of access/refresh tokens, resolved source, base URL) without exposing secrets.
- To test: restart Hermes, switch model to `moonshotai/kimi-k2.6`, send a chat message. The API call must include `X-Msh-*` headers or Kimi returns `access_terminated_error`.

## Active Branches on GitHub

- `main` — integration branch with all merged fixes/features.
- `feat/ctrl-c-configurable-priority`
- `fix/interrupt-history-sanitization`
- `fix/interrupt-multimodal-requeue`
- `feat/kimi-cli-oauth`
- `feat/tui-input-scrollbar-max-lines-rebased`
- `fix/hermes-model-kimi-oauth` — merged into main

## Custom Config Preferences (`~/.hermes/config.yaml`)

```yaml
display:
  ctrl_c_priority: clear_input
tui:
  input_max_lines: 30
  collapse_large_pastes: true
  history_nav_requires_empty_input: true
  show_full_input: true
```

## Gotchas

- `hermes update` hardcodes `branch = "main"` — cannot use a custom integration branch without patching `hermes_cli/main.py`.
- Symlinking `~/.hermes/hermes-agent` to `~/Projects/hermes-agent` fails because pip-install records absolute paths and the `hermes` entrypoint hardcodes the venv interpreter path.
- `~/.hermes/hermes-agent-upstream-backup` exists as a safety copy of the original upstream-only install.

## LLM Wiki (Karpathy pattern)

- Enabled via `WIKI_PATH=/home/nicolas/wiki` in `~/.hermes/.env`.
- Also set `OBSIDIAN_VAULT_PATH=/home/nicolas/wiki` for Obsidian skill integration.
- Initialized at `~/wiki` with SCHEMA.md, index.md, log.md, and full directory structure.
- Domain: AI/ML Research, Engineering, and Project Knowledge.
- To use: ask to "ingest <url> into my wiki", "what does my wiki say about X?", or "lint my wiki".
- Obsidian desktop can open `~/wiki` as a vault directly. For server-side sync, obsidian-headless is available (requires Obsidian Sync subscription).
- Default vault set to `~/wiki` via `~/.var/app/md.obsidian.Obsidian/config/obsidian/obsidian.json`.
- **AlterMundi Projects workflow:** `projects/<name>/` sub-wikis with their own `raw/`, `notes/`, and `index.md`. Global `raw/` for cross-cutting sources. Ingest coding projects or papers into a specific project, cross-link to global entities/concepts.
- **Kimi OAuth:** Hermes now reads Kimi CLI tokens from `~/.kimi/credentials/kimi-code.json`, can refresh the access token via the stored refresh token, and retries once on HTTP 401 before falling back.
