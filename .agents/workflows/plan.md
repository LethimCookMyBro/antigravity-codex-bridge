---
description: Generate a project plan or execution plan before implementation begins.
---

# $plan

$ARGUMENTS

Use this workflow when the next best step is a plan, not immediate code changes.

## Purpose

`$plan` exists to turn a request into an execution-ready plan with phases, dependencies, risks, and
verification criteria before implementation begins.

## What This Workflow Does

1. Clarifies the task scope.
2. Identifies constraints and unknowns.
3. Breaks the work into phases or milestones.
4. Produces a plan with verification points and recommended next workflow.

## Use When

- The task is large or multi-step.
- The user asked for a plan explicitly.
- The implementation path is not obvious.
- A migration or refactor needs sequencing.

## Do Not Use When

- The task is small and already well-scoped.
- The user only wants direct implementation.

## Planning Rules

- Do not implement while planning.
- Ask only the missing questions that materially affect sequencing.
- Prefer concrete phases over vague bullet dumps.
- Include validation criteria so the plan is actionable.

## Recommended Deliverable

For broad tasks, prefer a plan document under `docs/` such as:

- `docs/PLAN-auth-migration.md`
- `docs/PLAN-admin-portal.md`
- `docs/PLAN-dark-mode.md`

The exact file name should reflect the task clearly.

## Suggested Plan Structure

```md
## Plan

### Goal
- ...

### Constraints
- ...

### Phases
1. ...
2. ...
3. ...

### Risks
- ...

### Verification
- ...

### Next Workflow
- `$create` or `$enhance`
```

## Example Invocations

```text
$plan migrate this app from REST to tRPC
$plan build an internal admin portal
$plan add multi-tenant auth to the current product
$plan refactor the checkout flow safely
```

## Final Rule

A good plan should make implementation easier tomorrow, not just look organized today.
