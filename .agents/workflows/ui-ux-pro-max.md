---
description: Trigger the advanced UI/UX design workflow for redesign, exploration, and systemized visual work.
---

# $ui-ux-pro-max

$ARGUMENTS

Use this workflow for design-heavy web or mobile tasks where visual direction, design systems, and
implementation guidance should stay consistent.

## Purpose

`$ui-ux-pro-max` is the advanced design workflow for AG Kit. It helps Codex move from a loose visual or
product request to a systemized design direction backed by the repo's design-intelligence assets.

## What This Workflow Does

1. Extracts product type, industry, style signals, and stack.
2. Generates a design-system recommendation first.
3. Uses targeted follow-up searches for deeper detail only when needed.
4. Converts the design direction into implementation-ready notes.

## Use When

- The user asks for UI/UX redesign or visual direction.
- A page or product needs stronger visual identity.
- The project needs a design system, palette, typography, or layout direction.
- The task mixes aesthetics and implementation guidance.

## Do Not Use When

- The task is purely backend or infrastructure work.
- The user only wants a tiny CSS bug fixed with no design decision needed.

## Backing Commands

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Project Name"
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

## Recommended Sequence

### Phase 1: Extract Product Context

Identify:

- product type
- audience
- industry
- visual tone
- platform or stack

### Phase 2: Generate the Design System

Always start with a design-system query first so the direction is coherent.

### Phase 3: Add Focused Searches

Only run extra searches when they add missing detail such as:

- typography alternatives
- UX rules
- chart recommendations
- stack-specific patterns

### Phase 4: Translate Into Implementation

Turn the resulting design direction into:

- component guidance
- layout guidance
- color and typography guidance
- interaction and motion guidance

## Suggested Output

```md
## UI UX Summary

### Product Context
- ...

### Design Direction
- ...

### Palette / Typography / Style
- ...

### Component and Layout Notes
- ...

### Implementation Notes
- ...

### Next Step
- ...
```

## Example Invocations

```text
$ui-ux-pro-max redesign this SaaS dashboard
$ui-ux-pro-max create a premium wellness landing page
$ui-ux-pro-max improve the mobile checkout experience
$ui-ux-pro-max build a cleaner design system for this app
```

## Final Rule

Do not collapse into generic design advice. Keep the output visually opinionated and grounded in the
current product context.
