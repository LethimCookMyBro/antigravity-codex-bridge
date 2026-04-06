---
skill: devsecops
name: devsecops
version: 1.0.0
source: h4cker/devsecops
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 3
depends_on: [methodology]
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Review CI/CD, dependencies, secrets, and deployment automation with evidence-first security checks for owned repositories and pipelines.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: DevSecOps

Summary: Review CI/CD, dependencies, secrets, and deployment automation with evidence-first security checks for owned repositories and pipelines.
Does NOT cover live production mutation by default; review and validate before changing pipelines.

## WHEN TO USE THIS SKILL

- Use when the task involves CI/CD security, repository hardening, pipeline review, or release controls
- Use when Codex should inspect manifests, workflows, container build rules, and validation scripts before release
- Use when the user asks for secure automation, supply-chain review, or secret exposure checks in an owned repository
- Use when the result should distinguish configuration gaps, evidence collected, and safe remediation steps

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory pipeline and package surfaces

- Start by identifying the automation and dependency entry points:

```bash
mkdir -p devsecops-output
find . -maxdepth 3 \( -name ".github" -o -name ".gitlab-ci.yml" -o -name "azure-pipelines*.yml" -o -name "Jenkinsfile" \)
find . -maxdepth 3 \( -name "Dockerfile*" -o -name "docker-compose*.yml" -o -name "package.json" -o -name "requirements*.txt" -o -name "pyproject.toml" -o -name "go.mod" -o -name "Cargo.toml" \)
```

### Phase 2: Review secrets and risky automation patterns

- Search for high-signal misconfigurations before suggesting changes:

```bash
rg -n "AWS_|BEGIN (RSA|OPENSSH|PRIVATE KEY)|password\\s*=|token\\s*=|Authorization:" .
rg -n "curl .*\\|\\s*(bash|sh)|wget .*\\|\\s*(bash|sh)|chmod \\+x .*&&" .github .gitlab-ci.yml Jenkinsfile azure-pipelines*.yml 2>/dev/null
rg -n "latest|--privileged|CAP_SYS_ADMIN|hostNetwork: true|allowPrivilegeEscalation: true" .
```

### Phase 3: Run repo-local validation helpers

- Prefer the repo helpers before inventing ad-hoc checks:

```bash
python3 .agents/scripts/checklist.py . --url http://localhost:3000
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
```

- Capture the outputs for later reporting:

```bash
mkdir -p devsecops-output
python3 .agents/scripts/checklist.py . --url http://localhost:3000 > devsecops-output/checklist.txt 2>&1 || true
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e > devsecops-output/verify.txt 2>&1 || true
```

### Phase 4: Inspect container and deployment guardrails

- Review Docker and manifest posture with low-noise repo inspection:

```bash
rg -n "USER root|ADD http|curl .*\\| sh|apt-get upgrade|apk upgrade|sudo " Dockerfile* **/Dockerfile* 2>/dev/null
rg -n "imagePullPolicy: Always|privileged: true|hostPID: true|hostIPC: true|runAsUser: 0|runAsNonRoot: false" . 2>/dev/null
rg -n "permissions: write-all|id-token: write|pull_request_target|workflow_dispatch" .github/workflows 2>/dev/null
```

### Phase 5: Summarize dependency and artifact exposure

- Record what must be monitored or locked down:

```bash
find . -maxdepth 4 \( -name "package-lock.json" -o -name "pnpm-lock.yaml" -o -name "poetry.lock" -o -name "Cargo.lock" -o -name "go.sum" \) > devsecops-output/lockfiles.txt
find . -maxdepth 4 \( -name "*.pem" -o -name "*.key" -o -name ".env" -o -name ".npmrc" -o -name ".pypirc" \) > devsecops-output/sensitive-files.txt
```

### Decision rules

- If secrets appear committed in-repo, prioritize rotation and history cleanup before general pipeline hardening
- If release helpers already fail locally, fix validation fidelity before adding more pipeline stages
- If the project uses containers, treat Docker and workload policy review as part of the minimum baseline
- If the repo has no lockfiles, mark dependency reproducibility as a supply-chain gap

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Pipeline Inventory`
  - `Secret and Supply-Chain Findings`
  - `Container and Deployment Findings`
  - `Artifacts`
  - `Recommended Next Actions`

- `Scope` must state:
  - which repository or service was reviewed
  - which automation systems were present
  - whether repo-local validation helpers were run

- `Pipeline Inventory` should include:
  - workflow files found
  - container build files
  - dependency manifests and lockfiles

- `Secret and Supply-Chain Findings` must separate:
  - confirmed secret exposure
  - risky automation patterns
  - reproducibility or provenance gaps

- `Container and Deployment Findings` should include:
  - risky Dockerfile patterns
  - risky Kubernetes or compose settings
  - permission or token overreach in CI

- `Artifacts` should list:
  - `devsecops-output/checklist.txt`
  - `devsecops-output/verify.txt`
  - `devsecops-output/lockfiles.txt`
  - `devsecops-output/sensitive-files.txt`

- `Recommended Next Actions` must stay defensive:
  - secret rotation and cleanup
  - pipeline least privilege
  - dependency locking and review
  - container or manifest hardening

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

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper devsecops review.
```bash
# Create the output directory for this skill
mkdir -p devsecops-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > devsecops-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > devsecops-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 devsecops-output/artifact-manifest.txt | xargs -r sha256sum > devsecops-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > devsecops-output/review-start-utc.txt
date > devsecops-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > devsecops-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' devsecops-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 devsecops-output/signal-hits.txt | sort | uniq -c | sort -nr > devsecops-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > devsecops-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > devsecops-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' devsecops-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > devsecops-output/git-status.txt 2>/dev/null || true
git diff --stat > devsecops-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > devsecops-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > devsecops-output/devsecops-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > devsecops-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' devsecops-output/devsecops-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find devsecops-output -maxdepth 2 -type f | sort > devsecops-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf devsecops-output/devsecops-bundle.tgz devsecops-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf devsecops-output/devsecops-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 devsecops-output/signal-hits.txt | sort | uniq -c | sort -nr > devsecops-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' devsecops-output/review-queue.txt > devsecops-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' devsecops-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > devsecops-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> devsecops-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' devsecops-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > devsecops-output/devsecops-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > devsecops-output/devsecops-final.md
# Preview the output files for QA
sed -n '1,20p' devsecops-output/devsecops-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `sbom`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > devsecops-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 devsecops-output/devsecops-bundle.tgz > devsecops-output/devsecops-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > devsecops-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' devsecops-output/review-queue.txt > devsecops-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > devsecops-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find devsecops-output -maxdepth 2 -type f | sort > devsecops-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > devsecops-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' devsecops-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > devsecops-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > devsecops-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > devsecops-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > devsecops-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > devsecops-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `devsecops-output/devsecops-report.md`
- produce: `devsecops-output/output-manifest.txt`
- produce: `devsecops-output/devsecops-bundle.tgz`
- produce: `devsecops-output/devsecops-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `sbom`
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

- Confirm `devsecops-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `sbom` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `sbom`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `sbom` skill

- Load `sbom` next if the current findings need deeper validation or formal handoff.
