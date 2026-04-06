---
skill: ui-ux-pro-max
name: ui-ux-pro-max
version: 1.0.0
source: codex/ui-ux-pro-max
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot, macos]
python_min: 3.8
description: AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
# UI UX Pro Max

Summary: AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.
## WHEN TO USE THIS SKILL

- Use when the task clearly matches `ui-ux-pro-max` or the folder's specialized domain
- Use when Codex should follow a repeatable workflow instead of ad-hoc reasoning
- Use when the output should separate scope, evidence, findings, and next actions


This skill adapts the Antigravity `ui-ux-pro-max` workflow for Codex.
Use it for design-heavy web and mobile tasks where visual direction and design
system quality matter.

## Overview

Comprehensive design guidance for web and mobile applications, including:

- 50+ styles
- 97 color palettes
- 57 font pairings
- 99 UX guidelines
- 25 chart types
- 9 technology stacks

## Prerequisites

Check Python:

```bash
python3 --version || python --version
```

If Python is missing:

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Windows
winget install Python.Python.3.12
```

## Workflow

### Step 1: Analyze User Requirements

Extract:

- Product type
- Style keywords
- Industry
- Stack, defaulting to `html-tailwind`

### Step 2: Generate Design System

Always start with `--design-system`:

```bash
# Replace <product_type> <industry> <keywords> with a real search phrase such as "beauty spa wellness"
# Add -p "Project Name" only when you want the saved design system tagged with a project name
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Project Name"
```

This command:

1. Searches multiple domains in parallel
2. Applies reasoning rules from `ui-reasoning.csv`
3. Returns pattern, style, colors, typography, and effects
4. Includes anti-patterns to avoid

Example:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System

To persist the design system:

```bash
# Replace <query> with a concrete product + style query, for example "fintech dashboard minimal"
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech dashboard minimal" --design-system --persist -p "Project Name"
```

This creates:

- `design-system/MASTER.md`
- `design-system/pages/`

With page-specific override:

```bash
# Replace <query> with the design-system query and --page with the page you want overrides for
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech dashboard minimal" --design-system --persist -p "Project Name" --page "dashboard"
```

### Step 3: Supplement with Detailed Searches

Use additional searches when needed:

```bash
# Replace <keyword> with the concept to search for and <domain> with one of: style, chart, ux, typography, landing
# Add -n 20 only when you want to override the default result count
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux -n 20
```

Common domains:

| Need | Domain |
|------|--------|
| More style options | `style` |
| Chart recommendations | `chart` |
| UX best practices | `ux` |
| Typography options | `typography` |
| Landing structure | `landing` |

### Step 4: Stack Guidelines

If the user does not specify a stack, default to `html-tailwind`.

```bash
# Replace <keyword> with a concrete layout or component query
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "responsive pricing table" --stack html-tailwind
```

Available stacks include:

- `html-tailwind`
- `react`
- `nextjs`
- `vue`
- `svelte`
- `swiftui`
- `react-native`
- `flutter`
- `shadcn`
- `jetpack-compose`

## Example Workflow

User request:

```text
Build a landing page for a professional skincare service
```

Suggested sequence:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

## Output Formats

```bash
# ASCII box
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

## Tips for Better Results

1. Be specific with keywords.
2. Search multiple times from different angles.
3. Combine style, typography, color, and UX searches.
4. Always check accessibility and motion guidance.
5. Use stack-specific searches before implementation.
6. Iterate until the design system feels coherent.

## Common Rules for Professional UI

### Icons and Visual Elements

| Rule | Do | Don't |
|------|----|-------|
| No emoji icons | Use SVG icon sets | Use emoji as UI icons |
| Stable hover states | Use color or opacity transitions | Use transforms that shift layout |
| Correct brand logos | Verify official SVGs | Guess logo paths |
| Consistent icon sizing | Keep a fixed viewBox | Mix random icon sizes |

### Interaction and Cursor

| Rule | Do | Don't |
|------|----|-------|
| Cursor pointer | Add `cursor-pointer` to clickable cards | Leave default cursor |
| Hover feedback | Provide visual feedback | Give no interactive signal |
| Smooth transitions | Keep transitions around 150-300ms | Make transitions instant or very slow |

### Light and Dark Contrast

| Rule | Do | Don't |
|------|----|-------|
| Glass card light mode | Use `bg-white/80` or similar | Use very low opacity white |
| Text contrast light | Use dark text for body copy | Use washed-out gray body text |
| Muted text light | Keep sufficient contrast | Use text that is too faint |
| Border visibility | Use visible borders in light mode | Use near-invisible borders |

### Layout and Spacing

| Rule | Do | Don't |
|------|----|-------|
| Floating navbar | Add edge spacing | Stick everything to `top-0` |
| Content padding | Account for fixed navbar height | Hide content behind fixed elements |
| Consistent max-width | Reuse the same container widths | Mix widths randomly |

## Pre-Delivery Checklist

### Visual Quality

- [ ] No emoji icons
- [ ] Icons come from a consistent icon set
- [ ] Brand logos are correct
- [ ] Hover states do not cause layout shift
- [ ] Theme colors are applied consistently

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear feedback
- [ ] Transitions are smooth
- [ ] Focus states are visible

### Light and Dark Mode

- [ ] Text contrast is sufficient
- [ ] Glass elements stay visible
- [ ] Borders are visible in both modes
- [ ] Both modes were tested

### Layout

- [ ] Floating elements have proper spacing
- [ ] No content is hidden behind fixed nav
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility

- [ ] Images have alt text
- [ ] Inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` is respected


## OUTPUT FORMAT

- Return:
  - `Scope`
  - `Evidence`
  - `Findings`
  - `Artifacts`
  - `Next Actions`
- Name any generated files by exact path so the next reviewer does not have to rediscover them.

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
Use when you need a stable starting point before deeper ui-ux-pro-max review.
```bash
# Create the output directory for this skill
mkdir -p ui-ux-pro-max-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > ui-ux-pro-max-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > ui-ux-pro-max-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 ui-ux-pro-max-output/artifact-manifest.txt | xargs -r sha256sum > ui-ux-pro-max-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > ui-ux-pro-max-output/review-start-utc.txt
date > ui-ux-pro-max-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > ui-ux-pro-max-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' ui-ux-pro-max-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 ui-ux-pro-max-output/signal-hits.txt | sort | uniq -c | sort -nr > ui-ux-pro-max-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > ui-ux-pro-max-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > ui-ux-pro-max-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' ui-ux-pro-max-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > ui-ux-pro-max-output/git-status.txt 2>/dev/null || true
git diff --stat > ui-ux-pro-max-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > ui-ux-pro-max-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > ui-ux-pro-max-output/ui-ux-pro-max-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > ui-ux-pro-max-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' ui-ux-pro-max-output/ui-ux-pro-max-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find ui-ux-pro-max-output -maxdepth 2 -type f | sort > ui-ux-pro-max-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf ui-ux-pro-max-output/ui-ux-pro-max-bundle.tgz ui-ux-pro-max-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf ui-ux-pro-max-output/ui-ux-pro-max-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 ui-ux-pro-max-output/signal-hits.txt | sort | uniq -c | sort -nr > ui-ux-pro-max-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' ui-ux-pro-max-output/review-queue.txt > ui-ux-pro-max-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' ui-ux-pro-max-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > ui-ux-pro-max-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> ui-ux-pro-max-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' ui-ux-pro-max-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > ui-ux-pro-max-output/ui-ux-pro-max-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > ui-ux-pro-max-output/ui-ux-pro-max-final.md
# Preview the output files for QA
sed -n '1,20p' ui-ux-pro-max-output/ui-ux-pro-max-final.md
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
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > ui-ux-pro-max-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 ui-ux-pro-max-output/ui-ux-pro-max-bundle.tgz > ui-ux-pro-max-output/ui-ux-pro-max-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > ui-ux-pro-max-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' ui-ux-pro-max-output/review-queue.txt > ui-ux-pro-max-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > ui-ux-pro-max-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find ui-ux-pro-max-output -maxdepth 2 -type f | sort > ui-ux-pro-max-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > ui-ux-pro-max-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' ui-ux-pro-max-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > ui-ux-pro-max-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > ui-ux-pro-max-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > ui-ux-pro-max-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > ui-ux-pro-max-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > ui-ux-pro-max-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `ui-ux-pro-max-output/ui-ux-pro-max-report.md`
- produce: `ui-ux-pro-max-output/output-manifest.txt`
- produce: `ui-ux-pro-max-output/ui-ux-pro-max-bundle.tgz`
- produce: `ui-ux-pro-max-output/ui-ux-pro-max-findings.csv`

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

- Confirm `ui-ux-pro-max-output` contains the report, manifest, and at least one evidence artifact.
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
