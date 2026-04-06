---
skill: buffer-overflow-examples
name: buffer-overflow-examples
version: 1.0.0
source: h4cker/buffer-overflow-examples
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: Review memory-safety concepts, crash evidence, and secure remediation patterns without exploit weaponization.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: Buffer Overflow Examples

Summary: Review memory-safety concepts, crash evidence, and secure remediation patterns without exploit weaponization.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the task clearly maps to buffer-overflow-examples topics in an owned, authorized, or lab context
- Use when Codex should collect evidence first and avoid broad assumptions
- Use when the result should separate confirmed observations, unknowns, and safe next actions

## KEY TECHNIQUES & TOOLS

### Phase 1: Confirm the lab binary, source file, and crash artifact set

```bash
mkdir -p buffer-overflow-examples-output
find . -maxdepth 4 \( -iname "*.c" -o -iname "*.cpp" -o -iname "*.h" -o -perm -111 -o -iname "core*" \) | sort > buffer-overflow-examples-output/files.txt
file $(head -20 buffer-overflow-examples-output/files.txt 2>/dev/null) > buffer-overflow-examples-output/file-types.txt 2>/dev/null || true
sed -n '1,40p' buffer-overflow-examples-output/files.txt
```

### Phase 2: Inspect crash-relevant code paths and memory-safety signals

```bash
rg -n "strcpy|strcat|sprintf|gets|scanf|memcpy|alloca|read\\(|recv\\(|fgets\\(" . 2>/dev/null > buffer-overflow-examples-output/memory-risk-signals.txt || true
rg -n "stack smashing|segmentation fault|buffer overflow|core dumped|asan|ubsan" . 2>/dev/null > buffer-overflow-examples-output/crash-signals.txt || true
sed -n '1,60p' buffer-overflow-examples-output/memory-risk-signals.txt
```

### Phase 3: Capture exploit-mitigation and reproduction context without weaponizing it

```bash
find . -maxdepth 4 \( -iname "Makefile" -o -iname "CMakeLists.txt" -o -iname "*.sh" -o -iname "*.md" \) | sort > buffer-overflow-examples-output/build-context.txt
rg -n "FORTIFY|stack-protector|PIE|RELRO|ASLR|NX|canary" . 2>/dev/null > buffer-overflow-examples-output/mitigation-signals.txt || true
wc -l buffer-overflow-examples-output/files.txt buffer-overflow-examples-output/memory-risk-signals.txt buffer-overflow-examples-output/mitigation-signals.txt 2>/dev/null || true
```

### Decision rules

- If the scope is unclear, stop and ask for the owned asset, repository, or lab boundary
- If the binary crashes but no source is available, stay with crash evidence, mitigations, and reproduction notes instead of speculating about root cause
- If the code uses risky functions but no untrusted input path is visible, label it as a hardening concern rather than a confirmed exploitable overflow
- If compiler mitigations appear disabled, record that as a separate finding from the memory bug itself
- If the task would require exploit chaining or live-target abuse, stop at defensive analysis and remediation guidance only

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Crash Context`
  - `Unsafe Memory Operations`
  - `Mitigation Posture`
  - `Findings`
  - `Artifacts`
  - `Recommended Next Actions`

- `Artifacts` should list:
  - `buffer-overflow-examples-output/files.txt`
  - `buffer-overflow-examples-output/file-types.txt`
  - `buffer-overflow-examples-output/memory-risk-signals.txt`
  - `buffer-overflow-examples-output/crash-signals.txt`
  - `buffer-overflow-examples-output/build-context.txt`
  - `buffer-overflow-examples-output/mitigation-signals.txt`

## Quick Mode (< 5 minutes)

- Start with the first scope or inventory command, not the whole workflow.
- Limit the first pass to one binary or one crash sample.
- Stop after you have one risky code-path artifact and one mitigation note.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the source tree is incomplete, keep the review at artifact level and record exactly which source files are missing.
- If the binary is stripped, focus on crash strings, build flags, and known unsafe function usage from adjacent code or docs.
- Edge case 1: the target is CTF-only and intentionally unsafe; separate learning value from real-world remediation advice.
- Edge case 2: the crash appears only on one architecture or build profile; record the compiler and platform before comparing results.


## Phase Output Map

- Phase 1 output: binary, source, and crash-artifact inventory.
- Phase 2 output: unsafe function hits and crash-context evidence.
- Phase 3 output: mitigation posture and reproduction context for remediation review.


## Done When

- Scope is fixed to one owned lab program, binary set, or crash sample.
- At least one artifact-backed unsafe memory path or crash note is saved.
- Mitigations are classified as present, partial, or absent with evidence.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper work.
```bash
            # Create the output directory if it is not present yet
            mkdir -p buffer-overflow-examples-output
            # Save a full artifact manifest for the current workspace
            find . -maxdepth 5 -type f | sort > buffer-overflow-examples-output/artifact-manifest.txt
            # Write a short scope note starter
            printf '%s
' 'scope:' 'assumptions:' 'owner:' > buffer-overflow-examples-output/scope-note.txt
```
- Every later finding should trace back to this manifest.
- The scope note forces the reviewer to write boundaries down early.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they saw the same files.
```bash
# Hash a subset of files from the artifact manifest
head -30 buffer-overflow-examples-output/artifact-manifest.txt | xargs -r sha256sum > buffer-overflow-examples-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > buffer-overflow-examples-output/review-start-utc.txt
date > buffer-overflow-examples-output/review-start-local.txt
```
- Hashes and timestamps are the minimum reproducibility set.
- Keep UTC and local time together when teams work across zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening everything by hand.
```bash
# Search for high-signal words in the current tree
rg -n "error|warn|failed|secret|token|debug|staging|config" . > buffer-overflow-examples-output/signal-hits.txt 2>/dev/null || true
# Save a short preview of the signal list
sed -n '1,80p' buffer-overflow-examples-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 buffer-overflow-examples-output/signal-hits.txt | sort | uniq -c | sort -nr > buffer-overflow-examples-output/signal-hit-counts.txt 2>/dev/null || true
```
- This helps you choose which files deserve deeper review first.
- A file-count summary is often more useful than raw hits alone.

### Technique 4: Bundle artifacts for handoff
Use when the next reviewer should not have to recreate your workspace state.
```bash
# Build a compressed handoff bundle
tar -czf buffer-overflow-examples-output/review-bundle.tgz buffer-overflow-examples-output 2>/dev/null || true
# Hash the bundle for integrity checks
sha256sum buffer-overflow-examples-output/review-bundle.tgz > buffer-overflow-examples-output/review-bundle.tgz.sha256 2>/dev/null || true
# List bundle contents for a quick QA pass
tar -tzf buffer-overflow-examples-output/review-bundle.tgz | head -80 2>/dev/null || true
```
- The bundle should contain artifacts, not vague notes.
- A bundle hash is useful when more than one person touches the output.

### Technique 5: Manifest-driven report starter
Use when you want report writing to start from saved artifacts rather than memory.
```bash
            # Create a report starter that references artifact paths explicitly
            printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > buffer-overflow-examples-output/report-starter.md
            # Save a simple output manifest for the generated files
            find buffer-overflow-examples-output -maxdepth 2 -type f | sort > buffer-overflow-examples-output/output-manifest.txt
            # Preview the report starter
            sed -n '1,40p' buffer-overflow-examples-output/report-starter.md
```
- Report drafting should begin only after artifacts exist.
- The output manifest becomes the handoff map for the next skill.

### Technique 6: Binary and crash inventory
Use when source, binaries, and crash artifacts may all be present in one folder.
```bash
# Inventory likely source, binaries, and crash artifacts
find . -maxdepth 5 \( -iname "*.c" -o -iname "*.cpp" -o -iname "*.h" -o -perm -111 -o -iname "core*" \) | sort > buffer-overflow-examples-output/deep-files.txt
# Save file types for the first artifacts
head -25 buffer-overflow-examples-output/deep-files.txt | xargs -r file > buffer-overflow-examples-output/deep-file-types.txt
# Preview the inventory
sed -n '1,80p' buffer-overflow-examples-output/deep-files.txt
```
- This tells you whether the review should be source-led or crash-led.
- The file-type list also catches renamed samples.

### Technique 7: Header and segment review
Use when architecture, entry point, and segment layout matter before deeper analysis.
```bash
# Read the binary header
readelf -h ./challenge.bin > buffer-overflow-examples-output/readelf-header.txt 2>/dev/null || true
# Read program headers
readelf -l ./challenge.bin > buffer-overflow-examples-output/readelf-program-headers.txt 2>/dev/null || true
# Preview the header summary
sed -n '1,60p' buffer-overflow-examples-output/readelf-header.txt 2>/dev/null || true
```
- Start here before talking about 32-bit vs 64-bit or segment layout.
- Keep the error output if the file is not ELF because that also identifies the format boundary.

### Technique 8: Strings, symbols, and risky APIs
Use when you need clues about dangerous functions or missing symbol information.
```bash
# Save symbols and strings when available
nm -an ./challenge.bin > buffer-overflow-examples-output/nm-symbols.txt 2>/dev/null || true
strings -a ./challenge.bin | head -200 > buffer-overflow-examples-output/strings-head.txt 2>/dev/null || true
# Search for risky APIs in source or symbol output
rg -n "strcpy|strcat|sprintf|gets|scanf|memcpy|alloca|recv\(|read\(" . buffer-overflow-examples-output/nm-symbols.txt > buffer-overflow-examples-output/risky-api-hits.txt 2>/dev/null || true
```
- Stripped binaries may still yield useful strings or import hints.
- Keep source and symbol hits together for one review trail.

### Technique 9: Mitigation and build-flag review
Use when the core question is whether basic hardening is present.
```bash
# Search build files for hardening flags
rg -n "stack-protector|FORTIFY_SOURCE|PIE|RELRO|asan|ubsan|fno-omit-frame-pointer" . > buffer-overflow-examples-output/build-hardening-signals.txt 2>/dev/null || true
# Save dynamic section details
readelf -d ./challenge.bin > buffer-overflow-examples-output/readelf-dynamic.txt 2>/dev/null || true
# Preview hardening hits
sed -n '1,60p' buffer-overflow-examples-output/build-hardening-signals.txt
```
- Mitigation absence is its own finding even without a crash.
- Keep build and binary evidence separate so intent and result are both visible.

### Technique 10: Controlled gdb and sanitizer review
Use when you need lab-only crash context for debugging and remediation.
```bash
# Capture a batch-mode backtrace
gdb -q -batch -ex "run" -ex "bt" --args ./challenge.bin > buffer-overflow-examples-output/gdb-backtrace.txt 2>&1 || true
# Attempt a sanitizer-oriented lab build
CC=cc CFLAGS="-O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer" make > buffer-overflow-examples-output/asan-build.txt 2>&1 || true
# Preview the backtrace or build output
sed -n '1,80p' buffer-overflow-examples-output/gdb-backtrace.txt
```
- This is for owned lab builds and controlled debugging only.
- If the sanitizer build fails, keep the build log as evidence about the toolchain.


## Decision Logic

- If the first inventory artifact already answers the user question → stop and write the answer instead of widening scope.
- If the primary technique produces only weak or noisy evidence → switch to a fallback that preserves artifacts rather than guessing.
- If permissions block the happy path → prefer config review, offline artifacts, or read-only logs.
- If the work is limited to passive or lab-only scope → skip any technique that would add traffic or mutate state.
- If two evidence sources agree → increase confidence and keep both artifact paths in the report.
- If two evidence sources disagree → mark the finding unresolved and save both artifacts.
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `systematic-debugging`.
- If the filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove that command from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.


## Fallback Techniques

### ถ้า `gdb` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
strings -a ./challenge.bin > buffer-overflow-examples-output/strings-full-fallback.txt 2>/dev/null || true
```

### ถ้า `readelf` is unavailable:
```bash
# Alternative: preserve evidence with the least risky available path
objdump -x ./challenge.bin > buffer-overflow-examples-output/objdump-header-fallback.txt 2>/dev/null || true
```

### ถ้า source is missing:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 -perm -111 -type f | sort > buffer-overflow-examples-output/binary-only-fallback.txt
```

### ถ้า sanitizer build fails:
```bash
# Alternative: preserve evidence with the least risky available path
sed -n "1,120p" buffer-overflow-examples-output/asan-build.txt > buffer-overflow-examples-output/asan-build-first-120.txt 2>/dev/null || true
```

### ถ้า permissions block core-file access:
```bash
# Alternative: preserve evidence with the least risky available path
find . -maxdepth 5 -type f -readable | sort > buffer-overflow-examples-output/readable-artifacts.txt
```


## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find buffer-overflow-examples-output -maxdepth 2 -type f | sort > buffer-overflow-examples-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > buffer-overflow-examples-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' buffer-overflow-examples-output/quick-artifacts.txt 2>/dev/null || true
```


## Edge Cases

### Edge Case: Stripped binary
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
file ./challenge.bin > buffer-overflow-examples-output/stripped-edge.txt 2>/dev/null || true
```

### Edge Case: 32-bit vs 64-bit mismatch
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
readelf -h ./challenge.bin | grep -E "Class|Machine" > buffer-overflow-examples-output/arch-edge.txt 2>/dev/null || true
```

### Edge Case: Static binary
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
ldd ./challenge.bin > buffer-overflow-examples-output/ldd-edge.txt 2>&1 || true
```

### Edge Case: Optimization-specific crash
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
rg -n "-O0|-O1|-O2|-O3" . > buffer-overflow-examples-output/optimization-edge.txt 2>/dev/null || true
```

### Edge Case: CTF sample vs production-like code
สถานการณ์: this case changes how evidence should be interpreted or collected.
วิธีจัดการ:
```bash
printf "%s
" "Label the sample as CTF or production-like before assigning remediation priority" > buffer-overflow-examples-output/context-edge.txt
```


## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| readelf/objdump | Strong binary header detail | Less friendly to summarize | Format and segment review |
| strings/nm | Fast clue gathering | Incomplete on some stripped files | Import and text clues |
| gdb batch | Reusable crash traces | Needs runnable lab sample | Backtrace capture |


## Output Templates

- produce: `buffer-overflow-examples-output/buffer-overflow-examples-report.md`
- produce: `buffer-overflow-examples-output/output-manifest.txt`
- produce: `buffer-overflow-examples-output/review-bundle.tgz`
- produce: `buffer-overflow-examples-output/buffer-overflow-examples-findings.csv`

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

- Confirm `buffer-overflow-examples-output` contains the report, manifest, and at least one evidence artifact.
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


## Next: load `systematic-debugging` skill

- Load `systematic-debugging` next if you need to isolate the exact crash condition from saved evidence.
