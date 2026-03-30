---
name: deploy
description: Deployment command for production releases. Pre-flight checks and deployment execution.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Deploy

This skill adapts the Antigravity `/deploy` workflow for Codex.
Treat the user's message as the deployment target or deployment mode.

## Purpose

This skill handles deployment with pre-flight checks, execution, and verification.

## Sub-commands

```text
$deploy            - Interactive deployment flow
$deploy check      - Run pre-deployment checks only
$deploy preview    - Deploy to preview/staging
$deploy production - Deploy to production
$deploy rollback   - Roll back to previous version
```

## Pre-Deployment Checklist

Before any deployment:

```markdown
## Pre-Deploy Checklist

### Code Quality
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] ESLint passing (`npx eslint .`)
- [ ] All tests passing (`npm test`)

### Security
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Dependencies audited (`npm audit`)

### Performance
- [ ] Bundle size acceptable
- [ ] No console.log statements
- [ ] Images optimized

### Documentation
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs current

### Ready to deploy? (y/n)
```

## Deployment Flow

```text
[deploy]
   |
   v
[pre-flight checks]
   |
pass? ---- no ---> fix issues
   |
  yes
   |
   v
[build]
   |
   v
[deploy to platform]
   |
   v
[health check]
   |
   v
[complete]
```

## Output Format

### Successful Deploy

```markdown
## Deployment Complete

### Summary
- **Version:** v1.2.3
- **Environment:** production
- **Duration:** 47 seconds
- **Platform:** Vercel

### URLs
- Production: https://app.example.com
- Dashboard: https://vercel.com/project

### What Changed
- Added user profile feature
- Fixed login bug
- Updated dependencies

### Health Check
- API responding (200 OK)
- Database connected
- All services healthy
```

### Failed Deploy

```markdown
## Deployment Failed

### Error
Build failed at step: TypeScript compilation

### Details
error TS2345: Argument of type 'string' is not assignable...

### Resolution
1. Fix TypeScript error in `src/services/user.ts:45`
2. Run `npm run build` locally to verify
3. Try `$deploy` again

### Rollback Available
Previous version (v1.2.2) is still active.
Run `$deploy rollback` if needed.
```

## Platform Support

| Platform | Command | Notes |
|----------|---------|-------|
| Vercel | `vercel --prod` | Auto-detected for Next.js |
| Railway | `railway up` | Needs Railway CLI |
| Fly.io | `fly deploy` | Needs flyctl |
| Docker | `docker compose up -d` | For self-hosted |

## Examples

```text
$deploy
$deploy check
$deploy preview
$deploy production --skip-tests
$deploy rollback
```
