---
name: apple-grade-ui-system
description: Use when building or reviewing any UI change that must meet Apple-HIG-inspired quality, premium visual craft, strict feature-integration rigor, and end-to-end UX flow coherence; includes mandatory Design Mode, Product Integration Mode, and Gatekeeper Review Mode.
---

# Apple-Grade UI System

## Overview

A single master skill for UI work that unifies:
- creative direction from `frontend-design`
- technical rigor from `premium-frontend`
- anti-pattern suppression from `uncodixfy`
- structured quality checks from `ui-ux-pro-max`

This skill has three mandatory modes:
1. `Design Mode` for creation and refinement.
2. `Product Integration Mode` for feature placement, full journey design, and explicit UI behavior decisions.
3. `Gatekeeper Review Mode` for strict pass/block decisions.

"Apple-grade" in this skill means principle-level quality: clarity, restraint, hierarchy, continuity, discoverability, and feedback coherence. It does not mean copying Apple's visual identity.

## When To Use

Use this skill when:
- creating a new screen, component, flow, or UI feature
- revising layout, visual hierarchy, navigation, or interaction behavior
- reviewing UI changes before merge/release
- diagnosing why UI feels polished but still weak in UX

Do not use this skill for backend-only, infra-only, or non-UI work.

## Mandatory Process

1. Run `Design Mode` first when creating/changing UI.
2. Run `Product Integration Mode` before implementation sign-off.
3. Run `Gatekeeper Review Mode` before claiming completion.
4. Run the functional-depth gate before final verdict.
5. If review verdict is `BLOCKED`, fixes are mandatory before approval.
6. For any non-functional visual language change (color, typography tone, motion style, iconography style, decorative glass treatment), present recommendation + visual delta first and wait for explicit user approval before implementation.

Details:
- Design workflow: [design-mode.md](reference/design-mode.md)
- Product integration workflow: [product-integration-mode.md](reference/product-integration-mode.md)
- Review workflow: [gatekeeper-review-mode.md](reference/gatekeeper-review-mode.md)
- Functional-depth workflow: [functional-depth-gate.md](reference/functional-depth-gate.md)
- UI spec matrix: [ui-spec-matrix.md](reference/ui-spec-matrix.md)
- PM integration lens: [pm-integration-review.md](reference/pm-integration-review.md)

## Product Integration Artifacts (Required)

A feature cannot pass unless all artifacts below are complete:
- user intent and trigger context
- entry screen, re-entry screen, and discoverability path
- journey blueprint (`see -> click -> response -> next step`)
- failure and recovery path
- completion outcome state
- UI Spec Matrix completion for all affected surfaces

Missing artifacts force `BLOCKED`.

## Visual Change Consent Gate (Required)

This framework distinguishes **functional correctness fixes** from **visual-language changes**:

- Functional correctness fixes (crashes, broken interactions, <44pt hit targets, text clipping, unreadable contrast) may be implemented directly.
- Visual-language changes (palette/tone/style shifts that are not strictly required to restore function) require explicit user confirmation before code changes.

Mandatory behavior:
- If a style change is proposed, output a recommendation block with:
  - what changes visually
  - why it helps
  - fallback option that preserves current style language
- If user confirmation is missing, do **not** implement that visual change.
- In autonomous/autopilot execution, leave style changes as warnings/recommendations only until approved.

## Inputs Required For Review

Review must use both:
- implementation evidence (code/diff)
- rendered evidence (screenshots/video)

If either is missing, return `BLOCKED` with "insufficient review evidence".

Functional evidence is also required for approval:
- end-to-end execution evidence for critical flows
- crash/error evidence (logs, console, runtime output)
- regression evidence for adjacent flows

If functional evidence is missing, return `BLOCKED` with "insufficient functional evidence".

**Functional evidence is not optional and cannot be waived.** A code-diff-only review is insufficient regardless of code quality. Before any review begins, the reviewer must confirm that live execution screenshots or screen recordings exist for every critical flow. If they do not exist, the review must stop and return `BLOCKED` — not proceed with assumptions.

## Hard Auto-Block Rules

Any single trigger below forces verdict `BLOCKED`:
- primary action is unclear, ambiguous, or visually under-prioritized
- feature placement is not canonical and has no rationale
- journey transitions are broken, ambiguous, or missing next-state definitions
- key first-glance information is buried below fold without product reason
- duplicate or contradictory screens/labels/entry points exist
- required interaction feedback states are missing (loading/error/success)
- new feature has no discoverability path (entry + re-entry + help context)
- required UI Spec Matrix fields are unspecified (button/chart/icon/modal/form/motion)
- **any sheet, form, or modal uses native system styling (Form, default NavigationStack toolbar) instead of the app's design system**
- **a configurable option appears in a transient surface (popover, menu) instead of its canonical Settings location**
- **an OS integration (calendar, reminders, notifications, health) is enabled in UI but no evidence it actually reads/writes real data**
- **after OS permission dialog, the app does not restore focus to the active window**
- **a text input field uses a single-line widget (TextField) for content that is naturally multi-line (achievements, notes, descriptions, reflections)**
- **a form creates data without a corresponding path to delete or correct that data (CRUD completeness violation)**
- **a form asks the user to input a computed value they don't naturally know (user mental model mismatch — e.g., asking for "duration" when the user knows "start time" and "end time")**
- **any tappable element with a visible area smaller than 44×44pt that does not use `.contentShape(Rectangle())` or padding to expand the hit area to meet the minimum**
- **a `DisclosureGroup` or expandable row where only the disclosure indicator (chevron/triangle) is tappable — not the full row label area; native `DisclosureGroup` always fails this unless the label is replaced with a full-row `Button` + `.contentShape(Rectangle())`**
- **a continuous or multi-step analog value (effort level, intensity, score, mood) presented as radio buttons or small discrete targets requiring physical aim precision — must be replaced with a slider, stepper, or adequately spaced segmented control with ≥44pt per segment**
- **user-generated or data-entered text (achievements, notes, reflections, session context) that can truncate to a single line with `...` and provides no tap-to-expand, scroll, or reveal path**
- **any interactive element missing `.accessibilityLabel()` — VoiceOver must announce a meaningful action description, not silence or a raw variable name**
- **any state, status, or category communicated exclusively through color with no secondary non-color indicator (icon, label, pattern)**
- **any hardcoded non-semantic color value (`Color(.white)`, `Color(.black)`, hex/RGB) in a UI component that appears in both light and dark mode**
- **any prominent CTA (`.glassProminent` or equivalent filled primary action) where text/icon foreground uses the same or near-same hue as the fill tint, causing low readability contrast**
- **any transition update where motion intent is not explicitly classified as (a) disclosure/fold behavior vs (b) transient feedback behavior**
- **any expandable/disclosure section that collapses with translating motion (`.move(edge: ...)`) causing the container to shift instead of folding in place**
- **any popover/sheet/window interaction with abrupt first-run width/height jump and no geometry-stability evidence for initial render + first toggle**
- **any commit action from menu bar popover (start/resume/continue/take-break/end-session) that does not close the popover**
- **any single intervention decision rendered simultaneously in popover prompt and standalone coach window**
- **any fragmented lifecycle ownership where popover close/window open/app activation are controlled from unrelated paths without explicit orchestration policy**
- **generic notification/coaching message copy that would read identically for all users at all times — every coach or reminder message must reference actual user data or context**
- **any user-triggered operation >1s with no visible loading indicator — the user must never wonder if the app crashed or is still working**
- **any non-functional visual-language change (color/motion/type/icon style) implemented without explicit user approval and documented visual delta**

Full policy: [auto-block-rules.md](reference/auto-block-rules.md)

## Integration Feature Checklist (Mandatory For OS Integrations)

When any feature integrates with an OS service (Calendar, Reminders, Notifications, HealthKit, etc.), the review **must** verify all of the following before `PASS`:

1. **Permission flow**: grant → app regains focus → feature activates without additional user action
2. **Actual data appears**: real events/reminders/notifications are created and visible in the OS app
3. **Fetch scope**: data query is not unintentionally date-filtered or scope-filtered at the OS API level
4. **Retroactive sync**: behavior when integration is enabled after data already exists is documented and user-communicated
5. **Empty state accuracy**: "No items" empty state correctly distinguishes (a) truly empty vs (b) permission denied vs (c) wrong list selected vs (d) wrong filter active
6. **Error recovery**: permission denied state shows actionable path (System Settings deeplink), not just an error message

## Feature Placement Gate (Mandatory)

Before approving any new UI element, verify it is placed at the correct information hierarchy level:

| Surface | What belongs here |
|---------|------------------|
| Menu bar popover | Active session controls, immediate timer state only |
| Companion window main content | Today's data, sessions, projects, insights |
| Companion window Settings tab | All configuration, toggles, preferences, integration setup |
| Standalone window (SessionComplete etc.) | Single-focus post-session flows |

**Auto-block trigger**: a configuration toggle or preference appears in the popover or main content when it should be in Settings.

## Sheet & Form Design Gate (Mandatory)

Every sheet, modal, popover, or form must:
- Use the app's design system components (glass effects, custom panels, design tokens)
- NOT use native macOS `Form {}` wrapper (renders as system-styled table rows)
- NOT use `NavigationStack` toolbar for Save/Cancel actions in a sheet (use custom footer buttons)
- Have a visible close/cancel path that does not require keyboard shortcut
- Validate required fields inline before enabling the primary CTA

Auto-block: any `Form {}` wrapper in a user-facing sheet.

## Anti-AI Aesthetic Rules (Bounded)

Apply anti-pattern bans as one section of quality review, not the full standard.

Use [auto-block-rules.md](reference/auto-block-rules.md) for "style anti-pattern" checks inspired by Uncodixfy while preserving product context and usability.

## Mandatory Review Output Contract

Every Gatekeeper review must output exactly these sections:
1. Executive Verdict (`PASS`, `PASS_WITH_RISKS`, `BLOCKED`)
2. Critical Blockers
3. Screen-By-Screen Click Walkthrough
4. Placement And Discoverability Map
5. Top 5 Prioritized Fixes
6. Re-Review Checklist
7. Functional Validation Evidence
8. Explicit Assumptions
9. Product Integration Artifacts Check
10. UI Spec Matrix Completeness
11. Contrast and Motion Invariant Check
12. PM Integration Verdict
13. Approval-Gated Visual Recommendations

Format spec: [review-output-contract.md](reference/review-output-contract.md)

## Weak Output Diagnosis (Must Run)

Before final verdict, run the weak-output pre-check.

If any trigger is true, verdict cannot be `PASS`:
- style-only polish without flow quality
- missing placement rationale
- no contradiction/redundancy audit
- weak first-glance hierarchy
- incomplete feature journey blueprint
- missing UI visual/interaction decisions in spec matrix
- **integration feature present but no end-to-end data flow verified**
- **form/sheet uses native styling instead of app design system**
- **review was code-only — no live execution evidence for any critical flow**
- **form input widget types not explicitly reviewed (TextField vs TextEditor vs picker)**
- **CRUD completeness not checked — create/write operation present but delete path not verified**
- **user mental model not verified — form inputs not checked against what user naturally knows at point of entry**
- **interaction ergonomics not audited — hit target sizes, full-row tappability, text overflow strategies, and input modality precision not verified for any interactive element**
- **accessibility not audited — VoiceOver labels, color-only state, focus management not checked for any interactive element**
- **dark mode not verified — no visual evidence in dark mode, or hardcoded colors present in reviewed components**
- **notification/coach copy not reviewed — message copy not checked for specificity and data-grounding**
- **visual/style changes were implemented without explicit user confirmation and without a recommendation delta**
- **prominent CTA contrast invariant not verified — shared CTA components can produce same-hue text/fill collisions**
- **transition intent not classified — disclosure/fold vs transient feedback was not explicitly documented per transition**
- **first-run geometry stability not checked — initial render + first interaction sizing behavior lacks evidence**
- **window/popover orchestration not audited — lifecycle map and single-surface invariants were not verified**

Checklist: [diagnose-weak-output.md](reference/diagnose-weak-output.md)

## Determinism And Bias Controls

To avoid ambiguous or biased decisions:
- no pass/fail by preference language alone ("feels better", "looks nicer")
- every finding must cite observable evidence
- every recommendation must tie to user task completion, clarity, safety, or consistency
- unresolved ambiguity defaults to `BLOCKED` until validated
- no assumption may remain implicit; list assumptions explicitly in review output

## Review Phases

The review pipeline is fixed and ordered:
1. Product Integration (intent, trigger, placement, journey blueprint)
2. Structure (IA, naming, redundancy, contradiction)
3. Surface (hierarchy, sizing, spacing, first-glance clarity)
4. UI Spec Matrix (buttons/charts/icons/windows/forms/dialogs/type/color/components/motion)
5. Behavior (see/click/result + state transitions)
6. Discoverability (entry points, findability, help)
7. Coherence (cross-screen continuity and navigation integrity)
8. **Feature Placement** (each element at correct hierarchy level — popover/content/settings/standalone)
9. **Integration Data Flow** (OS integrations actually read/write data end-to-end)
10. **Sheet/Form Design** (no native Form wrappers, custom design system throughout)
11. **Interaction Ergonomics** (hit target sizes ≥44pt, full-row tappability on expandable rows, text overflow strategy on variable-length content, input modality precision match)
12. **Window/Popover Orchestration** (single owner for popover close/window open/activation, commit-action close rules, single-surface prompt invariant)
13. **Component Invariants and Contrast** (shared primitives like primary CTA buttons maintain high-contrast foreground regardless of tint/fill)
14. **Motion Intent Classification** (every transition is classified as disclosure/fold vs transient feedback, with behavior matched accordingly)
15. **First-Run Geometry Stability** (popover/sheet/window dimensions remain stable on initial render and first interaction)
16. PM Integration Lens (clarity vs complexity, fit to product model, conflict risk)
17. **Accessibility** (VoiceOver labels on interactive elements, color-only state backup indicators, focus management, decorative element hiding)
18. **Dark Mode and Color Adaptability** (no hardcoded colors, semantic tokens, glass/material verified in both modes)
19. **Performance and Responsiveness** (100ms tap feedback, loading indicators for >1s ops, no blocking main thread)
20. **Notification/Coach Message Quality** (specific copy, data-grounded, action path present)
21. **Design Ownership Consent Gate** (style changes require explicit user approval; otherwise recommendation-only)
22. Verdict (contract output + ranked fixes)

Reference: [gatekeeper-review-mode.md](reference/gatekeeper-review-mode.md)

## Baseline Standards

Use the following sources as internal references while applying this skill:
- [premium-frontend/SKILL.md](../premium-frontend/SKILL.md)
- [premium-frontend/reference/interaction-design.md](../premium-frontend/reference/interaction-design.md)
- [premium-frontend/reference/spatial-design.md](../premium-frontend/reference/spatial-design.md)
- [premium-frontend/reference/accessibility.md](../premium-frontend/reference/accessibility.md)

Treat these as supporting standards. This skill remains the primary gate.

## Validation Scenarios

Before concluding the review framework is healthy, run scenario checks in:
- [test-scenarios.md](reference/test-scenarios.md)
- [functional-depth-gate.md](reference/functional-depth-gate.md)
- [product-integration-mode.md](reference/product-integration-mode.md)
- [ui-spec-matrix.md](reference/ui-spec-matrix.md)
- [pm-integration-review.md](reference/pm-integration-review.md)

Minimum required scenario coverage:
- new feature placement and discoverability
- redundancy/contradiction failure
- hierarchy/sizing failure
- interaction feedback failure
- clean coherent golden path
- **OS integration data flow (permission → data appears → empty state accuracy)**
- **sheet/form design system compliance**
- **feature placement (popover vs content vs settings)**
- **feature ideation-to-journey completeness**
- **UI spec matrix completeness**
- **input widget type correctness (TextField vs TextEditor for multi-line content)**
- **CRUD completeness (create without delete = BLOCKED)**
- **user mental model match (form inputs match what user naturally knows)**
- **live execution evidence required (code-only review = BLOCKED)**
- **interaction ergonomics not audited (hit targets, full-row tappability, text overflow, analog input precision)**
- **accessibility not audited (VoiceOver labels, color-only state, focus management)**
- **dark mode not verified (hardcoded colors, glass composition in dark mode)**
- **notification/coach message quality not reviewed (generic vs. data-grounded copy)**
- **prominent CTA contrast invariant not reviewed (same-hue fill/text collision risk)**
- **motion intent classification not reviewed (fold/disclosure vs transient feedback)**
- **first-run geometry stability not reviewed (initial toggle width/height jump risk)**
- **window/popover orchestration not reviewed (commit-action closure, single-surface escalation, activation ownership)**
