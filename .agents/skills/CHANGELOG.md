# Changelog

## [2026-04-06]

### Created

- Added production docs:
  - `README.md`
  - `_shared/boilerplate.md`
  - `_shared/output-templates.md`
- Added production helper docs and scripts:
  - `../scripts/validate-skills.py`
  - `../scripts/check-stale.py`
  - `../scripts/setup.sh`
  - `../scripts/run.sh`
  - `../scripts/load-order.md`
- Added missing top-level skills:
  - `devsecops`
  - `networking`
  - `windows`
  - `sbom`
  - `docker-and-k8s-security`
  - `threat-intelligence`
  - `adversarial-emulation`
  - `buffer-overflow-examples`
  - `bug-bounties`
  - `car-hacking`
  - `cheat-sheets`
  - `darkweb-research`
  - `foundational-cybersecurity-concepts`
  - `fuzzing-resources`
  - `game-hacking`
  - `honeypots-honeynets`
  - `metasploit-resources`
  - `mobile-security`
  - `pen-testing-reports`
  - `programming-and-scripting-for-cybersecurity`
  - `python-ruby-and-bash`
  - `vulnerable-servers`
  - `wireless-resources`

### Modified

- Standardized metadata headers across all `SKILL.md` files:
  - added `skill`
  - added `version`
  - added `source`
  - added `last_updated`
  - added `reviewed_by`
  - added `next_review`
  - added `load_priority`
  - added `depends_on`
  - added `os_support`
  - added `python_min` when applicable
- Added `## WHEN TO USE THIS SKILL` to skills that were missing an explicit trigger section
- Preserved existing Codex frontmatter fields like `name`, `description`, and `allowed-tools`
- Continued using `_shared/common-commands.md` for deduplicated command references

### Validation

- Confirmed all non-shared top-level h4cker folders now have `SKILL.md`
- Confirmed metadata headers are present on all current `SKILL.md` files
- Confirmed repo-local script health checks still pass after the production prep pass
