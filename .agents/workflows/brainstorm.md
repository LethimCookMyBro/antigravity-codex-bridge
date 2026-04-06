---
description: Structured brainstorming before implementation so the team explores options first.
---

# $brainstorm

$ARGUMENTS

Use this workflow when the user wants structured idea exploration before committing to implementation.

## Purpose

`$brainstorm` exists to slow down just enough to avoid prematurely locking into a weak solution.
It is the right workflow when the team needs options, tradeoffs, constraints, and a recommendation,
not code.

## What This Workflow Does

1. Clarifies the actual problem and desired outcome.
2. Identifies constraints such as stack, timeline, team size, UX goals, or security requirements.
3. Produces multiple viable approaches.
4. Compares the approaches honestly.
5. Recommends one path and explains why.

## Use When

- The task is still ambiguous.
- The user asks to compare options.
- Multiple architectures or product directions are possible.
- The team needs alignment before implementation.
- The request is high-impact and hard to reverse later.

## Do Not Use When

- The user already chose the direction and just wants implementation.
- The task is a small bug fix.
- The issue is operational and needs debugging instead of exploration.

## Inputs To Clarify

Before giving options, extract or ask for only the minimum missing context:

- What is being built or changed?
- Who is the end user?
- What is the main success metric?
- Are there stack or platform constraints?
- Is speed, maintainability, cost, or polish the top priority?

## Recommended Thought Process

### Phase 1: Define the Problem

- Restate the request in one sentence.
- Separate the real goal from the user's first idea.
- Identify hidden assumptions.

### Phase 2: Set Constraints

- Existing stack
- Timeline
- Team skill level
- Budget or infrastructure limits
- UX, performance, or security constraints

### Phase 3: Generate Options

Produce at least 3 options when possible:

- conservative / low-risk option
- balanced option
- bold or unconventional option

### Phase 4: Compare Tradeoffs

For each option, assess:

- implementation effort
- future flexibility
- complexity
- operational burden
- compatibility with the current repo

### Phase 5: Recommend a Direction

End with one recommended option plus a clear next action:

- move into `$plan`
- move into `$create`
- move into `$enhance`
- or keep exploring one option in more depth

## Related Skills and Workflows

- `$brainstorming` for structured questioning
- `$plan` when the exploration is done and implementation should be sequenced
- `$architecture` when the decision is mostly architectural
- `$create` for new builds
- `$enhance` for changes to an existing project

## Suggested Output

```md
## Brainstorm

### Goal
- ...

### Constraints
- ...

### Option 1
- Summary:
- Pros:
- Cons:
- Risk:
- Effort:

### Option 2
- Summary:
- Pros:
- Cons:
- Risk:
- Effort:

### Option 3
- Summary:
- Pros:
- Cons:
- Risk:
- Effort:

### Recommendation
- Best fit:
- Why:
- What to do next:
```

## Good Output Characteristics

- concrete, not vague
- tradeoff-oriented, not sales-y
- tailored to the current repo or request
- avoids pretending there is only one good answer

## Example Invocations

```text
$brainstorm authentication system for a SaaS dashboard
$brainstorm state management for a complex form builder
$brainstorm architecture for an internal admin portal
$brainstorm feature ideas for a developer onboarding flow
```

## Final Rule

Do not jump into implementation inside this workflow unless the user clearly pivots from exploration
to execution.
