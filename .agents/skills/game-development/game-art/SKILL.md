---
skill: game-art
name: game-art
version: 1.0.0
source: codex/game-development/game-art
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, windows, macos]
description: Game art principles. Visual style selection, asset pipeline, animation workflow.
allowed-tools: Read, Glob, Grep
---
# Game Art Principles

Summary: Game art principles. Visual style selection, asset pipeline, animation workflow.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.
## WHEN TO USE THIS SKILL

- Use when the task clearly matches `game-art` or the folder's specialized domain
- Use when Codex should follow a repeatable workflow instead of ad-hoc reasoning
- Use when the output should separate scope, evidence, findings, and next actions


> Visual design thinking for games - style selection, asset pipelines, and art direction.

---

## 1. Art Style Selection

### Decision Tree

```
What feeling should the game evoke?
│
├── Nostalgic / Retro
│   ├── Limited palette? → Pixel Art
│   └── Hand-drawn feel? → Vector / Flash style
│
├── Realistic / Immersive
│   ├── High budget? → PBR 3D
│   └── Stylized realism? → Hand-painted textures
│
├── Approachable / Casual
│   ├── Clean shapes? → Flat / Minimalist
│   └── Soft feel? → Gradient / Soft shadows
│
└── Unique / Experimental
    └── Define custom style guide
```

### Style Comparison Matrix

| Style | Production Speed | Skill Floor | Scalability | Best For |
|-------|------------------|-------------|-------------|----------|
| **Pixel Art** | Medium | Medium | Hard to hire | Indie, retro |
| **Vector/Flat** | Fast | Low | Easy | Mobile, casual |
| **Hand-painted** | Slow | High | Medium | Fantasy, stylized |
| **PBR 3D** | Slow | High | AAA pipeline | Realistic games |
| **Low-poly** | Fast | Medium | Easy | Indie 3D |
| **Cel-shaded** | Medium | Medium | Medium | Anime, cartoon |

---

## 2. Asset Pipeline Decisions

### 2D Pipeline

| Phase | Tool Options | Output |
|-------|--------------|--------|
| **Concept** | Paper, Procreate, Photoshop | Reference sheet |
| **Creation** | Aseprite, Photoshop, Krita | Individual sprites |
| **Atlas** | TexturePacker, Aseprite | Spritesheet |
| **Animation** | Spine, DragonBones, Frame-by-frame | Animation data |
| **Integration** | Engine import | Game-ready assets |

### 3D Pipeline

| Phase | Tool Options | Output |
|-------|--------------|--------|
| **Concept** | 2D art, Blockout | Reference |
| **Modeling** | Blender, Maya, 3ds Max | High-poly mesh |
| **Retopology** | Blender, ZBrush | Game-ready mesh |
| **UV/Texturing** | Substance Painter, Blender | Texture maps |
| **Rigging** | Blender, Maya | Skeletal rig |
| **Animation** | Blender, Maya, Mixamo | Animation clips |
| **Export** | FBX, glTF | Engine-ready |

---

## 3. Color Theory Decisions

### Palette Selection

| Goal | Strategy | Example |
|------|----------|---------|
| **Harmony** | Complementary or analogous | Nature games |
| **Contrast** | High saturation differences | Action games |
| **Mood** | Warm/cool temperature | Horror, cozy |
| **Readability** | Value contrast over hue | Gameplay clarity |

### Color Principles

- **Hierarchy:** Important elements should pop
- **Consistency:** Same object = same color family
- **Context:** Colors read differently on backgrounds
- **Accessibility:** Don't rely only on color

---

## 4. Animation Principles

### The 12 Principles (Applied to Games)

| Principle | Game Application |
|-----------|------------------|
| **Squash & Stretch** | Jump arcs, impacts |
| **Anticipation** | Wind-up before attack |
| **Staging** | Clear silhouettes |
| **Follow-through** | Hair, capes after movement |
| **Slow in/out** | Easing on transitions |
| **Arcs** | Natural movement paths |
| **Secondary Action** | Breathing, blinking |
| **Timing** | Frame count = weight/speed |
| **Exaggeration** | Readable from distance |
| **Appeal** | Memorable design |

### Frame Count Guidelines

| Action Type | Typical Frames | Feel |
|-------------|----------------|------|
| Idle breathing | 4-8 | Subtle |
| Walk cycle | 6-12 | Smooth |
| Run cycle | 4-8 | Energetic |
| Attack | 3-6 | Snappy |
| Death | 8-16 | Dramatic |

---

## 5. Resolution & Scale Decisions

### 2D Resolution by Platform

| Platform | Base Resolution | Sprite Scale |
|----------|-----------------|--------------|
| Mobile | 1080p | 64-128px characters |
| Desktop | 1080p-4K | 128-256px characters |
| Pixel art | 320x180 to 640x360 | 16-32px characters |

### Consistency Rule

Choose a base unit and stick to it:
- Pixel art: Work at 1x, scale up (never down)
- HD art: Define DPI, maintain ratio
- 3D: 1 unit = 1 meter (industry standard)

---

## 6. Asset Organization

### Naming Convention

```
[type]_[object]_[variant]_[state].[ext]

Examples:
spr_player_idle_01.png
tex_stone_wall_normal.png
mesh_tree_oak_lod2.fbx
```

### Folder Structure Principle

```
assets/
├── characters/
│   ├── player/
│   └── enemies/
├── environment/
│   ├── props/
│   └── tiles/
├── ui/
├── effects/
└── audio/
```

---

## 7. Anti-Patterns

| Don't | Do |
|-------|-----|
| Mix art styles randomly | Define and follow style guide |
| Work at final resolution only | Create at source resolution |
| Ignore silhouette readability | Test at gameplay distance |
| Over-detail background | Focus detail on player area |
| Skip color testing | Test on target display |

---

> **Remember:** Art serves gameplay. If it doesn't help the player, it's decoration.



## OUTPUT FORMAT

- Return:
  - `Scope`
  - `Evidence`
  - `Findings`
  - `Artifacts`
  - `Next Actions`
- Name any generated files by exact path so the next reviewer does not have to rediscover them.

## Starter Commands

Run these first to capture the current workspace before applying the rest of the skill.

```bash
mkdir -p game-art-output
pwd > game-art-output/pwd.txt
rg --files . | head -200 > game-art-output/repo-files.txt
git status --short > game-art-output/git-status.txt 2>/dev/null || true
```

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
Use when you need a stable starting point before deeper game-art review.
```bash
# Create the output directory for this skill
mkdir -p game-art-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > game-art-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > game-art-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 game-art-output/artifact-manifest.txt | xargs -r sha256sum > game-art-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > game-art-output/review-start-utc.txt
date > game-art-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > game-art-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' game-art-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 game-art-output/signal-hits.txt | sort | uniq -c | sort -nr > game-art-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > game-art-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > game-art-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' game-art-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > game-art-output/git-status.txt 2>/dev/null || true
git diff --stat > game-art-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > game-art-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > game-art-output/game-art-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > game-art-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' game-art-output/game-art-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find game-art-output -maxdepth 2 -type f | sort > game-art-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf game-art-output/game-art-bundle.tgz game-art-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf game-art-output/game-art-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 game-art-output/signal-hits.txt | sort | uniq -c | sort -nr > game-art-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' game-art-output/review-queue.txt > game-art-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' game-art-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > game-art-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> game-art-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' game-art-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > game-art-output/game-art-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > game-art-output/game-art-final.md
# Preview the output files for QA
sed -n '1,20p' game-art-output/game-art-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > game-art-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 game-art-output/game-art-bundle.tgz > game-art-output/game-art-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > game-art-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' game-art-output/review-queue.txt > game-art-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > game-art-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find game-art-output -maxdepth 2 -type f | sort > game-art-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > game-art-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' game-art-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > game-art-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > game-art-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > game-art-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > game-art-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > game-art-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `game-art-output/game-art-report.md`
- produce: `game-art-output/output-manifest.txt`
- produce: `game-art-output/game-art-bundle.tgz`
- produce: `game-art-output/game-art-findings.csv`

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

- Confirm `game-art-output` contains the report, manifest, and at least one evidence artifact.
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
