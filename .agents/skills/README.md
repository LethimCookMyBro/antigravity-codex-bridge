# Skills System README

Last updated: 2026-04-06

This directory is the repo-local Codex skill system for this project. It contains:

- `SKILL.md` files per skill folder
- shared references under [`_shared`](./_shared)
- helper scripts under [`../scripts`](../scripts)
- production validation and load-order documentation

## Directory Layout

- `SKILL.md`: the primary instruction file that Codex loads
- `agents/openai.yaml`: optional metadata for discovery
- `_shared/common-commands.md`: deduplicated low-risk command patterns
- `_shared/boilerplate.md`: standard sections for new skills
- `_shared/output-templates.md`: reusable output/report templates

## Add A New Skill

Checklist:

1. Create a folder under `.agents/skills/<skill-name>/`
2. Add `SKILL.md` with metadata header:
   - `skill`
   - `version`
   - `source`
   - `last_updated`
   - `reviewed_by`
   - `next_review`
   - `load_priority`
   - `depends_on`
   - `os_support`
3. Include:
   - `## WHEN TO USE THIS SKILL`
   - `## KEY TECHNIQUES & TOOLS`
   - `## OUTPUT FORMAT`
4. Prefer shared references instead of duplicating common command blocks
5. If the skill uses repo-local helpers, reference `.agents/scripts/...`
6. Run validation:

```bash
python3 .agents/scripts/validate-skills.py --skills-dir .agents/skills
python3 .agents/scripts/check-stale.py --skills-dir .agents/skills
bash .agents/scripts/health-check.sh
```

## Validation Workflow

Use this sequence before commit or deploy:

```bash
python3 .agents/scripts/validate-skills.py --skills-dir .agents/skills
python3 .agents/scripts/check-stale.py --skills-dir .agents/skills
bash .agents/scripts/health-check.sh
bash .agents/scripts/run.sh
```

## Skill Chain Diagram

```text
methodology
├── recon
│   ├── osint
│   ├── osint-recon
│   └── web-application-testing
│       └── exploit-development
│           └── post-exploitation
├── dfir
│   ├── threat-hunting
│   └── threat-intelligence
├── capture-the-flag
│   ├── cracking-passwords
│   └── reverse-engineering
└── devsecops
    ├── sbom
    └── docker-and-k8s-security
```

## Troubleshooting

- `validate-skills.py` reports missing metadata:
  Add the required header fields and rerun validation.
- `check-stale.py` reports overdue reviews:
  Update `last_updated` and `next_review` after reviewing the skill.
- `health-check.sh` fails on a script:
  Fix the shebang, syntax, or `--help` behavior before shipping.
- Shared reference is broken:
  Confirm the target file and anchor exist.
- A skill is too generic:
  Move repeated blocks into `_shared` and tighten the skill output contract.

## Production Notes

- The canonical skill root for this repo is `.agents/skills`
- Open the repo root in VS Code, switch to the `CODEX` tab, reload skills, then invoke them with `$`
- Some user instructions refer to `/mnt/skills/user/`; in this workspace that path is not available, so validation is run against `.agents/skills`
