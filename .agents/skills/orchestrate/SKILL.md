---
skill: orchestrate
name: orchestrate
version: 1.0.0
source: codex/orchestrate
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---
# Orchestrate

Summary: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.
## WHEN TO USE THIS SKILL

- Use when the task clearly matches `orchestrate` or the folder's specialized domain
- Use when Codex should follow a repeatable workflow instead of ad-hoc reasoning
- Use when the output should separate scope, evidence, findings, and next actions


This skill adapts the Antigravity `/orchestrate` workflow for Codex.
Treat the user's message as the task to orchestrate.

## Critical Minimum Requirement

Orchestration means a minimum of 3 different agents.

- If you use fewer than 3 agents, you are delegating, not orchestrating.
- Before completion, validate that at least 3 distinct specialists were used.
- If the user has not explicitly allowed sub-agents, perform local orchestration instead: break the task into at least 3 specialist perspectives, work them sequentially, and state that delegation was simulated locally.

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

## Fallbacks

- If sub-agents are unavailable, blocked, or not explicitly requested by the user, stay local and produce the same orchestration report with `Execution Mode: Local`
- If fewer than 3 real domains are involved, do not force orchestration; say that the task is better handled directly
- If no `docs/PLAN.md` exists and planning is required, stop after planning and wait for approval before implementation

### Step 4: Verification

The last agent should run appropriate verification scripts when relevant, such as:

```bash
python3 .agents/skills/vulnerability-scanner/scripts/security_scan.py .
python3 .agents/skills/lint-and-validate/scripts/lint_runner.py .
```

### Step 5: Synthesize Results

Combine all agent outputs into one unified report.

## Output Format

```markdown
## Orchestration Report

### Task
[Original task summary]

### Mode
[Current mode / Execution Mode]

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


## OUTPUT FORMAT

- Return:
  - `Scope`
  - `Evidence`
  - `Findings`
  - `Artifacts`
  - `Next Actions`
- Name any generated files by exact path so the next reviewer does not have to rediscover them.

## Quick Mode (< 5 minutes)

- Start with the first scope or inventory command, not the whole workflow.
- Limit the first pass to one host, one file, one repo, or one artifact set.
- Stop after you have one saved artifact and a short findings draft.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the target blocks, errors, or returns nothing, capture the raw error output and narrow the scope before retrying.
- If the dataset is too large, split by host, file, or time window before rerunning the skill.
- Edge case 1: the source format is custom or incomplete; save a sample and document the gap.
- Edge case 2: the work depends on a non-default port, path, or encoding; record it before rerunning commands.


## Phase Output Map

- Phase 1 output: a scoped starting artifact such as an inventory file, target file, or working directory.
- Phase 2 output: one or more evidence files captured from the main validation step.
- Phase 3 output: a short findings set or structured artifact ready for review or handoff.


## Done When

- Scope is fixed and written down.
- At least one reproducible artifact is saved.
- The next skill or teammate can continue without re-discovering context.



- Load the next narrower or downstream skill only after saving artifacts from this one.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper orchestrate review.
```bash
# Create the output directory for this skill
mkdir -p orchestrate-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > orchestrate-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > orchestrate-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 orchestrate-output/artifact-manifest.txt | xargs -r sha256sum > orchestrate-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > orchestrate-output/review-start-utc.txt
date > orchestrate-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > orchestrate-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' orchestrate-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 orchestrate-output/signal-hits.txt | sort | uniq -c | sort -nr > orchestrate-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > orchestrate-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > orchestrate-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' orchestrate-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > orchestrate-output/git-status.txt 2>/dev/null || true
git diff --stat > orchestrate-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > orchestrate-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > orchestrate-output/orchestrate-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > orchestrate-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' orchestrate-output/orchestrate-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find orchestrate-output -maxdepth 2 -type f | sort > orchestrate-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf orchestrate-output/orchestrate-bundle.tgz orchestrate-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf orchestrate-output/orchestrate-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 orchestrate-output/signal-hits.txt | sort | uniq -c | sort -nr > orchestrate-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' orchestrate-output/review-queue.txt > orchestrate-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' orchestrate-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > orchestrate-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> orchestrate-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' orchestrate-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > orchestrate-output/orchestrate-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > orchestrate-output/orchestrate-final.md
# Preview the output files for QA
sed -n '1,20p' orchestrate-output/orchestrate-final.md
```
- The finding sheet keeps output machine-readable.
- The final markdown skeleton tells the next reviewer exactly what to expect.

## Decision Logic

- If the first inventory artifact already answers the question → stop and write the answer instead of widening scope.
- If the primary technique produces only noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only files.
- If the work is limited to passive or lab-only scope → skip any technique that would mutate state or add traffic.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `systematic-debugging`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > orchestrate-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 orchestrate-output/orchestrate-bundle.tgz > orchestrate-output/orchestrate-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > orchestrate-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' orchestrate-output/review-queue.txt > orchestrate-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > orchestrate-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find orchestrate-output -maxdepth 2 -type f | sort > orchestrate-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > orchestrate-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' orchestrate-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > orchestrate-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > orchestrate-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > orchestrate-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > orchestrate-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > orchestrate-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `orchestrate-output/orchestrate-report.md`
- produce: `orchestrate-output/output-manifest.txt`
- produce: `orchestrate-output/orchestrate-bundle.tgz`
- produce: `orchestrate-output/orchestrate-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `systematic-debugging`
```

machine-readable skeleton:
```text
artifact|type|purpose|used_in_finding
```

## Evidence Checklist

- Save the first inventory artifact before deeper analysis.
- Keep UTC timestamps for the review start.
- Keep raw and normalized outputs separate.
- Hash the final bundle if another reviewer will use it.
- Name output files with the skill prefix.
- Record whether evidence came from live inspection, config review, or offline artifacts.
- Record whether permissions limited the review.
- Keep exact artifact paths in every finding.
- Remove unrelated files from the final bundle.
- Verify all generated files still exist before closing the task.

## Common Mistakes to Avoid

- Expanding scope before the first inventory file is saved.
- Mixing lab-only and production evidence in one summary.
- Writing findings without exact artifact paths.
- Using generic names like `output.txt` or `report.md`.
- Treating missing permissions as proof that nothing exists.
- Keeping only screenshots without supporting raw text output.
- Forgetting time zone, host, package, or build context.
- Handing off without an artifact manifest.
- Reusing commands from another scope without renaming outputs.
- Deleting intermediate artifacts before the report is accepted.

## Verification Checklist

- Confirm `orchestrate-output` contains the report, manifest, and at least one evidence artifact.
- Confirm every finding cites an exact artifact path.
- Confirm the next skill is named explicitly.
- Confirm at least one fallback path is documented.
- Confirm the report separates observations, unknowns, and next actions.
- Confirm filenames are unique and skill-prefixed.
- Confirm no placeholder text remains.
- Confirm the quick mode output still makes sense if the full workflow was not run.
- Confirm the report can be read without reopening the terminal transcript.
- Confirm artifacts are still present on disk before closing the task.

## Review Questions for Junior Analysts

- Which artifact did you trust first, and why?
- Which artifact contradicted your first assumption?
- Which fallback would you use if the main tool disappeared?
- Which file would you open next if you had only two more minutes?
- Which output file would you hand to the next reviewer first?
- Which step created the strongest evidence for your finding?
- Which environment assumption would change your conclusion?
- Which artifact proves ownership, scope, or lab context?
- Which output names would confuse another reviewer if left generic?
- What exact question should the next skill `systematic-debugging` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `systematic-debugging`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load the next specialized skill

- Load the next narrower or downstream skill only after saving artifacts from this one.
