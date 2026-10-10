The average of 40 days of sales is 117.5. How reliable is this number; how
much would the average move with another 40 days? **The bootstrap** answers
this without a formula, using only random sampling: from the 40 days we have,
we draw 40 days **with replacement** thousands of times and take each one's
average.

```python
import numpy as np

rng = np.random.default_rng(11)
sales = rng.normal(120, 30, size=40).round(1)
samples = rng.choice(sales, size=(5_000, sales.size), replace=True)
means = samples.mean(axis=1)
low, high = np.percentile(means, [2.5, 97.5])
print(round(float(sales.mean()), 1), samples.shape)
print(round(float(low), 1), round(float(high), 1))
print(bool(low < sales.mean() < high))
```

```text
117.5 (5000, 40)
109.8 125.1
True
```

## The steps

1. **5000 samples in one call:** `rng.choice(sales, size=(5000, 40),
   replace=True)` is a 5000 × 40 matrix: each row is "another 40 days". No
   loop.
2. **The average of each row:** `mean(axis=1)` → 5000 averages.
3. **The middle 95%:** the 2.5th and 97.5th percentiles of these averages.
   The 95% confidence interval for the average is about **109.8 – 125.1**.

## Why with replacement?

Drawing 40 days out of 40 without replacement always gives the same days (the
order changes, the average does not). With replacement, some days come twice
and some not at all; this imitates the uncertainty of "had there been another
40 days".

## The role of the seed

Thanks to `default_rng(11)` the interval comes out the same on every run; the
number written in a report can be reproduced. Changing the seed moves the
limits a little (a few tenths with 5000 samples); the size of that movement
tells you whether more samples are needed.
