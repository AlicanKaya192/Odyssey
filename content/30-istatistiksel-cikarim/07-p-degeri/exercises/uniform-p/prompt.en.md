Draw two groups from the same population (page load times) and compare them
4000 times: `stats.ttest_ind(a, b, axis=1, equal_var=False)` for every pair
of rows. Print, one per line: the share with `p < 0.05`, the share with
`p < 0.10` (3 places) and how p falls into four equal slices
(`np.histogram(p, bins=4, range=(0, 1))[0].tolist()`).

**Expected output:**

```text
0.048
0.099
[941, 968, 1019, 1072]
```
