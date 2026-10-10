`compare_groups(a, b)` should compare two independent groups with **Welch's**
t-test (`stats.ttest_ind(b, a, equal_var=False)`: the spreads and group sizes
differ). Return `[difference, p, significant]`: the difference is `b`'s mean
minus `a`'s (2 places), p with 4 places, significant is `p < 0.05`
(`bool`). The starter code assumes equal spreads.

**Expected output:**

```
[11.89, 0.0302, True]
```
