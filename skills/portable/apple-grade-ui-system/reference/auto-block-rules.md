# Auto-Block Rules

Any trigger in this file forces verdict `BLOCKED`.

## Interaction Ergonomics Blockers

These physical usability failures make the UI functionally inaccessible for typical users and are always blocking:

- **undersized hit target:** Any tappable or clickable element (button, chip, row, toggle, picker option) that has a visible area smaller than 44×44pt AND does not use `.contentShape(Rectangle())` (or equivalent padding expansion) to meet the minimum. The 44pt rule applies to the *interactive area*, not the visual indicator alone. Verify by checking both the visual size AND the `.contentShape` or `.frame(minWidth:minHeight:)` modifier chain.

- **precision-only hit target on a navigational element:** A disclosure group, accordion, expandable row, or collapsible section where only the disclosure indicator (chevron `>`, arrow, triangle) registers taps — not the full visible row/label area. SwiftUI's native `DisclosureGroup` fails this rule by default; it must be replaced with a custom `Button` + `.contentShape(Rectangle())` covering the full row. Auto-block on any `DisclosureGroup` label that is not wrapped in a tappable container.

- **analog value via precision radio button:** A continuous or multi-step value (effort level, intensity, duration, mood score) is presented as radio buttons, small toggles, or discrete targets that each require precise aim to select. Minimum fix: use a `Slider`, a `Stepper`, a segmented control with adequate spacing, or a tap-anywhere row with a scale. Any input where the user must aim at a target smaller than 44pt to express a value on a spectrum is blocking.

- **text overflow with no recovery path:** A text field, label, or content area that truncates user-generated or system-generated content with `...` (or clips it) and provides no affordance to see the full text (expand, tooltip, scroll, or tap-to-reveal). This is auto-blocking when the truncated content is actionable, data the user entered, or context required to make a decision. Note: truncation is acceptable for decorative/secondary labels where full content is not needed for task completion.

- **interactive area smaller than visual area:** An element that appears large (a card, row, banner, or chip) but only registers taps on a small internal sub-element. The user's mental model is that the whole visible thing is clickable. Verify: does `.contentShape(Rectangle())` or equivalent cover the full perceived hit area?

- **missing `.contentShape` on full-row interactive containers:** Any `HStack`, `VStack`, or `ZStack` used as a button or tap target (via `.onTapGesture` or `Button {}`) that does not apply `.contentShape(Rectangle())`. Without it, taps only register on visible subviews — transparent/empty areas in the row will miss. This must be checked for every list row, calendar cell, and compound tap target.

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

## Contrast, Motion, and Geometry Blockers

These failures are high-impact UX regressions and are always blocking:
- **prominent CTA contrast collision:** Any prominent/filled primary action (`.glassProminent` or equivalent) where label/icon foreground uses the same or near-same hue/value as the fill tint (e.g., blue text on blue fill), resulting in unreadable or low-readability CTA text.
- **unclassified transition intent:** A transition was changed/reviewed without explicit classification as either (a) disclosure/fold behavior or (b) transient feedback behavior. Motion changes without intent classification are auto-blocking.
- **translating fold/disclosure collapse:** Expandable/disclosure content collapses using translating motion (`.move(edge: ...)`) that shifts the container/frame instead of folding in place.
- **first-run geometry instability:** Popover/sheet/window shows abrupt width/height jump on initial render or first toggle/open interaction, with no stabilization evidence.

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

## Window/Popover Orchestration Blockers

Blocking when presentation lifecycle ownership is fragmented or disruptive:
- **commit action leaves popover open:** Any commit action (start/resume/continue/take-break/end-session) executed from menu bar popover does not close the popover immediately after state commit.
- **dual-surface same-intent prompt:** A single intervention decision is rendered simultaneously as both popover prompt and standalone coach window.
- **no single lifecycle owner:** Window/popup open/close/activation behavior is spread across multiple unrelated surfaces without a single orchestrator/policy owner.
- **unbounded app activation:** `NSApplication.shared.activate(...)` is called from multiple ad-hoc paths with no explicit escalation/intent policy.
- **window escalation without popover arbitration:** Strong window escalation opens coach/completion window without explicitly dismissing/settling the popover surface first.

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
- **unapproved visual-language change:** Non-functional style changes (color palette shift, motion-tone shift, typography or icon-style shift) were implemented without explicit user confirmation and without a documented recommendation delta.

## Auto-Block Verdict Format

When blocked, explicitly state:
- trigger(s) that fired
- impacted screen(s)
- user impact
- minimum fix to clear block

## Accessibility Blockers

These failures make the UI inaccessible to users relying on assistive technologies and are always blocking:

- **missing VoiceOver label on interactive element:** Any button, toggle, icon-only control, or custom interactive view that has no `.accessibilityLabel()`. VoiceOver will read a meaningless value (raw variable name, placeholder text, or silence). Every non-decorative interactive element must have an explicit `.accessibilityLabel` that describes the action, not the appearance (e.g., "Start session" not "Play icon").
- **color-only state communication:** Any state, status, or category that is communicated exclusively through color with no secondary indicator (icon, label, pattern, badge). A user who cannot perceive color differences will receive no information. All status indicators must have at least one non-color signal.
- **missing `.accessibilityHint` on non-obvious action:** An interactive element whose label alone does not convey what happens when activated (e.g., "Close" is clear; "Session Ring" is not). Non-obvious controls require `.accessibilityHint` describing the outcome.
- **focus not restored after window dismiss:** When a modal, sheet, or floating window is dismissed, focus must return to the element that triggered it (or to a logical next element). Focus stranded in a dismissed window is a blocking accessibility failure.
- **decorative image without `.accessibilityHidden(true)`:** A non-informational image or icon that VoiceOver will announce unnecessarily. Mark decorative elements with `.accessibilityHidden(true)`.

## Dark Mode and Color Adaptability Blockers

- **hardcoded non-semantic color:** Any use of `Color(.white)`, `Color(.black)`, `Color(red:green:blue:)`, or any hardcoded hex/RGB value in a UI component that will be viewed in both light and dark mode. All UI colors must use semantic tokens (`Color(.label)`, `Color(.systemBackground)`, or the app's design token set) so they adapt automatically. Hardcoded colors are auto-blocking in any component that appears in dark mode.
- **missing dark mode visual verification:** A component was reviewed code-only without a screenshot in both light and dark mode. Even semantic tokens can produce unexpected results under glass/material effects in dark mode. Visual evidence in both modes is required.
- **glass effect on solid-background surface:** Applying `.ultraThinMaterial`, `.regularMaterial`, or similar vibrancy effects on a surface with a solid (non-blurred) background produces a flat grey square with no visual benefit. Glass effects must be used on surfaces with content behind them to blur.

## Performance and Responsiveness Blockers

- **no immediate tap feedback:** Any button, row, or interactive element where tapping produces no visual change within 100ms. The user must see that the tap registered before any async work completes. Acceptable: opacity change, scale pulse, background highlight. Not acceptable: nothing visible until the async operation finishes.
- **long operation without progress indication:** Any user-triggered operation that takes longer than 1 second (data fetch, file write, OS API call) with no loading indicator, progress bar, or activity spinner. The user must never wonder if the app crashed or is working.
- **blocking main thread during UI update:** Any synchronous heavy work (large loop, file I/O, SwiftData batch fetch) on the main actor that causes the UI to freeze visibly. Blocking ops must run on background actors/queues.

## Empty State Quality Blockers

Empty states convey as much product quality as filled states. These are blocking:

- **bare "no items" text without action path:** An empty state that shows only a plain text label ("No sessions", "Nothing here") with no call-to-action, explanation, or next step. Every empty state in a primary content area must include: (a) a human-readable reason why it's empty, and (b) a clear primary action to fill it or change the context.
- **first-use state identical to zero-data state:** The screen shown to a brand-new user who has never performed any action must differ from the screen shown to an established user who filtered everything away. The first-use state must provide onboarding orientation; the zero-results state must help the user adjust context.
- **permission-denied hidden as empty:** A content area that shows "No data" when the real reason is a missing OS permission. The empty state must explicitly tell the user permission is needed and provide a direct path to grant it (System Settings deeplink, not a generic message).

## Notification and In-App Message Quality Blockers

Notifications that are ignored are worse than no notifications — they train users to dismiss everything:

- **generic notification copy:** A notification whose body text would apply to any user at any time (e.g., "Time to focus!", "Don't forget your session!", "You have activity"). Copy must be specific to the user's current context, data, and state. A notification that contains no unique information about the user's situation is auto-blocking.
- **notification with no action path:** A notification that informs but provides no tap action or no deep link. Every notification must either open a specific screen when tapped or contain enough complete information that no tap is needed (purely informational announcements).
- **coach / intervention message that is not data-grounded:** A productivity coaching message that does not reference actual user data (idle time, app usage, session count, day context). Generic motivational copy in a coaching feature is auto-blocking because it trains users to dismiss the coach entirely.

## macOS Platform Convention Blockers

Premium macOS apps must respect platform conventions. Violations signal low quality:

- **standard keyboard shortcut unhandled:** The following must always work: `⌘W` closes the frontmost window, `Esc` dismisses a modal/sheet/popover, `⌘Q` quits the app, `⌘,` opens Settings/Preferences. Any of these shortcuts failing to work as expected is auto-blocking.
- **window presented as `.sheet` when it should be independent:** Data-entry flows that the user should be able to position or that must survive navigation changes should be standalone windows, not `.sheet` modals that block the parent view. Critical distinction for macOS companion app patterns.
- **no `defaultFocus` on text input in a form window:** When a form window or sheet opens, the first text input field must receive keyboard focus automatically. Requiring the user to click into a text field they obviously need to type into is a macOS convention failure.
