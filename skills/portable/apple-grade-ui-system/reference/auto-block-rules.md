# Auto-Block Rules

Any trigger in this file forces verdict `BLOCKED`.

## Core UX Blockers

1. Primary action unclear
- The main user action is visually weak, ambiguous, or displaced.

2. Key information buried
- First-glance essentials are pushed below fold or hidden behind unnecessary interactions.

3. Redundancy and contradiction
- Multiple screens claim the same job with conflicting naming, layout logic, or actions.

4. Missing feedback states
- Critical actions lack loading, error, or success behavior.

5. Discoverability gap
- New feature has no clear first-discovery path and no reliable re-entry path.

6. Functional instability
- Crash, fatal runtime error, or non-working critical path in reviewed flows.

7. Product integration incompleteness
- Missing feature journey blueprint artifacts (intent, placement, discovery, transition, recovery, completion).

8. Placement conflict
- Same feature behavior appears in conflicting surfaces without canonical ownership.

9. UI spec ambiguity
- Button/chart/icon/modal/form/animation behavior is unspecified or internally inconsistent.

10. Journey discontinuity
- User can perform an action but no clear next state or recovery path is defined.

## Anti-AI Style Blockers (Bounded Section)

Use these as style hygiene checks, not full UX strategy:
- decorative hero-like copy inside internal product surfaces without product need
- default metric-card dashboard layout as first instinct when task model does not require it
- oversized radii/pills or floating-glass shells that reduce clarity
- decorative gradients/shadows/glows used instead of hierarchy and information structure
- ornamental labels/badges that add noise but no decision value

A style issue is auto-blocking only when it damages clarity, hierarchy, or task completion.

## Visual Compositing Blockers

These compositing errors create visible rendering artifacts and are always blocking:
- **tint-on-glass:** `.tint()` applied to `.buttonStyle(.glass)` or `.glassProminent` creates opaque color blobs that destroy translucency. Use `.foregroundStyle()` on text/icons instead.
- **double-material stacking:** `.ultraThinMaterial` (or any material) as page background under `LiquidGlassPanel` or `.glassEffect()` containers creates grey/black color banding. Use only ONE layer of glass/material compositing.
- **stacked opacity layers:** Multiple `.background(Color.x.opacity(n))` layers that compound into unintended darkness or muddiness.

## Data Scope and Filter Blockers

These silently hide data from users and are always blocking:
- **hidden date filter:** A fetch call uses date bounds (start/end) but the UI shows no indication of the active date range, causing a misleading "empty" state.
- **hidden list/scope filter:** Data is filtered to a specific list/calendar/category but the UI does not name the active filter or offer a way to change it.
- **user has data but sees empty:** If the OS data store has items but the view shows "No items," the filter logic is wrong — the empty state must distinguish "truly empty" from "filtered empty."

## Visual Richness Floor Blockers

Blocking when a content area fails minimum visual engagement:
- **monochrome intensity:** A data grid (calendar, heatmap, chart) uses only one color/opacity level for all data values — must vary by intensity.
- **missing selection depth:** Selected items have only a background color change — must also have glow, shadow, or scale to convey depth.
- **invisible today/current indicator:** "Today" or "current" marker uses < 1.5px stroke at < 50% opacity — must be visually prominent without user effort.
- **no interactive feedback:** Clickable grid cells or list rows have no hover, press, or active state change.

## OS Integration Error Logging Blockers

Blocking when OS API calls can fail silently:
- **notification fire-and-forget:** `UNUserNotificationCenter.add(request)` called without completion handler — errors are invisible.
- **calendar/reminder write without verification:** `EKEventStore.save()` called with `try?` and no error surfacing to user or logs.
- **custom notification sound referencing non-bundled asset:** `UNNotificationSound(named:)` with a filename that doesn't exist in the app bundle — notification silently fails.

## Button-Behavior Mismatch Blockers

Blocking when a button's visible label does not match its actual coded behavior:
- **label-action disconnect:** Button text says "Continue Focusing" but the wired action is a no-op, calls the wrong function, or does something unrelated (e.g., dismisses the window without starting focus).
- **silent no-op button:** Button exists in the UI, has an action handler, but the handler does nothing observable — no state change, no navigation, no feedback.
- **duplicate action trigger:** The same side effect (e.g., opening a completion window, saving a session) is triggered by TWO OR MORE independent code paths. This causes race conditions, double-execution, or conflicting state.
- **state-inappropriate button:** Button appears in a state where its action is invalid or nonsensical (e.g., "Pause" appears when already paused, "Start Break" appears during a break).
- **destructive action without protection:** A button that deletes data, discards progress, or ends a session has no confirmation dialog and no undo path.

## State Coverage Blockers

Blocking when a component's state space is not fully reviewed:
- **unenumerated states:** A stateful component (timer, form, integration toggle, workflow) is reviewed without first listing ALL possible states. If the reviewer did not enumerate states before reviewing, the review is invalid.
- **unchecked state visual treatment:** A state exists in code but has no defined visual treatment — the user sees a broken, default, or inappropriate UI in that state.
- **missing transition definition:** The transition between two states has no defined trigger, no user feedback, and no visual change.
- **edge-case state ignored:** Boundary conditions (zero items, maximum items, midnight boundary, network timeout, permission revoked mid-use) were not considered.

## Patch Quality Blockers

Blocking when a fix creates new problems or uses shortcuts instead of addressing root cause:
- **timing workaround:** `sleep()`, `Task.sleep()`, `DispatchQueue.asyncAfter()`, or any delay used to work around a race condition or async timing issue instead of fixing the underlying state management. (Intentional animation delays with documented rationale are exempt.)
- **duplicate trigger introduced:** Fix adds a second code path for the same side effect (e.g., adding `.onChange` handler when a callback already exists for the same action), creating a race condition.
- **silent error swallowing:** `try?` without logging, completion handlers that discard error parameters, or API calls that never surface failures to user or developer on user-visible operations.
- **styling assumed correct:** Styling modifier combinations (tint + glass, material + overlay, opacity stacking) are assumed correct from code review without rendered visual verification. The combination may look correct in code but render incorrectly.
- **fix-introduces-regression:** Fixing bug A re-introduces or creates bug B in an adjacent flow. No evidence was gathered that adjacent flows still work after the fix.
- **hardcoded magic values:** Magic numbers for timing (sleep 600ms), sizing, or positioning without documented rationale or derivation from design tokens.

## Auto-Block Verdict Format

When blocked, explicitly state:
- trigger(s) that fired
- impacted screen(s)
- user impact
- minimum fix to clear block
