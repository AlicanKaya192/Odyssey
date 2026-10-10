`at_least(n, p, k)` should return the probability of **at least** `k`
successes in `n` trials with success probability `p`, rounded to 4 places.
`stats.binom(n, p).sf(x)` means "**greater** than x"; "at least k" = "greater
than k − 1". The starter code writes `sf(k)` and leaves exactly `k` out.

**Expected output:**

```
0.1719
0.8784
```
