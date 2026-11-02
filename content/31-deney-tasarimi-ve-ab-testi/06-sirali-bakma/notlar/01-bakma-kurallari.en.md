## The Bonferroni threshold by number of looks

```python
for looks in [1, 2, 7, 14]:
    print(looks, round(0.05 / looks, 4))
```

```text
1 0.05
2 0.025
7 0.0071
14 0.0036
```

Bonferroni is always safe, but since the looks see the same accumulating
data it is stricter than needed. A threshold calibrated by simulation
(Pocock type) or O'Brien–Fleming boundaries lose less power.

## Rules

| Allowed | Not allowed |
|---|---|
| Reading the result on the planned last day | Looking at p every day and stopping when significant |
| Stopping when a guardrail metric breaks | Extending the duration "to wait a bit longer" |
| Stopping early with a sequential design written in advance | Choosing sequential thresholds during the test |
| Watching the trend on a dashboard (without deciding) | Announcing an interim result to the team as "we are winning" |

## What goes into the plan

- How many looks, on which days.
- The threshold of each look.
- Whether early stopping is only for a win or also for harm.
- How the decision is made at the end of the duration.
