## A small Simpson example

```python
import pandas as pd

cells = pd.DataFrame({"week": [1, 1, 2, 2],
                      "group": ["A", "B", "A", "B"],
                      "buyers": [180, 22, 50, 52],
                      "users": [1500, 170, 1000, 1000]})
cells["rate"] = cells["buyers"] / cells["users"]
print(cells.pivot(index="week", columns="group", values="rate").round(3))
total = cells.groupby("group")[["buyers", "users"]].sum()
print((total["buyers"] / total["users"]).round(3).to_string())
share = cells.groupby("week")["users"].sum() / cells["users"].sum()
rates = cells.pivot(index="week", columns="group", values="rate")
print(round(((rates["B"] - rates["A"]) * share).sum(), 4))
```

```text
group     A      B
week              
1      0.12  0.129
2      0.05  0.052
group
A    0.092
B    0.063
0.0054
```

B is ahead in both weeks and behind in total; the stratified difference is
positive again.

## The stratified estimate step by step

1. In each stratum (week, platform...) compute the two groups' rates
   separately.
2. In each stratum take the difference: B − A.
3. Weight the differences by the stratum's share of **all** users and add
   them up.

Since the weight is the same for both groups, the difference in mix goes
away.

## When is it needed?

- When the assignment ratio changed mid-test (a slow opening).
- When there is SRM in one stratum but not in another (find the cause
  first).
- When strata behave very differently and the make-up is unbalanced
  between groups.

If assignment has the same ratio everywhere, the stratified estimate and
the total give almost the same result.
