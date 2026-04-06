---
description: Enter a systematic debugging flow for investigation, evidence collection, and root-cause analysis.
---

# $debug

$ARGUMENTS

Use this workflow when behavior is broken, inconsistent, flaky, or surprising and the next step should
be investigation instead of guesswork.

## Purpose

`$debug` exists to turn a vague bug report into a structured investigation with evidence, hypotheses,
root cause, fix, and verification.

## What This Workflow Does

1. Captures the symptom and the expected behavior.
2. Collects reproduction details and project context.
3. Forms hypotheses before changing code.
4. Verifies each hypothesis with evidence.
5. Explains root cause and confirms the fix.

## Use When

- The app returns errors or behaves unexpectedly.
- Tests started failing and the cause is unclear.
- A recent change introduced a regression.
- The issue is intermittent or hard to reproduce.

## Do Not Use When

- The user already knows the exact fix and only wants it applied.
- The request is architectural planning, not investigation.

## Helpful Tools and Skills

- `debugger` agent
- `explorer-agent`
- `$systematic-debugging`
- `$test`
- `$status`

## Repo-Local Commands

```bash
python3 .agents/scripts/session_manager.py status .
python3 .agents/scripts/session_manager.py info .
python3 .agents/scripts/checklist.py . --skip-performance
bash .agents/scripts/run.sh
```

## Recommended Flow

### Phase 1: Capture the Symptom

Record:

- what is happening
- what should happen instead
- where it happens
- whether it is reproducible

### Phase 2: Gather Context

Collect:

- reproduction steps
- recent changes
- error messages
- related files or services

### Phase 3: Form Hypotheses

Write down several plausible causes and order them by likelihood.

### Phase 4: Test the Hypotheses

- inspect logs
- inspect data flow
- isolate the failing step
- compare expected vs actual state

### Phase 5: Apply and Verify the Fix

After the fix:

- rerun the relevant test or check
- verify the original symptom is gone
- note any preventive follow-up such as tests or guardrails

## Suggested Output

```md
## Debug Report

### Symptom
- ...

### Reproduction
- ...

### Evidence
- ...

### Hypotheses
1. ...
2. ...
3. ...

### Root Cause
- ...

### Fix Applied
- ...

### Verification
- ...

### Prevention
- ...
```

## Example Invocations

```text
$debug login returns 500 after submit
$debug preview server starts but the page stays blank
$debug checkout tests started failing after refactor
$debug API request hangs only in production mode
```

## Final Rule

Do not call something the root cause until the observed behavior actually matches the evidence.
