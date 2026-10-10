`diff_interval(a, b)` should take the 95% confidence interval of the mean
difference `b − a` from Welch's test:
`stats.ttest_ind(b, a, equal_var=False).confidence_interval(0.95)`. Return
`[low, high, contains_zero]`: the limits with 2 places, the last item whether
the interval contains 0 (`bool`).

**Expected output:**

```
[1.42, 22.36, False]
```
