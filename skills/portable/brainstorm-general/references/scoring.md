# Scoring Rubric

Rate each shortlisted option from 1-5 on each metric.

## Metrics
- Impact: Expected upside if it works.
- Effort: Total cost in time/energy/resources.
- Risk: Probability and severity of downside.
- Confidence: Current evidence quality.
- Reversibility: Ease of rollback if wrong.

## Default Weighted Score
Use this unless the user asks for a custom weighting:

Score = (Impact * 0.35) + (Confidence * 0.25) + (Reversibility * 0.15) - (Effort * 0.15) - (Risk * 0.10)

## Confidence Gates
- 0.80+: strong evidence; proceed to limited rollout.
- 0.60-0.79: run a focused experiment before scaling.
- <0.60: hold; refine assumptions and re-test.

## Tie-Breakers
If scores are close:
1. Pick the faster-learning option.
2. Pick the more reversible option.
3. Pick the option with lower catastrophic downside.

## Failure-Mode Prompt
For each top option, capture:
- Most likely failure mode
- Earliest warning signal
- Mitigation or fallback
