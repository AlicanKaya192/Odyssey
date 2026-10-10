`ab_report(a, b)` should compare two groups with Welch's test and return a
short report:

- `"diff"`: `b`'s mean − `a`'s mean, 2 places
- `"interval"`: the 95% confidence interval of the difference `[low, high]`, 2
  places
- `"decision"`: `"unclear"` if the interval contains zero, `"b better"` if it
  is entirely above zero, `"a better"` if below

The test: `stats.ttest_ind(b, a, equal_var=False)` and
`.confidence_interval()`.

**Expected output:**

```
11.89 [1.42, 22.36]
b better
```
