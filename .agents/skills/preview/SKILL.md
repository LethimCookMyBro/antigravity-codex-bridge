---
name: preview
description: Preview server start, stop, and status check. Local development server management.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Preview

This skill adapts the Antigravity `/preview` workflow for Codex.
Treat the user's message as a preview management request.

## Task

Manage the preview server: start, stop, restart, or check status.

### Commands

```text
$preview           - Show current status
$preview start     - Start server
$preview stop      - Stop server
$preview restart   - Restart
$preview check     - Health check
```

## Usage Examples

### Start Server

```text
$preview start

Response:
Starting preview...
Port: 3000
Type: Next.js

Preview ready:
URL: http://localhost:3000
```

### Status Check

```text
$preview

Response:
=== Preview Status ===
URL: http://localhost:3000
Project: /path/to/project
Type: nextjs
Health: OK
```

### Port Conflict

```text
$preview start

Response:
Port 3000 is in use.

Options:
1. Start on port 3001
2. Close app on 3000
3. Specify different port
```

## Technical

Auto preview uses `auto_preview.py`:

```bash
python .agents/scripts/auto_preview.py start [port]
python .agents/scripts/auto_preview.py stop
python .agents/scripts/auto_preview.py status
```
