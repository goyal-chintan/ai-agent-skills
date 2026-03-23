# Test Scenarios

Use these scenarios to validate the skill behavior.

## 1) New Feature Insertion (Discoverability)

Setup:
- add a new feature with UI on one screen only
- no navigation entry or in-context discovery cue

Expected:
- review returns `BLOCKED`
- identifies missing first discovery and re-entry paths
- proposes concrete placement map

## 2) Redundancy / Contradiction

Setup:
- two screens expose same capability under different names
- action labels conflict (e.g., "Archive" vs "Hide" for same behavior)

Expected:
- review returns `BLOCKED`
- names duplicate destination and contradiction points
- provides consolidation recommendation

## 3) Hierarchy / Sizing Failure

Setup:
- oversized cards/buttons push key status below fold
- decorative sections dominate top viewport

Expected:
- review returns `BLOCKED`
- calls out first-glance hierarchy failure
- prescribes resizing and information reorder

## 4) Interaction Feedback Failure

Setup:
- submit action has no loading indicator
- failure state has no error message
- success state has no confirmation

Expected:
- review returns `BLOCKED`
- enumerates missing states and affected flows

## 5) Golden Path

Setup:
- coherent naming and navigation
- clear first-glance hierarchy
- complete feedback states
- discoverability path present

Expected:
- review returns `PASS` or `PASS_WITH_RISKS`
- only minor `P2`/`P3` recommendations allowed

## 6) Crash And Stability Failure

Setup:
- feature compiles but crashes during one critical action
- runtime console/log shows uncaught error

Expected:
- review returns `BLOCKED`
- cites failing flow and crash evidence
- requires root-cause fix plus regression retest evidence

## 7) Feature Ideation To Journey Completeness

Setup:
- input is only a high-level feature idea
- no explicit placement or interaction details provided

Expected:
- review requires full Product Integration artifacts
- if artifacts are missing, returns `BLOCKED`
- output includes a complete journey blueprint before implementation pass

## 8) UI Spec Matrix Incompleteness

Setup:
- proposal omits button state details, chart rationale, and modal behavior

Expected:
- review returns `BLOCKED`
- identifies missing matrix categories explicitly

## 9) Placement Conflict Across Screens

Setup:
- same feature appears in two screens with different names and behavior

Expected:
- review returns `BLOCKED`
- demands canonical ownership and consistency fix

## 10) Interaction Continuity Gap

Setup:
- action opens window/sheet but next step and close/recovery behavior are undefined

Expected:
- review returns `BLOCKED`
- cites journey discontinuity and required transition specification

## 11) Button Label-Action Mismatch

Setup:
- a button labeled "Continue Focusing" is wired to a no-op handler or wrong function
- OR a button labeled "Save & End" dismisses the window but does not save

Expected:
- review returns `BLOCKED`
- traces the action chain: label → handler → function → state change
- identifies the disconnect and requires the handler to match the label exactly
- verifies no other button has a duplicate trigger for the same action

## 12) Incomplete State Machine

Setup:
- a timer component has 7 possible states (idle, focusing, paused, overtime, break, break-overtime, manual-stop)
- the review only checks 4 states visually (idle, focusing, paused, break)
- overtime, break-overtime, and manual-stop states have no defined visual treatment or were not examined

Expected:
- review returns `BLOCKED`
- requires enumeration of ALL 7 states before proceeding
- each state must have: defined visual treatment, entry/exit transitions, user feedback
- edge cases (rapid state changes, boundary times, stale states on app relaunch) must be addressed

## 13) Rendering Composition Error

Setup:
- a button uses `.tint(Color.red)` combined with `.buttonStyle(.glass)` — this looks correct in code but renders as an opaque red blob that destroys the glass translucency effect
- OR multiple material/opacity layers are stacked, creating muddy visual banding
- OR `.foregroundStyle()` is set on a label inside `.glassProminent`, overriding the system's automatic label coloring

Expected:
- review returns `BLOCKED`
- requires visual verification (screenshot/rendered output) — code review alone is insufficient
- identifies the specific compositing conflict
- prescribes the correct combination (e.g., use `.glassProminent` + `.tint()` but NOT `.glass` + `.tint()`)

## 14) Silent API Failure

Setup:
- notification scheduling uses `UNUserNotificationCenter.add(request)` without a completion handler
- OR calendar event creation uses `try?` without logging the error
- OR reminder fetch succeeds but returns 0 results due to a hidden date filter, showing "No reminders" when reminders exist

Expected:
- review returns `BLOCKED`
- requires error logging on every OS API call (completion handler, do/catch with logging)
- requires user-visible feedback when an API operation fails
- requires data scope verification: trace the fetch predicate to confirm it matches user intent, not a silently narrow filter

## 15) Patch Quality Violation

Setup:
- a race condition causes a window to open and immediately close
- the "fix" adds `Task.sleep(nanoseconds: 500_000_000)` before opening the window
- OR the "fix" adds a second `.onChange` handler that opens the same window (creating a duplicate trigger)
- OR the "fix" uses `try?` to suppress an error that was causing a crash (hiding the bug instead of fixing it)

Expected:
- review returns `BLOCKED`
- requires root-cause analysis: identify WHY the race condition exists, not just delay the timing
- requires single-trigger verification: search for all code paths that trigger the same side effect
- requires regression evidence: after fix, verify adjacent flows still work
- prescribes: consolidate to one trigger, use proper state management, log errors instead of swallowing

## 16) Wrong Input Widget For Content Type

Setup:
- a "notes", "achievement", "description", or "reflection" field uses a single-line `TextField`
- the user attempts to write a multi-line entry and cannot because the input does not expand or accept newlines

Expected:
- review returns `BLOCKED`
- identifies the field name, current widget type, and required widget type
- confirms that `TextEditor` (or equivalent multiline widget) is required for any content that may span multiple sentences or lines
- verifies the replacement widget uses the app's design system (glass effect, correct padding, placeholder via ZStack overlay)

## 17) Missing Input For User's Natural Information

Setup:
- a "Log Session" form asks the user to enter a "Duration" (15 / 25 / 45 / 60 min presets)
- the user knows they started at 2:00pm and finished at 3:20pm, but does not know the exact duration
- the form has no "Ended at" field — the user must mentally compute 80 minutes and enter it manually

Expected:
- review returns `BLOCKED` on user mental model mismatch
- identifies that the user naturally possesses a start time and end time, not a duration
- requires the form to accept start + end time and derive duration, not the reverse
- if both duration preset AND end time picker are present for flexibility, this check passes

## 18) CRUD Completeness Violation

Setup:
- a feature allows the user to log, create, or record data (sessions, entries, records)
- no delete or remove path exists — incorrect data cannot be corrected
- the session list shows entries from testing that the user cannot remove

Expected:
- review returns `BLOCKED` on CRUD completeness violation
- identifies the create surface and the missing delete surface
- requires a delete action protected by a destructive confirmation dialog (no undo required if confirmation exists)
- verifies the delete removes all child records (cascade) to prevent orphaned data

## 19) Code-Only Review (No Live Execution Evidence)

Setup:
- reviewer reads the code and diff carefully
- reviewer issues a `PASS` verdict
- no screenshots, screen recordings, or console logs from running the app are provided
- a data-sync bug exists: after a manual action, a derived value in another view does not update
  (e.g., menu bar total does not refresh after logging a session manually)

Expected:
- review returns `BLOCKED` immediately at the evidence check stage
- the block fires before any code analysis begins: "rendered evidence missing — cannot proceed"
- the data-sync bug (which is invisible in code but immediately visible on screen) is cited as proof of why live execution is mandatory
- reviewer must provide at minimum: screenshot of the UI before the action, screenshot after the action, and confirmation that all derived values updated correctly

## 20) Precision-Only Hit Target (DisclosureGroup / Small Indicator)

Setup:
- a collapsible section uses SwiftUI `DisclosureGroup` with a label and chevron
- the user must tap the tiny `>` chevron to expand/collapse the section
- tapping anywhere else on the row label does nothing
- a separate section uses radio buttons (small circles ~20pt) to capture an effort level from 1–5

Expected:
- review returns `BLOCKED` on both elements
- identifies `DisclosureGroup` as the precision-only failure: only the chevron is tappable, not the full row
- requires replacement with `Button {} label: { rowContent }` + `.contentShape(Rectangle())` for the full row
- identifies radio buttons as an analog-value precision failure: effort/intensity values require slider or large segmented control
- requires minimum 44×44pt per interactive target, or a slider/stepper replacing the radio buttons
- reviewer must trace `.contentShape` usage — absence is the evidence of the bug

## 21) Text Truncation on User-Generated Content

Setup:
- a session history row shows an achievement text field
- the text is clipped to a single line with "..." at the end
- the user entered "Completed intro outline + chapter 1 draft\nAlso pushed a deploy" but sees only "Completed intro outline + chapter..."
- no tap-to-expand affordance exists on the row

Expected:
- review returns `BLOCKED`
- identifies the field as user-generated content that must not truncate without recovery
- checks `.lineLimit` usage — if `1` is set on a user-entered field, this is the root cause
- requires `.lineLimit(nil)` + `.fixedSize(horizontal: false, vertical: true)` for wrapping
- OR a tap-to-expand row that shows full content in a sheet/detail view
- verifies the fix does not break the row height in a list (check with long content AND single-word content)

## 22) Undersized Interactive Area in Compound Container

Setup:
- a chip, tag, or compact row is used as a button (e.g., skip reason chips, effort chips, app filter chips)
- the chip visual is 32×24pt with text and an emoji
- no padding expansion or `.contentShape(Rectangle())` is applied
- the user must tap exactly on the text or emoji to register the tap; tapping 3pt outside the text misses

Expected:
- review returns `BLOCKED` on undersized hit target
- measures or estimates visual size vs required 44pt minimum
- verifies `.contentShape(Rectangle())` is applied OR `.frame(minHeight: 44)` padding wraps the chip
- for chips in a flow layout (chips that wrap to multiple rows): each chip must individually meet the 44pt height requirement, even if the visual chip itself is shorter
- the fix must not require restructuring the layout — typically a `.padding(.vertical, 10)` inside the button frame is sufficient
- reviewer must confirm the fix was applied to ALL chips in the same component family, not just the one that was reported

## 23) Missing VoiceOver Label on Interactive Element

Setup:
- an icon-only button (e.g., `Image(systemName: "play.fill")`) is used as a primary action
- no `.accessibilityLabel()` is applied
- VoiceOver will either read silence or the raw system name "play.fill"

Expected:
- review returns `BLOCKED`
- identifies every icon-only button, custom control, and non-obvious interactive element
- requires `.accessibilityLabel("Start session")` or equivalent action-describing text
- NOT appearance-describing text ("Play icon") — the label must describe the action
- also flags any `.onTapGesture` containers without `.accessibilityElement(children: .combine)` + `.accessibilityLabel`

## 24) State Communicated Only Through Color

Setup:
- a session status is shown as a green/yellow/red circle with no text label
- a streak indicator turns blue when active and grey when inactive — no text or icon change

Expected:
- review returns `BLOCKED`
- identifies every color-coded state in the UI
- requires at least one non-color signal: icon shape change, text label, badge, or pattern
- example fix: green circle → green circle + "Active" label; grey circle → grey circle + "Paused" label
- a tooltip or hover-only reveal of the label is NOT sufficient — the primary state must be non-color-identifiable

## 25) Hardcoded Color Breaks in Dark Mode

Setup:
- a card component uses `Color(.white).opacity(0.15)` as its background in a glass effect
- in light mode it looks correct; in dark mode the white tint on a dark background creates a muddy grey appearance
- OR: a text label uses `Color(.black)` explicitly; in dark mode, the text becomes invisible on a dark background

Expected:
- review returns `BLOCKED`
- requires visual evidence in BOTH light and dark mode
- hardcoded `Color(.white)` / `Color(.black)` / `Color(red:green:blue:)` in any UI component auto-blocks
- correct fix: `Color(.label)` for text, `Color(.secondarySystemBackground)` for backgrounds, or app design token equivalents
- glass effects: use opacity values relative to the system material, not hardcoded white/black overlay

## 26) Generic Notification Copy (All Users, All Times)

Setup:
- focus coach sends: "Time to focus! Start a session now."
- the copy is identical regardless of whether the user has been idle 5 minutes or 2 hours
- the copy is identical regardless of whether the user is on track for their daily goal or far behind
- no user name, no session count, no idle time, no app context

Expected:
- review returns `BLOCKED`
- copy must reference at minimum ONE data point specific to this user and moment
- example: "You've been on Chrome for 38 min — your goal is 2 sessions today and you have 0 complete."
- generic motivational quotes may accompany data-grounded copy but cannot replace it
- a review that approves coaching messages without reading the actual copy text is invalid

## 27) Long Operation With No Loading State

Setup:
- user taps "Generate weekly insights"
- the app performs a 3-second data aggregation and report generation
- during those 3 seconds, the button shows no change, the content area shows no spinner, nothing indicates activity
- then suddenly the result appears

Expected:
- review returns `BLOCKED`
- every user-triggered operation >1s must show an immediate visual change: spinner, skeleton, progress bar, or button loading state
- the visual feedback must appear BEFORE the async work starts (synchronously, within the tap handler)
- acceptable: button goes to `.disabled` + `.opacity(0.6)`, content area shows `ProgressView()`
- not acceptable: nothing changes until the result is ready

## 28) Prominent CTA Same-Hue Contrast Collision

Setup:
- a shared primary button component uses `.glassProminent` for fill styling
- label/icon foreground is derived from the same tint token as the fill (e.g., `foregroundStyle(tint)`)
- on one surface, CTA appears as blue text on blue fill and looks washed out

Expected:
- review returns `BLOCKED`
- identifies shared component invariant breach (not just a one-screen bug)
- requires foreground token override to maintain contrast across all prominent CTA variants
- verifies all dependent CTA surfaces after component-level fix

## 29) Fold vs Transient Motion Intent Confusion

Setup:
- collapsible section uses `.transition(.move(edge: .top).combined(with: .opacity))`
- user reports section appears to "jump upward and disappear" instead of folding
- same codebase also contains transient banners that intentionally slide

Expected:
- review returns `BLOCKED` if transitions were not intent-classified
- classifies each transition as disclosure/fold vs transient feedback
- requires disclosure/fold surfaces to use non-translating collapse behavior
- preserves intentional transient entry motion where product intent requires it

## 30) First-Run Popover Geometry Jump

Setup:
- menu bar popover appears stable at launch
- first time user expands a card/section, popover width increases abruptly
- subsequent toggles are mostly stable, so steady-state review misses the defect

Expected:
- review returns `BLOCKED`
- explicitly calls out missing first-run geometry validation
- requires evidence for initial render + first interaction + repeated interactions
- requires layout stabilization for intrinsic width/height pressure paths

## 31) Commit Action Leaves Popover Open

Setup:
- user taps "Start Focus Session" from menu bar popover
- state transitions to focusing, but popover remains open
- subsequent windows/prompts may appear while popover is still visible

Expected:
- review returns `BLOCKED`
- identifies missing post-commit popover dismissal as orchestration defect
- requires single-commit/single-surface behavior with explicit close action

## 32) Strong Prompt Duplicated Across Surfaces

Setup:
- strong coach intervention escalates to standalone coach window
- same decision also appears as popover quick prompt simultaneously

Expected:
- review returns `BLOCKED`
- flags dual-surface same-intent conflict
- requires one primary surface per decision cycle and suppression of duplicate prompt surfaces

## 33) Fragmented Activation Ownership

Setup:
- app activation (`NSApplication.shared.activate`) is called in multiple unrelated view-model/view paths
- behavior differs by entry path and causes unpredictable focus jumps

Expected:
- review returns `BLOCKED`
- requires explicit activation policy and single orchestration owner
- requires lifecycle mapping that shows where activation is allowed vs disallowed
