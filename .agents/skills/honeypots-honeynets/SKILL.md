---
skill: honeypots-honeynets
name: honeypots-honeynets
version: 1.0.0
source: h4cker/honeypots-honeynets
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Deploy and review deception infrastructure, telemetry quality, and containment boundaries for defensive monitoring.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Honeypots Honeynets

Summary: Deploy and review deception infrastructure, telemetry quality, and containment boundaries for defensive monitoring.
Does NOT cover offensive interaction with third-party infrastructure; stay with owned sensors, captured telemetry, and containment review.

## WHEN TO USE THIS SKILL

- Use when the user wants to validate a honeypot or honeynet deployment in an owned lab or production defense environment
- Use when Codex should confirm isolation, telemetry capture, and alert quality before the deception platform is trusted
- Use when the result should separate confirmed attacker interaction, noisy internet background, and deployment mistakes
- Use when junior responders need a repeatable checklist for reviewing deception infrastructure safely

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory the deception estate

```bash
mkdir -p honeypots-honeynets-output
find . -maxdepth 4 \( -iname "*cowrie*" -o -iname "*dionaea*" -o -iname "*honeypot*" -o -iname "docker-compose*.yml" \) | sort > honeypots-honeynets-output/deception-files.txt
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}' > honeypots-honeynets-output/docker-ps.txt 2>/dev/null || true
ss -tulpen > honeypots-honeynets-output/listeners.txt
```

### Phase 2: Verify containment and routing boundaries

```bash
rg -n "bridge|hostNetwork|network_mode|iptables|publish|expose" . 2>/dev/null > honeypots-honeynets-output/network-config-signals.txt || true
ip route show > honeypots-honeynets-output/routes.txt
grep -E "LISTEN|ESTAB" honeypots-honeynets-output/listeners.txt | head -50
```

### Phase 3: Review captured interaction and alert quality

```bash
find . -maxdepth 5 \( -iname "*.log" -o -iname "*.json" -o -iname "*.pcap" \) | sort > honeypots-honeynets-output/telemetry-files.txt
rg -n "login|download|curl|wget|scanner|shell|malware|payload" . 2>/dev/null | head -200 > honeypots-honeynets-output/interaction-signals.txt || true
wc -l honeypots-honeynets-output/telemetry-files.txt honeypots-honeynets-output/interaction-signals.txt 2>/dev/null || true
```

### Decision rules

- If the honeypot appears reachable from internal production networks without clear isolation, treat that as a primary finding before reviewing alert content
- If the sensor records only generic internet noise and no meaningful protocol detail, classify telemetry quality as weak rather than claiming the deployment is useless
- If logs show real attacker interaction but timestamps, IPs, or artifacts are incomplete, hand off to `dfir` with the preserved telemetry bundle
- If the deployment uses container host networking or privileged mode, flag containment risk before tuning decoy fidelity

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Deception Inventory`
  - `Containment Findings`
  - `Telemetry Findings`
  - `Artifacts`
  - `Recommended Next Actions`

- `Artifacts` should list:
  - `honeypots-honeynets-output/deception-files.txt`
  - `honeypots-honeynets-output/docker-ps.txt`
  - `honeypots-honeynets-output/listeners.txt`
  - `honeypots-honeynets-output/telemetry-files.txt`
  - `honeypots-honeynets-output/interaction-signals.txt`

## Quick Mode (< 5 minutes)

- Confirm which sensor or compose stack is in scope.
- Capture listeners, routes, and one telemetry index file.
- Stop once you can answer whether the decoy is isolated and whether it is logging useful data.


## Troubleshooting / Fallback

- If Docker is unavailable, review compose files, system services, and listening sockets instead of runtime container state.
- If the sensor writes custom JSON or multiline logs, save a small sample and document the parser limitation before classifying the events.
- If the host records only outbound beacon noise from the internet, separate background scanning from meaningful session activity.
- Edge case 1: a reverse proxy terminates traffic before the honeypot; note that source visibility may be incomplete.
- Edge case 2: the honeypot binds to IPv6 only; record the address family so junior analysts do not assume IPv4 reachability.


## Phase Output Map

- Phase 1 output: deception component inventory plus active listeners.
- Phase 2 output: isolation and network-boundary evidence.
- Phase 3 output: telemetry samples and interaction indicators ready for analyst review.


## Done When

- The in-scope honeypot components and listeners are listed.
- Isolation or containment posture is described with evidence.
- Telemetry quality is classified as useful, weak, or inconclusive with saved artifacts.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper work.
```bash
            # Create the output directory if it is not present yet
            mkdir -p honeypots-honeynets-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > honeypots-honeynets-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > honeypots-honeynets-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 honeypots-honeynets-output/artifact-manifest.txt | xargs -r sha256sum > honeypots-honeynets-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > honeypots-honeynets-output/review-start-utc.txt
date > honeypots-honeynets-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > honeypots-honeynets-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' honeypots-honeynets-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 honeypots-honeynets-output/signal-hits.txt | sort | uniq -c | sort -nr > honeypots-honeynets-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf honeypots-honeynets-output/review-bundle.tgz honeypots-honeynets-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum honeypots-honeynets-output/review-bundle.tgz > honeypots-honeynets-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf honeypots-honeynets-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > honeypots-honeynets-output/report-starter.md
            # Save a simple output manifest for the generated files
            find honeypots-honeynets-output -maxdepth 2 -type f | sort > honeypots-honeynets-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' honeypots-honeynets-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Deception config inventory
Use when multiple honeypot technologies or compose files may exist in the same tree.
```bash
# Inventory common deception config files
find . -maxdepth 5 \( -iname "*cowrie*" -o -iname "*dionaea*" -o -iname "*tpot*" -o -iname "docker-compose*.yml" -o -iname "*.service" \) | sort > honeypots-honeynets-output/deception-configs.txt
# Save file types for the first configs
head -30 honeypots-honeynets-output/deception-configs.txt | xargs -r file > honeypots-honeynets-output/deception-config-types.txt
# Preview the inventory
sed -n '1,80p' honeypots-honeynets-output/deception-configs.txt
```
- This distinguishes real sensor config from stale notes or random images.
- The config type list helps route the next review step.

### Technique 7: Runtime state and listeners
Use when you need to know which decoys are active right now.
```bash
# Save docker state if present
docker ps --format '{{.Names}}|{{.Image}}|{{.Ports}}' > honeypots-honeynets-output/docker-ps-deep.txt 2>/dev/null || true
# Save socket state
ss -tulpn > honeypots-honeynets-output/deep-sockets.txt 2>/dev/null || true
# Save deception-related processes
ps aux | grep -E 'cowrie|dionaea|conpot|honey|tpot' | grep -v grep > honeypots-honeynets-output/deception-processes.txt 2>/dev/null || true
```
- Runtime state should be captured before making uptime or exposure claims.
- Sockets alone do not tell you which decoy owns a port.

### Technique 8: Network boundary review
Use when containment matters as much as telemetry quality.
```bash
# Save host addresses and routes
ip addr show > honeypots-honeynets-output/ip-addr.txt 2>/dev/null || true
ip route show > honeypots-honeynets-output/routes-deep.txt 2>/dev/null || true
# Search configs for host networking or published ports
rg -n "publish|expose|hostNetwork|network_mode|bridge|macvlan|ipv6" . > honeypots-honeynets-output/boundary-signals.txt 2>/dev/null || true
```
- Containment findings should always cite both config and runtime evidence.
- This is the first stop if the sensor might be reachable from the wrong network.

### Technique 9: Telemetry and pcap indexing
Use when the core question is whether the decoy is capturing useful signals.
```bash
                # Index logs, JSON events, and packet captures
                find . -maxdepth 6 \( -iname "*.log" -o -iname "*.json" -o -iname "*.pcap" -o -iname "*.pcapng" \) | sort > honeypots-honeynets-output/deep-telemetry-files.txt
                # Count file types
                python3 - <<'PY2'
from pathlib import Path
from collections import Counter
files=Path('honeypots-honeynets-output/deep-telemetry-files.txt').read_text(encoding='utf-8',errors='replace').splitlines()
c=Counter(Path(f).suffix for f in files)
Path('honeypots-honeynets-output/telemetry-extension-counts.txt').write_text('
'.join(f'{k} {v}' for k,v in sorted(c.items())))
PY2
                # Preview the telemetry inventory
                sed -n '1,80p' honeypots-honeynets-output/deep-telemetry-files.txt
```
- Telemetry inventory is often enough to classify a sensor as useful or weak.
- Differentiate logs from packet captures because they support different conclusions.

### Technique 10: Alert forwarding and time sync review
Use when the sensor logs locally but the team expects central visibility and timeline fidelity.
```bash
# Search for forwarding and retention hints
rg -n "syslog|logstash|elastic|loki|splunk|wazuh|fluent|rotate|retention|max_days|max_size" . > honeypots-honeynets-output/forwarding-and-retention.txt 2>/dev/null || true
# Save host time state
date -u > honeypots-honeynets-output/current-utc.txt
timedatectl status > honeypots-honeynets-output/timedatectl.txt 2>/dev/null || true
```
- Poor forwarding or time sync can make otherwise good telemetry useless in investigations.
- Keep storage and time findings separate so the next owner knows what to fix.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `dfir`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `docker` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "docker-compose*.yml" -o -iname "*.service" \) | sort > honeypots-honeynets-output/runtime-fallback-files.txt
```

### ถ้า `tshark` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
tcpdump -nr sample.pcap -c 200 > honeypots-honeynets-output/pcap-fallback.txt 2>/dev/null || true
```

### ถ้า `timedatectl` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
date -u > honeypots-honeynets-output/current-utc-fallback.txt
```

### ถ้า permissions block socket inspection:
```bash
# Alternative: preserve evidence with the least risky available path
find /proc -maxdepth 1 -type d | sort | head -50 > honeypots-honeynets-output/proc-fallback.txt 2>/dev/null || true
```

### ถ้า logs are rotated or compressed:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 6 \( -iname "*.gz" -o -iname "*.old" \) | sort > honeypots-honeynets-output/rotated-telemetry.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find honeypots-honeynets-output -maxdepth 2 -type f | sort > honeypots-honeynets-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > honeypots-honeynets-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' honeypots-honeynets-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: IPv6-only service
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "ipv6|::|listen \[::\]" . > honeypots-honeynets-output/ipv6-edge.txt 2>/dev/null || true
```

### Edge Case: Reverse proxy in front of the sensor
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "nginx|haproxy|traefik|proxy_pass|x-forwarded-for" . > honeypots-honeynets-output/proxy-edge.txt 2>/dev/null || true
```

### Edge Case: Shared host with other workloads
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
ps aux > honeypots-honeynets-output/full-process-list.txt 2>/dev/null || true
```

### Edge Case: Host networking enabled
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "hostNetwork|network_mode: host" . > honeypots-honeynets-output/host-network-edge.txt 2>/dev/null || true
```

### Edge Case: Short retention windows
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "retention|rotate|max_days|max_size" . > honeypots-honeynets-output/retention-edge.txt 2>/dev/null || true
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| docker ps | Strong runtime view | Needs Docker access | Container-backed sensors |
| ss + ip route | Strong boundary evidence | Does not explain app semantics | Containment review |
| tshark/tcpdump -r | Good pcap summary | Needs saved pcaps | Protocol mix triage |


## Output Templates

- produce: `honeypots-honeynets-output/honeypots-honeynets-report.md`
- produce: `honeypots-honeynets-output/output-manifest.txt`
- produce: `honeypots-honeynets-output/review-bundle.tgz`
- produce: `honeypots-honeynets-output/honeypots-honeynets-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `dfir`
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

- Confirm `honeypots-honeynets-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `dfir` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `dfir`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `dfir` skill

- Load `dfir` next if captured deception telemetry needs deeper timeline, IOC, or incident correlation work.
