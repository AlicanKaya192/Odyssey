`zscore_flags(baseline, values, limit)` should take the baseline's mean and
standard deviation (`statistics.mean`, `statistics.stdev`) and return, in
order, the values whose absolute z-score is **greater** than `limit`. If
the deviation is 0 (all baseline values are equal), every value not equal
to the mean is flagged.

**Expected output:**

```
[410, 100, 140]
[6]
```
