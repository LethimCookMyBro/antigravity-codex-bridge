# AG Kit

Portable Codex skills, specialist agents, workflows, and helper scripts packaged as one installable bundle.

`@lizmotia/ag-kit` installs a project-local `.agents` directory so OpenAI Codex can discover the same operating system across projects.

## Install

Run once inside the target project:

```bash
npx @lizmotia/ag-kit init
```

Or install globally:

```bash
npm install -g @lizmotia/ag-kit
ag-kit init
```

Update an existing installation:

```bash
npx @lizmotia/ag-kit update
```

If you explicitly want to overwrite `.agents` with `init`, this is equivalent:

```bash
npx @lizmotia/ag-kit init --force
```

Local development path:

```bash
node ./bin/ag-codex.js init --path ../my-project
```

Compatibility alias:

```bash
ag-codex init
```

## What It Installs

The CLI copies a portable `.agents` tree into the target project root.

That bundle currently includes:

| Component | Count | Purpose |
|---------|------:|---------|
| Agents | 20 | Specialist execution roles such as frontend, backend, security, QA, and planning |
| Skills | 96 top-level / 106 total SKILL files | Codex-readable guidance, patterns, checklists, and domain playbooks |
| Workflows | 11 | Entry workflows like `brainstorm`, `create`, `debug`, `plan`, and `test` |
| Scripts | 17 | Shared helpers for verification, preview, stale checks, health checks, load order, preview, checklist, and session tasks |

## Core Idea

AG Kit is designed for Codex skills, not custom slash-command runtimes.

- Use `$brainstorm`, `$create`, `$debug`, `$plan`, `$test`, and related skills inside Codex.
- Keep `.agents/` at the project root so Codex can discover it.
- Use one portable package instead of manually copying prompts and helper files between repositories.

## Typical Flow

1. Install `.agents` into a project.
2. Open that project in VS Code.
3. Switch to the `CODEX` tab.
4. Reload the window or run `Force reload skills`.
5. Invoke skills with `$`.

Examples:

```text
$brainstorm auth system for a SaaS dashboard
$create landing page for a skincare brand
$debug why login returns 500
$plan migrate this app from REST to tRPC
$clean-code review this module before shipping
$ui-ux-pro-max redesign the homepage
```

If someone clones this repository directly, `.agents/` is already included. They only need to:

1. Open the repo root in VS Code.
2. Switch to the `CODEX` tab.
3. Reload the window or run `Force reload skills`.
4. Start invoking skills with `$`.

## CLI

| Command | Description |
|---------|-------------|
| `ag-kit init` | Install `.agents` into the current directory |
| `ag-kit init --path ./my-project` | Install into a specific directory |
| `ag-kit update` | Reinstall and overwrite the existing `.agents` folder |
| `ag-kit init --force` | Overwrite an existing `.agents` installation during init |
| `ag-kit status` | Show whether `.agents` is installed and summarize its contents |
| `ag-kit help` | Show usage information |

## Package Scope

The published npm package is:

```bash
@lizmotia/ag-kit
```

The repository also keeps `ag-codex` as a CLI alias for compatibility, but `ag-kit` is the primary command going forward.

## Updating Existing Projects

Use `update` when `.agents` is already installed and you want the latest package contents:

```bash
npx @lizmotia/ag-kit update
```

If you just published a new package version and want to avoid stale `npx` cache, prefer:

```bash
npx @lizmotia/ag-kit@latest update
```

Global install equivalent:

```bash
ag-kit update
```

`init --force` is supported, but `update` is the clearer command for refreshes because it makes the overwrite behavior explicit.

## Repository Layout

```text
.
|-- .agents/
|   |-- agents/
|   |-- skills/
|   |-- workflows/
|   |-- scripts/
|   `-- .shared/
|-- bin/ag-codex.js
|-- AGENT_FLOW.md
|-- PUBLISHING.md
|-- SKILLS_AND_WORKFLOWS.md
|-- SKILLS_AND_WORKFLOWS_TH.md
|-- README.md
`-- README(th).md
```

## Published Scope

The npm package is intentionally limited to the portable runtime:

- `.agents/`
- `bin/`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `UPDATELIST.md`
- `SKILLS_AND_WORKFLOWS.md`
- `SKILLS_AND_WORKFLOWS_TH.md`
- `README.md`
- `README(th).md`
- `LICENSE`
- `package.json`

Local-only compatibility files are excluded from the published package.

## GitHub Push Notes

These files should ship:

- `.agents/`
- `bin/`
- `README.md`
- `README(th).md`
- `UPDATELIST.md`
- `SKILLS_AND_WORKFLOWS.md`
- `SKILLS_AND_WORKFLOWS_TH.md`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `LICENSE`
- `package.json`
- `.npmignore`

These should stay local-only and are ignored:

- `.agent/`
- `plugins/`
- `.agents/plugins/`
- `h4cker/`
- `awesome-design-md/`
- local audit and scratch reports

## Docs

- [Agent Flow](./AGENT_FLOW.md)
- [Publishing Guide](./PUBLISHING.md)
- [Update List](./UPDATELIST.md)
- [Skills and Workflows Catalog](./SKILLS_AND_WORKFLOWS.md)
- [Skills and Workflows Catalog (Thai)](./SKILLS_AND_WORKFLOWS_TH.md)

## License

MIT
