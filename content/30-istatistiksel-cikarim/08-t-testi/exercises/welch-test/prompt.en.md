In the design test with 200 people per group
(`make_design_test(n=200, seed=121)`), measure the effect of the new design
(B). Print, one per line: the mean difference B minus A (2 places), the p of
Welch's test (4 places) and the 95% confidence interval of the difference (2
places). The starter code writes `ttest_ind(a, b)`: the interval becomes "A
minus B" and has the opposite sign to the difference.

**Expected output:**

```text
0.26
0.6747
-0.97 1.49
```
