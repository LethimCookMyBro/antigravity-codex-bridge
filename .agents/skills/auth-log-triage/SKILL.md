---
skill: auth-log-triage
name: auth-log-triage
version: 1.0.0
source: codex/auth-log-triage
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Triage Linux authentication logs with grep, awk, and Python parsers to correlate users, failures, source IPs, and sudo activity.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Auth Log Triage

Summary: Triage Linux authentication logs with grep, awk, and Python parsers to correlate users, failures, source IPs, and sudo activity.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task is to investigate `/var/log/auth.log` or rotated auth logs for suspicious login activity
- Use when you need to pivot between usernames, source IPs, failed logins, successful logins, and sudo commands
- Use when quick shell-based triage should come first, followed by lightweight Python parsing for correlation
- Use when the source data may include plain text logs and `.gz` rotated archives
- Use when Codex must return evidence-backed findings, not just raw grep output

## KEY TECHNIQUES & TOOLS

### Phase 1: Define scope and preserve the source

- Identify the exact log source before searching:

```bash
ls -lh /var/log/auth.log*
file /var/log/auth.log /var/log/auth.log.1.gz
```

- Work from copies when possible:

```bash
cp /var/log/auth.log ./auth.log
zcat /var/log/auth.log.1.gz > ./auth.log.1
```

- Treat these event families as primary pivots:
  - `Accepted password for`
  - `Failed password for`
  - `for invalid user`
  - `authentication failure`
  - `sudo:`

### Phase 2: Use shell triage first

- Start with exact searches when you know the indicator:

```bash
grep "user hoover" /var/log/auth.log
grep "authentication failure" /var/log/auth.log
grep "sudo:" /var/log/auth.log
```

- Use regex when the raw string is too noisy:

```bash
grep -P "(?<=port\\s)4792" /var/log/auth.log
grep -E "Accepted password|Failed password|Invalid user" /var/log/auth.log
```

- Pull context around a suspicious event:

```bash
grep -B 3 -A 2 "Invalid user" /var/log/auth.log
grep -B 2 -A 3 "authentication failure" /var/log/auth.log
```

- Watch live failures during testing or incident response:

```bash
tail -f /var/log/auth.log | grep "Invalid user"
tail -f /var/log/auth.log | grep "Failed password"
```

- Parse key fields fast with `cut` and `awk`:

```bash
grep "authentication failure" /var/log/auth.log | cut -d '=' -f 8
awk '/sshd.*invalid user/ { print $9 }' /var/log/auth.log
awk '/.err>/ { print }' /var/log/auth.log
```

- Use shell triage to answer:
  - which usernames were targeted
  - which source IPs recur
  - whether failures later became successes
  - whether privileged commands were executed afterward

### Phase 3: Parse and correlate with Python

- The source folder contains a small parser split across `ParseLogs.py` and `logalyzer.py`
- The repo now includes a local helper adapted from that source at `.agents/scripts/h4cker_auth_logalyzer.py`
- The parser tracks these per-user buckets:
  - all matching logs
  - failure logs
  - success logs
  - source IPs
  - sudo commands

- Supported line patterns from the parser include:
  - accepted SSH logins
  - failed SSH logins
  - invalid users
  - `su` and `sudo` authentication failures
  - sudo command execution

- The parser can read plain files and `.gz` archives, so keep rotated logs in scope when needed

- Use the local helper like this:

```bash
python3 .agents/scripts/h4cker_auth_logalyzer.py ./auth.log
python3 .agents/scripts/h4cker_auth_logalyzer.py ./auth.log --user alice
python3 .agents/scripts/h4cker_auth_logalyzer.py ./auth.log.1.gz --format text
```

- The original source used a separate `logalyzer.py` CLI, but this repo standardizes on the local helper above so the commands stay runnable here.

- Use the CLI output to answer:
  - first seen and last seen activity for a user
  - which IPs were tied to a user
  - which failures and successes belong to the same account
  - which sudo commands were run by that user

### Decision rules

- If the log volume is small and the indicator is obvious, stay in shell first and only run the helper after you have one concrete pivot
- If the same account shows both failures and later successes, pivot into IP correlation immediately before making any compromise claim
- If rotated `.gz` logs exist, include them before deciding whether a pattern is isolated or recurring
- If `sudo:` events appear after a successful login, treat privilege-use correlation as higher priority than raw failure counts
- If a user is absent from the helper output, verify spelling and grep the raw file before assuming the account never appeared

## Fallbacks

- If the log path is missing, ask for the exact file or use the path the user already provided
- If the helper is unavailable, stay with `grep`, `awk`, and `zcat` pivots and state that parser correlation was skipped
- If timestamps are incomplete across rotated logs, report the gap before making chronology claims

### Phase 4: Build the incident picture

- Correlate by user first, then by IP, then by action
- Separate these cases:
  - repeated invalid usernames from one IP
  - repeated failures against one valid account
  - success after many failures
  - successful login followed by sudo command execution

- Build a minimal evidence workspace:

```bash
mkdir -p triage
grep -E "Accepted password|Failed password|Invalid user|sudo:" /var/log/auth.log > triage/auth-high-signal.txt
awk '/sshd.*invalid user/ { print $9 }' /var/log/auth.log | sort | uniq -c | sort -nr > triage/invalid-users.txt
python3 .agents/scripts/h4cker_auth_logalyzer.py ./auth.log > triage/auth-logalyzer.json
jq 'to_entries[] | {user: .key, ips: .value.ips, failure_count: .value.failure_count, success_count: .value.success_count}' triage/auth-logalyzer.json > triage/user-summary.json
```

- Prefer short, reproducible pivots over manual scrolling
- If the logs are very large, extract the high-signal subset first and preserve the raw file path in the report

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Log Sources`
  - `Triage Findings`
  - `Correlated Entities`
  - `Evidence`
  - `Recommended Next Actions`

- `Scope` must state:
  - which log files were analyzed
  - whether rotated or compressed logs were included
  - whether the review was shell-only or also used the Python parser

- `Log Sources` should list:
  - file paths
  - time coverage if visible
  - any gaps or assumptions

- `Triage Findings` must separate:
  - failed login patterns
  - successful login patterns
  - sudo or privilege-related activity
  - anomalous usernames or source IPs

- `Correlated Entities` should map:
  - user to IPs
  - user to failures
  - user to successes
  - user to commands

- `Evidence` must include the exact commands used and the most important matching lines
- `Evidence` should include both:
  - the quick shell pivots
  - the `.agents/scripts/h4cker_auth_logalyzer.py` output when it was used

- `Recommended Next Actions` should stay defensive:
  - deeper timeline review
  - IP reputation or ownership checks
  - account hardening
  - log retention and monitoring follow-up

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
Use when you need a stable starting point before deeper auth-log-triage review.
```bash
# Create the output directory for this skill
mkdir -p auth-log-triage-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > auth-log-triage-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > auth-log-triage-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 auth-log-triage-output/artifact-manifest.txt | xargs -r sha256sum > auth-log-triage-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > auth-log-triage-output/review-start-utc.txt
date > auth-log-triage-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > auth-log-triage-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' auth-log-triage-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 auth-log-triage-output/signal-hits.txt | sort | uniq -c | sort -nr > auth-log-triage-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > auth-log-triage-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > auth-log-triage-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' auth-log-triage-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > auth-log-triage-output/git-status.txt 2>/dev/null || true
git diff --stat > auth-log-triage-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > auth-log-triage-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > auth-log-triage-output/auth-log-triage-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > auth-log-triage-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' auth-log-triage-output/auth-log-triage-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find auth-log-triage-output -maxdepth 2 -type f | sort > auth-log-triage-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf auth-log-triage-output/auth-log-triage-bundle.tgz auth-log-triage-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf auth-log-triage-output/auth-log-triage-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 auth-log-triage-output/signal-hits.txt | sort | uniq -c | sort -nr > auth-log-triage-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' auth-log-triage-output/review-queue.txt > auth-log-triage-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' auth-log-triage-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > auth-log-triage-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> auth-log-triage-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' auth-log-triage-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > auth-log-triage-output/auth-log-triage-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > auth-log-triage-output/auth-log-triage-final.md
# Preview the output files for QA
sed -n '1,20p' auth-log-triage-output/auth-log-triage-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > auth-log-triage-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 auth-log-triage-output/auth-log-triage-bundle.tgz > auth-log-triage-output/auth-log-triage-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > auth-log-triage-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' auth-log-triage-output/review-queue.txt > auth-log-triage-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > auth-log-triage-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find auth-log-triage-output -maxdepth 2 -type f | sort > auth-log-triage-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > auth-log-triage-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' auth-log-triage-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > auth-log-triage-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > auth-log-triage-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > auth-log-triage-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > auth-log-triage-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > auth-log-triage-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `auth-log-triage-output/auth-log-triage-report.md`
- produce: `auth-log-triage-output/output-manifest.txt`
- produce: `auth-log-triage-output/auth-log-triage-bundle.tgz`
- produce: `auth-log-triage-output/auth-log-triage-findings.csv`

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

- Confirm `auth-log-triage-output` contains the report, manifest, and at least one evidence artifact.
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
