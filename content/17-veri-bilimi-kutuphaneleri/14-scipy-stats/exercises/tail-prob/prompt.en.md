`tail_prob(mean, sd, limit)` should return the probability that a value from a
normal distribution with mean `mean` and sd `sd` is **greater** than
`limit`, rounded to 4 places (`stats.norm(...).sf(limit)`). The starter code
uses `cdf`: that means "limit and below".

**Expected output:**

```
0.0228
0.0228
```
