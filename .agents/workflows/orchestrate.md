---
description: Coordinate multiple skills or agents for complex work that spans more than one domain.
---

# $orchestrate

$ARGUMENTS

Use this workflow for complex tasks that need coordinated planning, multi-domain execution, and a final
synthesis instead of a single narrow answer.

## Purpose

`$orchestrate` is the control workflow for work that spans more than one discipline. It exists to keep
ownership clear, prevent duplicated effort, and make validation explicit.

## What This Workflow Does

1. Splits the request into workstreams.
2. Decides whether the task needs planning first.
3. Chooses the relevant specialists or skills.
4. Coordinates execution by dependency order.
5. Synthesizes outputs into one result.

## Use When

- The task spans frontend, backend, database, testing, docs, or ops together.
- The user explicitly asks for multi-agent or delegated work.
- A single skill would miss important cross-domain concerns.
- The task is large enough that ownership and sequencing matter.

## Do Not Use When

- The task is a simple single-file change.
- A single specialist can clearly handle the work alone.

## Typical Specialists

- `project-planner`
- `frontend-specialist`
- `backend-specialist`
- `database-architect`
- `security-auditor`
- `test-engineer`
- `devops-engineer`
- `documentation-writer`

## Typical Skills That Pair Well

- `$plan`
- `$architecture`
- `$create`
- `$enhance`
- `$test`
- `$deploy`

## Recommended Sequence

### Phase 1: Scope the Work

- restate the task
- identify workstreams
- identify dependencies
- decide whether planning is required

### Phase 2: Assign Ownership

Examples:

- UI and interaction: `frontend-specialist`
- APIs and services: `backend-specialist`
- schema and data shape: `database-architect`
- validation and regression checks: `test-engineer`
- release and environment concerns: `devops-engineer`

### Phase 3: Execute in the Right Order

- do planning before implementation when the task is broad
- do foundational blockers first
- use parallel work only where dependencies allow it

### Phase 4: Validate

Use the appropriate repo-local helpers when relevant:

```bash
bash .agents/scripts/run.sh
python3 .agents/scripts/checklist.py .
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
```

### Phase 5: Synthesize

The final answer should combine:

- what was done
- what was verified
- what risks remain
- what should happen next

## Suggested Output

```md
## Orchestration Summary

### Task
- ...

### Workstreams
- ...

### Owners
- ...

### Dependencies
- ...

### Validation
- ...

### Final Synthesis
- ...
```

## Example Invocations

```text
$orchestrate build and validate a new SaaS dashboard
$orchestrate review this app across security, performance, and UX
$orchestrate plan and ship a multi-step migration
```

## Final Rule

Do not use orchestration as decoration. Use it only when coordination adds real value.
