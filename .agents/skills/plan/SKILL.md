---
name: plan
description: Create project plan using project-planner agent. No code writing, only plan file generation.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Plan

This skill adapts the Antigravity `/plan` workflow for Codex.
Treat the user's message as the planning request.

## Critical Rules

1. No code writing. This skill creates a plan only.
2. Use planning-first behavior and structured clarification.
3. Ask clarifying questions before planning when necessary.
4. Name the plan file dynamically based on the task.

## Task

Use the user's request as planning context.

### Naming Rules

1. Extract 2-3 key words from the request
2. Lowercase and hyphen-separated
3. Max 30 characters
4. Example: `e-commerce cart` -> `PLAN-ecommerce-cart.md`

### Rules

1. Clarify ambiguous requirements before planning
2. Create `docs/PLAN-{slug}.md` with task breakdown
3. Do not write implementation code
4. Report the exact file name created

## Expected Output

| Deliverable | Location |
|-------------|----------|
| Project Plan | `docs/PLAN-{task-slug}.md` |
| Task Breakdown | Inside plan file |
| Agent Assignments | Inside plan file |
| Verification Checklist | Inside plan file |

## After Planning

Tell the user:

```text
[OK] Plan created: docs/PLAN-{slug}.md

Next steps:
- Review the plan
- Run `$create` to start implementation
- Or modify the plan manually
```

## Naming Examples

| Request | Plan File |
|---------|-----------|
| `$plan e-commerce site with cart` | `docs/PLAN-ecommerce-cart.md` |
| `$plan mobile app for fitness` | `docs/PLAN-fitness-app.md` |
| `$plan add dark mode feature` | `docs/PLAN-dark-mode.md` |
| `$plan fix authentication bug` | `docs/PLAN-auth-fix.md` |
| `$plan SaaS dashboard` | `docs/PLAN-saas-dashboard.md` |

## Usage

```text
$plan e-commerce site with cart
$plan mobile app for fitness tracking
$plan SaaS dashboard with analytics
```
