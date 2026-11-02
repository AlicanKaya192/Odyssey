The day of 700 orders (`make_weekday_orders(n=700, seed=161)`). Print the
day counts from Monday to Sunday as a list, then test them against an even
distribution with `stats.chisquare`: χ² (2 places) and p (4 places). The
starter code gives the test **shares** (`normalize=True`); chi-square needs
counts.

**Expected output:**

```text
[82, 93, 80, 85, 104, 141, 115]
29.2 0.0001
```
