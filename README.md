# Antigravity Codex Bridge

Antigravity-inspired skills, agents, and workflows packaged for OpenAI Codex.

This repository installs a portable `.agents` bundle into any project so Codex can discover the same workflows, specialist agents, and support scripts locally.

## What This Is

- A Codex-first package for repo-local skills and agents
- A small CLI that installs `.agents` into a target project
- A bridge for Antigravity-style workflows such as `$brainstorm`, `$debug`, `$plan`, and `$create`

## Important Note

This package is for Codex skills, not Antigravity slash commands.

- Use `$brainstorm`, `$debug`, `$plan`, `$create`, `$clean-code`, and similar skills
- Do not expect custom `/brainstorm` or `/debug` commands in Codex
- Keep the `.agents/` folder in the project root so Codex can discover it

## Quick Start

Until this package is published to npm, use the local CLI.

From this repository:

```bash
node ./bin/ag-codex.js init --path ../my-project
```

From the target project when this repo is next to it:

```bash
node ../antigravity-codex-bridge/bin/ag-codex.js init --path .
```

Windows `cmd` example:

```bat
node "..\antigravity-codex-bridge\bin\ag-codex.js" init --path .
```

After npm publish:

```bash
npx antigravity-codex-bridge init
```

Or install globally:

```bash
npm install -g antigravity-codex-bridge
ag-codex init
```

## After Install

1. Open the target project in VS Code.
2. Switch to the `CODEX` tab.
3. Reload the window or run `Force reload skills`.
4. Invoke skills with `$`.

Examples:

```text
$brainstorm auth system for a SaaS dashboard
$create landing page for a skincare brand
$debug why login returns 500
$plan migrate this app from REST to tRPC
$clean-code review this module before shipping
$ui-ux-pro-max redesign the homepage
```

## CLI

| Command | Description |
|---------|-------------|
| `ag-codex init` | Install `.agents` into the current project |
| `ag-codex init --path ./my-project` | Install into a specific directory |
| `ag-codex update` | Reinstall and overwrite the existing `.agents` folder |
| `ag-codex status` | Show whether `.agents` is installed and summarize its contents |

## What's Included

| Component | Count | Description |
|----------|------:|-------------|
| **Agents** | 20 | Specialist prompts for planning, frontend, backend, security, QA, DevOps, and more |
| **Skills** | 48 | Codex-ready skills adapted from Antigravity and expanded for Codex usage |
| **Workflows** | 11 | Task entrypoints such as `brainstorm`, `debug`, `plan`, and `test` |
| **Scripts** | 4 | Shared helpers for preview, verification, checklist, and session tasks |

Highlighted workflow skills:

- `$brainstorm`
- `$create`
- `$debug`
- `$deploy`
- `$enhance`
- `$orchestrate`
- `$plan`
- `$preview`
- `$status`
- `$test`
- `$ui-ux-pro-max`

## Repository Docs

- [Agent Flow Architecture](./AGENT_FLOW.md)

## Publish Scope

This repository is meant to ship the portable Codex package only.

Include:

- `.agents/`
- `bin/`
- `.gitignore`
- `.npmignore`
- `LICENSE`
- `README.md`
- `README(th).md`
- `package.json`

Do not include local-only compatibility layers:

- `.agent/`
- `plugins/antigravity/`
- `.agents/plugins/`

## License

MIT
