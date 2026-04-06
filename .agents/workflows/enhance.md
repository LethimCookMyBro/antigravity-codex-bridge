---
description: Add or update features in an existing application through an iterative enhancement workflow.
---

# $enhance

$ARGUMENTS

Use this workflow to improve, extend, refactor, or add features to an existing application.

## Purpose

`$enhance` is the workflow for iterative development inside a codebase that already exists. It should
respect current architecture, avoid unnecessary churn, and make the requested change verifiable.

## What This Workflow Does

1. Inspects current project state first.
2. Determines affected files and likely blast radius.
3. Uses planning for large changes and direct edits for small ones.
4. Verifies the enhancement before calling it done.

## Use When

- The user wants to add a feature to an existing app.
- The request is an improvement, not a greenfield build.
- The app should keep its current stack and patterns.

## Do Not Use When

- The task is a brand-new project.
- The request is only analysis or planning.
- The main problem is a bug that needs debugging first.

## Project State Commands

```bash
python3 .agents/scripts/session_manager.py info .
python3 .agents/scripts/session_manager.py status .
python3 .agents/scripts/checklist.py . --skip-performance
```

## Recommended Flow

### Phase 1: Understand Current State

Check:

- existing architecture
- relevant features
- constraints from current stack
- likely owner areas

### Phase 2: Scope the Enhancement

Determine:

- what should change
- what should stay untouched
- which files or modules are affected
- whether approval is needed because the change is broad

### Phase 3: Implement Incrementally

- prefer focused changes over broad rewrites
- preserve established repo patterns
- keep the enhancement easy to review

### Phase 4: Verify

- run relevant tests
- sanity-check preview when applicable
- summarize what changed and what remains

## Suggested Output

```md
## Enhancement Summary

### Request
- ...

### Current State
- ...

### Change Plan
- ...

### Applied Updates
- ...

### Verification
- ...

### Next Step
- ...
```

## Example Invocations

```text
$enhance add dark mode to this dashboard
$enhance make the landing page responsive
$enhance add search and filtering to the product list
$enhance improve onboarding for first-time users
```

## Final Rule

Prefer minimal, compatible changes over broad rewrites unless the user clearly asks for a redesign or
refactor.
