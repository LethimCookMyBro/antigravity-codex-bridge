---
description: Show current project, preview, and task progress status.
---

# $status

$ARGUMENTS

Use this workflow to inspect current project state, preview status, and high-level readiness.

## Purpose

`$status` exists to answer "where are we right now?" without forcing the user to dig through files or
guess which script to run next.

## What This Workflow Shows

- current project path and session context
- preview server status
- useful next commands
- optional high-level readiness cues

## Backing Commands

```bash
python3 .agents/scripts/session_manager.py status .
python3 .agents/scripts/session_manager.py info .
python3 .agents/scripts/auto_preview.py status
```

## Recommended Flow

### Phase 1: Report Context

- current project
- current path
- any available session summary

### Phase 2: Report Preview

- preview running or not
- local URL if available
- obvious health signal if available

### Phase 3: Suggest What To Do Next

Examples:

- `$preview start`
- `$debug`
- `$test`
- `$deploy check`

## Suggested Output

```md
## Status

### Project
- ...

### Session
- ...

### Preview
- ...

### Suggested Next Step
- ...
```

## Example Invocations

```text
$status
$status current project
$status preview and session info
```

## Final Rule

Prefer a concise, actionable snapshot over a noisy dump of low-value details.
