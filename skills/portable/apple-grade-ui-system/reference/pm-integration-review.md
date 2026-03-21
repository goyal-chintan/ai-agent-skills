# PM Integration Review (Design-Focused)

Apply this as a blocking quality lens for product coherence.

## Objective

Ensure the feature improves task completion clarity without creating product-model confusion.

## Mandatory Questions

1. Product-model fit
- Does this feature belong in the chosen surface for the user task?
- Is there exactly one canonical place for this job?

2. Clarity vs complexity
- Does the feature reduce user effort or add navigation/cognitive overhead?
- Are we adding controls that duplicate existing capability?

3. Naming and behavior consistency
- Does the feature use existing product terms?
- Are similarly named actions behaviorally identical across screens?

4. Journey integrity
- Are transitions explicit at every critical step?
- Can users recover when operations fail?

5. Integration risk
- Could placement, naming, or behavior conflict with adjacent features?
- Are contradictions resolved before release?

## Blocking Conditions

Return `BLOCKED` if any is true:
- unclear fit to product model
- added complexity without task benefit
- conflicting feature naming/behavior
- unresolved journey integrity gaps
- unresolved integration conflicts with existing flows

## Output

- PM Integration Verdict: `Pass` or `Blocked`
- Product-model fit notes
- Complexity impact notes
- Conflicts found and required fixes
