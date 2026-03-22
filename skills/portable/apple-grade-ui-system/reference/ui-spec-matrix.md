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

## 10) Components

- approved component patterns selected
- composition rules defined
- reusable vs one-off components justified

## 11) Animation

- purpose for each animation is defined
- timing/easing tokens specified
- reduced-motion behavior specified
- no decorative-only motion in critical flows

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

## Completion Rule

If any category is missing or ambiguous, verdict must be `BLOCKED`.
