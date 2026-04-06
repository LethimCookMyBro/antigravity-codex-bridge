---
description: Generate, run, and review tests for the current code or feature.
---

# $test

$ARGUMENTS

Use this workflow to generate tests, run the current suite, inspect failures, or improve verification
coverage for a feature or module.

## Purpose

`$test` exists to turn vague testing requests into structured verification work that matches the current
project patterns and clearly reports pass/fail status.

## What This Workflow Does

1. Determines whether the task is test generation, test execution, or test repair.
2. Uses existing test conventions where possible.
3. Surfaces failures clearly.
4. Suggests the next step when tests fail.

## Use When

- The user asks to add tests.
- The user wants to run or fix the current suite.
- A feature needs verification before shipping.
- A regression needs a test to lock in the fix.

## Do Not Use When

- The main task is architectural planning.
- The main issue is runtime debugging without a test angle.

## Helpful Validation Commands

```bash
python3 .agents/scripts/checklist.py . --skip-performance
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
bash .agents/scripts/run.sh
```

## Related Skills

- `$testing-patterns`
- `$tdd-workflow`
- `$debug`

## Recommended Flow

### Phase 1: Identify the Scope

- which feature, file, or flow?
- is this generation, execution, or repair?

### Phase 2: Match Existing Patterns

- current test framework
- naming conventions
- mock patterns
- fixture conventions

### Phase 3: Run or Write the Tests

- prefer behavior-focused coverage
- keep tests readable
- include edge cases when they matter

### Phase 4: Summarize Results

- what passed
- what failed
- what still needs follow-up

## Suggested Output

```md
## Test Summary

### Scope
- ...

### Tests Added or Run
- ...

### Results
- ...

### Failures
- ...

### Follow-Up
- ...
```

## Example Invocations

```text
$test run the current suite
$test generate tests for auth service
$test fix the failing checkout tests
$test add regression coverage for this bug
```

## Final Rule

Do not present test work as complete unless the user can tell exactly what was run, added, or still
failing.
