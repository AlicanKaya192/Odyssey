`cosine_rate(base, epoch, total)` should compute the cosine schedule's rate at
that epoch with the formula `base · (1 + cos(π · epoch / total)) / 2`. Return
it with 4 places.

**Expected output:**

```
0.05
0.4268
```
