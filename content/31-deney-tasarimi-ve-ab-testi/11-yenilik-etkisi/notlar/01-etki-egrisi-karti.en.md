## Reading the curve's direction

```python
def trend(weekly_lifts, tol=0.01):
    change = weekly_lifts[-1] - weekly_lifts[0]
    if change < -tol:
        return "novelty"
    if change > tol:
        return "learning"
    return "stable"


print(trend([0.136, 0.066, 0.048, 0.052]))
print(trend([-0.03, 0.0, 0.02, 0.03]))
print(trend([0.04, 0.05, 0.04, 0.045]))
```

```text
novelty
learning
stable
```

This is a rough reading: weekly lifts are noisy too, and if `tol` is chosen
smaller than the noise every curve looks "changing". The curve is always
drawn and looked at too.

## The two effects side by side

| | Novelty effect | Learning effect |
|---|---|---|
| Cause | curiosity, "something new" | habit, resistance |
| First days | the effect looks large | the effect is small, even negative |
| Over time | fades | grows |
| A short test | optimistic | pessimistic |
| New users | not affected | not affected |

## Quick rules

- At least two full weeks; no decision before the curve flattens.
- Plot the effect per day or per week.
- Read the new-user cohort separately.
- A holdout for the lasting effect.
