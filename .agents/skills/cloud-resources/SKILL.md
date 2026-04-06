---
skill: cloud-resources
name: cloud-resources
version: 1.0.0
source: h4cker/cloud-resources
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 3
depends_on: [methodology]
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Review cloud exposure, logging posture, ownership signals, and service security evidence across AWS, Azure, and GCP with low-noise validation.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Cloud Resources Security Review

Summary: Review cloud exposure, logging posture, ownership signals, and service security evidence across AWS, Azure, and GCP with low-noise validation.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task is to review cloud-hosted assets, logging posture, ownership clues, or service exposure in AWS, Azure, or GCP
- Use when passive enrichment and low-noise verification should come before any deeper assessment
- Use when the output should connect internet-facing assets to likely cloud ownership, logging coverage, and defensive gaps
- Use when Codex should recommend cloud security improvements grounded in observable evidence
- Use when the user has domains, endpoints, or cloud service names but not a full architecture diagram

## KEY TECHNIQUES & TOOLS

### Phase 1: Resolve ownership and hosting clues

- Start with DNS and ownership enrichment:

```bash
dig app.example.com +short
```

→ See [common DNS baseline](../_shared/common-commands.md#dns-baseline) and [DNS ownership helper](../_shared/common-commands.md#dns-ownership-helper)

- Review TLS posture for exposed endpoints:

→ See [shared TLS audit helpers](../_shared/common-commands.md#tls-audit-helper)

- Record:
  - resolved IPs
  - cloud-provider hints
  - certificate issuer and SANs
  - ownership ambiguity

### Phase 2: Check logging and monitoring coverage

- Use the cloud-logging model from the source as the review backbone:
  - management-plane activity logs
  - data-access logs
  - network-flow logs
  - application logs
  - security-service alerts

- Ask or verify whether these exist:
  - AWS CloudTrail, CloudWatch Logs, VPC Flow Logs
  - Azure Activity Log, Log Analytics, NSG Flow Logs, Defender for Cloud
  - GCP Cloud Audit Logs, Cloud Logging, VPC Flow Logs, Security Command Center

- Capture evidence in a notes file:

```bash
mkdir -p cloud-review
printf "service,log_type,status,notes\n" > cloud-review/logging-matrix.csv
```

- If the user has screenshots, exported configs, or snippets, reduce them into one matrix instead of repeating prose

### Phase 3: Review common cloud logging threats

- Check for these risk classes from the source:
  - log injection or log poisoning
  - log tampering or deletion risk
  - missing immutable retention
  - weak access control around logging
  - disabled or partial audit coverage
  - insecure log transport or unencrypted storage

- Validate cloud logging hygiene with concrete questions:
  - Are control-plane events retained?
  - Are sensitive data stores audited?
  - Are flow logs or equivalent enabled?
  - Is log access least-privileged?
  - Is retention tiered and documented?

### Decision rules

- If ownership is uncertain, stop at passive enrichment and mark the asset as scope-sensitive until confirmed
- If the endpoint appears cloud-hosted but there is no evidence of audit or activity logging, prioritize visibility gaps before vulnerability speculation
- If certificate, DNS, and provider indicators disagree, report conflicting ownership clues instead of forcing one attribution
- If the user provides only one endpoint with no platform context, focus on ownership and logging questions rather than platform-specific remediation
- If the environment handles regulated data, treat missing audit or retention coverage as higher priority than generic best-practice drift

### Phase 4: Map service risks to platform-native controls

- For AWS-oriented reviews, look for:
  - CloudTrail enabled across accounts or regions
  - S3 access logging or equivalent data access visibility
  - GuardDuty, Config, and Security Hub coverage
  - VPC Flow Logs for sensitive networks

- For Azure-oriented reviews, look for:
  - Azure Activity Log retention
  - NSG Flow Logs and Log Analytics coverage
  - Defender for Cloud signal integration
  - RBAC around log workspaces

- For GCP-oriented reviews, look for:
  - Cloud Audit Logs enabled for admin and data access
  - VPC Flow Logs on critical subnets
  - IAM scoping for logging sinks and storage
  - Security Command Center signal flow

- Keep the assessment evidence-first; if you cannot see config proof, say so explicitly

### Phase 5: Produce a scoped review package

- Capture lightweight artifacts:

```bash
python3 .agents/scripts/h4cker_dns_ownership.py app.example.com > cloud-review/dns-ownership.json
python3 .agents/scripts/h4cker_tls_cert_audit.py app.example.com > cloud-review/tls-audit.json
jq '.hosting_hints, .whois' cloud-review/dns-ownership.json > cloud-review/ownership-summary.json
```

- If multiple hosts exist, review them one at a time:

```bash
while read -r host; do
  python3 .agents/scripts/h4cker_dns_ownership.py "$host" > "cloud-review/${host}.json"
done < hosts.txt
```

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Ownership and Exposure Summary`
  - `Logging Coverage Findings`
  - `Cloud Security Risks`
  - `Artifacts`
  - `Recommended Next Actions`

- `Scope` must state:
  - what asset or domain was reviewed
  - whether the work stayed passive or included low-noise TLS checks
  - which cloud platform is known or suspected

- `Ownership and Exposure Summary` should include:
  - resolved IPs
  - provider hints
  - certificate and DNS highlights
  - any scope uncertainty

- `Logging Coverage Findings` must group:
  - activity logging
  - data-access logging
  - network logging
  - retention and integrity

- `Cloud Security Risks` must separate:
  - confirmed visibility gaps
  - likely but unconfirmed gaps
  - platform questions still unanswered

- `Artifacts` should list:
  - DNS ownership output
  - TLS audit output
  - logging matrix or notes

- `Recommended Next Actions` must stay defensive:
  - enable missing logs
  - tighten IAM or RBAC
  - confirm ownership and service scope
  - review retention, encryption, and integrity controls

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
Use when you need a stable starting point before deeper cloud-resources review.
```bash
# Create the output directory for this skill
mkdir -p cloud-resources-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > cloud-resources-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > cloud-resources-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 cloud-resources-output/artifact-manifest.txt | xargs -r sha256sum > cloud-resources-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > cloud-resources-output/review-start-utc.txt
date > cloud-resources-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > cloud-resources-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' cloud-resources-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 cloud-resources-output/signal-hits.txt | sort | uniq -c | sort -nr > cloud-resources-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > cloud-resources-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > cloud-resources-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' cloud-resources-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > cloud-resources-output/git-status.txt 2>/dev/null || true
git diff --stat > cloud-resources-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > cloud-resources-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > cloud-resources-output/cloud-resources-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > cloud-resources-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' cloud-resources-output/cloud-resources-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find cloud-resources-output -maxdepth 2 -type f | sort > cloud-resources-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf cloud-resources-output/cloud-resources-bundle.tgz cloud-resources-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf cloud-resources-output/cloud-resources-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 cloud-resources-output/signal-hits.txt | sort | uniq -c | sort -nr > cloud-resources-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' cloud-resources-output/review-queue.txt > cloud-resources-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' cloud-resources-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > cloud-resources-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> cloud-resources-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' cloud-resources-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > cloud-resources-output/cloud-resources-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > cloud-resources-output/cloud-resources-final.md
# Preview the output files for QA
sed -n '1,20p' cloud-resources-output/cloud-resources-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `tls-cert-audit`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > cloud-resources-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 cloud-resources-output/cloud-resources-bundle.tgz > cloud-resources-output/cloud-resources-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > cloud-resources-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' cloud-resources-output/review-queue.txt > cloud-resources-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > cloud-resources-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find cloud-resources-output -maxdepth 2 -type f | sort > cloud-resources-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > cloud-resources-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' cloud-resources-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > cloud-resources-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > cloud-resources-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > cloud-resources-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > cloud-resources-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > cloud-resources-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `cloud-resources-output/cloud-resources-report.md`
- produce: `cloud-resources-output/output-manifest.txt`
- produce: `cloud-resources-output/cloud-resources-bundle.tgz`
- produce: `cloud-resources-output/cloud-resources-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `tls-cert-audit`
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

- Confirm `cloud-resources-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `tls-cert-audit` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `tls-cert-audit`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `tls-cert-audit` skill

- Load `tls-cert-audit` next if the current findings need deeper validation or formal handoff.
