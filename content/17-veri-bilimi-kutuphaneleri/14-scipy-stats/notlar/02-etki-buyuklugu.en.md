A p-value is a mix of two things: the **size** of the difference and the
**size** of the sample. With a big enough sample even a trivial difference
comes out "highly significant"; with a small one an important difference is
missed. That is why the size of the difference itself is always written next
to p.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(12)
a = rng.normal(100.0, 10, 200_000)
b = rng.normal(100.3, 10, 200_000)
res = stats.ttest_ind(b, a)
d = (b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
print(f"{res.pvalue:.1e}", round(float(b.mean() - a.mean()), 2), round(float(d), 3))
small_a = a[:20]
small_b = b[:20] + 5
res2 = stats.ttest_ind(small_b, small_a)
pooled = np.sqrt((small_a.var(ddof=1) + small_b.var(ddof=1)) / 2)
d2 = (small_b.mean() - small_a.mean()) / pooled
print(round(float(res2.pvalue), 3), round(float(d2), 2))
```

```text
7.9e-19 0.28 0.028
0.339 0.31
```

## Two extremes

- **A huge sample, a tiny difference.** 200,000 people each, a difference of
  0.28 points (out of 100). p = 7.9e-19: statistically "certain". But the
  effect size is d = 0.028; the two groups overlap almost completely. This
  difference means nothing in practice.
- **A small sample, a real difference.** 20 people each, 5 points added to
  the second group. p = 0.339: "not significant". Yet d = 0.31, a small to
  medium effect; it just does not show with so few people.

## Effect size (Cohen's d)

`d = (difference of the means) / (pooled standard deviation)`: how many
**deviations** is the difference? A rough reading: 0.2 small, 0.5 medium, 0.8
large. It is unit-free; it lets you compare different measures.

## What goes in the report?

1. The difference itself and its unit ("the mean is 4.3 points higher").
2. The confidence interval ("95% CI: −0.01 to 8.66").
3. The effect size (d).
4. The p-value: last, not alone.

Writing "p < 0.05" and stopping does not tell the reader how big the
difference is or how sure we are.
