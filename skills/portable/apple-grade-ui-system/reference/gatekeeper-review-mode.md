# Gatekeeper Review Mode

Use this mode for strict evaluation before approval.

## Evidence Requirement

Review is valid only if both are present:
- code/diff evidence
- rendered screenshots (or recordings)

If not, return `BLOCKED` immediately.

Functional validation is mandatory:
- end-to-end run of critical user flows
- crash/runtime error check
- regression check on adjacent flows

If these are missing, return `BLOCKED`.

## Fixed Review Pipeline

1. Product Integration
- Validate artifacts from `product-integration-mode.md`.
- Ensure feature journey blueprint is complete and coherent.

2. Structure
- Verify IA clarity and route ownership.
- Detect naming redundancy, duplicate destinations, contradictory flows.

3. Surface
- Validate hierarchy, spacing, sizing, and visible priority.
- Confirm first-glance information is not buried.

4. UI Spec Matrix
- Validate all matrix categories from `ui-spec-matrix.md`.
- Block if any visual/interaction behavior remains unspecified.

5. Behavior
- Walk every critical path using: see -> click -> result.
- Verify loading, error, success, and disabled states.

6. Button Behavioral Integrity
- For every button/toggle/interactive element: trace label → handler → function → state change → feedback.
- Verify label-action match: the visible text accurately describes the outcome.
- Verify single trigger: each action has exactly ONE code path. Search for duplicate handlers.
- Verify state validity: button only appears in states where its action is meaningful.
- Block if any button's label does not match its action or if duplicate triggers exist.

7. State Exhaustiveness
- Enumerate ALL states for every stateful component BEFORE reviewing.
- Verify visual treatment is defined for each state.
- Verify transitions between states have defined triggers and feedback.
- Test boundary states: zero items, max items, permission changes, rapid transitions.
- Block if any state was not enumerated and reviewed.

8. Discoverability
- Confirm first discovery surface for new feature.
- Confirm re-entry path and contextual help path.

9. Coherence
- Validate cross-screen consistency in nav, naming, and state language.
- Confirm no conflicting affordances or dead-end transitions.

10. Implementation Integrity
- Verify each fix addresses root cause, not symptom.
- Verify no duplicate action paths exist (same side effect from multiple triggers).
- Verify no silent error swallowing on user-visible operations.
- Verify no timing workarounds masking race conditions.
- Verify adjacent flows were regression-tested after fixes.
- Block if any patch quality violation is found.

11. Window/Popover Orchestration Integrity
- Build a surface lifecycle map for each critical action: action → state commit → popover/window close/open → activation.
- Verify a single owner governs popover close, coach window open, completion window open, and app activation policy.
- Verify single-commit/single-surface invariant:
  - commit actions from popover close popover immediately,
  - strong coach escalation does not duplicate same intent in popover and standalone window.
- Verify activation policy is explicit and bounded (e.g., only high-severity strong prompts or explicit user navigation).
- Block if lifecycle ownership is fragmented or if any dual-surface same-intent prompt exists.

12. **Interaction Ergonomics** ← NEW — run this for every screen with interactive elements
- **Hit target audit**: for every button, chip, row, toggle, picker option — is the interactive hit area ≥44×44pt? If the visual element is smaller, confirm `.contentShape(Rectangle())` or padding expands it. Absence of `.contentShape` on any `HStack`/`VStack` tap target is evidence of the bug.
- **Full-row tappability**: for every expandable/collapsible row, calendar cell, list row, or disclosure group — does the entire visible row register taps? Check for `DisclosureGroup` without a custom full-row `Button` wrapper. Any `DisclosureGroup` in the codebase is a red flag — confirm it was replaced with `Button { } label: { } .contentShape(Rectangle())`.
- **Text overflow strategy**: for every text field where length is variable or user-supplied — is an explicit overflow strategy declared? User-generated content (achievements, notes, reflections) must use `.lineLimit(nil)` or provide a tap-to-expand path. Single-line truncation of user data is auto-blocking.
- **Input modality precision**: for every selector, picker, or rating control — does choosing the correct option require physical aim precision? Continuous/ordinal values (effort, intensity, score) with >2 options must use slider, stepper, or ≥44pt segmented control. Small radio buttons or toggle groups where each option is <44pt tall are auto-blocking.
- **Compound widget hit area**: for chips, tags, filter pills, or any small interactive surface — confirm `.frame(minHeight: 44)` or `.padding(.vertical)` is applied. The user must be able to select any chip without aiming at the exact label pixels.
- Block if any of the above checks fail.

13. Component Invariants and Contrast
- For shared primitives (primary CTA/button components), verify foreground/background contrast invariant under all supported tints.
- Block if any prominent primary action can render same-hue or low-readability text/icon on filled backgrounds.

14. Motion Intent Classification
- Enumerate every reviewed transition and classify intent:
  - disclosure/fold (expand/collapse persistent content)
  - transient feedback (toast/banner/ephemeral system feedback)
- Disclosure/fold transitions must preserve container anchoring and avoid translating collapse that shifts layout.
- Block if intent classification is missing or disclosure transitions translate the container.

15. First-Run Geometry Stability
- Verify popover/sheet/window geometry at:
  - initial render
  - first user interaction (first toggle/open/expand)
  - steady-state repeated interactions
- Block if width/height jumps abruptly during first-run paths or if evidence is missing.

16. PM Integration Lens
- Apply checks from `pm-integration-review.md`.
- Block if feature integration adds unresolved product-model conflicts.

17. **Accessibility** ← mandatory for every screen with interactive elements
- VoiceOver labels: every non-decorative interactive element has `.accessibilityLabel()`. Icon-only buttons must have a label describing the action.
- Color-only state: every state, status, or category communicated by color has a secondary non-color indicator (icon, label, text, pattern).
- Decorative elements: every non-informational icon/image has `.accessibilityHidden(true)`.
- Focus management: after modal/sheet/window dismiss, focus returns to the triggering element or a logical next element.
- Non-obvious hints: any interactive element whose purpose isn't self-evident has `.accessibilityHint`.
- Block if any VoiceOver label is missing on an interactive element or any state is color-only.

18. **Dark Mode and Color Adaptability**
- No hardcoded color values (`Color(.white)`, `Color(.black)`, hex/RGB) in any UI component.
- All colors use semantic tokens or the app's design token set.
- Visual evidence required in BOTH light and dark mode for any component reviewed.
- Glass effects verified on appropriate backgrounds (content to blur must be present).
- Block if any hardcoded color exists in a visible component or if dark mode evidence is missing.

19. **Performance and Responsiveness**
- Every interactive element produces observable visual feedback within 100ms of a tap/click.
- Every operation >1s has a visible loading indicator.
- No heavy synchronous work on the main thread during UI updates.
- Block if any tap produces zero visual feedback before async completion, or if any operation >1s has no loading state.

20. **Notification and In-App Message Quality** (when feature includes coach, reminders, or alerts)
- Notification copy is specific to user's current context/data — not generic.
- Every notification has a tap action or is fully informational.
- Coach/intervention messages reference actual user data (idle time, app usage, session count).
- Block if any notification would read identically for all users at all times.

21. **Design Ownership Consent Gate**
- Identify all non-functional visual-language changes (palette/tone, decorative motion, icon style, typography tone).
- Verify explicit user approval exists for each such change.
- If approval is missing, convert the item to recommendation-only and block implementation.
- If unapproved style changes were already implemented, verdict must be `BLOCKED` until reverted or approved.

22. Verdict
- Apply auto-block rules.
- Apply functional-depth gate.
- Produce output exactly per review contract.

## Scoring Rubric (0-5)

Score each dimension and justify:
- Structure
- Surface
- Behavior
- Discoverability
- Coherence
- **Behavioral Integrity** (button label-action match, state exhaustiveness, single-trigger enforcement)
- **Implementation Quality** (root-cause fixes, no patches/workarounds, regression evidence, error observability)
- **Interaction Ergonomics** (hit target sizes, full-row tappability, text overflow strategies, input modality precision)
- **Accessibility** (VoiceOver labels, color-only state, focus management, decorative element hiding)
- **Platform Adaptability** (dark/light mode semantic colors, glass composition, keyboard shortcuts)

Scoring guidance:
- 0-1: broken or contradictory
- 2: major risk
- 3: acceptable with notable issues
- 4: strong
- 5: production-grade

A `PASS` requires no auto-block trigger and no dimension below 3.
A `PASS` also requires no failing functional-depth checks.
A `PASS` also requires Product Integration artifacts and UI Spec Matrix marked complete.
A `PASS` also requires Button Behavioral Integrity and State Exhaustiveness audits complete with no violations.

## Gatekeeper Posture

- Prefer explicit defects over vague advice.
- Block when core UX reliability is at risk.
- Keep fixes prioritized and implementation-ready.
- Reject partial implementations and shortcut fixes that skip root-cause validation.
