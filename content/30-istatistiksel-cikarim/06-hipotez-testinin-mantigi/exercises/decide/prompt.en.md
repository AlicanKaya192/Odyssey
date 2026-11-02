`decide(values, mu0, alpha)` should run the one-sample t-test
(`stats.ttest_1samp`) and return `[decision, p]`: if `p < alpha` the decision
is `"reject"`, otherwise `"keep"`; p with 4 places. The comparison in the
starter code is reversed.

**Expected output:**

```text
['reject', 0.008]
['keep', 1.0]
```
