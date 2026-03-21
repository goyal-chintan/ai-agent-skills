# Review Output Contract

Gatekeeper reviews must use this exact section order.

## 1) Executive Verdict

One of:
- `PASS`
- `PASS_WITH_RISKS`
- `BLOCKED`

Include one-sentence reason.

## 2) Critical Blockers

- List each blocker with screen reference and consequence.
- If none, write `None`.

## 3) Screen-By-Screen Click Walkthrough

For each critical flow path, provide rows:
- Screen
- What user sees first
- What user clicks/taps
- Immediate response
- Next screen/state

## 4) Placement And Discoverability Map

For each feature/change include:
- first discovery point
- repeat discovery/re-entry point
- where user learns "what this is" (tooltip/help/docs/inline copy)
- why this placement is better than nearby alternatives

## 5) Top 5 Prioritized Fixes

Provide exactly 5 entries in priority order:
- issue
- impact
- fix action
- expected UX outcome

## 6) Re-Review Checklist

Binary checklist (`[ ]` or `[x]`) for:
- primary action clarity
- first-glance hierarchy
- no contradictory/redundant screens
- complete feedback states
- validated discoverability path

## 7) Functional Validation Evidence

For each critical flow include:
- flow name
- steps executed
- expected result
- actual result
- evidence reference (log/screenshot/video/test output)
- pass/fail

If any critical flow fails, final verdict must be `BLOCKED`.

## 8) Explicit Assumptions

List assumptions that influenced the verdict.
If assumptions are high-impact and unverified, verdict cannot be `PASS`.

## 9) Product Integration Artifacts Check

For each required artifact, mark `Complete` or `Blocked`:
- feature intent and trigger
- canonical placement decision
- discovery and re-entry path
- journey blueprint (`see -> click -> response -> next step`)
- failure/recovery path
- completion outcome state

## 10) UI Spec Matrix Completeness

Report completion status for:
- buttons
- information visualization/chart choice
- settings icons
- placement rules
- window/modal/sheet behavior
- new-information request/forms
- dialog/box design
- typography
- colors
- components
- animation

If any category is incomplete, verdict must be `BLOCKED`.

## 11) PM Integration Verdict

Provide:
- product-model fit result
- clarity vs complexity assessment
- cross-feature conflict assessment
- final PM integration verdict (`Pass` or `Blocked`)

## Severity Levels

Use severity tags:
- `P0`: blocks task completion or causes major user error
- `P1`: high-friction issue affecting common flows
- `P2`: quality issue with moderate impact
- `P3`: polish issue
