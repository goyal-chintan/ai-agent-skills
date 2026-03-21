# Weak Output Diagnosis

Run this pre-check before final verdict.

## Trigger 1: Style-Only Polish

Fail if output focuses on visuals but lacks:
- task structure rationale
- interaction logic
- flow continuity

## Trigger 2: Missing Placement Rationale

Fail if feature placement was chosen without:
- discovery-path reasoning
- re-entry strategy
- comparison with adjacent placement options

## Trigger 3: No Contradiction Audit

Fail if review did not explicitly check:
- redundant screens
- conflicting names for same concept
- contradictory actions across similar surfaces

## Trigger 4: Weak First-Glance Hierarchy

Fail if first viewport does not clearly surface:
- primary action
- top-priority status/info
- next-step affordance

## Trigger 5: Incomplete Feature Journey

Fail if the output lacks:
- entry and re-entry path
- clear transition states
- recovery and completion states

## Trigger 6: UI Spec Ambiguity

Fail if core visual/interaction details are unspecified:
- buttons, chart choice, settings icon behavior
- window/modal behavior
- form/data request behavior
- typography/color/component/motion rules

## Trigger 7: Button-Behavior Disconnect

Fail if any button's visible label does not match its actual coded behavior:
- button text says one thing but the wired action does another (or nothing)
- action is wired to the wrong function or a no-op handler
- button appears in states where its action is invalid
- destructive action has no confirmation or undo path
- same action is triggered from multiple independent code paths (race condition risk)

## Trigger 8: Incomplete State Coverage

Fail if a stateful component was reviewed without first enumerating ALL its possible states:
- reviewer checked some states but not all (e.g., 4 of 7 timer states)
- edge-case states (empty, error, boundary, overtime, stale) were not considered
- transitional states (between two stable states) have no defined visual treatment
- state exists in code but was not reviewed for UI quality

## Trigger 9: Styling Composition Unverified

Fail if styling modifier combinations are assumed correct from code alone:
- tint + glass/translucent button styles compose to unexpected opaque blobs
- material + overlay stacking creates muddy visual banding
- opacity layers compound into unintended darkness
- foreground color overrides design system's automatic label coloring
- the rendered output was never visually verified — only the code was reviewed

## Trigger 10: Silent Error Paths

Fail if OS or network API calls can fail without any observable evidence:
- `try?` swallows errors without logging on user-visible operations
- completion handlers ignore error parameters
- notification/calendar/reminder API calls have no error callback
- API failure produces no user feedback (silent no-op)
- feature "works" in code but never actually reads/writes real data in the OS

## Trigger 11: Patch and Workaround Detection

Fail if any fix uses shortcuts instead of addressing root cause:
- timing workaround (sleep/delay) used to mask a race condition
- duplicate code path added instead of consolidating to single trigger
- fix applied without checking if adjacent flows still work
- hardcoded magic values without documented rationale
- fix for bug A introduces or re-introduces bug B

## Trigger Handling

If any trigger fails:
- verdict cannot be `PASS`
- add blocker in "Critical Blockers"
- include minimum corrective action
