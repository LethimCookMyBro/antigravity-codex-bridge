---
skill: bug-bounties
name: bug-bounties
version: 1.0.0
source: h4cker/bug-bounties
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Review scope notes, target inventory, evidence handling, and report-quality workflows for authorized bug bounty programs.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Bug Bounties

Summary: Review scope notes, target inventory, evidence handling, and report-quality workflows for authorized bug bounty programs.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to bug-bounties topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p bug-bounties-output
find . -maxdepth 3 -type f | sort | head -100 > bug-bounties-output/files.txt
ls -la bug-bounties-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > bug-bounties-output/signals.txt || true
sed -n '1,40p' bug-bounties-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > bug-bounties-output/inventory.txt
wc -l bug-bounties-output/inventory.txt bug-bounties-output/signals.txt 2>/dev/null || true
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
  - `bug-bounties-output/files.txt`
  - `bug-bounties-output/signals.txt`
  - `bug-bounties-output/inventory.txt`

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
            mkdir -p bug-bounties-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > bug-bounties-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > bug-bounties-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 bug-bounties-output/artifact-manifest.txt | xargs -r sha256sum > bug-bounties-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > bug-bounties-output/review-start-utc.txt
date > bug-bounties-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > bug-bounties-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' bug-bounties-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 bug-bounties-output/signal-hits.txt | sort | uniq -c | sort -nr > bug-bounties-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf bug-bounties-output/review-bundle.tgz bug-bounties-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum bug-bounties-output/review-bundle.tgz > bug-bounties-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf bug-bounties-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > bug-bounties-output/report-starter.md
            # Save a simple output manifest for the generated files
            find bug-bounties-output -maxdepth 2 -type f | sort > bug-bounties-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' bug-bounties-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Scope and exclusion extraction
Use when the first risk is testing an out-of-scope target.
```bash
# Search scope files for in-scope and exclusion language
rg -n "in scope|out of scope|excluded|test accounts|safe harbor|do not" . > bug-bounties-output/scope-signals.txt 2>/dev/null || true
# Build a candidate target list from local docs
rg -n "https?://|[A-Za-z0-9.-]+\.[A-Za-z]{2,}" . > bug-bounties-output/candidate-targets.txt 2>/dev/null || true
# Preview scope hints
sed -n '1,80p' bug-bounties-output/scope-signals.txt
```
- Always start with program rules before technical notes.
- A candidate target list is not proof of scope until the docs say so.

### Technique 7: Target inventory and ownership map
Use when the program covers many brands, APIs, or domains.
```bash
                # Create a target inventory sheet
                printf '%s
' 'target,type,in_scope,notes' > bug-bounties-output/target-inventory.csv
                # Save a simple unique host list from candidate targets
                cut -d: -f1 bug-bounties-output/candidate-targets.txt | sort -u > bug-bounties-output/candidate-target-hosts.txt 2>/dev/null || true
                # Preview the host list
                sed -n '1,60p' bug-bounties-output/candidate-target-hosts.txt
```
- Keep type and scope status together so later testing does not drift.
- Unknown scope should stay marked as unknown, not implicitly allowed.

### Technique 8: Evidence tree and finding template
Use when you want a clean place for notes, screenshots, and report-ready structure.
```bash
                # Create evidence folders
                mkdir -p bug-bounties-output/screenshots bug-bounties-output/raw-http bug-bounties-output/notes bug-bounties-output/retest
                # Create a submission-ready finding template
                printf '%s
' '## Title' '## Scope Proof' '## Reproduction Summary' '## Impact' '## Evidence Paths' '## Remediation' '## Report Notes' > bug-bounties-output/finding-template.md
                # Create a finding tracker
                printf '%s
' 'finding_id,title,target,status,platform_submission' > bug-bounties-output/finding-tracker.csv
```
- Use the same fields every time so review and submission stay consistent.
- The evidence tree should exist before screenshots or raw HTTP captures are moved around.

### Technique 9: Severity, duplicate, and retest tracking
Use when the program may have similar findings or multiple follow-up cycles.
```bash
                # Create severity and duplicate tracking sheets
                printf '%s
' 'finding_id,severity,impact,customer_path,notes' > bug-bounties-output/severity-sheet.csv
                printf '%s
' 'finding_id,possible_duplicate_of,reason' > bug-bounties-output/duplicates.csv
                printf '%s
' 'finding_id,retest_date,result,evidence_path' > bug-bounties-output/retest.csv
```
- Many good submissions fail because duplicate or retest state is unclear.
- Keep stable IDs across every tracker.

### Technique 10: Submission draft and final bundle
Use when another reviewer or a platform submission is the next step.
```bash
                # Create a submission draft skeleton
                printf '%s
' '# Submission Draft' '## Scope Proof' '## Reproduction' '## Impact' '## Supporting Evidence' '## Requested Follow-up' > bug-bounties-output/submission-draft.md
                # Save an output manifest
                find bug-bounties-output -maxdepth 2 -type f | sort > bug-bounties-output/output-manifest.txt
                # Bundle the review package
                tar -czf bug-bounties-output/bug-bounty-review.tgz bug-bounties-output 2>/dev/null || true
```
- The submission draft is where scope proof should become explicit.
- A bundle helps a second reviewer sanity-check the report before submission.


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

### ถ้า scope documentation is missing:
```bash
# Alternative: preserve evidence with the least risky available path
printf "%s
" "No local scope docs found; do not proceed past inventory" > bug-bounties-output/no-scope-warning.txt
```

### ถ้า screenshots are unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "*.png" -o -iname "*.jpg" \) | sort > bug-bounties-output/image-fallback.txt
```

### ถ้า platform export is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
cp bug-bounties-output/submission-draft.md bug-bounties-output/submission-draft-fallback.md 2>/dev/null || true
```

### ถ้า permission is limited to notes only:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 4 -type f -readable | sort > bug-bounties-output/readable-evidence.txt
```

### ถ้า multiple brands share infrastructure:
```bash
# Alternative: preserve evidence with the least risky available path
printf "%s
" "Review brand-to-target ownership before submission" > bug-bounties-output/shared-brand-warning.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find bug-bounties-output -maxdepth 2 -type f | sort > bug-bounties-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > bug-bounties-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' bug-bounties-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: CDN or shared edge infrastructure
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Confirm the behavior belongs to the program and not only the shared edge provider" > bug-bounties-output/cdn-edge.txt
```

### Edge Case: Preview or ephemeral review apps
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Record whether the asset is preview-only before assigning severity" > bug-bounties-output/preview-edge.txt
```

### Edge Case: Duplicate behavior across many subdomains
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Track the canonical proof host and repeated hosts separately" > bug-bounties-output/duplicate-hosts-edge.txt
```

### Edge Case: Issue requires authenticated test account
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Document the approved account boundary and data-handling rules" > bug-bounties-output/auth-edge.txt
```

### Edge Case: Gradual rollout fixes
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Retest all in-scope assets before closing the finding" > bug-bounties-output/rollout-edge.txt
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| Markdown draft | Fast narrative shaping | Needs consistency checks | Single finding review |
| CSV trackers | Good for duplicates and retests | Not narrative-friendly | Program management |
| Tar bundle | Strong reviewer handoff | Needs redaction discipline | Second-analyst review |


## Output Templates

- produce: `bug-bounties-output/bug-bounties-report.md`
- produce: `bug-bounties-output/output-manifest.txt`
- produce: `bug-bounties-output/review-bundle.tgz`
- produce: `bug-bounties-output/bug-bounties-findings.csv`

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

- Confirm `bug-bounties-output` contains the report, manifest, and at least one evidence artifact.
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
