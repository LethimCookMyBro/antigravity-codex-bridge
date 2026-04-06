---
skill: osint-recon
name: osint-recon
version: 1.0.0
source: codex/osint-recon
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 2
depends_on: [methodology, recon]
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Authorized passive reconnaissance and controlled surface validation for domains, identities, exposed services, and public web assets.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: OSINT Recon

Summary: Authorized passive reconnaissance and controlled surface validation for domains, identities, exposed services, and public web assets.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task is to map a target's public footprint before deeper testing
- Use when you need domains, subdomains, exposed hosts, public files, metadata, identities, or tech-stack clues
- Use when the target is in scope for authorized assessment, internal validation, bug bounty, or lab work
- Use when passive recon should come first and active validation should stay limited and deliberate
- Use when Codex must return evidence-backed findings plus the safest next recon steps

## KEY TECHNIQUES & TOOLS

### Phase 1: Scope, identity, and DNS baseline

- Start with ownership and DNS context:

```bash
whois example.com
dig example.com +short
dig NS example.com +short
dig MX example.com +short
dig TXT example.com +short
```

- Record:
  - registrant or organization clues
  - name servers
  - mail providers
  - SPF, DKIM, or other TXT records
  - CDN or edge-provider hints

- The repo includes local helpers that can tighten this phase:
  - `.agents/scripts/h4cker_dns_ownership.py`
  - `.agents/scripts/h4cker_tls_cert_audit.py`

→ See [shared DNS ownership helper](../_shared/common-commands.md#dns-ownership-helper) and [shared TLS audit helpers](../_shared/common-commands.md#tls-audit-helper)

- Expand passive domain discovery:

```bash
# WARNING: authorized targets only; keep recon passive and scoped
amass enum -passive -d example.com
subfinder -d example.com -all -silent
theHarvester -d example.com -b crtsh,anubis,certspotter
```

- Look specifically for naming patterns such as:
  - `staging`
  - `dev`
  - `admin`
  - `api`
  - `vpn`
  - `mail`
  - `legacy`
  - environment or region suffixes

### Phase 2: Search-driven exposure discovery

- Use search operators to uncover public files, portals, and leaked structure:

```text
site:example.com
site:example.com ext:pdf
site:example.com ext:doc OR ext:docx OR ext:xlsx OR ext:csv
site:example.com inurl:login
site:example.com inurl:signup OR inurl:register
site:example.com intitle:"index of"
site:example.com inurl:admin
site:example.com inurl:wp-content OR inurl:wp-admin
```

- Hunt for:
  - public documents
  - login and registration pages
  - exposed directories
  - backup or export files
  - CMS fingerprints
  - support, partner, and internal-looking portals

- If the task is broad, treat search results as discovery only until validated by DNS or HTTP evidence

### Phase 3: Certificates, internet exposure, and service intelligence

- Use certificate transparency and public exposure platforms to enrich the inventory
- For Shodan-style research, use filters deliberately:

```bash
# WARNING: use third-party exposure data only for owned or explicitly authorized targets
shodan search 'hostname:"example.com"' --fields ip_str,port,org,hostnames
shodan search 'ssl.cert.subject.cn:"example.com"' --fields ip_str,port,org
shodan host 203.0.113.10
```

- Useful search shapes:
  - product-based
  - organization-based
  - country-based
  - vulnerability-tag-based
  - service or banner-based

- Example query patterns:

```text
apache
product:"GoAhead-Webs"
org:"Example Corp"
port:22 country:"US"
vuln:CVE-2021-44228
```

- Extract:
  - IPs
  - ports
  - org or ISP
  - banner strings
  - exposed products
  - vulnerability labels requiring manual verification

### Phase 4: Identity, metadata, and relationship mapping

- Extract metadata from public files:

```bash
exiftool public-file.pdf
exiftool public-image.jpg
```

- Use metadata and public profiles to infer:
  - employee naming conventions
  - email address formats
  - software author names
  - internal hostnames
  - document paths or usernames

- Use graph-based or transform-based tooling when the investigation benefits from relationship mapping:
  - Maltego-style entity graphs
  - recon-ng style module chaining
  - username or email enrichment workflows

- Focus the graph around:
  - domains
  - email addresses
  - employees
  - certificates
  - related organizations

### Phase 5: Lightweight host and web validation

- Validate discovered hosts without jumping to aggressive scanning:

```bash
# WARNING: authorized targets only; start with low-noise validation
# Use this discovery-oriented variant for an ad-hoc host list when you need lightweight evidence only.
curl -I https://sub.example.com
httpx -l hosts.txt -title -tech-detect -status-code -follow-host-redirects
```

- Record:
  - status code
  - redirect chain
  - page title
  - detected technology
  - auth or admin entry points
  - API docs or exposed debug pages

- For controlled web validation in authorized scope, use targeted checks instead of broad scans:

```bash
# WARNING: authorized targets only; keep checks low-noise and rate-limited
# Use this broader variant for recon confirmation; switch to web-application-testing for deep app review.
nikto -h app.example.com -ssl -p 443 -output osint-recon-output/nikto-report.html -Format html
nuclei -u https://app.example.com -tags cve,exposure,misconfig -rl 50 -c 10
```

- Use Nikto for:
  - default content
  - dangerous files
  - missing headers
  - risky HTTP methods
  - exposed admin or status endpoints

- Use Nuclei for:
  - template-based validation
  - CVE checks
  - exposure patterns
  - focused misconfiguration testing

- Prefer narrowed template sets and explicit rate limits over "scan everything"

### Decision rules

- If the target is clearly third-party hosted, stop after ownership enrichment and ask for scope confirmation before doing active validation
- If search results reveal auth panels or admin portals, verify them with low-noise HTTP metadata first before running template scanners
- If the task is passive-only, skip Nikto, Nuclei, and service enumeration entirely and stay in certificate, DNS, and public-source workflows
- If internal ranges or AD services are not explicitly authorized, do not move into SMB, LDAP, or RDP-oriented checks

### Phase 6: Internal or service-specific enumeration

- If the authorized scope includes internal hosts, use targeted discovery:

```bash
# WARNING: authorized internal scope only
nmap -Pn -sC -sV -p 53,80,88,135,139,389,445,636,3389,5985,5986 target
nbtscan -r 192.168.11.0/24
enum4linux-ng.py -A -oJ osint-recon-output/enum4linux-ng target
smbmap -u "" -p "" -H target
```

- For Windows or AD-style surface mapping, extract:
  - DNS domain names
  - NetBIOS names
  - LDAP exposure
  - SMB signing state
  - RDP identity details
  - HTTP management endpoints

- For SMB-focused validation, use:

```bash
# WARNING: authorized internal scope only
nmap --script smb-os-discovery,smb-enum-shares,smb-enum-users,smb-security-mode -p 139,445 target
rpcclient -U "" target
smbclient -L //target -N
```

- Treat service enumeration as confirmation and inventory, not exploitation

### Phase 7: DNS misconfiguration validation

- Use zone transfer checks only for owned domains or safe labs:

```bash
dig axfr @nsztm1.digi.ninja zonetransfer.me
```

- Use the result to identify:
  - subdomains
  - mail endpoints
  - internal naming
  - TXT records
  - unexpected service exposure

- Do not treat AXFR as a default step for arbitrary public targets

### Phase 8: Recon automation and evidence collection

- Use quick automation only when it stays inside authorized public-source or low-noise checks
- Example workspace pattern:

```bash
# WARNING: authorized targets only; keep automation scoped to approved domains and low-noise validation
mkdir -p osint-recon-output
whois example.com > osint-recon-output/whois.txt
subfinder -d example.com -all -silent | tee osint-recon-output/subdomains.txt
httpx -l osint-recon-output/subdomains.txt -title -tech-detect -status-code > osint-recon-output/httpx.txt
nikto -h app.example.com -ssl -p 443 -output osint-recon-output/nikto.html -Format html
nuclei -l osint-recon-output/subdomains.txt -tags exposure,misconfig -jsonl -o osint-recon-output/nuclei.jsonl
```

- Normalize the evidence into:
  - confirmed assets
  - likely related assets
  - exposed documents
  - external attack surface
  - credential or identity clues
  - follow-up validation targets

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Inventory`
  - `Evidence`
  - `Findings`
  - `Recommended Next Steps`

- `Scope` must state:
  - target
  - assumptions
  - whether the work stayed passive only or included controlled validation

- `Inventory` should group:
  - domains and subdomains
  - hosts and ports
  - web endpoints
  - public files
  - identity clues

- `Evidence` must include the strongest commands run and the important outputs they produced

- `Findings` must separate:
  - confirmed evidence
  - inferred relationships
  - items needing manual verification

- `Recommended Next Steps` must stay safe and scoped:
  - more passive enrichment
  - narrow validation
  - remediation or hardening checks
  - ownership confirmation

- Prefer short tables and grouped bullets over long narrative prose

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
Use when you need a stable starting point before deeper osint-recon review.
```bash
# Create the output directory for this skill
mkdir -p osint-recon-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > osint-recon-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > osint-recon-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 osint-recon-output/artifact-manifest.txt | xargs -r sha256sum > osint-recon-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > osint-recon-output/review-start-utc.txt
date > osint-recon-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > osint-recon-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' osint-recon-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 osint-recon-output/signal-hits.txt | sort | uniq -c | sort -nr > osint-recon-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > osint-recon-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > osint-recon-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' osint-recon-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > osint-recon-output/git-status.txt 2>/dev/null || true
git diff --stat > osint-recon-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > osint-recon-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > osint-recon-output/osint-recon-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > osint-recon-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' osint-recon-output/osint-recon-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find osint-recon-output -maxdepth 2 -type f | sort > osint-recon-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf osint-recon-output/osint-recon-bundle.tgz osint-recon-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf osint-recon-output/osint-recon-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 osint-recon-output/signal-hits.txt | sort | uniq -c | sort -nr > osint-recon-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' osint-recon-output/review-queue.txt > osint-recon-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' osint-recon-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > osint-recon-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> osint-recon-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' osint-recon-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > osint-recon-output/osint-recon-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > osint-recon-output/osint-recon-final.md
# Preview the output files for QA
sed -n '1,20p' osint-recon-output/osint-recon-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > osint-recon-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 osint-recon-output/osint-recon-bundle.tgz > osint-recon-output/osint-recon-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > osint-recon-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' osint-recon-output/review-queue.txt > osint-recon-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > osint-recon-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find osint-recon-output -maxdepth 2 -type f | sort > osint-recon-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > osint-recon-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' osint-recon-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > osint-recon-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > osint-recon-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > osint-recon-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > osint-recon-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > osint-recon-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `osint-recon-output/osint-recon-report.md`
- produce: `osint-recon-output/output-manifest.txt`
- produce: `osint-recon-output/osint-recon-bundle.tgz`
- produce: `osint-recon-output/osint-recon-findings.csv`

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

- Confirm `osint-recon-output` contains the report, manifest, and at least one evidence artifact.
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
