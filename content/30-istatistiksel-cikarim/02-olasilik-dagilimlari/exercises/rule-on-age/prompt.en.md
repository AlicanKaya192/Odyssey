Does the 68–95–99.7 rule hold for the `age` column? For `k` = 1, 2, 3, print
on one line `k`, the standard normal's share between `-k` and `k`
(`stats.norm.cdf(k) - stats.norm.cdf(-k)`) and the real share of ages at
most `k` standard deviations from the mean (4 places).

**Expected output:**

```text
1 0.6827 0.661
2 0.9545 0.9749
3 0.9973 0.9986
```
