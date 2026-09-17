---
name: Technical Audit Lab Notebook
colors:
  surface: '#07122a'
  surface-dim: '#07122a'
  surface-bright: '#2f3952'
  surface-container-lowest: '#030d25'
  surface-container-low: '#101b33'
  surface-container: '#151f37'
  surface-container-high: '#1f2942'
  surface-container-highest: '#2a344e'
  on-surface: '#d9e2ff'
  on-surface-variant: '#d6c4b0'
  inverse-surface: '#d9e2ff'
  inverse-on-surface: '#263049'
  outline: '#9e8e7c'
  outline-variant: '#514536'
  surface-tint: '#ffb956'
  primary: '#ffc16c'
  on-primary: '#462b00'
  primary-container: '#e8a33d'
  on-primary-container: '#5f3c00'
  inverse-primary: '#835400'
  secondary: '#7dd6c7'
  on-secondary: '#003731'
  secondary-container: '#007367'
  on-secondary-container: '#9bf4e5'
  tertiary: '#ffbbb5'
  on-tertiary: '#65080d'
  tertiary-container: '#ff928a'
  on-tertiary-container: '#811e1e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffddb5'
  primary-fixed-dim: '#ffb956'
  on-primary-fixed: '#2a1800'
  on-primary-fixed-variant: '#643f00'
  secondary-fixed: '#99f3e3'
  secondary-fixed-dim: '#7dd6c7'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005047'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410003'
  on-tertiary-fixed-variant: '#852220'
  background: '#07122a'
  on-background: '#d9e2ff'
  surface-variant: '#2a344e'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 19px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-code-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: -0.01em
  label-code-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 15px
    letterSpacing: 0.02em
  label-code-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '400'
    lineHeight: 13px
    letterSpacing: 0.04em
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes a high-density, forensic developer interface tailored for technical audits, capability benchmarks, and autonomous agent feasibility research. Designed specifically for AI Product Ops, systems architects, and developer tooling leads, the visual tone balances empirical laboratory documentation with the tactical utility of an advanced terminal diagnostic suite.

The aesthetic fuses **Precision Brutalism** and **Instrumental Data Density**:
- **Utilitarian Rigor:** Zero decorative fluff, zero soft gradients, and zero diffuse SaaS shadows. Layouts prioritize scannable telemetry, schema definitions, and direct audit logs.
- **Architectural Division:** Surfaces are delineated through razor-sharp 1px hairline rules, calibrated contrast shifts, and functional status indicators rather than dimensional elevation.
- **Evidentiary Clarity:** Content is displayed as structured proofs, ledger entries, and empirical results. The interface communicates uncompromised objectivity, reproducibility, and industrial resilience.

## Colors

The palette operates in a calibrated deep-spectrum dark mode, minimizing eye fatigue during exhaustive telemetry scans while preserving surgical color contrast for rapid triage.

### Surface Tiers
- **Canvas Base (`#12151a`):** Deep ink ground for root application backdrops and master terminal gutters.
- **Surface Layer 1 (`#181c24`):** Primary structural substrate for data sheets, audit tables, and master panels.
- **Surface Layer 2 (`#1f242e`):** Secondary container tier for card modules, inspect panels, and grouped ledger items.
- **Surface Layer 3 (`#262d3a`):** Interactive active states, highlighted row entries, and terminal code blocks.

### Hairlines & Boundaries
- **Hairline Border Base (`#2d3545`):** Universal structural divider for 1px cell rules and perimeter borders.
- **Hairline Border Focus / Active (`#3b4559`):** Accentuated separation for interactive fields, hovered records, and split-pane dividers.

### Data & State Semantics
- **Amber Benchmark (`#e8a33d`):** Primary metric callouts, headline aggregate numbers, pending verification runs, and calibration milestones.
- **Teal / Cyan Verified (`#7fd8c9`):** Empirical success, production-ready pathways, fully functional agent tool integrations, and verified endpoints.
- **Coral / Red Gated (`#e2665f`):** Unfeasible states, authentication walls, schema breakages, missing webhook infrastructure, and critical blockers.
- **Muted Slate (`#8892b0`):** Structural metadata, parameter keys, secondary labels, timestamp offsets, and inactive flags.

## Typography

The type ecosystem uses three deliberate typefaces to segment hierarchy, technical telemetry, and documentation narrative:

1. **Space Grotesk (Headlines):** Imparts geometric weight and deliberate technical sharpness to major report section headings, section tallies, and executive summaries.
2. **Inter (Analytical Body):** Ensures maximum neutral readability across long-form synthesis notes, diagnostic post-mortems, and technical feasibility commentary.
3. **JetBrains Mono (Telemetry, Badges, & Logs):** Serves as the first-class data font for runtime metrics, status badges, CLI traces, payload key/values, and calibration specs.

All uppercase tags rendered in JetBrains Mono use positive tracking (`letterSpacing: 0.04em`) to ensure legibility at micro sizes (10–11px).

## Layout & Spacing

The layout is built on an analytical, dense multi-column grid architecture designed for comparative assessment:

- **Desktop (1200px+):** 12-column or 16-column continuous tabular grid with a 1rem gutter and 1.5rem canvas margin. The layout accommodates split-screen viewing: persistent filter/status sidebar (3 columns), master registry table (8 columns), and diagnostic drawer / inspector panel (5 columns overlaid or dockable).
- **Tablet (768px – 1199px):** 8-column layout. Metric bands wrap into 2x2 cards. Sidebars convert into horizontal collapsible command bars.
- **Mobile (<768px):** 4-column single-stream data ledger. Multi-column tables collapse into vertical diagnostic index cards with horizontal swipe telemetry strips.

Spacing values favor tight compactness (`space-xs` through `space-md`) within panels and data tables to preserve informational throughput on standard displays, reserving larger scale jumps (`space-lg` to `space-xl`) strictly for demarcating independent audit sections.

## Elevation & Depth

This design system completely eliminates diffuse drop shadows and blurred depth illusions. Depth is conveyed strictly through **Tonal Inset Shifting** and **Crisp Structural Hairlines**:

- **Ground Level (Zero Depth):** Base surface `#12151a`.
- **Level 1 (Card & Module Shells):** Background `#181c24` wrapped in a 1px solid `#2d3545` border.
- **Level 2 (Panels, Inspect Trays & Raised Elements):** Background `#1f242e` with a 1px solid `#3b4559` border.
- **Overlays, Popovers & Diagnostics Drawers:** Base `#1f242e` with high-contrast perimeter border `1px solid #8892b0` at 30% opacity, paired with an ambient 2px directional border shift (`box-shadow: 2px 2px 0px 0px #000000`).
- **Focus & Selection States:** High-luminance perimeter outlines (e.g., 1px solid `#e8a33d` or `#7fd8c9`) replace standard SaaS halo glows.

## Shapes

The design system enforces an uncompromising **Sharp (`0`)** corner geometry (`border-radius: 0px`).

Every interactive button, table cell, data badge, filter pill, modal, and log viewer maintains strict rectangular perimeters. This reinforces the aesthetic of physical terminal hardware, scientific ledger grids, and precision instrument panels. In situations where an element must indicate an interactive toggle track, a maximum radius of `1px` to `2px` is permitted, but default to `0px` across all structural containers.

## Components

### Buttons
- **Primary Action (Run / Export Audit):** Sharp rectangle (`0px` radius), solid background `#e8a33d`, text `#12151a` (`Space Grotesk`, 600 weight, 12px), 1px solid `#e8a33d`. On hover: `#f5b658`.
- **Secondary Action (Filter / Inspect):** Background `#181c24`, text `#8892b0`, 1px solid `#2d3545`. On hover: text `#f0f2f5`, border `#3b4559`, background `#1f242e`.
- **Destructive / Reset:** Background transparent, text `#e2665f`, 1px solid `#e2665f`. On hover: background `#e2665f` with text `#12151a`.

### Status Badges & Chips
- **Monospace Pill Geometry:** Rendered in `JetBrains Mono` at 11px uppercase, zero border radius, padded with `2px 6px`.
- **Verified / Buildable:** Background `rgba(127, 216, 201, 0.12)`, text `#7fd8c9`, border `1px solid rgba(127, 216, 201, 0.4)`.
- **Gated / Blocker:** Background `rgba(226, 102, 95, 0.12)`, text `#e2665f`, border `1px solid rgba(226, 102, 95, 0.4)`.
- **Pending / Benchmarking:** Background `rgba(232, 163, 61, 0.12)`, text `#e8a33d`, border `1px solid rgba(232, 163, 61, 0.4)`.
- **Secondary Meta:** Background `#1f242e`, text `#8892b0`, border `1px solid #2d3545`.

### Data Tables & Audit Ledgers
- **Header:** Background `#181c24`, bottom border `1px solid #3b4559`, text `#8892b0` in `JetBrains Mono` 10px uppercase with `letterSpacing: 0.04em`.
- **Row Grid:** Alternating stripes disabled; rows delineated by `1px solid #2d3545` bottom borders.
- **Row Interaction:** On hover, surface changes to `#1f242e`, with a 2px left border indicator in `#e8a33d`.
- **Cell Content:** Numerical metrics aligned right using tabular numbers (`font-variant-numeric: tabular-nums`).

### Input Fields & Search Bars
- **Container:** Background `#12151a`, 1px solid `#2d3545`, zero border radius. Text `#f0f2f5` in `JetBrains Mono` 12px. Placeholder text `#8892b0` at 60% opacity.
- **Focus:** 1px solid `#e8a33d`, zero outline ring. Prefix icon or CLI prompt prefix (`> `) in `#e8a33d`.

### Checkboxes & Segmented Controls
- **Checkboxes:** 14px square, `0px` radius, background `#12151a`, 1px solid `#2d3545`. Checked state: background `#e8a33d`, check icon in `#12151a`.
- **Segmented Filter Bar:** Continuous connected rectangular frame with `1px solid #2d3545`. Active segment filled with `#262d3a` and text `#f0f2f5`; inactive segments `#181c24` with text `#8892b0`.

### Cards & Telemetry Blocks
- **Metric Tile:** Background `#181c24`, 1px solid `#2d3545`, internal padding `space-md` (`0.75rem`). Metric value in `Space Grotesk` 22px (`#f0f2f5` or `#e8a33d`), with upper micro-label in `JetBrains Mono` 10px (`#8892b0`).
- **Terminal / Raw Audit Log Pane:** Background `#12151a`, border `1px solid #2d3545`, text `#8892b0`, highlighted log parameters in `#7fd8c9` (valid outputs) or `#e2665f` (trace errors).