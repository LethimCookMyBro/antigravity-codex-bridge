---
skill: wireless-resources
name: wireless-resources
version: 1.0.0
source: h4cker/wireless-resources
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Document authorized wireless inventory, signal baseline, and defensive monitoring steps in owned environments.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Wireless Resources

Summary: Document authorized wireless inventory, signal baseline, and defensive monitoring steps in owned environments.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to wireless-resources topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p wireless-resources-output
find . -maxdepth 3 -type f | sort | head -100 > wireless-resources-output/files.txt
ls -la wireless-resources-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > wireless-resources-output/signals.txt || true
sed -n '1,40p' wireless-resources-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > wireless-resources-output/inventory.txt
wc -l wireless-resources-output/inventory.txt wireless-resources-output/signals.txt 2>/dev/null || true
```

### Decision rules

- If the scope is unclear, stop and ask for the owned asset, repository, or lab boundary
- If evidence is weak or partial, label it as inconclusive instead of escalating the claim
- If another specialized skill fits better, hand off with the captured inventory and signals
- If the task would require unsafe or unapproved actions, stop at defensive analysis only

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Evidence Collected`
  - `Findings`
  - `Artifacts`
  - `Recommended Next Actions`

- `Artifacts` should list:
  - `wireless-resources-output/files.txt`
  - `wireless-resources-output/signals.txt`
  - `wireless-resources-output/inventory.txt`

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
Use when you need a stable starting point before deeper work.
```bash
            # Create the output directory if it is not present yet
            mkdir -p wireless-resources-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > wireless-resources-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > wireless-resources-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 wireless-resources-output/artifact-manifest.txt | xargs -r sha256sum > wireless-resources-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > wireless-resources-output/review-start-utc.txt
date > wireless-resources-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > wireless-resources-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' wireless-resources-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 wireless-resources-output/signal-hits.txt | sort | uniq -c | sort -nr > wireless-resources-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf wireless-resources-output/review-bundle.tgz wireless-resources-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum wireless-resources-output/review-bundle.tgz > wireless-resources-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf wireless-resources-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > wireless-resources-output/report-starter.md
            # Save a simple output manifest for the generated files
            find wireless-resources-output -maxdepth 2 -type f | sort > wireless-resources-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' wireless-resources-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Interface and adapter inventory
Use when the first question is which wireless radios or adapters actually exist.
```bash
# Save wireless interface and device state
iw dev > wireless-resources-output/iw-dev.txt 2>/dev/null || true
nmcli device status > wireless-resources-output/nmcli-device-status.txt 2>/dev/null || true
ip link show > wireless-resources-output/ip-link.txt 2>/dev/null || true
```
- This tells you whether the review is live-radio, config-only, or offline-only.
- Keep iw and nmcli outputs together because they answer different questions.

### Technique 7: Regulatory and channel baseline
Use when channel plans or country settings may explain visibility or reachability issues.
```bash
# Save regulatory domain and channel information
iw reg get > wireless-resources-output/iw-reg.txt 2>/dev/null || true
iwlist chan > wireless-resources-output/iwlist-channels.txt 2>/dev/null || true
# Preview the first channel lines
sed -n '1,80p' wireless-resources-output/iwlist-channels.txt 2>/dev/null || true
```
- Regulatory context often explains why a network is not visible on a given adapter.
- Record this early when comparing multiple sites or devices.

### Technique 8: Associated link health
Use when an owned device is already connected and you need signal and addressing context.
```bash
# Save current link state and device details
iw dev wlan0 link > wireless-resources-output/iw-link.txt 2>/dev/null || true
nmcli -f GENERAL,IP4,IP6 device show wlan0 > wireless-resources-output/nmcli-device-show.txt 2>/dev/null || true
# Preview the current link state
sed -n '1,80p' wireless-resources-output/iw-link.txt 2>/dev/null || true
```
- This is safer than broad discovery when a device is already associated.
- Signal strength and IP data together make a better baseline.

### Technique 9: Authorized SSID and BSSID survey
Use when you need a quick wireless inventory in owned or allowed airspace.
```bash
# Save a scan list from NetworkManager
nmcli dev wifi list > wireless-resources-output/nmcli-wifi-list.txt 2>/dev/null || true
# Save a raw scan when iw supports it
iw dev wlan0 scan > wireless-resources-output/iw-scan.txt 2>/dev/null || true
# Preview the scan list
sed -n '1,80p' wireless-resources-output/nmcli-wifi-list.txt 2>/dev/null || true
```
- Use this only in authorized spaces.
- Keep the scan artifact because channel and BSSID details matter later.

### Technique 10: Config and log review for auth issues
Use when connection problems need configuration and log evidence rather than deeper radio work.
```bash
# Search wifi config files for auth and network settings
grep -RIn "ssid=\|psk=\|eap=\|identity=\|priority=\|proto=" /etc/NetworkManager /etc/wpa_supplicant 2>/dev/null > wireless-resources-output/wifi-config-signals.txt || true
# Search logs for wlan, dhcp, dns, roam, and 802.1X terms
journalctl -n 300 | grep -Ei "wlan|wpa|dhcp|dns|roam|802.1x|eap" > wireless-resources-output/wifi-journal-sample.txt 2>/dev/null || true
# Save a manifest for handoff
find wireless-resources-output -maxdepth 2 -type f | sort > wireless-resources-output/output-manifest.txt
```
- This is often enough to explain why a client fails even when scans look fine.
- Separate PSK and enterprise auth findings in the report.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `networking`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `iw` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
nmcli device status > wireless-resources-output/nmcli-fallback-status.txt 2>/dev/null || true
```

### ถ้า `nmcli` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
iwlist scan > wireless-resources-output/iwlist-scan-fallback.txt 2>/dev/null || true
```

### ถ้า packet capture tools are unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
journalctl -n 300 | grep -Ei "wlan|wpa|dhcp|dns" > wireless-resources-output/log-only-fallback.txt 2>/dev/null || true
```

### ถ้า permissions block live interface access:
```bash
# Alternative: preserve evidence with the least risky available path
find /etc -maxdepth 3 \( -iname "*NetworkManager*" -o -iname "*wpa*" \) | sort > wireless-resources-output/config-only-fallback.txt 2>/dev/null || true
```

### ถ้า no wireless adapter is present:
```bash
# Alternative: preserve evidence with the least risky available path
ls /sys/class/net > wireless-resources-output/no-radio-fallback.txt 2>/dev/null || true
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find wireless-resources-output -maxdepth 2 -type f | sort > wireless-resources-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > wireless-resources-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' wireless-resources-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Hidden SSID environment
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Use BSSID, channel, and auth hints from authorized logs or configs when SSID broadcast is absent" > wireless-resources-output/hidden-ssid-edge.txt
```

### Edge Case: MAC filtering
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Record the approved MAC list source before judging connectivity issues" > wireless-resources-output/mac-filter-edge.txt
```

### Edge Case: Enterprise 802.1X auth
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Separate EAP, identity, CA, and RADIUS findings from PSK findings" > wireless-resources-output/eap-edge.txt
```

### Edge Case: Multi-AP or roaming environment
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Track BSSID and channel per observation so roaming is not mistaken for instability" > wireless-resources-output/multi-ap-edge.txt
```

### Edge Case: IPv6-heavy segment
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Record IPv6 DNS, RA, and address evidence alongside IPv4 data" > wireless-resources-output/ipv6-edge.txt
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| iw/iwlist | Strong radio and channel detail | Verbose and driver-dependent | Low-level survey detail |
| nmcli | Friendly client-state view | Less protocol detail | Fast site survey |
| journalctl/grep | Strong client log context | Needs local log access | Join and auth troubleshooting |


## Output Templates

- produce: `wireless-resources-output/wireless-resources-report.md`
- produce: `wireless-resources-output/output-manifest.txt`
- produce: `wireless-resources-output/review-bundle.tgz`
- produce: `wireless-resources-output/wireless-resources-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `networking`
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

- Confirm `wireless-resources-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `networking` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `networking`.

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
