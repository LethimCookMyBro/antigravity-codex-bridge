---
skill: recon
name: recon
version: 1.0.0
source: h4cker/recon
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 2
depends_on: [methodology]
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Authorized low-noise reconnaissance router. Build a scoped target inventory, preserve evidence, and hand off clean inputs to web application testing.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Recon

Summary: Authorized low-noise reconnaissance router. Build a scoped target inventory, preserve evidence, and hand off clean inputs to web application testing.
Does NOT cover deep web exploitation; stop at scoped discovery and low-noise validation.

## WHEN TO USE THIS SKILL

- Use when a target domain, hostname, or small IP scope must be mapped before deeper review
- Use when public-source discovery and low-noise validation should happen before web testing
- Use when the user asks for asset discovery, subdomains, exposed hosts, or attack-surface inventory
- Use when Codex must return a clean target list that another skill can consume

## INPUT FROM

- user-provided target scope
- bug bounty program scope notes
- prior `methodology` plan if one exists

## KEY TECHNIQUES & TOOLS

### Phase 1: Confirm scope and seed targets

- Start by normalizing the target into one of:
  - single domain
  - list of subdomains
  - small explicit IP list

```bash
mkdir -p recon
printf '%s\n' example.com > recon/scope.txt
whois example.com > recon/whois.txt
dig example.com +short | tee recon/root-a.txt
```

- If the scope is unclear, stop and ask for:
  - owned target
  - testing authorization
  - passive-only vs validation allowed

### Phase 2: Passive discovery first

```bash
# WARNING: authorized targets only; keep discovery passive in this phase
subfinder -d example.com -all -silent | tee recon/subdomains.txt
amass enum -passive -d example.com | tee -a recon/subdomains.txt
sort -u recon/subdomains.txt -o recon/subdomains.txt
python3 .agents/scripts/h4cker_dns_ownership.py example.com > recon/dns-ownership.json
```

- If `subfinder` or `amass` is unavailable, fall back to:

```bash
dig NS example.com +short
dig MX example.com +short
python3 .agents/scripts/h4cker_dns_ownership.py example.com
```

### Phase 3: Low-noise HTTP and TLS validation

```bash
# WARNING: authorized targets only; validate lightly before deeper testing
httpx -l recon/subdomains.txt -status-code -title -tech-detect -json -o recon/httpx.jsonl
python3 .agents/scripts/h4cker_tls_cert_audit.py example.com > recon/tls-root.json
curl -I https://example.com
```

- If `httpx` is unavailable, validate only the top candidates:

```bash
while read -r host; do curl -k -I "https://$host" | head -20; done < recon/subdomains.txt
```

### Decision rules

- If the request is passive-only, stop before Nuclei, Nikto, or version scanning
- If the target is a third-party SaaS or vendor endpoint, return ownership context and ask for scope confirmation before further validation
- If a discovered host is clearly a login, admin, or API surface, promote it into the handoff list for `web-application-testing`
- If the scope contains raw IPs only, inventory them and avoid hostname assumptions

## OUTPUT FORMAT

- Produce:
  - `Scope`
  - `Targets Confirmed`
  - `Discovery Evidence`
  - `High-Value Web Targets`
  - `Recommended Handoff`

- Write or describe these artifacts when possible:
  - `recon/scope.txt`
  - `recon/subdomains.txt`
  - `recon/httpx.jsonl`
  - `recon/dns-ownership.json`

- `High-Value Web Targets` must be a newline list that `web-application-testing` can consume directly

## HANDOFF

- Input to `web-application-testing`:
  - `recon/subdomains.txt`
  - prioritized URLs from `recon/httpx.jsonl`
  - any admin, auth, upload, or API endpoints found during validation

## Quick Mode (< 5 minutes)

- Confirm one domain or one small IP list before expanding scope.
- Run only the passive discovery block first and save `recon/subdomains.txt`.
- Stop once you have a clean host list plus one validation artifact.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the target blocks, errors, or returns nothing, capture the raw error output and narrow the scope before retrying.
- If the dataset is too large, split by host, file, or time window before rerunning the skill.
- Edge case 1: IPv6-only hosts; record that IPv4-only validation is incomplete.
- Edge case 2: non-standard HTTPS ports; save the port with the hostname in the handoff list.


## Phase Output Map

- Phase 1 output: a scoped starting artifact such as an inventory file, target file, or working directory.
- Phase 2 output: one or more evidence files captured from the main validation step.
- Phase 3 output: a short findings set or structured artifact ready for review or handoff.


## Done When

- A scope file, host list, and one validation artifact exist.
- High-value web targets are listed one per line for handoff.
- The next tester can continue without asking what was in scope.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper recon review.
```bash
# Create the output directory for this skill
mkdir -p recon-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > recon-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > recon-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 recon-output/artifact-manifest.txt | xargs -r sha256sum > recon-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > recon-output/review-start-utc.txt
date > recon-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > recon-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' recon-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 recon-output/signal-hits.txt | sort | uniq -c | sort -nr > recon-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > recon-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > recon-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' recon-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > recon-output/git-status.txt 2>/dev/null || true
git diff --stat > recon-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > recon-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > recon-output/recon-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > recon-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' recon-output/recon-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find recon-output -maxdepth 2 -type f | sort > recon-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf recon-output/recon-bundle.tgz recon-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf recon-output/recon-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 recon-output/signal-hits.txt | sort | uniq -c | sort -nr > recon-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' recon-output/review-queue.txt > recon-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' recon-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > recon-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> recon-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' recon-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > recon-output/recon-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > recon-output/recon-final.md
# Preview the output files for QA
sed -n '1,20p' recon-output/recon-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `web-application-testing`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > recon-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 recon-output/recon-bundle.tgz > recon-output/recon-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > recon-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' recon-output/review-queue.txt > recon-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > recon-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find recon-output -maxdepth 2 -type f | sort > recon-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > recon-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' recon-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > recon-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > recon-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > recon-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > recon-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > recon-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `recon-output/recon-report.md`
- produce: `recon-output/output-manifest.txt`
- produce: `recon-output/recon-bundle.tgz`
- produce: `recon-output/recon-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `web-application-testing`
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

- Confirm `recon-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `web-application-testing` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `web-application-testing`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `web-application-testing` skill

- Load `web-application-testing` next if the current findings need deeper validation or formal handoff.
