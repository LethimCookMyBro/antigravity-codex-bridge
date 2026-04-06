---
skill: mobile-security
name: mobile-security
version: 1.0.0
source: h4cker/mobile-security
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Review mobile app packaging, storage, transport, and permission posture for owned Android or iOS applications.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Mobile Security

Summary: Review mobile app packaging, storage, transport, and permission posture for owned Android or iOS applications.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to mobile-security topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Inventory in-scope assets and boundaries

```bash
mkdir -p mobile-security-output
find . -maxdepth 3 -type f | sort | head -100 > mobile-security-output/files.txt
ls -la mobile-security-output
```

### Phase 2: Review high-signal artifacts

```bash
rg -n "error|alert|warning|TODO|FIXME|password|token|secret" . 2>/dev/null | head -100 > mobile-security-output/signals.txt || true
sed -n '1,40p' mobile-security-output/signals.txt
```

### Phase 3: Preserve reproducible evidence

```bash
find . -maxdepth 4 -type f | sort > mobile-security-output/inventory.txt
wc -l mobile-security-output/inventory.txt mobile-security-output/signals.txt 2>/dev/null || true
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
  - `mobile-security-output/files.txt`
  - `mobile-security-output/signals.txt`
  - `mobile-security-output/inventory.txt`

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
            mkdir -p mobile-security-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > mobile-security-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > mobile-security-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 mobile-security-output/artifact-manifest.txt | xargs -r sha256sum > mobile-security-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > mobile-security-output/review-start-utc.txt
date > mobile-security-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > mobile-security-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' mobile-security-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 mobile-security-output/signal-hits.txt | sort | uniq -c | sort -nr > mobile-security-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf mobile-security-output/review-bundle.tgz mobile-security-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum mobile-security-output/review-bundle.tgz > mobile-security-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf mobile-security-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > mobile-security-output/report-starter.md
            # Save a simple output manifest for the generated files
            find mobile-security-output -maxdepth 2 -type f | sort > mobile-security-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' mobile-security-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Package inventory
Use when the build folder may contain APK, AAB, IPA, manifest, or plist files.
```bash
# Inventory Android and iOS package artifacts
find . -maxdepth 5 \( -iname "*.apk" -o -iname "*.aab" -o -iname "*.ipa" -o -iname "AndroidManifest.xml" -o -iname "Info.plist" \) | sort > mobile-security-output/package-files.txt
# Record file types for the first package set
head -20 mobile-security-output/package-files.txt | xargs -r file > mobile-security-output/package-types.txt
# Preview package inventory
sed -n '1,60p' mobile-security-output/package-files.txt
```
- This distinguishes real packages from renamed archives.
- Use the inventory to decide whether the review is Android, iOS, or mixed.

### Technique 7: Manifest and permission review
Use when you need exported components, debug flags, or high-risk permissions.
```bash
# Dump Android package metadata when aapt is present
aapt dump badging app.apk > mobile-security-output/aapt-badging.txt 2>/dev/null || true
# Print the manifest with apkanalyzer when available
apkanalyzer manifest print app.apk > mobile-security-output/manifest-print.txt 2>/dev/null || true
# Grep source and decoded output for exported components and flags
rg -n "android:exported|android:debuggable|android.permission|usesCleartextTraffic" . > mobile-security-output/manifest-signals.txt 2>/dev/null || true
```
- Use the grep output even when package tooling is unavailable.
- Exported components and debug flags are usually early findings.

### Technique 8: Static decompilation and archive review
Use when you need source-like output or resource names without altering the original package.
```bash
# Decode resources without rebuilding the package
apktool d -s app.apk -o mobile-security-output/apktool-out 2>/dev/null || true
# Create a Java-like view when jadx is present
jadx -d mobile-security-output/jadx-out app.apk 2>/dev/null || true
# Fallback to an archive listing when needed
unzip -l app.apk > mobile-security-output/unzip-list.txt 2>/dev/null || true
```
- Decoded output is easier to grep than raw binary content.
- Keep decompiled output in a dedicated folder for later diffs.

### Technique 9: Secret, URL, and storage signal search
Use when you need quick evidence of endpoints, tokens, or local persistence.
```bash
# Search for URLs, keys, and debug words
rg -n "https?://|api[_-]?key|token|secret|debug|staging|sandbox" mobile-security-output/jadx-out mobile-security-output/apktool-out . > mobile-security-output/endpoint-signals.txt 2>/dev/null || true
# Search for storage classes and file-system paths
rg -n "SharedPreferences|NSUserDefaults|sqlite|realm|RoomDatabase|Keychain|Documents/|Caches/" . > mobile-security-output/storage-signals.txt 2>/dev/null || true
# Review endpoint hits first
sed -n '1,80p' mobile-security-output/endpoint-signals.txt
```
- Do not assume an endpoint is live just because it appears in code.
- Separate staging and production URLs in the report.

### Technique 10: Transport and signing review
Use when TLS behavior, ATS, or signing trust is relevant to the mobile threat model.
```bash
# Search for network security config and ATS exceptions
rg -n "networkSecurityConfig|cleartextTrafficPermitted|NSAppTransportSecurity|NSAllowsArbitraryLoads" . > mobile-security-output/transport-signals.txt 2>/dev/null || true
# Print signer details when apksigner is available
apksigner verify --print-certs app.apk > mobile-security-output/apksigner-certs.txt 2>/dev/null || true
# Hash the package for traceability
sha256sum app.apk > mobile-security-output/app.sha256 2>/dev/null || true
```
- Transport and signing findings should stay separate because they answer different risks.
- Package hashes matter when you compare two builds or ask for retest evidence.


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

### ถ้า `aapt` or `apkanalyzer` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
unzip -l app.apk > mobile-security-output/package-list-fallback.txt 2>/dev/null || true
```

### ถ้า `jadx` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
strings -a app.apk | head -200 > mobile-security-output/package-strings.txt 2>/dev/null || true
```

### ถ้า `adb` access is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "*.apk" -o -iname "*.ipa" \) | sort > mobile-security-output/static-only-package-list.txt
```

### ถ้า the package is split into multiple APKs:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 \( -iname "base.apk" -o -iname "split_config*.apk" \) | sort > mobile-security-output/split-apk-files.txt
```

### ถ้า permission is limited on a test device:
```bash
# Alternative: preserve evidence with the least risky available path
adb shell pm list packages -f > mobile-security-output/adb-packages-f.txt 2>/dev/null || true
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find mobile-security-output -maxdepth 2 -type f | sort > mobile-security-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > mobile-security-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' mobile-security-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Certificate pinning present
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "pinning|CertificatePinner|TrustKit|SecTrust" . > mobile-security-output/pinning-edge.txt 2>/dev/null || true
```

### Edge Case: Root or jailbreak detection logic
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "rooted|su|Magisk|jailbreak|Cydia|frida" . > mobile-security-output/root-detection-edge.txt 2>/dev/null || true
```

### Edge Case: Heavy obfuscation
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "proguard|r8|minifyEnabled|obfuscate" . > mobile-security-output/obfuscation-edge.txt 2>/dev/null || true
```

### Edge Case: iOS-only bundle
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
find . -maxdepth 5 -iname "Info.plist" | sort > mobile-security-output/ios-plists.txt
```

### Edge Case: Enterprise or MDM-managed build
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "mdm|managed app|enterprise" . > mobile-security-output/mdm-edge.txt 2>/dev/null || true
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| apktool | Good for resources and manifest extraction | Less readable than jadx for logic | Resource review |
| jadx | Good source-like view | May miss exact bytecode detail | Static logic review |
| aapt/apkanalyzer | Fast metadata triage | Narrower than full decompile | Package triage |


## Output Templates

- produce: `mobile-security-output/mobile-security-report.md`
- produce: `mobile-security-output/output-manifest.txt`
- produce: `mobile-security-output/review-bundle.tgz`
- produce: `mobile-security-output/mobile-security-findings.csv`

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

- Confirm `mobile-security-output` contains the report, manifest, and at least one evidence artifact.
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
