---
skill: web-application-testing
name: web-application-testing
version: 1.0.0
source: h4cker/web-application-testing
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 3
depends_on: [methodology, recon]
os_support: [kali, ubuntu, parrot]
description: Authorized web application review using scoped inventory, low-noise validation, and evidence-first findings that can hand off to deeper root-cause analysis.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Web Application Testing

Summary: Authorized web application review using scoped inventory, low-noise validation, and evidence-first findings that can hand off to deeper root-cause analysis.
Does NOT cover exploit execution; stop at reproducible evidence and safe handoff.

## WHEN TO USE THIS SKILL

- Use when a scoped web target has already been identified and needs structured testing
- Use when the user asks for a web assessment, web pentest, OWASP review, or API surface validation
- Use when Codex should produce reproducible findings instead of broad scan output dumps
- Use when handoff to root-cause review is needed without creating exploit instructions

## INPUT FROM

- `recon/subdomains.txt`
- prioritized URLs from `recon/httpx.jsonl`
- explicit endpoints supplied by the user

## KEY TECHNIQUES & TOOLS

### Phase 1: Normalize targets and auth boundaries

```bash
mkdir -p web-review
cp recon/subdomains.txt web-review/targets.txt 2>/dev/null || true
printf '%s\n' https://example.com > web-review/targets.txt
```

- Record:
  - target URLs
  - whether authenticated testing is allowed
  - rate limits or safe-hours restrictions

### Phase 2: Safe fingerprinting and header review

```bash
# WARNING: authorized targets only; stay within the scoped host list
# Write JSON evidence here because downstream findings and handoff depend on saved web-app artifacts.
httpx -l web-review/targets.txt -status-code -title -tech-detect -follow-host-redirects -json -o web-review/httpx.jsonl
curl -isk https://example.com/ | sed -n '1,40p' > web-review/root-response.txt
curl -isk https://example.com/robots.txt > web-review/robots.txt
```

- Inspect for:
  - security headers
  - cookies and flags
  - redirect behavior
  - framework fingerprints
  - exposed docs or debug routes

### Phase 3: Focused validation

```bash
# WARNING: authorized targets only; keep validation low-noise and rate-limited
# Focus here on confirmed web targets and preserve app-specific evidence for later validation or review.
nikto -h example.com -ssl -p 443 -Format txt -output web-review/nikto.txt
nuclei -u https://example.com -tags exposure,misconfig,cve -rl 25 -c 5 -jsonl -o web-review/nuclei.jsonl
katana -u https://example.com -silent -d 2 -o web-review/katana.txt
```

- If a target list exists:

```bash
# WARNING: authorized targets only; run only against the scoped target list
nuclei -l web-review/targets.txt -tags exposure,misconfig -rl 25 -c 5 -jsonl -o web-review/nuclei.jsonl
```

- If `nikto` or `nuclei` is unavailable, stay with:
  - manual `curl`
  - `httpx`
  - route and header review

### Phase 4: Parameter and workflow review

- Check:
  - auth-required routes
  - upload flows
  - redirects
  - API docs
  - GraphQL or REST entry points
  - error message leakage

```bash
# WARNING: authorized targets only; use read-only request patterns first
curl -isk https://example.com/login
curl -isk https://example.com/api/health
curl -isk https://example.com/graphql
```

### Decision rules

- If the app is out of scope or third-party hosted, stop and return ownership findings only
- If authenticated paths are discovered but credentials or approval are missing, mark them as untested and do not improvise access
- If a finding looks real but proof would require exploit execution, stop at evidence capture and hand off to `exploit-development` for root-cause review without weaponized steps
- If the request is broad, prioritize auth, admin, upload, API, and debug surfaces first

## OUTPUT FORMAT

- Produce:
  - `Scope`
  - `Targets Tested`
  - `Evidence Collected`
  - `Validated Findings`
  - `Untested Areas`
  - `Recommended Handoff`

- Artifacts should include:
  - `web-review/targets.txt`
  - `web-review/httpx.jsonl`
  - `web-review/nikto.txt` if used
  - `web-review/nuclei.jsonl` if used

- `Validated Findings` must include:
  - URL
  - category
  - evidence
  - impact
  - safe next action

## HANDOFF

- Input to `exploit-development`:
  - finding summary
  - exact URL or component
  - raw request/response evidence
  - why deeper reproduction is needed

## Quick Mode (< 5 minutes)

- Start with one scoped URL or one target list file.
- Run the header and fingerprint block before any crawler or scanner.
- Stop after you have one reproducible finding or a clean no-finding baseline.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the target blocks, errors, or returns nothing, capture the raw error output and narrow the scope before retrying.
- If the dataset is too large, split by host, file, or time window before rerunning the skill.
- Edge case 1: a WAF or rate limit blocks requests; keep evidence and reduce request rate.
- Edge case 2: the app is only on a custom port or path prefix; record the exact base URL before continuing.


## Phase Output Map

- Phase 1 output: a scoped starting artifact such as an inventory file, target file, or working directory.
- Phase 2 output: one or more evidence files captured from the main validation step.
- Phase 3 output: a short findings set or structured artifact ready for review or handoff.


## Done When

- The tested target list is saved.
- Each finding has URL, evidence, impact, and safe next action.
- Untested areas are listed explicitly instead of implied.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper web-application-testing review.
```bash
# Create the output directory for this skill
mkdir -p web-application-testing-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > web-application-testing-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > web-application-testing-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 web-application-testing-output/artifact-manifest.txt | xargs -r sha256sum > web-application-testing-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > web-application-testing-output/review-start-utc.txt
date > web-application-testing-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > web-application-testing-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' web-application-testing-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 web-application-testing-output/signal-hits.txt | sort | uniq -c | sort -nr > web-application-testing-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > web-application-testing-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > web-application-testing-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' web-application-testing-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > web-application-testing-output/git-status.txt 2>/dev/null || true
git diff --stat > web-application-testing-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > web-application-testing-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > web-application-testing-output/web-application-testing-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > web-application-testing-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' web-application-testing-output/web-application-testing-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find web-application-testing-output -maxdepth 2 -type f | sort > web-application-testing-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf web-application-testing-output/web-application-testing-bundle.tgz web-application-testing-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf web-application-testing-output/web-application-testing-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 web-application-testing-output/signal-hits.txt | sort | uniq -c | sort -nr > web-application-testing-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' web-application-testing-output/review-queue.txt > web-application-testing-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' web-application-testing-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > web-application-testing-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> web-application-testing-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' web-application-testing-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > web-application-testing-output/web-application-testing-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > web-application-testing-output/web-application-testing-final.md
# Preview the output files for QA
sed -n '1,20p' web-application-testing-output/web-application-testing-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `exploit-development`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > web-application-testing-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 web-application-testing-output/web-application-testing-bundle.tgz > web-application-testing-output/web-application-testing-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > web-application-testing-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' web-application-testing-output/review-queue.txt > web-application-testing-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > web-application-testing-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find web-application-testing-output -maxdepth 2 -type f | sort > web-application-testing-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > web-application-testing-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' web-application-testing-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > web-application-testing-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > web-application-testing-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > web-application-testing-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > web-application-testing-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > web-application-testing-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `web-application-testing-output/web-application-testing-report.md`
- produce: `web-application-testing-output/output-manifest.txt`
- produce: `web-application-testing-output/web-application-testing-bundle.tgz`
- produce: `web-application-testing-output/web-application-testing-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `exploit-development`
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

- Confirm `web-application-testing-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `exploit-development` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `exploit-development`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `exploit-development` skill

- Load `exploit-development` next if the current findings need deeper validation or formal handoff.
