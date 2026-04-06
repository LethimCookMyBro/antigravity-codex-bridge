---
skill: cheat-sheets
name: cheat-sheets
version: 1.0.0
source: h4cker/cheat-sheets
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Quick-reference operational patterns for safe evidence collection, validation, and reporting across defensive skill workflows.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Cheat Sheets

Summary: Quick-reference operational patterns for safe evidence collection, validation, and reporting across defensive skill workflows.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to cheat-sheets topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p cheat-sheets-output
find . -maxdepth 3 -type f | sort | head -100 > cheat-sheets-output/files.txt
ls -la cheat-sheets-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > cheat-sheets-output/signals.txt || true
sed -n '1,40p' cheat-sheets-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > cheat-sheets-output/inventory.txt
wc -l cheat-sheets-output/inventory.txt cheat-sheets-output/signals.txt 2>/dev/null || true
```

### Decision rules

- If the scope is unclear, stop and ask for the owned asset, repository, or lab boundary
- If evidence is weak or partial, label it as inconclusive instead of escalating the claim
- If another specialized skill fits better, hand off with the captured inventory and signals
- If the task would require unsafe or unapproved actions, stop at defensive analysis only

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Evidence Collected`
  - `Findings`
  - `Artifacts`
  - `Recommended Next Actions`

- `Artifacts` should list:
  - `cheat-sheets-output/files.txt`
  - `cheat-sheets-output/signals.txt`
  - `cheat-sheets-output/inventory.txt`

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
Use when you need a stable starting point before deeper work.
```bash
            # Create the output directory if it is not present yet
            mkdir -p cheat-sheets-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > cheat-sheets-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > cheat-sheets-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 cheat-sheets-output/artifact-manifest.txt | xargs -r sha256sum > cheat-sheets-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > cheat-sheets-output/review-start-utc.txt
date > cheat-sheets-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > cheat-sheets-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' cheat-sheets-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 cheat-sheets-output/signal-hits.txt | sort | uniq -c | sort -nr > cheat-sheets-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf cheat-sheets-output/review-bundle.tgz cheat-sheets-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum cheat-sheets-output/review-bundle.tgz > cheat-sheets-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf cheat-sheets-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > cheat-sheets-output/report-starter.md
            # Save a simple output manifest for the generated files
            find cheat-sheets-output -maxdepth 2 -type f | sort > cheat-sheets-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' cheat-sheets-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Quick file inventory
Use when the repo or evidence set is unfamiliar and you need the first artifact map.
```bash
# Capture a full file list for the working scope
find . -maxdepth 4 -type f | sort > cheat-sheets-output/files-deep.txt
# Save a short directory map
find . -maxdepth 2 -type d | sort > cheat-sheets-output/dirs-deep.txt
# Review the first lines before opening specific files
sed -n '1,50p' cheat-sheets-output/files-deep.txt
```
- Prefer this over opening random files.
- Keep the directory map beside the file list for orientation.

### Technique 7: Socket and route baseline
Use when you need a one-shot host-network snapshot for later comparison.
```bash
# Save listeners and active sockets
ss -tulpn > cheat-sheets-output/ss.txt 2>/dev/null || true
# Save IP addresses and routes
ip addr show > cheat-sheets-output/ip-addr.txt 2>/dev/null || true
ip route show > cheat-sheets-output/routes.txt 2>/dev/null || true
```
- This is strong first-pass evidence for service exposure.
- Do not interpret a listener as reachable without route context.

### Technique 8: Process and service triage
Use when you need a runtime snapshot before a service restarts or changes.
```bash
# Save top processes by CPU and memory
ps aux --sort=-%cpu,-%mem | head -60 > cheat-sheets-output/process-top.txt
# Save running services when systemd is present
systemctl list-units --type=service --state=running > cheat-sheets-output/services-running.txt 2>/dev/null || true
# Review failed services if any exist
systemctl --failed > cheat-sheets-output/services-failed.txt 2>/dev/null || true
```
- Runtime context often explains later findings.
- Keep both process and service views because they answer different questions.

### Technique 9: Log slicing by keyword
Use when raw logs are too large and you need the first high-signal slice.
```bash
# Pull common high-signal keywords from the current tree
rg -n "error|warn|failed|denied|timeout|exception" . > cheat-sheets-output/log-keywords.txt 2>/dev/null || true
# Save the last 200 lines from likely log files
find . -maxdepth 4 -type f -iname "*.log" | head -10 | xargs -r tail -200 > cheat-sheets-output/log-tail.txt 2>/dev/null || true
# Preview the first keyword hits
sed -n '1,60p' cheat-sheets-output/log-keywords.txt
```
- Use this to choose the next log file instead of guessing.
- Keep raw and sliced log output in separate files.

### Technique 10: Git and workspace delta review
Use when code or config drift may explain the current state.
```bash
# Save git status and diff stats
git status --short > cheat-sheets-output/git-status.txt 2>/dev/null || true
git diff --stat > cheat-sheets-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > cheat-sheets-output/git-log.txt 2>/dev/null || true
```
- This is especially useful before writing regression findings.
- A short git history often explains why a service or config changed.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `systematic-debugging`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception" . > cheat-sheets-output/log-keywords-grep.txt 2>/dev/null || true
```

### ถ้า `ss` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
netstat -tulpn > cheat-sheets-output/netstat.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
shasum -a 256 cheat-sheets-output/evidence-bundle.tgz > cheat-sheets-output/evidence-bundle.shasum 2>/dev/null || true
```

### ถ้า logs are huge:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 4 -type f -iname "*.log" | head -20 > cheat-sheets-output/log-candidates.txt
```

### ถ้า permission is limited:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 3 -type f -readable | sort > cheat-sheets-output/readable-files.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find cheat-sheets-output -maxdepth 2 -type f | sort > cheat-sheets-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > cheat-sheets-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' cheat-sheets-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Read-only evidence mount
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f | sort > /tmp/cheat-sheets-readonly-files.txt
```

### Edge Case: Very large repository
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg --files . | head -500 > cheat-sheets-output/first-500-files.txt
```

### Edge Case: Rotated logs
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find . -maxdepth 4 \( -iname "*.gz" -o -iname "*.old" -o -iname "*.1" \) | sort > cheat-sheets-output/rotated-log-files.txt
```

### Edge Case: Non-English locale
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
LC_ALL=C ps aux --sort=-%cpu,-%mem | head -40 > cheat-sheets-output/process-top-c.txt
```

### Edge Case: Mixed time zones
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
date -u > cheat-sheets-output/current-utc.txt
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search | May be absent | Keyword triage |
| grep -R | Universal fallback | Less friendly on big trees | Fallback search |
| find | Precise inventory | Needs more piping | Artifact manifests |


## Output Templates

- produce: `cheat-sheets-output/cheat-sheets-report.md`
- produce: `cheat-sheets-output/output-manifest.txt`
- produce: `cheat-sheets-output/review-bundle.tgz`
- produce: `cheat-sheets-output/cheat-sheets-findings.csv`

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

- Confirm `cheat-sheets-output` contains the report, manifest, and at least one evidence artifact.
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
- Which file or log would you open next if you had only two more minutes?
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
