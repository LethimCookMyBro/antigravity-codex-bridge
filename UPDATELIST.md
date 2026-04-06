# Update List

Last updated: 2026-04-06

This file is a simple running log of what has been added, changed, fixed, or prepared in this repository.
Use it as a human-friendly update journal alongside commit history.

## Current Snapshot

- Package: `@lizmotia/ag-kit`
- CLI: `ag-kit` and compatibility alias `ag-codex`
- Agents: `20`
- Skills: `96` top-level / `106` total `SKILL.md` files
- Workflows: `11`
- Scripts: `17`

## 2026-04-06

### Package and Install Flow

- Packaged the project as an installable npm bundle under `@lizmotia/ag-kit`
- Added CLI support for:
  - `ag-kit init`
  - `ag-kit update`
  - `ag-kit status`
  - `ag-kit help`
- Added overwrite support with `npx @lizmotia/ag-kit init --force`
- Clarified that `npx @lizmotia/ag-kit update` is the preferred refresh flow for existing projects

### Codex Runtime Structure

- Standardized the portable `.agents` layout for Codex
- Kept project-local skills, workflows, agents, scripts, and shared resources inside `.agents/`
- Verified that required h4cker-derived folders exist and are represented in the skill system

### Skills and Workflows

- Added and normalized project-local workflows under `.agents/workflows/`
- Added and expanded the project skill library to `106` total `SKILL.md` files
- Added defensive/security-focused skills derived from the local h4cker source material
- Added helper/shared docs under `.agents/skills/_shared/`
- Added bilingual catalog files:
  - `SKILLS_AND_WORKFLOWS.md`
  - `SKILLS_AND_WORKFLOWS_TH.md`

### Validation and Automation

- Added script inventory and validation helpers in `.agents/scripts/`
- Added:
  - `validate-skills.py`
  - `check-stale.py`
  - `health-check.sh`
  - `setup.sh`
  - `run.sh`
  - `load-order.md`
  - security helper scripts for logs, DNS, TLS, packet capture, and probes
- Verified script syntax and no-arg/help behavior
- Verified skill validation and stale checks

### Documentation

- Refreshed root documentation to match the current package state
- Updated:
  - `README.md`
  - `README(th).md`
  - `AGENT_FLOW.md`
  - `PUBLISHING.md`
- Added this file as a simple update journal for future changes

### Publishing and Repo Hygiene

- Added MIT licensing for open-source reuse
- Updated ignore rules for local-only folders and scratch content
- Kept local source/reference material out of the publish scope where appropriate
- Verified package contents with npm dry-run before publish-oriented cleanup

## Suggested Format For Future Updates

Copy this block for the next entry:

```md
## YYYY-MM-DD

### Added

- ...

### Changed

- ...

### Fixed

- ...

### Notes

- ...
```

## Notes

- Use this file for high-level human-readable updates.
- Use Git commits for precise file-level history.
- If a change affects install flow, package scope, or skill counts, update this file and the README files together.
