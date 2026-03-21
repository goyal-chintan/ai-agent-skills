# Functional-Depth Gate

This gate prevents half-complete or unstable UI changes from passing review.

## Required Before PASS

1. Critical path E2E validation
- Run each high-frequency user flow from entry to completion.
- Verify expected state transitions and persistence behavior.

2. Crash and runtime stability
- Confirm no app crash on critical path.
- Confirm no uncaught runtime errors in console/logs for reviewed flows.

3. Regression safety
- Test adjacent flows likely impacted by the change.
- Confirm no broken navigation, state loss, or action failures.

4. Error recovery quality
- Trigger at least one error path.
- Verify user gets clear recovery action (retry, edit, or fallback).

5. Completion integrity
- Confirm feature is not left in placeholder, TODO, or incomplete state.
- Confirm no dead UI controls ("clicks do nothing" or silent failure).

## Auto-Block Functional Triggers

Any trigger below forces `BLOCKED`:
- crash or fatal error during critical flow
- reproducible runtime exception in reviewed area
- critical flow incomplete or non-functional
- regression in adjacent common path
- missing recovery behavior for known failure state

## Button Action Verification

For every button, toggle, and interactive element in reviewed flows:

1. **Trace the action chain**: Label → tap handler → function called → state change → user feedback
2. **Verify label-action match**: The visible text/icon accurately describes the outcome
3. **Confirm single trigger**: The action is triggered from exactly ONE code path. Search for duplicate `.onChange`, callback, or notification handlers that fire the same side effect.
4. **Confirm state validity**: The button only appears in states where its action is meaningful
5. **Confirm completion feedback**: Every tap produces observable change — state update, animation, navigation, or inline confirmation

**Auto-block**: Any button where the traced action chain does not match the label, or where duplicated triggers exist.

## State Machine Completeness

For every stateful component:

1. **Enumerate all states** before reviewing — list every possible state the component can be in, including edge cases (empty, error, boundary, transitional, overtime, stale)
2. **Map all transitions** — for each pair of states, define what triggers the transition and what the user sees
3. **Verify visual treatment** for each state — confirm the UI correctly represents the current state
4. **Test boundary states** — zero items, maximum items, midnight rollover, permission changes mid-session, rapid state transitions

**Auto-block**: Any component where the state enumeration was not performed before review, or where a state exists in code without visual treatment.

## API Error Observability

For every OS or network API call:

1. **No fire-and-forget**: Every async API call must handle its completion/error callback
2. **Error logging**: Failed API calls must log the error with enough context to diagnose (function name, parameters, error description)
3. **User feedback on failure**: If the API failure affects user-visible behavior, the user must be informed (banner, toast, inline message)
4. **Graceful degradation**: If an API is unavailable, the feature must degrade gracefully — not crash, not show broken UI, not silently do nothing

**Auto-block**: Any API call that uses `try?` without logging, ignores completion handler errors, or fails silently on user-visible operations.

## Regression and Patch Quality Checks

After every fix, before marking it complete:

1. **Root-cause verification**: Confirm the fix addresses the underlying cause, not just the visible symptom. Ask: "If I remove this fix, what exact code path causes the bug?" If you cannot answer, the root cause is not understood.
2. **Single-responsibility check**: Confirm each action (save, open window, trigger notification) has exactly ONE trigger point in the codebase. Search for duplicate handlers.
3. **Adjacent flow regression**: After fixing flow A, run flows B and C that share any state, data, or UI surface with A. Document which flows were checked and their results.
4. **Styling composition verification**: If the fix involves any styling modifiers, verify the rendered output matches expectations — code review is insufficient for visual correctness.
5. **No workaround shortcuts**: Reject fixes that use `sleep()`, retry loops, or timing delays to work around race conditions. Require proper state management fixes.

**Auto-block**: Fix that cannot identify its root cause, introduces duplicate triggers, or lacks adjacent flow regression evidence.

## Evidence Format

For each critical flow report:
- Flow name
- Steps executed
- Expected result
- Actual result
- Evidence artifact (log/screenshot/video/test output)
- Pass/Fail

If any critical flow fails, final verdict must be `BLOCKED`.
