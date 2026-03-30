# Antigravity Codex Bridge

> Antigravity-inspired skills, agents, and workflows packaged for OpenAI Codex.

This repository turns the Antigravity workflow style into a Codex-friendly, repo-local `.agents` package that can be installed into any project and used as Codex skills.

## Quick Install

This package is not currently published to npm yet.

Run from the cloned repository:

```bash
node ./bin/ag-codex.js init --path /path/to/your-project
```

If you are already inside the target project, use the full path to this repository:

```bash
node /path/to/antigravity-codex-bridge/bin/ag-codex.js init --path .
```

Windows `cmd` example:

```bat
node "C:\Users\User\Downloads\forCODEX\bin\ag-codex.js" init --path .
```

After publishing this package to npm:

```bash
npx antigravity-codex-bridge init
```

Then open the target project in VS Code with Codex enabled and reload skills.

## Important Note

This package is built for **Codex skills**, not Antigravity slash commands.

- Use `$brainstorm`, `$debug`, `$plan`, `$create`, `$clean-code`, etc.
- Do not expect custom `/brainstorm` or `/debug` slash commands in Codex.
- Keep the `.agents/` folder in the project root so Codex can discover the skills.

## What's Included

| Component | Count | Description |
|----------|------:|-------------|
| **Agents** | 20 | Specialist prompts for planning, frontend, backend, security, QA, DevOps, and more |
| **Skills** | 48 | Codex-ready skills adapted from Antigravity and expanded for Codex usage |
| **Workflows** | 11 | Command-style workflow documents mapped into Codex skill behavior |
| **Scripts** | 4 | Shared helper scripts for preview, verification, checklists, and status |

## Usage

After installing `.agents` into your project:

1. Open the project in VS Code.
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

## CLI Commands

| Command | Description |
|---------|-------------|
| `ag-codex init` | Install `.agents` into the current project |
| `ag-codex init --path ./my-project` | Install into a specific directory |
| `ag-codex update` | Reinstall and overwrite the existing `.agents` folder |
| `ag-codex status` | Show whether `.agents` is installed and count its contents |

## Core Command Skills

These Antigravity-style workflow skills are included:

| Skill | Description |
|-------|-------------|
| `$brainstorm` | Structured exploration before implementation |
| `$create` | Start a new app or feature build |
| `$debug` | Systematic debugging and root-cause analysis |
| `$deploy` | Pre-flight checks and deployment flow |
| `$enhance` | Improve an existing project or feature |
| `$orchestrate` | Multi-agent coordination for complex tasks |
| `$plan` | Planning-only workflow |
| `$preview` | Local preview management |
| `$status` | Project and workflow status |
| `$test` | Test generation and execution flow |
| `$ui-ux-pro-max` | Design-heavy UI workflow with design system support |

## Top-Level Skills

This bridge also includes domain skills from the Antigravity ecosystem, including:

- `api-patterns`
- `app-builder`
- `architecture`
- `bash-linux`
- `behavioral-modes`
- `brainstorming`
- `clean-code`
- `database-design`
- `documentation-templates`
- `frontend-design`
- `game-development`
- `geo-fundamentals`
- `i18n-localization`
- `intelligent-routing`
- `lint-and-validate`
- `mcp-builder`
- `mobile-design`
- `nodejs-best-practices`
- `parallel-agents`
- `performance-profiling`
- `plan-writing`
- `powershell-windows`
- `python-patterns`
- `react-best-practices`
- `red-team-tactics`
- `rust-pro`
- `seo-fundamentals`
- `server-management`
- `systematic-debugging`
- `tailwind-patterns`
- `tdd-workflow`
- `testing-patterns`
- `vulnerability-scanner`
- `web-design-guidelines`
- `webapp-testing`

## What Should Be Pushed

This repository is intended to publish the portable Codex package only.

Push these files:

- `.agents/`
- `bin/`
- `.gitignore`
- `.npmignore`
- `LICENSE`
- `README.md`
- `README(th).md`
- `package.json`

Do not push these local-only compatibility layers:

- `.agent/`
- `plugins/antigravity/`
- `.agents/plugins/`

## Repository Goal

The goal is to ship a clean Codex-first package:

- no duplicate `.agent` and `.agents` trees in the published repo
- no local plugin bridge required for end users
- no dependency on hidden workspace-only paths
- just a portable `.agents` folder plus a tiny installer CLI

## Credits

Inspired by the original Antigravity Kit workflow system and adapted for Codex-first usage.

## License

MIT
