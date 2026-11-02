`iqr_outliers(values)` should return the values outside the 1.5 × IQR
rule as a sorted list. `q1, q3 = np.percentile(values, [25, 75])`,
`iqr = q3 - q1`; the lower limit is `q1 - 1.5 * iqr`, the upper limit
`q3 + 1.5 * iqr`. Values **outside** the limits (low or high) are
outliers.

**Expected output:**

```text
[100]
[-40]
```
