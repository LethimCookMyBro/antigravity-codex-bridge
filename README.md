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
| Skills | 48 | Codex-readable guidance, patterns, checklists, and domain playbooks |
| Workflows | 11 | Entry workflows like `brainstorm`, `create`, `debug`, `plan`, and `test` |
| Scripts | 4 | Shared helpers for verification, preview, checklist, and session tasks |

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

## CLI

| Command | Description |
|---------|-------------|
| `ag-kit init` | Install `.agents` into the current directory |
| `ag-kit init --path ./my-project` | Install into a specific directory |
| `ag-kit update` | Reinstall and overwrite the existing `.agents` folder |
| `ag-kit status` | Show whether `.agents` is installed and summarize its contents |
| `ag-kit help` | Show usage information |

## Package Scope

The published npm package is:

```bash
@lizmotia/ag-kit
```

The repository also keeps `ag-codex` as a CLI alias for compatibility, but `ag-kit` is the primary command going forward.

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
|-- README.md
`-- README(th).md
```

## Published Scope

The npm package is intentionally limited to the portable runtime:

- `.agents/`
- `bin/`
- `AGENT_FLOW.md`
- `PUBLISHING.md`
- `README.md`
- `README(th).md`
- `LICENSE`
- `package.json`

Local-only compatibility files are excluded from the published package.

## Docs

- [Agent Flow](./AGENT_FLOW.md)
- [Publishing Guide](./PUBLISHING.md)

## License

MIT
