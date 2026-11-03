# Novelty Effects and Long-Term Impact

An A/B test looks through a short window: two weeks, a month. The effect of
the decision lasts for months. The two do not always say the same thing.
A new button or a new design gets clicked in the first days out of
**curiosity**; this rise fades over time. This is called the **novelty
effect**. The opposite happens too: users first resist a change that breaks
their habits, then get used to it (the **learning effect**, primacy). This
section measures how the first days of a test can misstate the long-term
effect.

## The effect day by day

In a test that runs for 28 days we follow users' daily clicks. We made the
data: B's lasting effect is 4%. Users who know the old design get a novelty
bonus on top: 20% on the first day, halving every three days. New users who
never saw the design (20%) get no bonus.

```python
import numpy as np
from ab_data import make_novelty_test

clicks = make_novelty_test()
daily = clicks.groupby(["day", "group"])["clicks"].mean().unstack()
lift = daily["B"] / daily["A"] - 1
print(lift.iloc[[0, 2, 6, 13, 20, 27]].round(3).to_string())
```

```text
day
1     0.190
3     0.153
7     0.100
14    0.059
21    0.054
28    0.058
```

On the first day B is 19.0% ahead; by the fourth week the lift
drops to around 5.8%. Nothing broke: users got used to the new
thing.

## What would a one-week test have said?

```python
clicks["week"] = (clicks["day"] - 1) // 7 + 1
weekly = clicks.groupby(["week", "group"])["clicks"].mean().unstack()
print((weekly["B"] / weekly["A"] - 1).round(3).to_string())
```

```text
week
1    0.136
2    0.066
3    0.048
4    0.052
```

A test that looks only at the first week would have reported the effect as
13.6%; the lasting effect is 4%. If the product decision, the
investment case and the expected revenue are built on this number, they
are three times too optimistic. So as not to tie this to one data set, let
us build the same test with 20 different seeds:

```python
first, last = [], []
for s in range(100, 120):
    t = make_novelty_test(n=10000, seed=s)
    t["week"] = (t["day"] - 1) // 7 + 1
    w = t.groupby(["week", "group"])["clicks"].mean().unstack()
    lift_w = w["B"] / w["A"] - 1
    first.append(lift_w[1])
    last.append(lift_w[4])
print(round(float(np.mean(first)), 3), round(float(np.mean(last)), 3))
```

```text
0.122 0.037
```

The first week averages 12.2%, the fourth week 3.7%:
the difference is not chance, it comes from the design itself.

## New users: those who never saw the novelty

For someone who never saw the old design, B is not "new"; it is just the
design. That is why the effect for new users is close to the lasting
effect from the start:

```python
for new, part in clicks.groupby("is_new"):
    w = part.groupby(["week", "group"])["clicks"].mean().unstack()
    print(new, (w["B"] / w["A"] - 1).round(3).tolist())
```

```text
False [0.16, 0.073, 0.047, 0.053]
True [0.04, 0.038, 0.054, 0.047]
```

For existing users (`False`) the first week is 16.0%, for new
users (`True`) 4.0%. The new users' first week looks like the
existing users' last week. If the two groups' curves come together, there
is a novelty effect; the new-user curve is an early estimate of the lasting
effect. (New users are fewer, so their numbers are noisier.)

## What to do?

- **Run the test long enough:** at least two full weeks; until the effect
  curve flattens.
- **Plot the effect over time:** the lift per day or per week. A falling
  curve is novelty, a rising curve is learning.
- **Separate new and existing users:** the new-user cohort gives a view
  free of novelty.
- **A long-term holdout:** after the change is opened to everyone, a small
  group (e.g. 5%) is kept on the old version for months; the lasting effect
  is measured against it.

Stopping early has its own cost here: a test that stops early under the
rules of the Peeking Trap and Sequential Testing section may stop before
the novelty has faded.

## Summary

- The novelty effect enlarges the effect in the first days, then fades;
  the learning effect does the opposite.
- In this section's data, a one-week test exaggerates the lasting effect
  three times.
- Plotting the effect over time and reading new users separately makes
  both effects visible.
- The lasting effect needs a long test or a holdout.
