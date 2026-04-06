---
description: Start a new application or project build and route the request into the creation workflow.
---

# $create

$ARGUMENTS

Use this workflow to kick off a new application, product prototype, scaffold, or greenfield feature area.

## Purpose

`$create` is the entry workflow for new builds. It helps Codex move from a user request to a planned,
scoped, and verified implementation path without pretending every request is already fully specified.

## What This Workflow Does

1. Understands the product request and required scope.
2. Detects whether the task is small enough to build directly or large enough to plan first.
3. Routes into the correct skills, agents, and scripts.
4. Produces a concrete implementation summary and next steps.

## Use When

- The user wants a new app, site, service, or prototype.
- A fresh feature shell or new module needs to be created.
- A new project needs an initial structure, stack, and first pass.

## Do Not Use When

- The project already exists and only needs modifications.
- The user wants analysis only, not implementation.
- The work is mainly debugging or deployment.

## Primary Routing

- Planning: `project-planner` agent or `$plan`
- Build orchestration: `$app-builder`
- UI work: `frontend-specialist`
- API/server work: `backend-specialist`
- Data design: `database-architect`
- Testing: `$test` or `test-engineer`

## Repo-Local Commands

Use these helpers when they add signal:

```bash
python3 .agents/scripts/session_manager.py info .
python3 .agents/scripts/checklist.py .
python3 .agents/scripts/auto_preview.py start
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
```

## Recommended Flow

### Phase 1: Clarify the Request

Extract:

- product type
- main audience
- core features
- preferred stack
- constraints or deadlines

Ask only the missing questions that materially change what gets built.

### Phase 2: Decide Whether Planning Comes First

Go straight to implementation if:

- the request is narrow
- the stack is obvious
- the blast radius is small

Switch to `$plan` first if:

- the request spans multiple domains
- architecture is unclear
- there are many moving parts or unknowns

### Phase 3: Build the Smallest Viable Useful Version

- prefer the simplest path that satisfies the request
- follow current repo patterns when working in an existing codebase
- keep changes verifiable

### Phase 4: Validate

At minimum:

- run the most relevant project tests
- check preview when a local app is involved
- summarize what was built and what remains

## Output Expectations

```md
## Create Summary

### Request
- ...

### Chosen Stack
- ...

### Scope
- ...

### Files or Areas Affected
- ...

### Validation
- ...

### Preview
- ...

### Next Step
- ...
```

## Example Invocations

```text
$create internal admin dashboard with auth
$create landing page for a wellness brand
$create mobile habit tracker app
$create small FastAPI backend for a note-taking app
```

## Final Rule

Do not overbuild the first version. Prefer a shippable baseline with clear follow-up steps over a
bloated first pass.
