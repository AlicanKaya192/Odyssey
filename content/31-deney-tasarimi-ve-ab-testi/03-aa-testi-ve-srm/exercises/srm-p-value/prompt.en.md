`srm_p(n_a, n_b, share_b=0.5)` should test whether the group counts match
the designed split with a chi-square goodness of fit test and return p with
4 places. The expected counts are `[total * (1 - share_b), total *
share_b]`. The starter code always expects 50/50.

**Expected output:**

```text
0.0246
0.3173
```
