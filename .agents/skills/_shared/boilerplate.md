# Skill Boilerplate

Use this template when creating a new skill.

```md
---
skill: example-skill
name: example-skill
version: 1.0.0
source: h4cker/example-folder
last_updated: 2026-04-06
reviewed_by: Codex
next_review: 2026-07-05
load_priority: 3
depends_on: [methodology]
os_support: [kali, ubuntu, parrot, windows, macos]
python_min: 3.8
description: One-sentence summary of what the skill does.
allowed-tools: Read, Glob, Grep, Bash
---

# SKILL: Example Skill

## WHEN TO USE THIS SKILL

- Use when ...
- Use when ...
- Use when ...

## KEY TECHNIQUES & TOOLS

### Phase 1: Scope

```bash
mkdir -p example-output
```

### Decision rules

- If ...
- If ...
- If ...

## OUTPUT FORMAT

- Produce these sections:
  - `Scope`
  - `Evidence`
  - `Findings`
  - `Recommended Next Actions`
```
