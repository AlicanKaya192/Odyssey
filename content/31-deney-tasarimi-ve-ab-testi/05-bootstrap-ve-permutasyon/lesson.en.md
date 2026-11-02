# The Bootstrap and the Permutation Test

So far every question had a formula: the z-test for rates, Welch for means.
But not every statistic has a ready formula: the **median** difference of
two groups, a percentile, the ratio of two totals. This section shows two
methods that use the computer's power instead of a formula: the
**bootstrap** for confidence intervals and the **permutation test** for
hypothesis tests.

## The bootstrap: resampling the sample

In the Sample and Population section we drew thousands of samples from the
same population and saw how an estimate moves. In real life we do not have
the population; we have only one sample. The idea of the **bootstrap**:
put the sample itself in place of the population, draw new samples of the
same size from it **with replacement** (the same row can be picked more
than once), and compute the statistic in each. The distribution of these
values shows how much the estimate moves.

For the revenue difference from the Analysing Your First A/B Test section:

```python
import numpy as np
from scipy import stats
from ab_data import make_experiment

test = make_experiment()
rev_a = test.loc[test["group"] == "A", "revenue"].to_numpy()
rev_b = test.loc[test["group"] == "B", "revenue"].to_numpy()
rng = np.random.default_rng(501)
diffs = []
for _ in range(2000):
    sample_a = rng.choice(rev_a, size=len(rev_a))
    sample_b = rng.choice(rev_b, size=len(rev_b))
    diffs.append(sample_b.mean() - sample_a.mean())
low, high = np.percentile(diffs, [2.5, 97.5])
print(round(low, 2), round(high, 2))
se = np.sqrt(rev_a.var(ddof=1) / len(rev_a) + rev_b.var(ddof=1) / len(rev_b))
diff = rev_b.mean() - rev_a.mean()
print(round(diff - 1.96 * se, 2), round(diff + 1.96 * se, 2))
```

```text
-1.02 1.41
-0.98 1.38
```

The first line is the bootstrap's **percentile interval** (the middle 95%
of 2000 differences), the second line the Welch formula's interval. They
are almost the same: with 15,000 per group the central limit theorem works
and the formula is right. Where the bootstrap really helps is where there
is no formula.

## A statistic without a formula: the median

Did the change alter the order size (what buyers spent)? Order sizes are
very skewed, so we may want to look at the median. The difference of two
medians has no simple standard error formula, but the bootstrap does not
care:

```python
order_a = rev_a[rev_a > 0]
order_b = rev_b[rev_b > 0]
med = []
for _ in range(2000):
    med.append(np.median(rng.choice(order_b, size=len(order_b)))
               - np.median(rng.choice(order_a, size=len(order_a))))
print(round(np.median(order_a), 2), round(np.median(order_b), 2))
print(np.round(np.percentile(med, [2.5, 97.5]), 2))
```

```text
71.72 66.47
[-9.48  0.04]
```

The median order looks 5.25 lower in B, but the interval
contains zero: the difference can be explained by chance. (We generated the
data; in truth order sizes come from the same distribution in both
groups.) The median is much noisier than the mean; the width of the
interval shows it.

## The permutation test: shuffling the labels

H₀ says "B has no effect at all". If that is true, the label saying whether
a person is A or B does not change the outcome; the differences that appear
when the labels are shuffled are the differences possible in the H₀ world.
The **permutation test** does this shuffle thousands of times and counts the
share of differences at least as extreme as the real one: that share is the
p-value.

```python
labels = (test["group"] == "B").to_numpy()
bought = test["bought"].to_numpy()
observed = bought[labels].mean() - bought[~labels].mean()
count = 0
for _ in range(5000):
    shuffled = rng.permutation(labels)
    diff_perm = bought[shuffled].mean() - bought[~shuffled].mean()
    count += abs(diff_perm) >= abs(observed)
print(round(observed, 4), round(count / 5000, 4))
```

```text
0.0123 0.0016
```

The permutation p is 0.0016; the z-test in the Analysing Your
First A/B Test section gave 0.0012. The two methods meet. The
permutation test assumes no distribution: it rests only on random
assignment. That is why it is especially natural in A/B testing: shuffling
the labels means redoing the assignment.

Two notes:

- With 5000 shuffles the smallest measurable p is roughly 1/5000. Very small
  p-values need more shuffles.
- In The Logic of Hypothesis Testing section we built the H₀ world by
  simulation; the permutation test is the same idea done with the data we
  have.

## The bootstrap is not magic

On a small and very skewed sample the bootstrap struggles too. Let's draw
400 samples of 20 from a skewed distribution whose true mean is known, and
count how often each interval catches the true mean:

```python
rng2 = np.random.default_rng(502)
true_mean = np.exp(4.2 + 0.9 ** 2 / 2)
hits_t = hits_boot = 0
for _ in range(400):
    x = rng2.lognormal(4.2, 0.9, 20)
    se_x = x.std(ddof=1) / np.sqrt(20)
    low, high = stats.t.interval(0.95, 19, loc=x.mean(), scale=se_x)
    hits_t += low <= true_mean <= high
    means = rng2.choice(x, size=(2000, 20)).mean(axis=1)
    low, high = np.percentile(means, [2.5, 97.5])
    hits_boot += low <= true_mean <= high
print(hits_t / 400, hits_boot / 400)
```

```text
0.875 0.855
```

Both "95%" intervals catch the true value only 87.5% and
85.5% of the time. The bootstrap is no better than the t
interval: a sample of 20 often contains none of the large values in the
tail, and the bootstrap can only resample what is in the sample. The
bootstrap replaces the formula, not the data.

## Summary

- The bootstrap: resample the sample with replacement, compute the
  statistic, take the middle 95%.
- It helps for statistics without a formula (median, percentile, ratios).
- The permutation test: shuffle the labels; the share more extreme than the
  real difference is p; it rests only on random assignment.
- With large samples they give the same result as the formulas.
- On small, skewed samples the bootstrap is not reliable either.
