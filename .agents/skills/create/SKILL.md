---
name: create
description: Create new application command. Triggers App Builder skill and starts interactive dialogue with user.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Create

This skill adapts the Antigravity `/create` workflow for Codex.
Treat the user's message as the application request.

## Task

This skill starts a new application creation process.

### Steps

1. **Request analysis**
   - Understand what the user wants
   - If key information is missing, ask targeted questions before building

2. **Project planning**
   - Use the `app-builder` skill and supporting specialists as needed
   - Determine the tech stack
   - Plan file structure
   - Create a plan before building

3. **Application building**
   - Coordinate the relevant expert skills and agents
   - Typical domains:
     - `database-architect` for schema
     - `backend-specialist` for API
     - `frontend-specialist` for UI

4. **Preview**
   - Start preview tooling when complete
   - Present the preview URL to the user

## Usage Examples

```text
$create blog site
$create e-commerce app with product listing and cart
$create todo app
$create Instagram clone
$create crm system with customer management
```

## Before Starting

If the request is unclear, ask these questions:

- What type of application is it?
- What are the basic features?
- Who will use it?

Use sensible defaults when possible, then refine details later.
