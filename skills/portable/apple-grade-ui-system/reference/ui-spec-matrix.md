# UI Spec Matrix

Complete this matrix for every feature before `PASS`.

## 1) Buttons

- primary, secondary, tertiary roles defined
- size tokens and radius specified
- states defined: default, hover/focus, active, disabled, loading, success/error feedback
- CTA hierarchy aligned with task criticality

## 2) Information Visualization

- chart type rationale defined
- bar graph usage justified (comparison across categories) or rejected with reason
- non-chart alternative considered where charts add noise
- legends/labels/units specified

## 3) Settings Icons

- icon family declared (single family only)
- stroke/fill style consistent with system
- semantic mapping consistent across screens
- icon placement follows platform conventions

## 4) Placement Rules

- canonical screen/surface specified
- duplicate entry points avoided or justified
- settings/configuration not placed in transient surfaces unless explicitly justified

## 5) Window / Modal / Sheet Behavior

- open trigger and opening behavior defined
- close behavior defined (cancel/escape/backdrop/system action)
- focus restoration and accessibility behavior defined
- transition timing/easing specified

## 6) New Information Requests (Forms)

- what information is required and why
- progressive disclosure strategy
- validation behavior (inline + submit)
- error and recovery messaging
- **input widget type matches content type**: single-line `TextField` only for short identifiers or labels; `TextEditor` (or equivalent multiline widget) required for any field where the user may enter multiple sentences, bullet points, or line breaks — reviewer must explicitly confirm this for every text input
- **user mental model check**: for each input field, ask "what information does the user *naturally possess* when they arrive at this form?" — if the form forces the user to *compute* a value they don't have (e.g., duration when they only know start and end time), the form design fails this check and must be revised to accept the user's native information
- **CRUD completeness**: for every `create` or `write` operation in a form, verify a corresponding `edit` and `delete` path exists; if a user can create incorrect data, they must be able to correct or remove it

## 7) Dialog / Box Design

- layout anatomy (title/body/fields/actions)
- spacing and hierarchy
- CTA ordering and destructive action handling
- copy clarity and action specificity

## 8) Typography

- type scale and hierarchy
- readability constraints (line length, contrast support)
- emphasis strategy (weights/size) aligned with hierarchy

## 9) Colors

- semantic tokens mapped (primary/surface/text/status)
- contrast constraints satisfied
- status colors aligned with meaning and accessibility
- **prominent CTA contrast invariant defined**: for every filled/primary CTA variant, foreground token remains high-contrast independent of fill tint (never tint-matched foreground)

## 10) Components

- approved component patterns selected
- composition rules defined
- reusable vs one-off components justified

## 11) Animation

- purpose for each animation is defined
- timing/easing tokens specified
- reduced-motion behavior specified
- no decorative-only motion in critical flows
- **motion intent classifier completed for each transition**: disclosure/fold vs transient feedback
- **disclosure/fold transitions are non-translating on collapse** unless explicitly justified by product behavior

## 16) First-Run Geometry Stability

- for every popover/sheet/window: initial render dimensions documented
- first interaction path validated (first toggle/open/expand) with no abrupt width/height jump
- repeated interaction behavior remains stable (no drift between first-run and steady-state geometry)
- any intentional geometry change is explicit, bounded, and user-comprehensible

## 12) State Coverage

- all possible states for every stateful component are enumerated (idle, active, loading, error, empty, partial, disabled, transitional, overtime, boundary, edge-case)
- visual treatment is defined for each state — what the user sees
- transitions between states have defined triggers and user feedback
- edge-case states are addressed: zero items, maximum items, midnight boundary, permission change mid-use, rapid state transitions, app relaunch with stale state
- no state exists in code without a corresponding UI design decision

## 13) Button Integrity

- every button's label accurately describes its action
- each action has exactly one trigger point in the codebase
- buttons only appear in states where their action is valid
- every button tap produces observable feedback (state change, animation, navigation, or confirmation)
- destructive actions have confirmation or undo paths
- no silent no-op buttons exist

## 14) Implementation Quality

- fixes address root cause, not visible symptom
- no timing workarounds (sleep/delay) masking race conditions
- no duplicate action triggers (same side effect from multiple code paths)
- no silent error swallowing (`try?` without logging) on user-visible operations
- styling modifier combinations are visually verified (not just code-reviewed)
- adjacent flows are regression-tested after fixes

## 15) Interaction Ergonomics

This section must be completed for every screen that contains tappable, clickable, selectable, or scrollable elements. Absence of this section from the review is a `BLOCKED` trigger.

**Hit target size audit:**
- Every interactive element (button, row, chip, link, toggle, disclosure, picker option) must have a minimum hit area of 44×44pt on all platforms. This applies to the *interactive area*, not the visual indicator. A 16×16pt icon that sits inside a 44×44pt transparent button frame passes. A 16×16pt icon with no frame padding fails.
- Verify using: `.frame(minWidth: 44, minHeight: 44)` + `.contentShape(Rectangle())` for non-button containers; `.frame(width: 44, height: 44)` for icon-only buttons.

**Full-container tappability audit:**
- For every list row, expandable row, calendar cell, option chip, or card: confirm that the *entire visible area* registers the interaction, not just a sub-element.
- SwiftUI `DisclosureGroup` default: FAIL — only the disclosure chevron registers taps. Replace with `Button {}` + `.contentShape(Rectangle())` + `@State isExpanded`.
- Containers used as tap targets (HStack/VStack/ZStack with `.onTapGesture` or `Button`) MUST include `.contentShape(Rectangle())` to make transparent gaps tappable.

**Input modality precision audit:**
- For every input control (picker, selector, slider, stepper, radio, segmented, toggle): ask "does selecting the correct option require physical precision under normal conditions?"
- For analog or 5+-step values (effort level, intensity score, duration preference): slider or stepper required — NOT radio buttons, NOT small discrete targets. Minimum target size per option: 44×44pt.
- For 2–5 discrete options of equal visual weight: segmented control preferred over radio buttons. Every segment must be ≥44pt tall.
- For binary values: toggle or two-button row; each option ≥44pt.

**Text overflow and truncation audit:**
- For every text field, label, card cell, or list row where the content length is variable or user-supplied: explicitly declare the overflow strategy.
  - **Wrapping** (`.lineLimit(nil)`, `.fixedSize(horizontal: false, vertical: true)`): use for achievement text, notes, reflections, descriptions — any user-generated content.
  - **Truncation** (`.lineLimit(n)` + `.truncationMode`): acceptable ONLY for secondary/decorative labels where full content is not needed for task completion. Must not be used on actionable or data-entered content.
  - **Scrollable**: use when content may be very long but must be fully accessible (e.g., detailed session notes in a sheet).
- Auto-block if any user-generated content field can clip to a single line without a tap-to-expand or scroll path.

**Expandable row replacement checklist (when `DisclosureGroup` is used anywhere):**
- [ ] Replace with `Button { isExpanded.toggle() } label: { rowContent }` + `.contentShape(Rectangle())`
- [ ] State driven by `@State var isExpanded: Bool`
- [ ] Chevron rotates 90° on expand (`.rotationEffect(.degrees(isExpanded ? 90 : 0))`)
- [ ] Full row background/highlight on hover
- [ ] Accessibility: `.accessibilityElement(children: .combine)` + `.accessibilityHint(isExpanded ? "Collapse" : "Expand")`

## Completion Rule

If any category is missing or ambiguous, verdict must be `BLOCKED`.
