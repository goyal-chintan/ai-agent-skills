# Product Integration Mode

Use this mode to turn a feature idea into a fully-integrated product journey before implementation sign-off.

## Objective

Guarantee the feature belongs in the right place, behaves coherently across screens, and is unambiguous for users.

## Required Inputs

- feature intent and trigger
- target user context and task frequency
- existing navigation model and screen inventory
- constraints (platform, design system, technical limitations)

## Required Artifacts

1. Feature intent and trigger
- What user need starts this flow?
- What event/state should surface this feature?

2. Placement decision
- Canonical screen/surface for primary use
- Why this location beats alternatives
- Where configuration should live (if any)

3. Discoverability model
- First discovery point
- Re-entry point
- Education/help point

4. Journey blueprint
- `see -> click -> response -> next step` for critical paths
- Completion outcome state
- Failure and recovery path
- **User mental model check**: for each input in a form or flow, confirm the user naturally *has* that information at the point of entry — if the UI asks them to compute a value they don't know (e.g., "duration" when they know "start time and end time"), redesign to accept their native input
- **CRUD completeness check**: for every create/write operation, confirm a matching delete/remove path exists; if a user can enter incorrect data, they must be able to remove it; absence of delete is a journey discontinuity

5. Consistency audit
- Naming consistency across screens
- No duplicate/contradictory features
- Navigation continuity preserved

6. UI spec handoff
- Completed matrix from [ui-spec-matrix.md](ui-spec-matrix.md)

7. Data flow trace (mandatory for external data features)
- For any feature that fetches, transforms, or displays data from an external source (OS API, network, database, file system), trace the complete data path:
  - **Source**: Where does the data come from? (e.g., `EKEventStore.fetchReminders`, `UNUserNotificationCenter`, API endpoint)
  - **Filter**: What predicates, date ranges, or scope restrictions are applied? Are they intentional and visible to the user?
  - **Transform**: How is the raw data transformed for display? (grouping, sorting, formatting, deduplication)
  - **Display**: What does the user see? Does the displayed result accurately represent the filtered data?
  - **Empty state accuracy**: If the display shows "no items," is it because (a) there truly are no items, (b) the filter is too narrow, (c) permission was denied, or (d) an error occurred silently?
- If any step in the trace is unclear, undocumented, or silently filtering data, return `BLOCKED`.

8. Button-action integrity report
- For every button, toggle, and interactive element in the feature:
  - Trace: label → handler → function → state change → user feedback
  - Confirm the label accurately describes the action
  - Confirm the action has exactly one trigger point
  - Confirm the button only appears in states where its action is valid
- If any button's label does not match its behavior, return `BLOCKED`.

## Blocking Conditions

Return `BLOCKED` if any is true:
- no canonical placement decision
- discovery exists but re-entry missing
- journey has unresolved transition states
- failure/recovery path missing
- configuration is placed in transient surfaces without rationale
- UI spec matrix is incomplete
- data flow trace missing for features that fetch external data
- button-action integrity not verified for interactive elements
- **user mental model check failed**: form inputs require the user to compute values they don't naturally possess
- **CRUD completeness violated**: a create/write operation exists without a corresponding delete/remove path

## Output Template

- Feature Intent
- Placement Decision Record
- Discoverability Map
- Journey Blueprint
- Failure/Recovery Design
- Consistency Audit Results
- Data Flow Trace (for external data features)
- Button-Action Integrity Report
- UI Spec Matrix Status (`Complete` or `Blocked`)
