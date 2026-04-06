---
skill: ai-research
name: ai-research
version: 1.0.0
source: h4cker/ai-research
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 5
depends_on: []
os_support: [kali, ubuntu, parrot]
python_min: 3.8
description: Review AI-system security posture across prompts, RAG, connectors, models, and governance with safe research outputs.
allowed-tools: Read, Glob, Grep, Bash
---
# SKILL: AI Security Research

Summary: Review AI-system security posture across prompts, RAG, connectors, models, and governance with safe research outputs.
Does NOT cover unapproved live-target actions, unauthorized access, or unverified assumptions.

## WHEN TO USE THIS SKILL

- Use when the target system includes LLMs, RAG, assistants, agents, or MCP-style connectors
- Use when the user asks for AI security review, prompt injection risk, data exposure, or model misuse analysis
- Use when Codex should map the system and recommend defensive tests or controls

## INPUT FROM

- architecture notes
- prompt files
- connector or tool configuration
- RAG or retrieval pipeline details

## KEY TECHNIQUES & TOOLS

### Phase 1: Map the AI surface

```bash
mkdir -p ai-research-output
rg -n "openai|anthropic|llm|prompt|rag|vector|embedding|tool|mcp" . > ai-research-output/ai-surface-hits.txt || true
find . -maxdepth 4 \\( -name '*.prompt' -o -name '*.md' -o -name '*.yaml' -o -name '*.json' \\) | sort > ai-research-output/ai-surface-files.txt
sed -n '1,80p' ai-research-output/ai-surface-hits.txt
```

### Phase 2: Classify risk areas

- Review:
  - prompt injection exposure
  - connector/tool overreach
  - retrieval leakage
  - model selection and logging
  - secrets in prompts or configs

```bash
find . -maxdepth 5 \\( -iname '*prompt*' -o -iname '*rag*' -o -iname '*vector*' -o -iname '*mcp*' \\) | sort > ai-research-output/ai-risk-files.txt
python3 - <<'PY'
from pathlib import Path
hits = []
for path in Path('.').rglob('*'):
    if path.is_file() and path.suffix in {'.py', '.ts', '.js', '.md', '.json', '.yaml', '.yml'}:
        text = path.read_text(encoding='utf-8', errors='replace')
        if any(k in text.lower() for k in ['prompt', 'embedding', 'rag', 'tool', 'mcp']):
            hits.append(str(path))
Path('ai-research-output/discovered-ai-files.txt').write_text('\\n'.join(hits[:50]), encoding='utf-8')
PY
sed -n '1,80p' ai-research-output/discovered-ai-files.txt
```

### Phase 3: Turn the surface map into reviewable security questions

```bash
printf '%s\n' "surface,question,priority" > ai-research-output/review-questions.csv
printf '%s\n' "RAG,Can retrieved content override system intent?,high" >> ai-research-output/review-questions.csv
printf '%s\n' "Tools,Can a model-triggered tool mutate state without approval?,high" >> ai-research-output/review-questions.csv
cat ai-research-output/review-questions.csv
```

### Decision rules

- If the system uses external retrieval, inspect source trust and citation boundaries before model behavior claims
- If tools can mutate systems, flag least-privilege and approval boundaries
- If the repo has no AI surface, return that result explicitly instead of forcing findings
- If the review touches prompts only, do not claim model-training or weight-level risk without evidence
- If the system sends user data to third-party APIs, record logging, retention, and redaction questions explicitly

## Fallbacks

- If no AI-related files or dependencies are found, return `No AI surface detected` with the exact files searched
- If the repo mixes AI and non-AI systems, scope the review to the folders that actually contain prompts, tools, models, or retrieval logic
- If architecture context is missing, mark findings as provisional and ask for the missing deployment or data-flow detail

## OUTPUT FORMAT

- Produce:
  - `AI Surface Map`
  - `Risk Areas`
  - `Evidence`
  - `Recommended Controls`
  - `Suggested Next Skill`

- `Artifacts` should list:
  - `ai-research-output/ai-surface-hits.txt`
  - `ai-research-output/ai-surface-files.txt`
  - `ai-research-output/ai-risk-files.txt`
  - `ai-research-output/discovered-ai-files.txt`
  - `ai-research-output/review-questions.csv`

## Quick Mode (< 5 minutes)

- Search for AI surface indicators first.
- Limit the first pass to one app, one assistant, or one connector boundary.
- Stop once you know whether the main risk is prompt, retrieval, tool, or governance related.


## Troubleshooting / Fallback

- If the primary tool is missing, use the repo-local helper script or the simplest shell fallback already shown in the skill.
- If the repo contains many false-positive matches, scope to folders that actually call model APIs or store prompts.
- If retrieval content is external, record the trust boundary before reviewing prompts in isolation.
- Edge case 1: the assistant is configuration-driven and the prompt lives in a database or admin UI; note the missing source.
- Edge case 2: the system mixes classic search and RAG; keep those data paths separate in the report.


## Phase Output Map

- Phase 1 output: AI-surface hit list and file inventory.
- Phase 2 output: risk-relevant files and evidence snippets.
- Phase 3 output: review questions and priority map for the next assessor.


## Done When

- Scope is fixed to one AI-enabled app, assistant, or pipeline.
- The review identifies at least one concrete surface: prompt, retrieval, tool, model config, or logging path.
- A junior reviewer can say what to inspect next without rereading the whole repo.

## Technique Depth

### Technique 1: Artifact manifest and scope note
Use when you need a stable starting point before deeper ai-research review.
```bash
# Create the output directory for this skill
mkdir -p ai-research-output
# Save a full file manifest for the current workspace
find . -maxdepth 5 -type f | sort > ai-research-output/artifact-manifest.txt
# Start a short scope note so the reviewer records boundaries first
printf '%s
' 'scope:' 'assumptions:' 'owner:' > ai-research-output/scope-note.txt
```
- The artifact manifest is the baseline for every later finding.
- The scope note prevents the reviewer from silently widening the task.

### Technique 2: Hash and timestamp the first review set
Use when another reviewer may need to confirm they inspected the same files.
```bash
# Hash the first review set so the handoff can be reproduced
head -30 ai-research-output/artifact-manifest.txt | xargs -r sha256sum > ai-research-output/artifact-hashes.txt
# Save UTC and local timestamps for the review start
date -u > ai-research-output/review-start-utc.txt
date > ai-research-output/review-start-local.txt
```
- Hashes and timestamps make the first evidence slice reproducible.
- Keep UTC and local time together when the team works across time zones.

### Technique 3: Keyword-based signal hunt
Use when you need the first evidence slice without opening every file manually.
```bash
# Search for high-signal words in the current workspace
rg -n "error|warn|failed|denied|timeout|exception|secret|token|config" . > ai-research-output/signal-hits.txt 2>/dev/null || true
# Preview the first hits so the next step is explicit
sed -n '1,80p' ai-research-output/signal-hits.txt
# Count which files produced the most hits
cut -d: -f1 ai-research-output/signal-hits.txt | sort | uniq -c | sort -nr > ai-research-output/signal-hit-counts.txt 2>/dev/null || true
```
- This narrows the first review path quickly.
- The hit-count summary is often more useful than raw matches alone.

### Technique 4: Directory map and extension inventory
Use when the workspace layout is unfamiliar or inconsistent.
```bash
# Capture a short directory map
find . -maxdepth 3 -type d | sort > ai-research-output/directory-map.txt
# Capture a file-extension summary for the current tree
find . -maxdepth 5 -type f | sed 's|^.*/||' | awk -F. 'NF>1 {print $NF}' | sort | uniq -c | sort -nr > ai-research-output/extension-summary.txt
# Review the top entries before opening files by hand
sed -n '1,40p' ai-research-output/extension-summary.txt
```
- The directory map tells a junior reviewer where to look first.
- Extension counts reveal whether the scope is mostly code, docs, logs, or artifacts.

### Technique 5: Git and workspace delta review
Use when code drift may explain the current state.
```bash
# Save git status and diff stats if the workspace is a repo
git status --short > ai-research-output/git-status.txt 2>/dev/null || true
git diff --stat > ai-research-output/git-diff-stat.txt 2>/dev/null || true
git log --oneline -n 20 > ai-research-output/git-log.txt 2>/dev/null || true
```
- A short git history often explains why a review target changed.
- Keep repo state beside findings so later reviewers see the same context.

### Technique 6: Structured notes and report starter
Use when you want report writing to begin from saved artifacts rather than memory.
```bash
# Create a report starter with the required sections
printf '%s
' '# Summary' '## Scope' '## Evidence' '## Findings' '## Next Actions' > ai-research-output/ai-research-report-starter.md
# Save a structured note file for reviewer observations
printf '%s
' 'observation:' 'confidence:' 'artifact:' 'next_step:' > ai-research-output/review-notes.txt
# Preview the report starter
sed -n '1,40p' ai-research-output/ai-research-report-starter.md
```
- Report drafting should start only after artifacts exist.
- Structured notes make the handoff cleaner and easier to verify.

### Technique 7: Output manifest and bundle preview
Use when another person will need the complete artifact set.
```bash
# Save an output manifest for everything produced by this skill
find ai-research-output -maxdepth 2 -type f | sort > ai-research-output/output-manifest.txt
# Build a compressed handoff bundle
tar -czf ai-research-output/ai-research-bundle.tgz ai-research-output 2>/dev/null || true
# Preview bundle contents for a quick QA pass
tar -tzf ai-research-output/ai-research-bundle.tgz | head -80 2>/dev/null || true
```
- The manifest becomes the handoff map for the next skill.
- The bundle makes the review portable without copying terminal history.

### Technique 8: Artifact ranking and review queue
Use when there are too many candidate files for a single pass.
```bash
# Count which files appear most often in the signal set
cut -d: -f1 ai-research-output/signal-hits.txt | sort | uniq -c | sort -nr > ai-research-output/review-queue.txt 2>/dev/null || true
# Save the top ranked entries for the next pass
sed -n '1,30p' ai-research-output/review-queue.txt > ai-research-output/review-queue-top.txt 2>/dev/null || true
# Preview the ranked queue
sed -n '1,30p' ai-research-output/review-queue-top.txt
```
- A ranked queue prevents random file selection.
- It also keeps the next step explicit for junior reviewers.

### Technique 9: Readable-file fallback inventory
Use when permissions or tool availability limit the happy path.
```bash
# Save only the readable files in the current tree
find . -maxdepth 4 -type f -readable | sort > ai-research-output/readable-files.txt
# Capture unreadable-path errors separately when possible
find . -maxdepth 4 -type f 2> ai-research-output/find-errors.txt >/dev/null || true
# Review the first readable entries
sed -n '1,50p' ai-research-output/readable-files.txt
```
- This keeps the workflow moving even with partial permissions.
- Save permission limits explicitly instead of treating them as absence of data.

### Technique 10: Finding sheet and final skeleton
Use when the skill is ready to hand off to reporting or a narrower review.
```bash
# Create a CSV finding sheet with stable columns
printf '%s
' 'item,severity,detail,artifact,next_step' > ai-research-output/ai-research-findings.csv
# Create a final markdown skeleton with explicit handoff
printf '%s
' '# Summary' '## Findings' '## Commands Used' '## Artifacts Produced' '## Next Steps' > ai-research-output/ai-research-final.md
# Preview the output files for QA
sed -n '1,20p' ai-research-output/ai-research-final.md
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
- If the current skill reveals a narrower follow-on task → save artifacts first, then load `architecture`.
- If filenames are generic or ambiguous → rename them with the skill prefix before moving on.
- If the reviewer cannot explain why a command was run → remove it from the narrative and keep only artifact-backed steps.
- If the report can be written from existing artifacts → stop collecting more data and finish the report.

## Fallback Techniques

### ถ้า `rg` is missing:
```bash
# Alternative: preserve evidence with the least risky available path
grep -RIn "error\|warn\|failed\|denied\|timeout\|exception\|secret\|token\|config" . > ai-research-output/signal-hits-grep.txt 2>/dev/null || true
```

### ถ้า `sha256sum` is missing:
```bash
# Alternative: use a portable SHA-256 command when available
shasum -a 256 ai-research-output/ai-research-bundle.tgz > ai-research-output/ai-research-bundle.shasum 2>/dev/null || true
```

### ถ้า `git` metadata is unavailable:
```bash
# Alternative: keep a plain file and directory snapshot instead of repo history
find . -maxdepth 4 -type f | sort > ai-research-output/workspace-files.txt
```

### ถ้า logs or source trees are too large:
```bash
# Alternative: review only the first ranked evidence slice
sed -n '1,100p' ai-research-output/review-queue.txt > ai-research-output/review-queue-slice.txt 2>/dev/null || true
```

### ถ้า permission is limited:
```bash
# Alternative: preserve the readable subset and note the boundary explicitly
find . -maxdepth 3 -type f -readable | sort > ai-research-output/permission-limited-files.txt
```

## Quick Mode (< 5 นาที) — Expanded

- Use this when you have less than five minutes, need the first artifact fast, or only need enough evidence to pick the next skill.
- Keep scope to one app, one host, one artifact set, or one lab segment.
- Stop after one inventory artifact, one evidence artifact, and one explicit next action are saved.

```bash
# Minimal quick-pass artifact list
find ai-research-output -maxdepth 2 -type f | sort > ai-research-output/quick-artifacts.txt 2>/dev/null || true
# Minimal quick-pass timestamp
date -u > ai-research-output/quick-timestamp.txt
# Minimal quick-pass preview
sed -n '1,40p' ai-research-output/quick-artifacts.txt 2>/dev/null || true
```

## Edge Cases

### Edge Case: Read-only evidence set
สถานการณ์: the workspace can be inspected but cannot be modified or bundled freely.
วิธีจัดการ:
```bash
find . -maxdepth 3 -type f -readable | sort > ai-research-output/readonly-files.txt
```

### Edge Case: Very large workspace
สถานการณ์: the repo or evidence set is too large for a first-pass full review.
วิธีจัดการ:
```bash
rg --files . | head -500 > ai-research-output/first-500-files.txt
```

### Edge Case: Non-standard directory layout
สถานการณ์: important files are nested deeper than expected or split across unusual paths.
วิธีจัดการ:
```bash
find . -maxdepth 6 -type d | sort > ai-research-output/deep-directory-map.txt
```

### Edge Case: Missing git metadata
สถานการณ์: the workspace is a bundle, export, or copied evidence set instead of a live repo.
วิธีจัดการ:
```bash
find . -maxdepth 5 -type f | sort > ai-research-output/ungitted-manifest.txt
```

### Edge Case: Mixed time zones
สถานการณ์: logs, notes, or findings were collected across different systems and time zones.
วิธีจัดการ:
```bash
date -u > ai-research-output/current-utc.txt
```

## Tool Comparison

| tool | ข้อดี | ข้อเสีย | ใช้เมื่อ |
|---|---|---|---|
| rg | Fast recursive search with line numbers | May not be installed everywhere | First-pass keyword triage |
| grep -R | Universal fallback on most systems | Noisy on large trees | Fallback recursive search |
| find | Precise inventory and manifest generation | Needs more piping for summaries | Artifact mapping and file counts |

## Output Templates

- produce: `ai-research-output/ai-research-report.md`
- produce: `ai-research-output/output-manifest.txt`
- produce: `ai-research-output/ai-research-bundle.tgz`
- produce: `ai-research-output/ai-research-findings.csv`

structure:
```markdown
# Summary
## Scope
## Findings
| item | severity | detail | artifact |
|---|---|---|---|
## Commands Used
## Artifacts Produced
## Next Steps → load `architecture`
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

- Confirm `ai-research-output` contains the report, manifest, and at least one evidence artifact.
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
- What exact question should the next skill `architecture` answer?

## Handoff Data to Preserve

- Review start time in UTC.
- Output manifest path.
- Bundle hash path.
- Scope note path.
- First inventory file path.
- First high-signal evidence file path.
- Fallback artifact path if the happy path failed.
- The exact next skill name: `architecture`.

## Scope Traps

- Do not widen from one artifact set to a whole environment without writing the reason.
- Do not merge findings from different apps, hosts, or lab segments into one unlabeled statement.
- Do not treat guessed ownership as confirmed scope.
- Do not assume a path is production just because it looks important.
- Do not claim absence of evidence until the inventory step is complete.
- Do not discard contradictory artifacts; preserve and explain them.
- Do not skip naming the next skill or next owner.
- Do not finish until the bundle and manifest are readable by the next reviewer.


## Next: load `architecture` skill

- Load `architecture` next if the AI surface map needs a clearer trust-boundary or component diagram review.
