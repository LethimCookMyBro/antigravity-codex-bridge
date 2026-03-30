---
name: brainstorm
description: Structured brainstorming for projects and features. Explores multiple options before implementation.
allowed-tools: Read, Glob, Grep
---

# Brainstorm

This skill adapts the Antigravity `/brainstorm` workflow for Codex.
Treat the user's message as the brainstorm topic.

## Purpose

This skill activates BRAINSTORM mode for structured idea exploration.
Use it when you need to explore options before committing to implementation.

## Behavior

When `$brainstorm` is triggered:

1. **Understand the goal**
   - What problem are we solving?
   - Who is the user?
   - What constraints exist?

2. **Generate options**
   - Provide at least 3 different approaches
   - Each with pros and cons
   - Consider unconventional solutions

3. **Compare and recommend**
   - Summarize tradeoffs
   - Give a recommendation with reasoning

## Output Format

```markdown
## Brainstorm: [Topic]

### Context
[Brief problem statement]

---

### Option A: [Name]
[Description]

Pros:
- [benefit 1]
- [benefit 2]

Cons:
- [drawback 1]

Effort: Low | Medium | High

---

### Option B: [Name]
[Description]

Pros:
- [benefit 1]

Cons:
- [drawback 1]
- [drawback 2]

Effort: Low | Medium | High

---

### Option C: [Name]
[Description]

Pros:
- [benefit 1]

Cons:
- [drawback 1]

Effort: Low | Medium | High

---

## Recommendation

**Option [X]** because [reasoning].

What direction would you like to explore?
```

## Examples

```text
$brainstorm authentication system
$brainstorm state management for complex form
$brainstorm database schema for social app
$brainstorm caching strategy
```

## Key Principles

- No code. This is about ideas, not implementation.
- Use diagrams when architecture would be clearer visually.
- Be honest about tradeoffs and complexity.
- Present options clearly, then let the user decide.
