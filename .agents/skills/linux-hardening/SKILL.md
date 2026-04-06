---
skill: linux-hardening
name: linux-hardening
version: 1.0.0
source: h4cker/linux-hardening
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 3
depends_on: [methodology]
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Harden Linux systems with evidence-based checks for compromise, firewall posture, system integrity, privilege exposure, and log visibility.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Linux Hardening

Summary: Harden Linux systems with evidence-based checks for compromise, firewall posture, system integrity, privilege exposure, and log visibility.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the user wants to secure a Linux host, review a hardening baseline, or investigate signs of compromise
- Use when the task involves firewall selection, kernel-module review, process triage, integrity checks, or auth-log inspection
- Use when Codex should recommend practical remediation steps instead of generic benchmark lists
- Use when the host is owned or administratively controlled and defensive validation is allowed
- Use when the output should distinguish quick triage, baseline hardening, and deeper forensic follow-up

## KEY TECHNIQUES & TOOLS

### Phase 1: Triage for compromise first

- Start by checking whether the host already shows compromise indicators:

```bash
cat /proc/sys/kernel/tainted
lsmod
cat /proc/modules
sudo rkhunter -c --skip-keypress --report-warnings-only
sudo chkrootkit
```

- Check suspicious processes and open deleted files:

```bash
ps auxww | grep -v "^\\[" | awk '{print $1, $11}'
lsof | grep deleted
ps aux | grep -E '(/tmp|/dev/shm|/var/tmp)'
```

- Review auth activity quickly:

```bash
tail -100 /var/log/auth.log | grep "Accepted\\|Failed"
python3 .agents/scripts/h4cker_auth_logalyzer.py /var/log/auth.log --format text
```

### Phase 2: Inspect kernel and persistence exposure

- Compare module views and look for hidden or tainted modules:

```bash
diff <(lsmod | awk '{print $1}' | sort) <(cat /proc/modules | awk '{print $1}' | sort)
ls /sys/module
cat /sys/module/*/taint 2>/dev/null | head
```

- Review eBPF and system hooks when relevant:

```bash
sudo bpftool prog list
sudo bpftool map list
dmesg | grep -i bpf
```

- Check preload and library hijacking paths:

```bash
cat /etc/ld.so.preload 2>/dev/null
grep -r "LD_PRELOAD" /etc /var /home 2>/dev/null
ls -la /etc/ld.so.conf.d/
```

### Phase 3: Review filesystem integrity

- Look for recent changes in sensitive paths:

```bash
find /bin /sbin /usr/bin /usr/sbin -type f -mtime -1 2>/dev/null
find / -type f -ctime -1 2>/dev/null | head -100
```

- Check immutable or privilege-bearing files:

```bash
lsattr -R /bin /sbin /usr/bin /usr/sbin 2>/dev/null | grep -i immutable
find / -type f -perm /u+s,g+s 2>/dev/null
```

- Verify package integrity where supported:

```bash
sudo debsums -c
sudo rpm -V $(rpm -qa)
```

### Phase 4: Review firewall and network posture

- Inventory listening services and established connections:

```bash
sudo ss -tulnp
sudo lsof -i -P -n | grep LISTEN
ss -tanp | grep ESTABLISHED
```

- Choose firewall tooling deliberately:
  - `nftables` for modern low-level rule management
  - `iptables` for legacy environments
  - `ufw` for simpler Debian or Ubuntu workflows
  - `firewalld` for zone-based dynamic policy on RHEL-family systems

- Validate the active firewall state:

```bash
sudo nft list ruleset
sudo iptables -S
sudo ufw status verbose
sudo firewall-cmd --list-all
```

### Decision rules

- If compromise indicators appear during hardening review, stop expanding baseline advice and move into containment or DFIR flow
- If the host already runs a firewall abstraction such as `ufw` or `firewalld`, do not recommend parallel rule management through another layer
- If recent changes appear under `/bin`, `/sbin`, or preload paths, treat integrity investigation as higher priority than general hardening
- If auth logs show repeated failures followed by success, prioritize account and access review before service tuning
- If package-integrity checks and process review are clean, continue with baseline hardening rather than incident escalation

### Phase 5: Apply baseline hardening controls

- Review SSH exposure and login paths:

```bash
sudo grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|AllowUsers|AllowGroups)" /etc/ssh/sshd_config
sudo sshd -t
```

- Review scheduled tasks and startup persistence:

```bash
systemctl list-unit-files --state=enabled
crontab -l
sudo ls -la /etc/cron.*
```

- Review patching, logs, and service minimization:

```bash
uname -a
systemctl --failed
journalctl -p err -b
```

- Capture a minimal hardening workspace:

```bash
mkdir -p linux-hardening-output
sudo ss -tulnp > linux-hardening-output/listeners.txt
systemctl list-unit-files --state=enabled > linux-hardening-output/enabled-services.txt
journalctl -p err -b > linux-hardening-output/boot-errors.txt
```

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Compromise Checks`
  - `Hardening Findings`
  - `Network and Firewall Posture`
  - `Artifacts`
  - `Recommended Next Actions`

- `Scope` must state:
  - hostname or system role
  - distro family if known
  - whether the task was hardening-only or included compromise triage

- `Compromise Checks` must separate:
  - clean indicators
  - suspicious indicators
  - items requiring deeper DFIR

- `Hardening Findings` should group:
  - SSH and access control
  - persistence and startup
  - filesystem integrity
  - patching and service exposure

- `Network and Firewall Posture` must include:
  - active firewall layer
  - unexpected listeners
  - policy or visibility gaps

- `Artifacts` should list:
  - helper-script output
  - captured command output
  - generated notes or files

- `Recommended Next Actions` must stay defensive:
  - immediate containment
  - baseline hardening tasks
  - log and monitoring improvements
  - deeper incident review if needed

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
Use when you need a stable starting point before deeper linux-hardening review.
```bash
# Create the output directory for this skill
mkdir -p linux-hardening-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > linux-hardening-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > linux-hardening-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 linux-hardening-output/artifact-manifest.txt | xargs -r sha256sum > linux-hardening-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > linux-hardening-output/review-start-utc.txt
date > linux-hardening-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > linux-hardening-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' linux-hardening-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 linux-hardening-output/signal-hits.txt | sort | uniq -c | sort -nr > linux-hardening-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > linux-hardening-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > linux-hardening-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' linux-hardening-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > linux-hardening-output/git-status.txt 2>/dev/null || true
git diff --stat > linux-hardening-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > linux-hardening-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > linux-hardening-output/linux-hardening-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > linux-hardening-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' linux-hardening-output/linux-hardening-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find linux-hardening-output -maxdepth 2 -type f | sort > linux-hardening-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf linux-hardening-output/linux-hardening-bundle.tgz linux-hardening-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf linux-hardening-output/linux-hardening-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 linux-hardening-output/signal-hits.txt | sort | uniq -c | sort -nr > linux-hardening-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' linux-hardening-output/review-queue.txt > linux-hardening-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' linux-hardening-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > linux-hardening-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> linux-hardening-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' linux-hardening-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > linux-hardening-output/linux-hardening-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > linux-hardening-output/linux-hardening-final.md
# Preview the output files for QA
sed -n '1,20p' linux-hardening-output/linux-hardening-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > linux-hardening-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 linux-hardening-output/linux-hardening-bundle.tgz > linux-hardening-output/linux-hardening-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > linux-hardening-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' linux-hardening-output/review-queue.txt > linux-hardening-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > linux-hardening-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find linux-hardening-output -maxdepth 2 -type f | sort > linux-hardening-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > linux-hardening-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' linux-hardening-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > linux-hardening-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > linux-hardening-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > linux-hardening-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > linux-hardening-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > linux-hardening-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `linux-hardening-output/linux-hardening-report.md`
- produce: `linux-hardening-output/output-manifest.txt`
- produce: `linux-hardening-output/linux-hardening-bundle.tgz`
- produce: `linux-hardening-output/linux-hardening-findings.csv`

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

- Confirm `linux-hardening-output` contains the report, manifest, and at least one evidence artifact.
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
