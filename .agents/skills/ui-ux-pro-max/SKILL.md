---
name: ui-ux-pro-max
description: AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# UI UX Pro Max

This skill adapts the Antigravity `ui-ux-pro-max` workflow for Codex.
Use it for design-heavy web and mobile tasks where visual direction and design
system quality matter.

## Overview

Comprehensive design guidance for web and mobile applications, including:

- 50+ styles
- 97 color palettes
- 57 font pairings
- 99 UX guidelines
- 25 chart types
- 9 technology stacks

## Prerequisites

Check Python:

```bash
python3 --version || python --version
```

If Python is missing:

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Windows
winget install Python.Python.3.12
```

## Workflow

### Step 1: Analyze User Requirements

Extract:

- Product type
- Style keywords
- Industry
- Stack, defaulting to `html-tailwind`

### Step 2: Generate Design System

Always start with `--design-system`:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This command:

1. Searches multiple domains in parallel
2. Applies reasoning rules from `ui-reasoning.csv`
3. Returns pattern, style, colors, typography, and effects
4. Includes anti-patterns to avoid

Example:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System

To persist the design system:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

This creates:

- `design-system/MASTER.md`
- `design-system/pages/`

With page-specific override:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

### Step 3: Supplement with Detailed Searches

Use additional searches when needed:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

Common domains:

| Need | Domain |
|------|--------|
| More style options | `style` |
| Chart recommendations | `chart` |
| UX best practices | `ux` |
| Typography options | `typography` |
| Landing structure | `landing` |

### Step 4: Stack Guidelines

If the user does not specify a stack, default to `html-tailwind`.

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks include:

- `html-tailwind`
- `react`
- `nextjs`
- `vue`
- `svelte`
- `swiftui`
- `react-native`
- `flutter`
- `shadcn`
- `jetpack-compose`

## Example Workflow

User request:

```text
Build a landing page for a professional skincare service
```

Suggested sequence:

```bash
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

## Output Formats

```bash
# ASCII box
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown
python3 .agents/.shared/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

## Tips for Better Results

1. Be specific with keywords.
2. Search multiple times from different angles.
3. Combine style, typography, color, and UX searches.
4. Always check accessibility and motion guidance.
5. Use stack-specific searches before implementation.
6. Iterate until the design system feels coherent.

## Common Rules for Professional UI

### Icons and Visual Elements

| Rule | Do | Don't |
|------|----|-------|
| No emoji icons | Use SVG icon sets | Use emoji as UI icons |
| Stable hover states | Use color or opacity transitions | Use transforms that shift layout |
| Correct brand logos | Verify official SVGs | Guess logo paths |
| Consistent icon sizing | Keep a fixed viewBox | Mix random icon sizes |

### Interaction and Cursor

| Rule | Do | Don't |
|------|----|-------|
| Cursor pointer | Add `cursor-pointer` to clickable cards | Leave default cursor |
| Hover feedback | Provide visual feedback | Give no interactive signal |
| Smooth transitions | Keep transitions around 150-300ms | Make transitions instant or very slow |

### Light and Dark Contrast

| Rule | Do | Don't |
|------|----|-------|
| Glass card light mode | Use `bg-white/80` or similar | Use very low opacity white |
| Text contrast light | Use dark text for body copy | Use washed-out gray body text |
| Muted text light | Keep sufficient contrast | Use text that is too faint |
| Border visibility | Use visible borders in light mode | Use near-invisible borders |

### Layout and Spacing

| Rule | Do | Don't |
|------|----|-------|
| Floating navbar | Add edge spacing | Stick everything to `top-0` |
| Content padding | Account for fixed navbar height | Hide content behind fixed elements |
| Consistent max-width | Reuse the same container widths | Mix widths randomly |

## Pre-Delivery Checklist

### Visual Quality

- [ ] No emoji icons
- [ ] Icons come from a consistent icon set
- [ ] Brand logos are correct
- [ ] Hover states do not cause layout shift
- [ ] Theme colors are applied consistently

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear feedback
- [ ] Transitions are smooth
- [ ] Focus states are visible

### Light and Dark Mode

- [ ] Text contrast is sufficient
- [ ] Glass elements stay visible
- [ ] Borders are visible in both modes
- [ ] Both modes were tested

### Layout

- [ ] Floating elements have proper spacing
- [ ] No content is hidden behind fixed nav
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility

- [ ] Images have alt text
- [ ] Inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` is respected
