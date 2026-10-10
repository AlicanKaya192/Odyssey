`click_test(table)` should test a contingency table of the form `[[clicked,
not_clicked], ...]` with `stats.chi2_contingency`. Return:

- `"stat"`: the chi-square value, 2 places
- `"dof"`: the degrees of freedom
- `"significant"`: `p < 0.05` (`bool`)
- `"expected"`: the expected counts, a list of lists with 1 place

**Expected output:**

```
26.07 1 True
[[67.5, 82.5], [67.5, 82.5]]
```
