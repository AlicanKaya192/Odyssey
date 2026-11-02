From 60 people picked with `random_state=51`, print the mean page load time
(`load_ms`) and its 95% confidence interval. For the interval use
`stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)`. The starter code
uses the multiplier 1.96. The mean on the first line (1 place), the limits
on the second (1 place).

**Expected output:**

```text
843.8
813.9 873.7
```
