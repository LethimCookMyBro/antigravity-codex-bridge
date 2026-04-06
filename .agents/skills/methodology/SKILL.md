---
skill: methodology
name: methodology
version: 1.0.0
source: h4cker/methodology
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 1
depends_on: []
os_support: [kali, ubuntu, parrot]
description: Build a scoped security assessment plan with phase gates, evidence requirements, and clean handoffs between recon, testing, and defensive review.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Security Methodology

Summary: Build a scoped security assessment plan with phase gates, evidence requirements, and clean handoffs between recon, testing, and defensive review.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the request is broad and needs a phased plan before execution
- Use when multiple security skills must hand off cleanly
- Use when the user needs scope controls, evidence requirements, and stop conditions

## INPUT FROM

- user goals
- scope notes
- existing outputs from `recon`, `web-application-testing`, or `iot-hacking`

## KEY TECHNIQUES & TOOLS

### Phase 1: Define the assessment lanes

- Separate work into:
  - discovery
  - validation
  - root-cause review
  - defensive follow-up

```bash
mkdir -p methodology-output
printf '%s\n' "discovery" "validation" "root-cause review" "defensive follow-up" > methodology-output/lanes.txt
cat methodology-output/lanes.txt
```

### Phase 2: Set evidence requirements

- Require:
  - target list
  - timestamps
  - raw request/response or command output
  - explicit scope note for any higher-risk action

```bash
printf '%s\n' "phase,goal,input,stop_condition" > assessment-plan.csv
printf '%s\n' "recon,inventory,scope.txt,scope unclear" >> assessment-plan.csv
cat assessment-plan.csv
```

### Phase 3: Tie each phase to a concrete owner and handoff

```bash
printf '%s\n' "phase,primary_skill,handoff_output" > methodology-output/skill-handoffs.csv
printf '%s\n' "recon,recon,live-hosts.txt + ports.txt" >> methodology-output/skill-handoffs.csv
printf '%s\n' "validation,web-application-testing,findings.md + raw-http/" >> methodology-output/skill-handoffs.csv
cat methodology-output/skill-handoffs.csv
```

### Decision rules

- If a downstream skill would require more aggressive behavior than the scope allows, stop at the current phase and report the blocker
- If the user only wants planning, do not run commands
- If a finding is not evidence-backed, do not promote it into the next phase

## Fallbacks

- If the scope is missing, return a planning template with the unknown fields clearly marked
- If only one phase is authorized, collapse the plan to that phase and list what remains blocked
- If multiple skills overlap, choose one primary owner and list the others as supporting handoffs

## OUTPUT FORMAT

- Produce:
  - `Objective`
  - `Scope`
  - `Phase Plan`
  - `Required Inputs`
  - `Stop Conditions`
  - `Next Skill`

- `Artifacts` should list:
  - `methodology-output/lanes.txt`
  - `assessment-plan.csv`
  - `methodology-output/skill-handoffs.csv`

## HANDOFF

- Input to `recon`, `web-application-testing`, or `iot-hacking`:
  - phase order
  - scope boundaries
  - evidence requirements
  - stop conditions

## Quick Mode (< 5 minutes)

- Write the phase lanes first.
- Add one stop condition per phase.
- Stop once the next skill and required inputs are explicit.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the user wants planning only, skip execution commands and keep the output as a phase plan plus handoffs.
- If two skills appear to own the same phase, choose one as primary and list the other as support.
- Edge case 1: the scope contains both cloud and on-prem assets; split them into separate lanes.
- Edge case 2: only one tiny phase is authorized; keep the unused phases documented as blocked, not omitted.


## Phase Output Map

- Phase 1 output: named assessment lanes.
- Phase 2 output: evidence and stop-condition matrix.
- Phase 3 output: skill ownership and handoff artifact list.


## Done When

- Scope, lanes, and stop conditions are all written down.
- Each phase has a primary skill and expected handoff artifact.
- A junior tester can tell what to do first and what not to do yet.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper methodology review.
```bash
# Create the output directory for this skill
mkdir -p methodology-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > methodology-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > methodology-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 methodology-output/artifact-manifest.txt | xargs -r sha256sum > methodology-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > methodology-output/review-start-utc.txt
date > methodology-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > methodology-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' methodology-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 methodology-output/signal-hits.txt | sort | uniq -c | sort -nr > methodology-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > methodology-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > methodology-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' methodology-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > methodology-output/git-status.txt 2>/dev/null || true
git diff --stat > methodology-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > methodology-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > methodology-output/methodology-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > methodology-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' methodology-output/methodology-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find methodology-output -maxdepth 2 -type f | sort > methodology-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf methodology-output/methodology-bundle.tgz methodology-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf methodology-output/methodology-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 methodology-output/signal-hits.txt | sort | uniq -c | sort -nr > methodology-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' methodology-output/review-queue.txt > methodology-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' methodology-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > methodology-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> methodology-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' methodology-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > methodology-output/methodology-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > methodology-output/methodology-final.md
# Preview the output files for QA
sed -n '1,20p' methodology-output/methodology-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `recon`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > methodology-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 methodology-output/methodology-bundle.tgz > methodology-output/methodology-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > methodology-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' methodology-output/review-queue.txt > methodology-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > methodology-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find methodology-output -maxdepth 2 -type f | sort > methodology-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > methodology-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' methodology-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > methodology-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > methodology-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > methodology-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > methodology-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > methodology-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `methodology-output/methodology-report.md`
- produce: `methodology-output/output-manifest.txt`
- produce: `methodology-output/methodology-bundle.tgz`
- produce: `methodology-output/methodology-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `recon`
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

- Confirm `methodology-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `recon` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `recon`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `recon` skill

- Load `recon` next if the current findings need deeper validation or formal handoff.
