If loads really became 40 ms slower, how often would tests with 20 and 80
measurements catch it? For each `n` draw 3000 samples of `n` from the old
times, **add 40 to every value**, apply `ttest_1samp` against `old.mean()`
(`axis=1`) and print the share with `p < 0.05` together with `n` (3
places). The starter code forgot to add 40: it measures the false alarm
rate.

**Expected output:**

```text
20 0.294
80 0.846
```
