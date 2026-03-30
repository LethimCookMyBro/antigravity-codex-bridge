---
name: status
description: Display agent and project status. Progress tracking and status board.
allowed-tools: Read, Glob, Grep, Bash
---

# Status

This skill adapts the Antigravity `/status` workflow for Codex.
Treat the user's message as a request for current state and progress.

## Task

Show the current project and agent status.

### What It Shows

1. **Project info**
   - Project name and path
   - Tech stack
   - Current features

2. **Agent status board**
   - Which agents are running
   - Which tasks are completed
   - Pending work

3. **File statistics**
   - Files created count
   - Files modified count

4. **Preview status**
   - Whether the server is running
   - URL
   - Health check

## Example Output

```text
=== Project Status ===

Project: my-ecommerce
Path: /path/to/my-ecommerce
Type: nextjs-ecommerce
Status: active

Tech Stack:
- Framework: next.js
- Database: postgresql
- Auth: clerk
- Payment: stripe

Features:
- product-listing
- cart
- checkout
- user-auth
- order-history

Pending:
- admin-panel
- email-notifications

Files: 73 created, 12 modified

=== Agent Status ===

- database-architect -> Completed
- backend-specialist -> Completed
- frontend-specialist -> Dashboard components (60%)
- test-engineer -> Waiting

=== Preview ===

URL: http://localhost:3000
Health: OK
```

## Technical

Status can use:

```bash
python .agents/scripts/session_manager.py status
python .agents/scripts/auto_preview.py status
```
