---
name: enhance
description: Add or update features in existing application. Used for iterative development.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Enhance

This skill adapts the Antigravity `/enhance` workflow for Codex.
Treat the user's message as the requested update to an existing project.

## Task

This skill adds features or makes updates to an existing application.

### Steps

1. **Understand current state**
   - Load current project context
   - Understand existing features and tech stack

2. **Plan changes**
   - Determine what will be added or changed
   - Detect affected files
   - Check dependencies

3. **Present plan to user for major changes**
   - Estimate the scope
   - Explain what files or areas will change
   - Ask for approval before large updates

4. **Apply**
   - Call relevant agents or skills
   - Make the changes
   - Test the result

5. **Update preview**
   - Hot reload or restart when relevant

## Usage Examples

```text
$enhance add dark mode
$enhance build admin panel
$enhance integrate payment system
$enhance add search feature
$enhance edit profile page
$enhance make responsive
```

## Caution

- Get approval for major changes.
- Warn on conflicting requests, such as introducing Firebase into a PostgreSQL project.
- Keep changes scoped and verified before moving on.
