---
skill: ai-incident-log-analysis
name: ai-incident-log-analysis
version: 1.0.0
source: codex/ai-incident-log-analysis
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Use structured AI-assisted log analysis for incident response, IOC extraction, and triage summaries with a local helper script.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: AI Incident Log Analysis

Summary: Use structured AI-assisted log analysis for incident response, IOC extraction, and triage summaries with a local helper script.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when a user has log files and wants fast triage, IOC extraction, or incident-response summaries
- Use when shell triage alone is too slow and an LLM can help classify findings into threat levels and recommendations
- Use when the task is defensive or authorized incident response, not offensive simulation
- Use when Codex should combine deterministic prep steps with structured AI analysis instead of pasting logs directly into chat
- Use when the output needs a stable JSON artifact plus a human-readable summary

## KEY TECHNIQUES & TOOLS

### Phase 1: Prepare the log set

- Identify which files matter before invoking the model:

```bash
ls -lh /path/to/logs
rg -n "Failed password|Accepted password|sudo:|error|denied|malware|alert" /path/to/logs
```

- Extract a high-signal subset if the logs are very large:

```bash
mkdir -p ir-work
rg -n "Failed password|Accepted password|sudo:|error|alert|unauthorized|denied" /path/to/logs > ir-work/high-signal.log
```

- Normalize encoding and preserve a stable input file path for the report
- Prefer one focused log per run over an unbounded directory dump

### Phase 2: Run the local analysis helper

- The repo includes a helper script at `.agents/scripts/h4cker_ai_log_analysis.py`
- The script is based on the `h4cker/ai-for-incident-response` example and keeps the source idea:
  - read a log file
  - send a structured IR prompt to an OpenAI model
  - return JSON with summary, threat level, findings, IOCs, and recommendations

- Run it like this:

```bash
python3 .agents/scripts/h4cker_ai_log_analysis.py ir-work/high-signal.log
python3 .agents/scripts/h4cker_ai_log_analysis.py /path/to/auth.log --output ir-work/auth-analysis.json
python3 .agents/scripts/h4cker_ai_log_analysis.py /path/to/firewall.log --model gpt-4.1-mini --max-chars 30000
```

- Use environment variables when needed:

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=gpt-4.1-mini
```

- Treat the AI result as triage guidance, not as final proof

### Decision rules

- If the raw log file is larger than the helper's `--max-chars` limit, slice it into focused subsets before calling the model
- If the model reports an IOC that does not appear in the raw evidence, mark it as inferred and verify it before escalating severity
- If the log source mixes unrelated systems, split by source type before running the helper so the JSON output stays coherent
- If the first pass returns only generic findings, tighten the input file with `rg` and rerun on a smaller high-signal subset
- If the log contains secrets, tokens, or customer data, redact or narrow it before sending it to the model

### Phase 3: Validate the AI result with local evidence

- Cross-check the strongest claims with shell pivots:

```bash
jq . ir-work/auth-analysis.json
rg -n "203.0.113.45|alice|sudo:" /path/to/auth.log
```

- Validate:
  - suspicious IPs
  - usernames
  - domains
  - file hashes
  - timestamps
  - repeated failure patterns

- Separate:
  - confirmed findings visible in raw logs
  - plausible findings inferred by the model
  - claims that need manual verification

### Phase 4: Turn JSON into an IR summary

- Use the JSON output as the evidence anchor
- Pull out:
  - `summary`
  - `threat_level`
  - `findings`
  - `iocs`
  - `recommendations`

- Favor these workflows:
  - auth log triage
  - firewall or proxy alert review
  - host telemetry spot checks
  - suspicious application log review

- Do not use this skill to automate enforcement or containment without human review

### Post-processing patterns

```bash
python3 .agents/scripts/h4cker_ai_log_analysis.py ir-work/high-signal.log --output ir-work/analysis.json
jq '.summary, .threat_level, .iocs' ir-work/analysis.json
```

```bash
jq -r '.findings[] | [.severity, .type, .description] | @tsv' ir-work/analysis.json > ir-work/findings.tsv
```

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Input Logs`
  - `AI Analysis Summary`
  - `Validated Findings`
  - `IOCs`
  - `Recommended Next Actions`

- `Scope` must state:
  - the log source
  - what subset was analyzed
  - which model and script were used

- `Input Logs` should list:
  - file paths
  - time coverage if known
  - any filtering performed before analysis

- `AI Analysis Summary` must include:
  - threat level
  - whether malicious activity was detected
  - the top findings from the JSON output

- `Validated Findings` must separate:
  - confirmed by raw evidence
  - plausible but unconfirmed
  - false-positive risks

- `IOCs` should group:
  - IP addresses
  - domains
  - file hashes
  - user accounts

- `Recommended Next Actions` must stay defensive:
  - further log pivots
  - containment review
  - monitoring updates
  - hardening or detection improvements

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
Use when you need a stable starting point before deeper ai-incident-log-analysis review.
```bash
# Create the output directory for this skill
mkdir -p ai-incident-log-analysis-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > ai-incident-log-analysis-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > ai-incident-log-analysis-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 ai-incident-log-analysis-output/artifact-manifest.txt | xargs -r sha256sum > ai-incident-log-analysis-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > ai-incident-log-analysis-output/review-start-utc.txt
date > ai-incident-log-analysis-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > ai-incident-log-analysis-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' ai-incident-log-analysis-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 ai-incident-log-analysis-output/signal-hits.txt | sort | uniq -c | sort -nr > ai-incident-log-analysis-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > ai-incident-log-analysis-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > ai-incident-log-analysis-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' ai-incident-log-analysis-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > ai-incident-log-analysis-output/git-status.txt 2>/dev/null || true
git diff --stat > ai-incident-log-analysis-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > ai-incident-log-analysis-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > ai-incident-log-analysis-output/ai-incident-log-analysis-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > ai-incident-log-analysis-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' ai-incident-log-analysis-output/ai-incident-log-analysis-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find ai-incident-log-analysis-output -maxdepth 2 -type f | sort > ai-incident-log-analysis-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf ai-incident-log-analysis-output/ai-incident-log-analysis-bundle.tgz ai-incident-log-analysis-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf ai-incident-log-analysis-output/ai-incident-log-analysis-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 ai-incident-log-analysis-output/signal-hits.txt | sort | uniq -c | sort -nr > ai-incident-log-analysis-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' ai-incident-log-analysis-output/review-queue.txt > ai-incident-log-analysis-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' ai-incident-log-analysis-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > ai-incident-log-analysis-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> ai-incident-log-analysis-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' ai-incident-log-analysis-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > ai-incident-log-analysis-output/ai-incident-log-analysis-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > ai-incident-log-analysis-output/ai-incident-log-analysis-final.md
# Preview the output files for QA
sed -n '1,20p' ai-incident-log-analysis-output/ai-incident-log-analysis-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > ai-incident-log-analysis-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 ai-incident-log-analysis-output/ai-incident-log-analysis-bundle.tgz > ai-incident-log-analysis-output/ai-incident-log-analysis-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > ai-incident-log-analysis-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' ai-incident-log-analysis-output/review-queue.txt > ai-incident-log-analysis-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > ai-incident-log-analysis-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find ai-incident-log-analysis-output -maxdepth 2 -type f | sort > ai-incident-log-analysis-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > ai-incident-log-analysis-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' ai-incident-log-analysis-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > ai-incident-log-analysis-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > ai-incident-log-analysis-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > ai-incident-log-analysis-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > ai-incident-log-analysis-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > ai-incident-log-analysis-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `ai-incident-log-analysis-output/ai-incident-log-analysis-report.md`
- produce: `ai-incident-log-analysis-output/output-manifest.txt`
- produce: `ai-incident-log-analysis-output/ai-incident-log-analysis-bundle.tgz`
- produce: `ai-incident-log-analysis-output/ai-incident-log-analysis-findings.csv`

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

- Confirm `ai-incident-log-analysis-output` contains the report, manifest, and at least one evidence artifact.
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
