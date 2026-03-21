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
