`paired_p(before, after)` should find the paired t-test's p without
`ttest_rel`: compute the differences (`before - after`) and test them against
0 with `ttest_1samp`; return p with 4 places. The starter code tests
`before` against the mean of `after`: it forgets the partners.

**Expected output:**

```text
0.0037
```
