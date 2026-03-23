# Design Mode

Use this mode when creating or changing UI.

## Objective

Produce premium UI with strong visual craft and clear user flow, not style-only polish.

## Inputs

- user goal and target audience
- existing product constraints (brand, platform, design system)
- current screen inventory and navigation model

## Process

1. Define intent and success
- Write one sentence for user outcome.
- Identify primary action and secondary actions for each target screen.

2. Place the feature in the product map
- Pick primary discovery surface (where user first finds feature).
- Pick re-entry surface (where user finds it again later).
- Define help/education surface (tooltip, inline help, docs link, onboarding cue).

3. Draft screen architecture
- List impacted screens and each screen's role.
- Detect naming conflicts and redundant surfaces before building.
- Keep one canonical destination for each task.

3.5. Enumerate component states
- For every stateful component (timers, forms, toggles, integrations, workflows), list ALL possible states — not just the primary ones.
- Include: idle, active, loading, error, empty, partial, disabled, transitional, overtime, boundary, and edge-case states.
- Define the visual treatment for each state.
- Define what triggers each state transition and what feedback the user sees.
- This enumeration must be complete BEFORE proceeding to design hierarchy.

4. Design hierarchy and density
- Ensure first-glance information appears at top hierarchy.
- Size components by priority, not decoration.
- Reduce oversized UI blocks that push important data below fold.

5. Define interaction behavior
- For each key action, define: what user sees, clicks, and what happens next.
- Define required states: default, hover/focus, active, disabled, loading, error, success.

5.5. Verify button label-action integrity
- For every button, toggle, and interactive element: confirm the visible label accurately describes what the action does.
- Trace: label → handler → function → state change → user feedback. If any link in this chain is broken, mismatched, or missing, fix before proceeding.
- Confirm each action has exactly ONE code path that triggers it. Duplicate triggers (e.g., both a callback and an `.onChange` handler firing the same side effect) cause race conditions and must be consolidated.
- Confirm destructive actions (delete, discard, end session) have either a confirmation step or an undo path.

5.6. Verify interaction ergonomics at design time
This step must be completed BEFORE implementation begins. Catching ergonomic failures at design time costs nothing; fixing them post-build is expensive.
- **Hit targets**: for every tappable element in the design — is it reachable without precision aim? Check: will a user's finger or cursor land reliably in one motion? Any control smaller than 44×44pt must use invisible padding or `.contentShape(Rectangle())` to expand its hit area. Document the expansion strategy in the spec.
- **Full-row tappability**: any expandable row, accordion, list item, or calendar cell — the full row must be the hit target, not just the indicator chevron. Do not use `DisclosureGroup` without replacing its label with a full-row `Button`.
- **Input modality match**: any selection with 2+ analog/ordinal steps — is a slider, stepper, or adequately-spaced segmented control used? Radio buttons and small discrete targets are not acceptable for continuous values. Document the chosen control and segment size.
- **Text overflow strategy**: for every text field with variable-length or user-generated content — explicitly declare the overflow strategy (wrapping, scroll, tap-to-expand). Single-line truncation of user data is never acceptable. Document `.lineLimit(nil)` or the expansion path.
- **Tap response immediacy**: every tap must produce visual feedback within 100ms. For async operations, a visual state change (loading, highlight, opacity) must occur immediately on tap — not after the async work completes.

5.7. Verify glass and material composition
- When using glass effects (`.ultraThinMaterial`, `.glassEffect()`, `.glassProminent`), verify the surface has blurrable content behind it. Glass on a solid background is a flat grey rectangle — use `.background(Color.x)` or a dark overlay instead.
- Never apply `.tint()` to a glass button style — use `.foregroundStyle()` on the label content only. Tint on glass creates opaque color blobs that destroy translucency.
- Never stack two material layers (e.g., `.ultraThinMaterial` background under a `LiquidGlassPanel`). Use exactly one compositing layer per surface depth.
- Verify in both light and dark mode: glass effects behave differently under the two modes and must be tested visually in both.

6. Check coherence
- Ensure navigation placement is consistent across screens.
- Ensure terminology, iconography, and state language are consistent.

7. Implementation quality check
- Review every code change for design integrity — does it solve the root cause or patch the symptom?
- Verify no duplicate event paths exist (same side effect triggered from multiple independent handlers).
- Confirm styling modifier combinations render correctly — code review alone is insufficient. Visual evidence required.
- Ensure error paths have both logging (for developers) AND user feedback (for users).
- Verify that fixing one flow does not break adjacent flows — document which adjacent flows were tested.
- Reject timing workarounds (`sleep`, `asyncAfter`) that mask race conditions instead of fixing them.

8. Visual Change Consent Check
- Split proposed changes into:
  - **functional fixes** (must implement)
  - **style recommendations** (approval-gated)
- For each style recommendation, provide plain-language visual delta and rationale.
- Do not implement style recommendations until explicit user approval is given.

## Design Deliverable

Design Mode output must include:
- Screen map with feature placement rationale
- Primary and secondary action hierarchy per screen
- First-glance information list (top-visible essentials)
- Interaction flow summary (see/click/result)
- Contradiction and redundancy notes

## Handoff Requirement

Do not finalize Design Mode until the output is handed off to `Product Integration Mode` for:
- complete feature journey blueprint
- UI Spec Matrix completion
- PM integration fit checks
