`daily_change(values)` should compute the daily **rate of change**
(`pct_change`) from the values of consecutive days; the first day has no rate
and is dropped. Return the result as a list rounded to 3 places. The starter
code computes the difference (`diff`); the rate is wanted: `0.1` for 100 →
110. **Do not write a loop.**

**Expected output:**

```
[0.1, -0.1, 0.212, 0.0]
```
