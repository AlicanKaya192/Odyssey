The same experiment with a real 10% difference (300 people per group) was
repeated 2000 times. Instead of printing one experiment's p, print, one per
line: the share with `p < 0.05` (the power, 3 places) and the 10th, 50th
and 90th percentiles of p
(`np.round(np.percentile(p, [10, 50, 90]), 3).tolist()`).

**Expected output:**

```text
0.41
[0.002, 0.082, 0.574]
```
