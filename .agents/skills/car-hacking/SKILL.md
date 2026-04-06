---
skill: car-hacking
name: car-hacking
version: 1.0.0
source: h4cker/car-hacking
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Review automotive lab assets, buses, firmware evidence, and safe defensive validation boundaries in owned labs.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Car Hacking

Summary: Review automotive lab assets, buses, firmware evidence, and safe defensive validation boundaries in owned labs.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to car-hacking topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p car-hacking-output
find . -maxdepth 3 -type f | sort | head -100 > car-hacking-output/files.txt
ls -la car-hacking-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > car-hacking-output/signals.txt || true
sed -n '1,40p' car-hacking-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > car-hacking-output/inventory.txt
wc -l car-hacking-output/inventory.txt car-hacking-output/signals.txt 2>/dev/null || true
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
  - `car-hacking-output/files.txt`
  - `car-hacking-output/signals.txt`
  - `car-hacking-output/inventory.txt`

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
            mkdir -p car-hacking-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > car-hacking-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > car-hacking-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 car-hacking-output/artifact-manifest.txt | xargs -r sha256sum > car-hacking-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > car-hacking-output/review-start-utc.txt
date > car-hacking-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > car-hacking-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' car-hacking-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 car-hacking-output/signal-hits.txt | sort | uniq -c | sort -nr > car-hacking-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf car-hacking-output/review-bundle.tgz car-hacking-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum car-hacking-output/review-bundle.tgz > car-hacking-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf car-hacking-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > car-hacking-output/report-starter.md
            # Save a simple output manifest for the generated files
            find car-hacking-output -maxdepth 2 -type f | sort > car-hacking-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' car-hacking-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Artifact inventory
Use when the lab evidence set mixes DBC files, firmware, and CAN captures.
```bash
# Inventory automotive artifacts
find . -maxdepth 6 \( -iname "*.dbc" -o -iname "*.arxml" -o -iname "*.asc" -o -iname "*.blf" -o -iname "*.mf4" -o -iname "*.hex" -o -iname "*.bin" \) | sort > car-hacking-output/automotive-artifacts.txt
# Save file types for the first artifacts
head -30 car-hacking-output/automotive-artifacts.txt | xargs -r file > car-hacking-output/automotive-file-types.txt
# Preview the artifact list
sed -n '1,80p' car-hacking-output/automotive-artifacts.txt
```
- This tells you whether the review is log-based, firmware-based, or both.
- The inventory keeps the work tied to owned lab artifacts only.

### Technique 7: Interface and bus baseline
Use when the host may have SocketCAN, virtual CAN, or other automotive interfaces configured.
```bash
# Save interface details and device names
ip -details link show > car-hacking-output/ip-link-details.txt 2>/dev/null || true
ls /sys/class/net > car-hacking-output/net-devices.txt 2>/dev/null || true
# Search repo notes for CAN, UDS, or gateway references
rg -n "can0|vcan|uds|isotp|j1939|dbc|arxml|gateway" . > car-hacking-output/can-signals.txt 2>/dev/null || true
```
- This separates live-interface review from offline-only review.
- Keep interface state and repo hints together for context.

### Technique 8: Passive bus and capture review
Use when you need observation only and want to avoid transmitting on the bus.
```bash
# Try a short passive capture if candump is available
timeout 10 candump any > car-hacking-output/candump-sample.log 2>/dev/null || true
# Save the head of ASCII capture files
find . -maxdepth 5 -iname "*.asc" | head -5 | xargs -r head -50 > car-hacking-output/asc-head.txt 2>/dev/null || true
# Preview passive sample output
sed -n '1,40p' car-hacking-output/candump-sample.log 2>/dev/null || true
```
- Use passive observation only from this skill.
- If no live interface exists, stay with offline captures.

### Technique 9: Firmware and protocol clue review
Use when strings, DBC notes, or configs may reveal ECU or protocol context.
```bash
# Save firmware strings when a binary exists
strings -a firmware.bin | head -200 > car-hacking-output/firmware-strings.txt 2>/dev/null || true
# Search for protocol and ECU terms
rg -n "CAN|J1939|UDS|ISO-TP|diagnostic|ECU|gateway|VIN" . > car-hacking-output/protocol-keywords.txt 2>/dev/null || true
# Preview protocol hits
sed -n '1,80p' car-hacking-output/protocol-keywords.txt
```
- Strings are clues, not proof of active behavior.
- Keep source files or notes linked to every protocol claim.

### Technique 10: Segmentation and safety boundary review
Use when the key question is how buses or functions are separated in the lab.
```bash
                # Search for segmentation or domain terms
                rg -n "gateway|segmentation|body|powertrain|adas|infotainment|diagnostic" . > car-hacking-output/segmentation-signals.txt 2>/dev/null || true
                # Create a segment map starter
                printf '%s
' 'segment,bus,notes' > car-hacking-output/segment-map.csv
                # Save an output manifest for handoff
                find car-hacking-output -maxdepth 2 -type f | sort > car-hacking-output/output-manifest.txt
```
- This keeps the review focused on evidence and safety boundaries.
- The segment map helps separate safety-critical and convenience domains.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `pen-testing-reports`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `candump` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "*.asc" -o -iname "*.blf" -o -iname "*.mf4" \) | sort > car-hacking-output/offline-captures-fallback.txt
```

### ถ้า live CAN interfaces are unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
ip -details link show > car-hacking-output/ip-link-fallback.txt 2>/dev/null || true
```

### ถ้า firmware filename is unknown:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "*.bin" -o -iname "*.hex" \) | sort > car-hacking-output/firmware-fallback.txt
```

### ถ้า permission is limited to repo files:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 6 -type f -readable | sort > car-hacking-output/readable-files.txt
```

### ถ้า capture formats are mixed:
```bash
# Alternative: preserve evidence with the least risky available path
head -20 car-hacking-output/automotive-artifacts.txt | xargs -r file > car-hacking-output/artifact-types-fallback.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find car-hacking-output -maxdepth 2 -type f | sort > car-hacking-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > car-hacking-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' car-hacking-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Extended CAN IDs
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -o "[0-9A-F]{8}" car-hacking-output/candump-sample.log | sort | uniq -c > car-hacking-output/extended-id-edge.txt 2>/dev/null || true
```

### Edge Case: Multiple buses or gateways
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Document which bus each artifact belongs to before comparing them" > car-hacking-output/multi-bus-edge.txt
```

### Edge Case: Offline-only review
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find . -maxdepth 6 \( -iname "*.dbc" -o -iname "*.asc" -o -iname "*.bin" \) | sort > car-hacking-output/offline-only-edge.txt
```

### Edge Case: Safety-critical and infotainment data mixed
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Separate ADAS, powertrain, body, and infotainment findings in the report" > car-hacking-output/safety-separation-edge.txt
```

### Edge Case: Different bus rates or link types
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Record baud or bus type in every artifact filename or summary row" > car-hacking-output/bus-rate-edge.txt
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| find + file + strings | Good offline triage | No direct live bus view | Firmware and note review |
| ip link + candump | Good passive live view | Needs lab hardware | Passive bus observation |
| rg + CSV outputs | Good report-ready evidence | Needs cleanup on noisy inputs | Protocol notes and segmentation evidence |


## Output Templates

- produce: `car-hacking-output/car-hacking-report.md`
- produce: `car-hacking-output/output-manifest.txt`
- produce: `car-hacking-output/review-bundle.tgz`
- produce: `car-hacking-output/car-hacking-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `pen-testing-reports`
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

- Confirm `car-hacking-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `pen-testing-reports` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `pen-testing-reports`.

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
