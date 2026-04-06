---
skill: pen-testing-reports
name: pen-testing-reports
version: 1.0.0
source: h4cker/pen-testing-reports
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Structure evidence-first findings, remediation notes, and executive summaries for authorized testing engagements.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Pen Testing Reports

Summary: Structure evidence-first findings, remediation notes, and executive summaries for authorized testing engagements.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to pen-testing-reports topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p pen-testing-reports-output
find . -maxdepth 3 -type f | sort | head -100 > pen-testing-reports-output/files.txt
ls -la pen-testing-reports-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > pen-testing-reports-output/signals.txt || true
sed -n '1,40p' pen-testing-reports-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > pen-testing-reports-output/inventory.txt
wc -l pen-testing-reports-output/inventory.txt pen-testing-reports-output/signals.txt 2>/dev/null || true
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
  - `pen-testing-reports-output/files.txt`
  - `pen-testing-reports-output/signals.txt`
  - `pen-testing-reports-output/inventory.txt`

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
            mkdir -p pen-testing-reports-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > pen-testing-reports-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > pen-testing-reports-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 pen-testing-reports-output/artifact-manifest.txt | xargs -r sha256sum > pen-testing-reports-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > pen-testing-reports-output/review-start-utc.txt
date > pen-testing-reports-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > pen-testing-reports-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' pen-testing-reports-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 pen-testing-reports-output/signal-hits.txt | sort | uniq -c | sort -nr > pen-testing-reports-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf pen-testing-reports-output/review-bundle.tgz pen-testing-reports-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum pen-testing-reports-output/review-bundle.tgz > pen-testing-reports-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf pen-testing-reports-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > pen-testing-reports-output/report-starter.md
            # Save a simple output manifest for the generated files
            find pen-testing-reports-output -maxdepth 2 -type f | sort > pen-testing-reports-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' pen-testing-reports-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Evidence tree creation
Use when screenshots, request captures, notes, and remediation items need a predictable home.
```bash
# Create a report workspace with evidence subfolders
mkdir -p pen-testing-reports-output/screenshots pen-testing-reports-output/raw-http pen-testing-reports-output/notes pen-testing-reports-output/appendix
# Save the resulting directory layout
find pen-testing-reports-output -maxdepth 2 -type d | sort > pen-testing-reports-output/report-tree.txt
# Preview the tree
cat pen-testing-reports-output/report-tree.txt
```
- A stable evidence tree reduces broken links and lost artifacts.
- Start here before writing any findings.

### Technique 7: Finding and severity skeletons
Use when every finding should have the same fields and a severity mapping.
```bash
                # Create a markdown finding template
                printf '%s
' '## Finding Title' '### Summary' '### Evidence' '### Impact' '### Reproduction' '### Remediation' '### Validation Notes' > pen-testing-reports-output/finding-template.md
                # Create a CSV tracker for findings
                printf '%s
' 'id,severity,title,asset,status' > pen-testing-reports-output/findings.csv
                # Create a severity matrix starter
                printf '%s
' 'severity,likelihood,impact,fix_priority' 'low,low,limited,planned' 'medium,possible,meaningful,scheduled' 'high,likely,material,urgent' > pen-testing-reports-output/severity-matrix.csv
```
- Use the same fields for every finding to keep review consistent.
- Severity and evidence paths should be explicit, not implied.

### Technique 8: Reproduction and retest tracking
Use when issues will move through remediation and follow-up cycles.
```bash
                # Create remediation and retest trackers
                printf '%s
' 'finding_id,owner,action,target_date,status' > pen-testing-reports-output/remediation-tracker.csv
                printf '%s
' 'finding_id,retest_date,result,evidence_path' > pen-testing-reports-output/retest-tracker.csv
                # Preview both trackers
                cat pen-testing-reports-output/remediation-tracker.csv
                cat pen-testing-reports-output/retest-tracker.csv
```
- This prevents follow-up work from drifting into email threads or vague notes.
- Use stable finding IDs across the whole lifecycle.

### Technique 9: Redaction and export preparation
Use when evidence contains tokens, personal data, or environment-specific secrets.
```bash
# Redact obvious bearer tokens in a draft copy
sed -E 's/(Bearer )[A-Za-z0-9._-]+/REDACTED/g' draft.md > pen-testing-reports-output/draft-redacted.md 2>/dev/null || true
# Redact email addresses in a second copy
sed -E 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/[REDACTED_EMAIL]/g' draft.md > pen-testing-reports-output/draft-redacted-emails.md 2>/dev/null || true
# Preview the redacted draft
sed -n '1,60p' pen-testing-reports-output/draft-redacted.md 2>/dev/null || true
```
- Redact copies, not the only original notes file.
- Record what changed so internal and external drafts do not diverge silently.

### Technique 10: Bundle final report artifacts
Use when another reviewer or project owner needs the report package and evidence index together.
```bash
# Build the final report bundle
tar -czf pen-testing-reports-output/report-bundle.tgz pen-testing-reports-output 2>/dev/null || true
# Hash the bundle
sha256sum pen-testing-reports-output/report-bundle.tgz > pen-testing-reports-output/report-bundle.tgz.sha256 2>/dev/null || true
# Save an output manifest
find pen-testing-reports-output -maxdepth 2 -type f | sort > pen-testing-reports-output/output-manifest.txt
```
- Bundle after redaction and evidence indexing are complete.
- The manifest is the fastest quality gate before sharing.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `status`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `tree` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
find pen-testing-reports-output -maxdepth 2 -type d | sort > pen-testing-reports-output/report-tree-fallback.txt
```

### ถ้า screenshots are unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) | sort > pen-testing-reports-output/image-inventory.txt
```

### ถ้า pandoc or export tooling is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
cp pen-testing-reports-output/finding-template.md pen-testing-reports-output/shareable-report.md 2>/dev/null || true
```

### ถ้า raw notes are messy:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "TODO\|FIXME\|evidence\|impact" . > pen-testing-reports-output/note-keywords.txt 2>/dev/null || true
```

### ถ้า sensitive data cannot be shared externally:
```bash
# Alternative: preserve evidence with the least risky available path
cp pen-testing-reports-output/finding-template.md pen-testing-reports-output/external-template.md 2>/dev/null || true
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find pen-testing-reports-output -maxdepth 2 -type f | sort > pen-testing-reports-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > pen-testing-reports-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' pen-testing-reports-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Duplicate findings across assets
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "duplicate_group,finding_id,primary_asset" > pen-testing-reports-output/duplicates.csv
```

### Edge Case: Partial reproduction only
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "finding_id,missing_step,blocking_reason" > pen-testing-reports-output/partial-repro.csv
```

### Edge Case: Highly sensitive evidence
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find pen-testing-reports-output -type f | sort > pen-testing-reports-output/redaction-review-files.txt
```

### Edge Case: Multi-step chain finding
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "step,artifact,dependency" > pen-testing-reports-output/attack-chain.csv
```

### Edge Case: Retest after environment rebuild
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "finding_id,baseline_before,baseline_after" > pen-testing-reports-output/rebuild-retest.csv
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| Markdown | Easy to diff | Needs discipline for consistency | Findings and appendices |
| CSV | Great for trackers | Poor for narrative | Retest and ownership |
| Tar bundle | Strong handoff artifact | Not human-readable alone | Final package |


## Output Templates

- produce: `pen-testing-reports-output/pen-testing-reports-report.md`
- produce: `pen-testing-reports-output/output-manifest.txt`
- produce: `pen-testing-reports-output/review-bundle.tgz`
- produce: `pen-testing-reports-output/pen-testing-reports-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `status`
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

- Confirm `pen-testing-reports-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `status` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `status`.

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
