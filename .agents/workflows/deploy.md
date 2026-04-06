---
description: Run the deployment workflow with pre-flight checks, release steps, and verification.
---

# $deploy

$ARGUMENTS

Use this workflow for release readiness checks, preview deploys, production deployment planning,
verification, and rollback preparation.

## Purpose

`$deploy` exists to reduce release mistakes. It makes Codex slow down and verify readiness before
describing or executing deployment steps.

## What This Workflow Does

1. Reviews deployment readiness.
2. Checks build, test, and environment assumptions.
3. Identifies the relevant release path for the project.
4. Produces a verification and rollback-aware deploy summary.

## Use When

- The user wants to deploy or prepare for deployment.
- A release check is needed before shipping.
- A staging or preview release should be validated.
- The team needs a rollback-aware release plan.

## Do Not Use When

- The task is just local preview.
- The request is mainly feature work or debugging.

## Repo-Local Verification Commands

```bash
python3 .agents/scripts/checklist.py .
bash .agents/scripts/run.sh
python3 .agents/scripts/verify_all.py . --url http://localhost:3000 --no-e2e
```

## Pre-Flight Checklist

Before any deploy-oriented answer, verify or ask about:

- build status
- test status
- environment variables
- migration needs
- preview or staging health
- rollback path

## Recommended Flow

### Phase 1: Identify the Release Context

- preview / staging / production
- platform or hosting target
- whether the request is planning only or execution support

### Phase 2: Review Readiness

Check or confirm:

- build passes
- critical tests pass
- secrets are not hardcoded
- required environment config exists
- known risks are surfaced

### Phase 3: Describe the Release Path

Summarize:

- what should be deployed
- what sequence should be followed
- what should be checked immediately after

### Phase 4: Confirm Verification and Rollback

Always include:

- how success will be confirmed
- what rollback or mitigation exists if the deploy fails

## Suggested Output

```md
## Deploy Summary

### Environment
- ...

### Pre-Flight Result
- ...

### Release Steps
- ...

### Verification
- ...

### Rollback Notes
- ...
```

## Example Invocations

```text
$deploy check production readiness
$deploy preview release for staging
$deploy production release for the current app
$deploy rollback plan after a failed release
```

## Final Rule

Never treat deployment as complete until post-release verification is explicitly addressed.
