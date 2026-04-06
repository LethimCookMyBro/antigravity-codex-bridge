---
description: Manage the local preview server by starting, stopping, restarting, or checking status.
---

# $preview

$ARGUMENTS

Use this workflow to manage the local preview server for the current project.

## Purpose

`$preview` gives a simple operational wrapper around the local preview lifecycle so the user can start,
stop, inspect, or recover the local app preview consistently.

## What This Workflow Does

1. Shows preview status when no action is specified.
2. Starts the preview server when requested.
3. Stops or restarts it when needed.
4. Reports the outcome and the most useful next step.

## Backing Script

```bash
python3 .agents/scripts/auto_preview.py status
python3 .agents/scripts/auto_preview.py start
python3 .agents/scripts/auto_preview.py stop
python3 .agents/scripts/auto_preview.py start 3001
```

## Supported Actions

- status
- start
- stop
- restart

## Recommended Behavior

### If No Subcommand Is Provided

Show current preview status first.

### If Starting

- try the default port first
- if that fails, suggest the next sensible port
- report the local URL if known

### If Restarting

- stop the previous process cleanly
- start again
- report any port change

### If Unhealthy

Point to the next likely recovery path:

- `$debug`
- `$status`
- `checklist.py`

## Suggested Output

```md
## Preview Status

### Action
- start | stop | status | restart

### Result
- ...

### URL
- ...

### Notes
- ...

### Next Step
- ...
```

## Example Invocations

```text
$preview
$preview start
$preview stop
$preview restart
```

## Final Rule

If preview state is unclear, prefer reporting status over pretending the server is healthy.
