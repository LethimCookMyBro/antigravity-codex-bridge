---
skill: adversarial-emulation
name: adversarial-emulation
version: 1.0.0
source: h4cker/adversarial-emulation
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Translate defensive findings into ATT&CK-aligned detection validation and purple-team planning without operational payload guidance.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Adversarial Emulation

Summary: Translate defensive findings into ATT&CK-aligned detection validation and purple-team planning without operational payload guidance.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to adversarial-emulation topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Define the emulation scope, ATT&CK goal, and telemetry sources

```bash
mkdir -p adversarial-emulation-output
printf '%s\n' "goal=Tactic or detection objective" "scope=owned lab, purple-team range, or replay dataset" "telemetry=EDR, auth, proxy, DNS, cloud" > adversarial-emulation-output/scope.txt
find . -maxdepth 4 \( -iname "*.yml" -o -iname "*.yaml" -o -iname "*.json" -o -iname "*.md" -o -iname "*.sigma" \) | sort > adversarial-emulation-output/detection-content.txt
sed -n '1,40p' adversarial-emulation-output/detection-content.txt
```

### Phase 2: Map defensive evidence to ATT&CK-style validation targets

```bash
rg -n "sigma|analytic|alert|detection|ATT&CK|tactic|technique|coverage|telemetry" . 2>/dev/null > adversarial-emulation-output/coverage-signals.txt || true
printf '%s\n' "Initial Access" "Execution" "Persistence" "Privilege Escalation" "Defense Evasion" "Credential Access" "Discovery" "Lateral Movement" "Collection" "Exfiltration" > adversarial-emulation-output/attack-phases.txt
sed -n '1,60p' adversarial-emulation-output/coverage-signals.txt
```

### Phase 3: Produce a replay-ready validation plan without operational payloads

```bash
printf "phase\tdetection\ttelemetry\tgap\tnext_action\n" > adversarial-emulation-output/validation-plan.tsv
wc -l adversarial-emulation-output/detection-content.txt adversarial-emulation-output/coverage-signals.txt adversarial-emulation-output/attack-phases.txt 2>/dev/null || true
```

### Decision rules

- If the scope is unclear, stop and ask for the owned asset, repository, or lab boundary
- If no detection content exists, return a coverage-gap assessment instead of pretending emulation is ready
- If the user asks for payloads or operator tradecraft, redirect to detection validation, replay datasets, or atomic-style test planning only
- If telemetry exists but is not normalized, list the missing fields that block correlation before suggesting emulation scope
- If another specialized skill fits better, hand off with the saved ATT&CK goal and evidence map

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Telemetry Sources`
  - `Coverage Findings`
  - `Validation Plan`
  - `Artifacts`
  - `Recommended Next Actions`

- `Artifacts` should list:
  - `adversarial-emulation-output/scope.txt`
  - `adversarial-emulation-output/detection-content.txt`
  - `adversarial-emulation-output/coverage-signals.txt`
  - `adversarial-emulation-output/attack-phases.txt`
  - `adversarial-emulation-output/validation-plan.tsv`

## Quick Mode (< 5 minutes)

- Start with the first scope or inventory command, not the whole workflow.
- Limit the first pass to one ATT&CK goal and one telemetry source.
- Stop once you know whether the environment is ready for safe replay-based validation.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the coverage docs are scattered across many folders, start with the analytics or Sigma rules before reading runbooks.
- If ATT&CK language is absent, map findings to plain-language phases such as execution, credential access, or lateral movement.
- Edge case 1: the range is cloud-only; capture control-plane logs separately from host telemetry.
- Edge case 2: purple-team replay uses historical logs only; document that the result validates detections, not prevention.


## Phase Output Map

- Phase 1 output: scope sheet plus detection-content inventory.
- Phase 2 output: ATT&CK-style coverage evidence tied to real telemetry.
- Phase 3 output: a replay-ready validation plan with explicit gaps.


## Done When

- Scope is fixed to one owned lab, replay dataset, or purple-team range.
- The target ATT&CK goal is mapped to at least one telemetry source.
- The next reviewer can tell whether to validate detections, improve logging, or refine hypotheses.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper work.
```bash
            # Create the output directory if it is not present yet
            mkdir -p adversarial-emulation-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > adversarial-emulation-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > adversarial-emulation-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 adversarial-emulation-output/artifact-manifest.txt | xargs -r sha256sum > adversarial-emulation-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > adversarial-emulation-output/review-start-utc.txt
date > adversarial-emulation-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > adversarial-emulation-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' adversarial-emulation-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 adversarial-emulation-output/signal-hits.txt | sort | uniq -c | sort -nr > adversarial-emulation-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf adversarial-emulation-output/review-bundle.tgz adversarial-emulation-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum adversarial-emulation-output/review-bundle.tgz > adversarial-emulation-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf adversarial-emulation-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > adversarial-emulation-output/report-starter.md
            # Save a simple output manifest for the generated files
            find adversarial-emulation-output -maxdepth 2 -type f | sort > adversarial-emulation-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' adversarial-emulation-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: ATT&CK goal and scope sheet
Use when the team wants validation but has not fixed the tactic, platform, or telemetry source yet.
```bash
                # Record the ATT&CK goal, scope, and telemetry sources
                printf '%s
' 'goal=credential access' 'scope=owned purple-team range' 'telemetry=edr,dns,proxy' > adversarial-emulation-output/deep-scope.txt
                # Save current host and time context
                hostname > adversarial-emulation-output/hostname.txt 2>/dev/null || true
                date -u > adversarial-emulation-output/current-utc.txt
```
- Do this before reading detection content so the review has a fixed purpose.
- A clear goal prevents drift into generic purple-team advice.

### Technique 7: Detection content inventory
Use when you need to know whether any Sigma, rule, or analytic content exists at all.
```bash
# Inventory likely detection content
find . -maxdepth 6 \( -iname "*.sigma" -o -iname "*.yml" -o -iname "*.yaml" -o -iname "*.json" -o -iname "*.ndjson" \) | sort > adversarial-emulation-output/detection-files.txt
# Grep for ATT&CK or detection-language hints
rg -n "ATT&CK|sigma|analytic|rule|coverage|telemetry" . > adversarial-emulation-output/detection-grep.txt 2>/dev/null || true
# Preview the inventory
sed -n '1,80p' adversarial-emulation-output/detection-files.txt
```
- This tells you whether the environment has anything concrete to validate.
- Keep raw grep hits because rule names alone are often too vague.

### Technique 8: Telemetry schema sampling
Use when field names and event shape determine whether replay validation is possible.
```bash
                # Sample likely JSON keys from telemetry files
                python3 - <<'PY2'
from pathlib import Path
import json
rows=[]
for p in Path('.').rglob('*.json'):
    try:
        data=json.loads(p.read_text(encoding='utf-8', errors='replace'))
    except Exception:
        continue
    if isinstance(data, dict):
        rows.append(f'{p}: ' + ','.join(sorted(data.keys())[:20]))
    if len(rows) >= 20:
        break
Path('adversarial-emulation-output/json-key-samples.txt').write_text('
'.join(rows), encoding='utf-8')
PY2
                # Grep for common telemetry fields
                rg -n "event_id|timestamp|host|user|process|dns|url|src_ip|dst_ip" . > adversarial-emulation-output/telemetry-field-signals.txt 2>/dev/null || true
```
- Field coverage matters more than rule count when deciding if emulation is practical.
- Do not promise replay if the essential fields are absent.

### Technique 9: Gap matrix and hunt handoff
Use when the next reviewer needs a concrete validation matrix and analyst pivot questions.
```bash
                # Create a gap matrix starter
                printf '%s
' 'phase,detection_present,telemetry_ready,gap,next_step' > adversarial-emulation-output/gap-matrix.csv
                # Create a hunt handoff starter
                printf '%s
' 'goal,indicator,source,pivot_question' > adversarial-emulation-output/hunt-handoff.csv
                # Preview the starters
                cat adversarial-emulation-output/gap-matrix.csv
                cat adversarial-emulation-output/hunt-handoff.csv
```
- A matrix prevents the review from ending as vague prose.
- Questions are more useful to a hunt team than unlabeled indicators.

### Technique 10: Replay-prerequisite review
Use when the team wants safe validation from historical logs or artifacts, not live operator tradecraft.
```bash
                # Inventory candidate replay artifacts
                find . -maxdepth 6 \( -iname "*.json" -o -iname "*.csv" -o -iname "*.evtx" -o -iname "*.log" -o -iname "*.pcap" \) | sort > adversarial-emulation-output/replay-candidates.txt
                # Create a replay prerequisite sheet
                printf '%s
' 'artifact,timestamped,host_bound,fields_ready,notes' > adversarial-emulation-output/replay-prereqs.csv
                # Preview candidate artifacts
                sed -n '1,80p' adversarial-emulation-output/replay-candidates.txt
```
- This keeps the workflow on evidence replay and validation rather than payloads.
- If no candidates exist, that is a real gap and should be reported.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `threat-hunting`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า ATT&CK IDs are missing:
```bash
# Alternative: preserve evidence with the least risky available path
rg -n "initial access|execution|credential|lateral movement|collection|exfiltration" . > adversarial-emulation-output/plain-language-phases.txt 2>/dev/null || true
```

### ถ้า JSON telemetry is malformed:
```bash
# Alternative: preserve evidence with the least risky available path
python3 -m json.tool sample.json > adversarial-emulation-output/json-tool-fallback.txt 2>/dev/null || true
```

### ถ้า no rule files are present:
```bash
# Alternative: preserve evidence with the least risky available path
printf "%s
" "No local detection content found" > adversarial-emulation-output/no-detections.txt
```

### ถ้า permissions block host-log review:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 6 -type f -readable | sort > adversarial-emulation-output/readable-files.txt
```

### ถ้า only historical incident data exists:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 6 \( -iname "*.zip" -o -iname "*.tar" -o -iname "*.tgz" \) | sort > adversarial-emulation-output/archive-candidates.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find adversarial-emulation-output -maxdepth 2 -type f | sort > adversarial-emulation-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > adversarial-emulation-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' adversarial-emulation-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Cloud-only telemetry
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "cloudtrail|azure monitor|workspace audit|okta|idp" . > adversarial-emulation-output/cloud-only-edge.txt 2>/dev/null || true
```

### Edge Case: Historical replay only
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find . -maxdepth 6 \( -iname "*.evtx" -o -iname "*.log" -o -iname "*.pcap" \) | sort > adversarial-emulation-output/historical-only-edge.txt
```

### Edge Case: Multiple schemas
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "schema|mapping|parser|normalization" . > adversarial-emulation-output/schema-drift-edge.txt 2>/dev/null || true
```

### Edge Case: SaaS-only application
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "audit log|admin log|activity feed|event export" . > adversarial-emulation-output/saas-edge.txt 2>/dev/null || true
```

### Edge Case: Missing timestamps
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "timestamp|time|eventTime" . > adversarial-emulation-output/timestamp-edge.txt 2>/dev/null || true
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg + inventory | Fast local discovery | No semantic rule validation | First-pass content inventory |
| python3 + json.tool | Flexible schema sampling | Needs sample data | Telemetry field readiness |
| CSV matrices | Easy to review and diff | Less expressive than narrative | Gap tracking |


## Output Templates

- produce: `adversarial-emulation-output/adversarial-emulation-report.md`
- produce: `adversarial-emulation-output/output-manifest.txt`
- produce: `adversarial-emulation-output/review-bundle.tgz`
- produce: `adversarial-emulation-output/adversarial-emulation-findings.csv`

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

- Confirm `adversarial-emulation-output` contains the report, manifest, and at least one evidence artifact.
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

- Load `threat-hunting` next if the emulation plan needs analyst pivots and evidence-correlation logic.
