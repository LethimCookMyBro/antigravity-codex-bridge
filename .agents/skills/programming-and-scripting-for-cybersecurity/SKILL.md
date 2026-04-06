---
skill: programming-and-scripting-for-cybersecurity
name: programming-and-scripting-for-cybersecurity
version: 1.0.0
source: h4cker/programming-and-scripting-for-cybersecurity
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Implement small defensive helper scripts and parsing patterns after a primary security skill has already defined the target, scope, and evidence goal.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Programming and Scripting for Cybersecurity

Summary: Use small scripts and parsing patterns to automate defensive evidence collection and validation tasks.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to programming-and-scripting-for-cybersecurity topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p programming-and-scripting-for-cybersecurity-output
find . -maxdepth 3 -type f | sort | head -100 > programming-and-scripting-for-cybersecurity-output/files.txt
ls -la programming-and-scripting-for-cybersecurity-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > programming-and-scripting-for-cybersecurity-output/signals.txt || true
sed -n '1,40p' programming-and-scripting-for-cybersecurity-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > programming-and-scripting-for-cybersecurity-output/inventory.txt
wc -l programming-and-scripting-for-cybersecurity-output/inventory.txt programming-and-scripting-for-cybersecurity-output/signals.txt 2>/dev/null || true
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
  - `programming-and-scripting-for-cybersecurity-output/files.txt`
  - `programming-and-scripting-for-cybersecurity-output/signals.txt`
  - `programming-and-scripting-for-cybersecurity-output/inventory.txt`

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
            mkdir -p programming-and-scripting-for-cybersecurity-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > programming-and-scripting-for-cybersecurity-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > programming-and-scripting-for-cybersecurity-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 programming-and-scripting-for-cybersecurity-output/artifact-manifest.txt | xargs -r sha256sum > programming-and-scripting-for-cybersecurity-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > programming-and-scripting-for-cybersecurity-output/review-start-utc.txt
date > programming-and-scripting-for-cybersecurity-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > programming-and-scripting-for-cybersecurity-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' programming-and-scripting-for-cybersecurity-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 programming-and-scripting-for-cybersecurity-output/signal-hits.txt | sort | uniq -c | sort -nr > programming-and-scripting-for-cybersecurity-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf programming-and-scripting-for-cybersecurity-output/review-bundle.tgz programming-and-scripting-for-cybersecurity-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum programming-and-scripting-for-cybersecurity-output/review-bundle.tgz > programming-and-scripting-for-cybersecurity-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf programming-and-scripting-for-cybersecurity-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > programming-and-scripting-for-cybersecurity-output/report-starter.md
            # Save a simple output manifest for the generated files
            find programming-and-scripting-for-cybersecurity-output -maxdepth 2 -type f | sort > programming-and-scripting-for-cybersecurity-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' programming-and-scripting-for-cybersecurity-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Script and data inventory
Use when you need to know whether Bash, Python, JSON, CSV, or logs dominate the working set.
```bash
                # Inventory likely script and data files
                find . -maxdepth 5 \( -iname "*.py" -o -iname "*.sh" -o -iname "*.js" -o -iname "*.json" -o -iname "*.csv" -o -iname "*.log" \) | sort > programming-and-scripting-for-cybersecurity-output/script-inventory.txt
                # Group by extension for planning
                python3 - <<'PY2'
from pathlib import Path
from collections import Counter
c=Counter(Path(p).suffix for p in Path('.').rglob('*') if p.is_file())
Path('programming-and-scripting-for-cybersecurity-output/extension-counts.txt').write_text('
'.join(f'{k} {v}' for k,v in sorted(c.items())))
PY2
                # Preview the inventory
                sed -n '1,80p' programming-and-scripting-for-cybersecurity-output/script-inventory.txt
```
- Use the extension mix to choose the right parser tool first.
- This inventory helps you avoid building the wrong helper script.

### Technique 7: Text-log parsing with awk and sort
Use when the input is line-oriented and you need quick counts or field extraction.
```bash
# Count common first fields in a sample log
awk '{print $1}' sample.log | sort | uniq -c | sort -nr > programming-and-scripting-for-cybersecurity-output/field1-counts.txt 2>/dev/null || true
# Extract likely timestamp and status columns
awk '{print $1, $2, $3}' sample.log > programming-and-scripting-for-cybersecurity-output/first-three-fields.txt 2>/dev/null || true
# Preview the counts
sed -n '1,40p' programming-and-scripting-for-cybersecurity-output/field1-counts.txt
```
- Use awk for stable column text, not for nested or quoted formats.
- Always save the slice to a new file instead of editing the original log.

### Technique 8: JSON normalization with jq and python3
Use when APIs or logs emit JSON and you need flat, reviewable fields.
```bash
# Pretty-print a sample JSON file
jq . sample.json > programming-and-scripting-for-cybersecurity-output/sample-pretty.json 2>/dev/null || true
# Extract selected fields when the file is a list of records
jq -r '.[] | [.timestamp, .user, .action] | @tsv' sample.json > programming-and-scripting-for-cybersecurity-output/sample-fields.tsv 2>/dev/null || true
# Fall back to python json.tool when needed
python3 -m json.tool sample.json > programming-and-scripting-for-cybersecurity-output/sample-json-tool.txt 2>/dev/null || true
```
- Use jq when the shape is stable and python when the shape is messy.
- TSV is easier to diff and summarize than nested JSON.

### Technique 9: Reusable parser skeleton
Use when a one-off command should become a repeatable helper for another reviewer.
```bash
                # Create a tiny argparse skeleton as a reusable starting point
                printf '%s
' '#!/usr/bin/env python3' 'import argparse' 'from pathlib import Path' 'p=argparse.ArgumentParser()' "p.add_argument('input_path')" "p.add_argument('--output', default='parser-output.txt')" 'args=p.parse_args()' "Path(args.output).write_text(Path(args.input_path).read_text(encoding='utf-8', errors='replace'))" > programming-and-scripting-for-cybersecurity-output/parser_skeleton.py
                # Check the generated help output
                python3 programming-and-scripting-for-cybersecurity-output/parser_skeleton.py --help > programming-and-scripting-for-cybersecurity-output/parser-help.txt 2>/dev/null || true
                # Preview the help text
                sed -n '1,40p' programming-and-scripting-for-cybersecurity-output/parser-help.txt
```
- This is useful when another analyst needs to rerun the same logic.
- Keep input and output paths explicit so the parser is easy to review.

### Technique 10: Packaging parsed outputs for reporting
Use when normalized outputs must feed a report or handoff instead of staying raw.
```bash
                # Create a report skeleton for parsed outputs
                printf '%s
' '## Summary' '## Evidence' '## Parsed Outputs' '## Next Steps' > programming-and-scripting-for-cybersecurity-output/report-skeleton.md
                # Build an output manifest
                find programming-and-scripting-for-cybersecurity-output -maxdepth 2 -type f | sort > programming-and-scripting-for-cybersecurity-output/output-manifest.txt
                # Bundle the outputs for peer review
                tar -czf programming-and-scripting-for-cybersecurity-output/script-review.tgz programming-and-scripting-for-cybersecurity-output 2>/dev/null || true
```
- Use this when parsed outputs will be referenced in a formal finding.
- The manifest is the fastest starting point for a peer reviewer.


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

### ถ้า `jq` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
python3 -m json.tool sample.json > programming-and-scripting-for-cybersecurity-output/sample-json-tool-fallback.txt 2>/dev/null || true
```

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|secret\|token" . > programming-and-scripting-for-cybersecurity-output/grep-fallback.txt 2>/dev/null || true
```

### ถ้า encoding is inconsistent:
```bash
# Alternative: preserve evidence with the least risky available path
iconv -f utf-8 -t utf-8 -c sample.csv > programming-and-scripting-for-cybersecurity-output/sample-utf8-clean.csv 2>/dev/null || true
```

### ถ้า permissions are limited:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 -type f -readable | sort > programming-and-scripting-for-cybersecurity-output/readable-files.txt
```

### ถ้า input is too large:
```bash
# Alternative: preserve evidence with the least risky available path
split -l 50000 sample.log programming-and-scripting-for-cybersecurity-output/log-split- 2>/dev/null || true
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find programming-and-scripting-for-cybersecurity-output -maxdepth 2 -type f | sort > programming-and-scripting-for-cybersecurity-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > programming-and-scripting-for-cybersecurity-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' programming-and-scripting-for-cybersecurity-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Malformed JSON records
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
python3 -m json.tool sample.json > programming-and-scripting-for-cybersecurity-output/json-tool-edge.txt 2>/dev/null || true
```

### Edge Case: Mixed delimiters in CSV
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
head -100 sample.csv > programming-and-scripting-for-cybersecurity-output/csv-sample.txt 2>/dev/null || true
```

### Edge Case: Huge logs
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
split -l 50000 sample.log programming-and-scripting-for-cybersecurity-output/log-part- 2>/dev/null || true
```

### Edge Case: Timezone drift
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
date -u > programming-and-scripting-for-cybersecurity-output/current-utc.txt
```

### Edge Case: Binary blobs mixed with text
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
file sample.log > programming-and-scripting-for-cybersecurity-output/file-type-edge.txt 2>/dev/null || true
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| awk | Fast on fixed-column text | Weak on nested data | Text-log field extraction |
| jq | Strong on stable JSON | Fails on malformed input | JSON normalization |
| python3 | Flexible across formats | More code to review | Reusable parsers |


## Output Templates

- produce: `programming-and-scripting-for-cybersecurity-output/programming-and-scripting-for-cybersecurity-report.md`
- produce: `programming-and-scripting-for-cybersecurity-output/output-manifest.txt`
- produce: `programming-and-scripting-for-cybersecurity-output/review-bundle.tgz`
- produce: `programming-and-scripting-for-cybersecurity-output/programming-and-scripting-for-cybersecurity-findings.csv`

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

- Confirm `programming-and-scripting-for-cybersecurity-output` contains the report, manifest, and at least one evidence artifact.
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
