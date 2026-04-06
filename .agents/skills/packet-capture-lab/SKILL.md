---
skill: packet-capture-lab
name: packet-capture-lab
version: 1.0.0
source: codex/packet-capture-lab
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Use Scapy and PyShark for authorized packet capture, pcap inspection, protocol debugging, and tightly scoped network validation in labs or owned environments.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Packet Capture Lab

Summary: Use Scapy and PyShark for authorized packet capture, pcap inspection, protocol debugging, and tightly scoped network validation in labs or owned environments.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task is to capture, inspect, or replay packets in a lab or owned environment
- Use when you need quick packet-level validation with Scapy or PyShark instead of a full Wireshark workflow
- Use when the source material includes small Python scripts for sniffing, pcap handling, or controlled service validation
- Use when Codex should explain packet observations, saved artifacts, and next validation steps clearly
- Use when the work must stay tightly scoped, authorized, and low-noise

## KEY TECHNIQUES & TOOLS

### Phase 1: Set up the capture path

- Treat `pyshark` as a wrapper around `tshark` and `scapy` as the packet crafting and sniffing workhorse
- Install only what the task needs:

```bash
python3 -m pip install pyshark scapy prettytable
python3 -c "import pyshark, scapy"
```

- Confirm the interface and permissions before capture:

```bash
# WARNING: live capture must be limited to owned or explicitly authorized interfaces and filters
ip addr
sudo python3 .agents/scripts/packet_capture_lab.py --iface eth0 --count 5 --bpf "tcp"
```

- Use explicit scope for:
  - interface
  - host filter
  - port filter
  - packet count
  - output pcap path

### Decision rules

- If live capture would gather unrelated traffic, narrow the BPF filter before collecting even a single packet
- If root access is unavailable, prefer offline pcap review instead of attempting partial live capture
- If the goal is protocol debugging rather than service validation, save a pcap first so the review is repeatable
- If the target behavior is noisy or intermittent, increase packet count gradually instead of removing the filter entirely

### Phase 2: Capture packets live

- Use the PyShark pattern from the source for quick live inspection:

```python
import pyshark
capture = pyshark.LiveCapture(interface='eth0')
for packet in capture.sniff_continuously(packet_count=5):
    print(packet)
```

- Use Scapy when you need callback-driven packet inspection:

```python
from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())

sniff(prn=packet_callback, filter="tcp", count=1)
```

- Narrow the filter aggressively:

```python
sniff(prn=packet_callback, filter="tcp and host 10.1.1.2 and port 80", count=10)
```

- Record:
  - interface
  - BPF filter
  - count limit
  - whether root privileges were required

### Phase 3: Save and inspect pcaps

- Save captured packets during the callback:

```python
from scapy.all import wrpcap
wrpcap("captured_packets.pcap", packet, append=True)
```

- Re-open the pcap for offline review:

```python
from scapy.all import rdpcap
packets = rdpcap("captured_packets.pcap")
for packet in packets:
    print(packet.show())
```

- Inspect protocol layers and filter in Python:

```python
for packet in packets:
    print(packet.ls())

filtered_packets = [p for p in packets if p.haslayer(IP) and p[IP].dst == "10.1.1.2"]
```

- Use offline inspection when you want repeatable analysis without touching the network again

### Phase 4: Craft packets for protocol validation

- The source includes simple Scapy crafting patterns such as:

```python
from scapy.all import IP, TCP, send
packet = IP(src="10.1.1.2", dst="10.3.2.88")/TCP(dport=445)
send(packet)
```

- Use packet crafting only for:
  - owned hosts
  - lab ranges
  - protocol testing
  - debugging firewall or service behavior

- When validating a TCP service, interpret SYN or SYN/ACK behavior carefully instead of assuming a missing reply proves the port is closed

### Phase 5: Run tightly scoped Scapy validation

- The source includes a larger `scapscan.py` script that supports:
  - TCP connect checks
  - SYN-style validation
  - ACK/window checks
  - UDP response checks
  - single ports, lists, and ranges

- Keep usage narrow and explicit:

```bash
# WARNING: use only against owned or explicitly authorized lab hosts
python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --ports 443 --timeout 2
python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --ports 22,80,443 --timeout 2
python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --port-range 20-25 --timeout 2
```

- Use this style of script to compare response classes such as:
  - open
  - closed
  - filtered
  - open or filtered
  - unfiltered

- Prefer:
  - a small port set
  - short timeouts
  - one host at a time
  - explicit justification for any UDP probing

- Do not turn packet-crafting examples into broad scanning or stealth playbooks

### Phase 6: Preserve evidence and conclusions

- Build an artifact directory as you capture:

```bash
mkdir -p packet-lab
sudo python3 .agents/scripts/packet_capture_lab.py --iface eth0 --count 5 --bpf "tcp" > packet-lab/live-capture.txt
cp captured_packets.pcap packet-lab/
python3 .agents/scripts/scapy_port_probe.py 10.0.0.5 --ports 22,80,443 --timeout 2 > packet-lab/packet-capture-lab-scan-results.txt
```

```bash
# WARNING: inspect only owned or explicitly authorized packet captures
tcpdump -nn -r captured_packets.pcap | head
```

- Keep:
  - the capture script or command
  - the filter used
  - the pcap file path
  - a short summary of packet or port observations

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Capture Setup`
  - `Observations`
  - `Artifacts`
  - `Evidence`
  - `Recommended Next Steps`

- `Scope` must state:
  - target or lab range
  - interface
  - whether the work was passive capture, packet crafting, or limited validation

- `Capture Setup` should include:
  - tools used
  - filters
  - packet count
  - timeout values

- `Observations` must separate:
  - packet-level findings
  - service-response findings
  - anything inferred but not directly confirmed

- `Artifacts` should list:
  - generated pcaps
  - saved output files
  - scripts or commands used to produce them

- `Evidence` must include the most important commands and the key packet or response details they produced

- `Recommended Next Steps` should stay safe and scoped:
  - deeper offline pcap inspection
  - narrower protocol tests
  - service-owner validation
  - firewall or application review

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
Use when you need a stable starting point before deeper packet-capture-lab review.
```bash
# Create the output directory for this skill
mkdir -p packet-capture-lab-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > packet-capture-lab-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > packet-capture-lab-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 packet-capture-lab-output/artifact-manifest.txt | xargs -r sha256sum > packet-capture-lab-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > packet-capture-lab-output/review-start-utc.txt
date > packet-capture-lab-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > packet-capture-lab-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' packet-capture-lab-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 packet-capture-lab-output/signal-hits.txt | sort | uniq -c | sort -nr > packet-capture-lab-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > packet-capture-lab-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > packet-capture-lab-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' packet-capture-lab-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > packet-capture-lab-output/git-status.txt 2>/dev/null || true
git diff --stat > packet-capture-lab-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > packet-capture-lab-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > packet-capture-lab-output/packet-capture-lab-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > packet-capture-lab-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' packet-capture-lab-output/packet-capture-lab-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find packet-capture-lab-output -maxdepth 2 -type f | sort > packet-capture-lab-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf packet-capture-lab-output/packet-capture-lab-bundle.tgz packet-capture-lab-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf packet-capture-lab-output/packet-capture-lab-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 packet-capture-lab-output/signal-hits.txt | sort | uniq -c | sort -nr > packet-capture-lab-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' packet-capture-lab-output/review-queue.txt > packet-capture-lab-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' packet-capture-lab-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > packet-capture-lab-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> packet-capture-lab-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' packet-capture-lab-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > packet-capture-lab-output/packet-capture-lab-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > packet-capture-lab-output/packet-capture-lab-final.md
# Preview the output files for QA
sed -n '1,20p' packet-capture-lab-output/packet-capture-lab-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > packet-capture-lab-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 packet-capture-lab-output/packet-capture-lab-bundle.tgz > packet-capture-lab-output/packet-capture-lab-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > packet-capture-lab-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' packet-capture-lab-output/review-queue.txt > packet-capture-lab-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > packet-capture-lab-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find packet-capture-lab-output -maxdepth 2 -type f | sort > packet-capture-lab-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > packet-capture-lab-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' packet-capture-lab-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > packet-capture-lab-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > packet-capture-lab-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > packet-capture-lab-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > packet-capture-lab-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > packet-capture-lab-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `packet-capture-lab-output/packet-capture-lab-report.md`
- produce: `packet-capture-lab-output/output-manifest.txt`
- produce: `packet-capture-lab-output/packet-capture-lab-bundle.tgz`
- produce: `packet-capture-lab-output/packet-capture-lab-findings.csv`

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

- Confirm `packet-capture-lab-output` contains the report, manifest, and at least one evidence artifact.
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
