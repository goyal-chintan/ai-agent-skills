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

11. PM Integration Lens
- Apply checks from `pm-integration-review.md`.
- Block if feature integration adds unresolved product-model conflicts.

12. Verdict
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
