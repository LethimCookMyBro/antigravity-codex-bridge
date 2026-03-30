---
name: orchestrate
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Orchestrate

This skill adapts the Antigravity `/orchestrate` workflow for Codex.
Treat the user's message as the task to orchestrate.

## Critical Minimum Requirement

Orchestration means a minimum of 3 different agents.

- If you use fewer than 3 agents, you are delegating, not orchestrating.
- Before completion, validate that at least 3 distinct specialists were used.

### Agent Selection Matrix

| Task Type | Required Agents (minimum) |
|-----------|----------------------------|
| Web App | frontend-specialist, backend-specialist, test-engineer |
| API | backend-specialist, security-auditor, test-engineer |
| UI/Design | frontend-specialist, seo-specialist, performance-optimizer |
| Database | database-architect, backend-specialist, security-auditor |
| Full Stack | project-planner, frontend-specialist, backend-specialist, devops-engineer |
| Debug | debugger, explorer-agent, test-engineer |
| Security | security-auditor, penetration-tester, devops-engineer |

## Pre-Flight Mode Check

| Current Mode | Task Type | Action |
|--------------|-----------|--------|
| plan | Any | Proceed with planning-first approach |
| edit | Simple execution | Proceed directly |
| edit | Complex or multi-file | Switch to planning-first orchestration |
| ask | Any | Ask whether to switch to planning or implementation |

## Strict 2-Phase Orchestration

### Phase 1: Planning

Sequential only. No parallel agents yet.

| Step | Agent | Action |
|------|-------|--------|
| 1 | `project-planner` | Create `docs/PLAN.md` |
| 2 | `explorer-agent` | Optional codebase discovery |

Only `project-planner` and `explorer-agent` should run during planning.

### Checkpoint: User Approval

After `PLAN.md` is complete, ask for approval before implementation.
Do not proceed to phase 2 without explicit approval.

### Phase 2: Implementation

After approval, agents can run in parallel.

| Parallel Group | Agents |
|----------------|--------|
| Foundation | `database-architect`, `security-auditor` |
| Core | `backend-specialist`, `frontend-specialist` |
| Polish | `test-engineer`, `devops-engineer` |

## Available Agents

| Agent | Domain | Use When |
|-------|--------|----------|
| `project-planner` | Planning | Task breakdown, `PLAN.md` |
| `explorer-agent` | Discovery | Codebase mapping |
| `frontend-specialist` | UI/UX | React, Vue, CSS, HTML |
| `backend-specialist` | Server | API, Node.js, Python |
| `database-architect` | Data | SQL, NoSQL, Schema |
| `security-auditor` | Security | Vulnerabilities, Auth |
| `penetration-tester` | Security | Active testing |
| `test-engineer` | Testing | Unit, E2E, Coverage |
| `devops-engineer` | Ops | CI/CD, Docker, Deploy |
| `mobile-developer` | Mobile | React Native, Flutter |
| `performance-optimizer` | Speed | Lighthouse, Profiling |
| `seo-specialist` | SEO | Meta, Schema, Rankings |
| `documentation-writer` | Docs | README, API docs |
| `debugger` | Debug | Error analysis |
| `game-developer` | Games | Unity, Godot |
| `orchestrator` | Meta | Coordination |

## Orchestration Protocol

### Step 1: Analyze Task Domains

Identify all domains touched by the task:

- Security
- Backend/API
- Frontend/UI
- Database
- Testing
- DevOps
- Mobile
- Performance
- SEO
- Planning

### Step 2: Phase Detection

| If Plan Exists | Action |
|----------------|--------|
| No `docs/PLAN.md` | Go to phase 1 |
| `docs/PLAN.md` exists and user approved | Go to phase 2 |

### Step 3: Execute Based on Phase

**Phase 1**
- Use `project-planner` to create `PLAN.md`
- Stop after planning
- Ask for approval

**Phase 2**
- Invoke multiple agents in parallel with clear scopes

### Critical Context Passing

When invoking any subagent, include:

1. Original user request
2. Decisions already made
3. Previous agent work
4. Current plan state and relevant files

Do not invoke subagents with partial context.

### Step 4: Verification

The last agent should run appropriate verification scripts when relevant, such as:

```bash
python .agents/skills/vulnerability-scanner/scripts/security_scan.py .
python .agents/skills/lint-and-validate/scripts/lint_runner.py .
```

### Step 5: Synthesize Results

Combine all agent outputs into one unified report.

## Output Format

```markdown
## Orchestration Report

### Task
[Original task summary]

### Mode
[Current mode]

### Agents Invoked (minimum 3)
| # | Agent | Focus Area | Status |
|---|-------|------------|--------|
| 1 | project-planner | Task breakdown | Done |
| 2 | frontend-specialist | UI implementation | Done |
| 3 | test-engineer | Verification | Done |

### Verification Scripts Executed
- security_scan.py -> Pass/Fail
- lint_runner.py -> Pass/Fail

### Key Findings
1. [Agent 1] Finding
2. [Agent 2] Finding
3. [Agent 3] Finding

### Deliverables
- [ ] PLAN.md created
- [ ] Code implemented
- [ ] Tests passing
- [ ] Scripts verified

### Summary
[Unified synthesis]
```
