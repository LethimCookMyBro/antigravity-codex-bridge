---
skill: dfir
name: dfir
version: 1.0.0
source: h4cker/dfir
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 1
depends_on: [methodology]
os_support: [windows, kali, ubuntu, parrot]
python_min: 3.8
description: Perform defensive digital forensics and incident response triage across logs, pcaps, host artifacts, and timelines using low-noise evidence collection patterns.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Digital Forensics and Incident Response

Summary: Perform defensive digital forensics and incident response triage across logs, pcaps, host artifacts, and timelines using low-noise evidence collection patterns.
Does NOT cover offensive replay; stay with evidence collection, correlation, and response support.

## WHEN TO USE THIS SKILL

- Use when the task is to investigate a suspected compromise, suspicious host behavior, malware indicators, or unusual network activity
- Use when evidence must be collected and preserved before making remediation or containment claims
- Use when the user has logs, pcaps, host triage output, memory-analysis notes, or threat-hunting artifacts that need correlation
- Use when the work must stay defensive, evidence-backed, and reproducible
- Use when Codex should produce a clean incident narrative, IOC list, timeline, and next-response actions

## INPUT FROM

- raw logs, pcaps, or host artifacts supplied by the user
- `post-exploitation` impact review outputs
- `exploit-development` indicators that must be hunted historically
- `threat-hunting` correlations that need formal incident handling

## KEY TECHNIQUES & TOOLS

### Phase 1: Set scope and preserve evidence

- Start by identifying what evidence classes exist:
  - host logs
  - auth logs
  - firewall or proxy logs
  - Zeek or HTTP logs
  - pcaps
  - memory notes
  - disk artifacts
  - suspicious files

- Build a working directory immediately:

```bash
mkdir -p dfir/{raw,working,notes,output}
find /path/to/evidence -maxdepth 2 -type f | sort > dfir/notes/evidence-index.txt
```

- Preserve metadata before transforming anything:

```bash
sha256sum /path/to/evidence/* > dfir/notes/hashes.txt
file /path/to/evidence/* > dfir/notes/file-types.txt
```

- If the source data is already a copy, note that explicitly in the final report
- If the source data is volatile or remote, collect only what is needed for the current hypothesis and document gaps

### Phase 2: Quick triage by evidence type

- For auth or system logs:

```bash
rg -n "Failed password|Accepted password|sudo:|authentication failure" /path/to/logs
python3 .agents/scripts/h4cker_auth_logalyzer.py /path/to/auth.log --format text
```

- For generic security logs or mixed telemetry:

```bash
python3 .agents/scripts/h4cker_ai_log_analysis.py /path/to/logs/security.log --output dfir/output/ai-log-analysis.json
jq '.summary, .threat_level, .iocs' dfir/output/ai-log-analysis.json
```

- For network captures:

```bash
# WARNING: capture and inspect only owned or explicitly authorized packet data
tcpdump -nn -r captured.pcap | head -100
tshark -r captured.pcap -q -z io,phs
```

- For Zeek-style HTTP or scan indicators:

```bash
rg -n "Nmap|masscan|curl|wget|sqlmap" /path/to/http.log
python3 - <<'PY'
import csv
from collections import Counter
from pathlib import Path
path = Path('/path/to/http.log')
counts = Counter()
for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
    if 'Nmap' in line or 'masscan' in line:
        counts['scanner-indicators'] += 1
print(counts)
PY
```

- For suspicious files or archives:

```bash
sha256sum suspicious.bin
strings -a suspicious.bin | head -100
file suspicious.bin
```

### Phase 3: Correlate and reduce noise

- Correlate across:
  - timestamp
  - user
  - host
  - source IP
  - destination IP
  - process or command
  - filename or hash

- Build focused pivots instead of scanning everything at once:

```bash
rg -n "203.0.113.45|alice|powershell|sudo:" /path/to/evidence
rg -n "malware.example|evilcdn|wget|curl" /path/to/evidence
```

- Normalize evidence into buckets:
  - confirmed malicious
  - suspicious but unconfirmed
  - benign background noise
  - requires more evidence

### Decision rules

- If a claimed IOC appears only in AI output and not in raw evidence, mark it as inferred until verified
- If auth, network, and application evidence disagree on chronology, build a timeline before assigning root cause
- If a file or host indicator appears once with no supporting context, preserve it as weak evidence instead of escalating it
- If a pcap, Zeek log, and auth log all implicate the same IP or user, prioritize that entity for timeline construction
- If the evidence source is incomplete or obviously truncated, state the limitation before offering remediation advice

### Phase 4: Build the timeline

- Use the simplest consistent format possible:

```bash
printf "timestamp\tsource\tentity\tevent\n" > dfir/output/timeline.tsv
```

- Append key events as you confirm them:

```bash
printf "2026-04-06T02:14:31Z\tauth.log\talice\tfailed login from 203.0.113.45\n" >> dfir/output/timeline.tsv
printf "2026-04-06T02:17:10Z\thttp.log\t203.0.113.45\tNmap-style probe indicator\n" >> dfir/output/timeline.tsv
```

- Sort when needed:

```bash
sort dfir/output/timeline.tsv > dfir/output/timeline-sorted.tsv
```

- Capture uncertainty in the event wording instead of rewriting timestamps to fit a theory

### Phase 5: Produce IOC and artifact bundles

- Maintain one machine-readable IOC file:

```bash
cat > dfir/output/iocs.json <<'JSON'
{
  "ip_addresses": [],
  "domains": [],
  "urls": [],
  "file_hashes": [],
  "user_accounts": []
}
JSON
```

- Extract or append indicators as they are validated:

```bash
jq '.ip_addresses += ["203.0.113.45"] | .user_accounts += ["alice"]' dfir/output/iocs.json > dfir/output/iocs.tmp && mv dfir/output/iocs.tmp dfir/output/iocs.json
```

- Store report-supporting artifacts:
  - triage output
  - hashes
  - IOC bundle
  - timeline
  - screenshots or notebook excerpts if the source came from Jupyter or dashboards

### Phase 6: Escalate with precision

- Use these escalation paths:
  - ask for more evidence when the story is incomplete
  - recommend containment when the evidence is strong and current
  - recommend hardening when the evidence shows exposure but not confirmed compromise
  - recommend monitoring updates when the evidence is weak but repeatable

- If the investigation touches a cloud or internet-facing host, combine this skill with:
  - `.agents/scripts/h4cker_dns_ownership.py`
  - `.agents/scripts/h4cker_tls_cert_audit.py`

```bash
python3 .agents/scripts/h4cker_dns_ownership.py suspicious.example.com
python3 .agents/scripts/h4cker_tls_cert_audit.py suspicious.example.com --check-weak-ciphers
```

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Evidence Reviewed`
  - `Timeline`
  - `Validated Findings`
  - `IOCs`
  - `Artifacts Produced`
  - `Recommended Next Actions`

- `Scope` must state:
  - what incident or hypothesis was investigated
  - which evidence sources were in scope
  - what was unavailable or incomplete

- `Evidence Reviewed` should list:
  - file paths
  - log types
  - packet captures
  - triage helper scripts used

- `Timeline` must include:
  - timestamp
  - source
  - entity
  - event summary
  - whether the event is confirmed or inferred

- `Validated Findings` must separate:
  - confirmed malicious activity
  - suspicious but unconfirmed activity
  - environmental noise or false-positive candidates

- `IOCs` must group:
  - IP addresses
  - domains
  - URLs
  - file hashes
  - user accounts

- `Artifacts Produced` must include:
  - generated JSON
  - TSV timelines
  - any helper-script outputs

- `Recommended Next Actions` must stay defensive:
  - containment review
  - further collection
  - host isolation criteria
  - logging improvements
  - hardening or detection updates

## HANDOFF

- Input to `threat-hunting`:
  - validated IOCs
  - timeline anchors
  - candidate entities for broader hunts

## Quick Mode (< 5 minutes)

- Create the working directory and hash the supplied evidence first.
- Pivot on one IOC, one user, or one time window instead of the full dataset.
- Stop once timeline, IOC bundle, and top findings are written.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the target blocks, errors, or returns nothing, capture the raw error output and narrow the scope before retrying.
- If the dataset is too large, split by host, file, or time window before rerunning the skill.
- Edge case 1: logs are compressed or rotated; normalize one file at a time.
- Edge case 2: timestamps use mixed time zones; build the timeline in UTC before concluding sequence.


## Phase Output Map

- Phase 1 output: a scoped starting artifact such as an inventory file, target file, or working directory.
- Phase 2 output: one or more evidence files captured from the main validation step.
- Phase 3 output: a short findings set or structured artifact ready for review or handoff.


## Done When

- Evidence hashes, timeline, and IOC bundle are saved.
- Confirmed findings are separated from inferred findings.
- A responder can continue from the saved artifacts without re-triaging from scratch.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper dfir review.
```bash
# Create the output directory for this skill
mkdir -p dfir-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > dfir-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > dfir-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 dfir-output/artifact-manifest.txt | xargs -r sha256sum > dfir-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > dfir-output/review-start-utc.txt
date > dfir-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > dfir-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' dfir-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 dfir-output/signal-hits.txt | sort | uniq -c | sort -nr > dfir-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > dfir-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > dfir-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' dfir-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > dfir-output/git-status.txt 2>/dev/null || true
git diff --stat > dfir-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > dfir-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > dfir-output/dfir-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > dfir-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' dfir-output/dfir-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find dfir-output -maxdepth 2 -type f | sort > dfir-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf dfir-output/dfir-bundle.tgz dfir-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf dfir-output/dfir-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 dfir-output/signal-hits.txt | sort | uniq -c | sort -nr > dfir-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' dfir-output/review-queue.txt > dfir-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' dfir-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > dfir-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> dfir-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' dfir-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > dfir-output/dfir-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > dfir-output/dfir-final.md
# Preview the output files for QA
sed -n '1,20p' dfir-output/dfir-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `threat-hunting`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > dfir-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 dfir-output/dfir-bundle.tgz > dfir-output/dfir-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > dfir-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' dfir-output/review-queue.txt > dfir-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > dfir-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find dfir-output -maxdepth 2 -type f | sort > dfir-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > dfir-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' dfir-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > dfir-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > dfir-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > dfir-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > dfir-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > dfir-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `dfir-output/dfir-report.md`
- produce: `dfir-output/output-manifest.txt`
- produce: `dfir-output/dfir-bundle.tgz`
- produce: `dfir-output/dfir-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `threat-hunting`
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

- Confirm `dfir-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `threat-hunting` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `threat-hunting`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `threat-hunting` skill

- Load `threat-hunting` next if the current findings need deeper validation or formal handoff.
