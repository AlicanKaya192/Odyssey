# scipy.stats

`scipy.stats` is the toolbox of statistics: probability distributions,
summary measures and hypothesis tests in one module. In the Mathematics path
you learned what these concepts **mean**; this section covers how to use them
**in code** and how to read the output. The section's most important lesson
is not a line of code either: "p < 0.05" neither proves nor disproves a
result. We will see this by measuring.

## Distribution objects

```python
from scipy import stats

height = stats.norm(loc=170, scale=8)
print(round(float(height.pdf(170)), 4), round(float(height.cdf(186)), 4))
print(round(float(height.sf(186)), 4), round(float(height.ppf(0.975)), 1))
print(height.rvs(size=3, random_state=1).round(1).tolist())
coin = stats.binom(n=10, p=0.5)
print(round(float(coin.pmf(5)), 4), round(float(coin.cdf(2)), 4))
```

```text
0.0499 0.9772
0.0228 185.7
[183.0, 165.1, 165.8]
0.2461 0.0547
```

`stats.norm(loc=mean, scale=sd)` builds a distribution **object**; every
distribution has the same methods:

| Method | Question | Here |
|---|---|---|
| `pdf(x)` / `pmf(k)` | the density / probability of this value | exactly 5 heads in 10 tosses: 0.2461 |
| `cdf(x)` | x **or less** | 186 cm and below: 97.7% |
| `sf(x)` | **more** than x (1 − cdf) | above 186: 2.3% |
| `ppf(q)` | below which value q lies (the inverse of cdf) | the 97.5% limit: 185.7 |
| `rvs(size=, random_state=)` | a random sample | reproducible with a seed |

- For small probabilities `sf` is more accurate than `1 - cdf`.
- For a continuous distribution `pdf` is **not** a probability, it is a
  density: 0.0499 does not mean "the probability of being 170 cm".
  Probability is the area of an **interval** (`cdf(b) - cdf(a)`).

## Summary measures

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(8)
times = rng.exponential(scale=10, size=500)
d = stats.describe(times)
print(d.nobs, round(float(d.mean), 2), round(float(d.variance), 1))
print(round(float(d.skewness), 2), round(float(np.median(times)), 2))
print(round(float(stats.sem(times)), 3), round(float(stats.iqr(times)), 2))
```

```text
500 9.67 90.8
1.88 6.87
0.426 10.36
```

- `describe` gives the count, mean, variance, skewness and kurtosis in one
  call.
- In right-skewed data like waiting times (skewness 1.88) the mean (9.67) is
  clearly larger than the median (6.87): a few long waits pull the mean. For
  a "typical" value the median is more honest.
- `sem` is the standard error of the mean: how much the mean itself can move.
  `iqr` is the width of the middle half; robust to outliers.

## Comparing two groups: the t-test

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(9)
old = rng.normal(52, 10, 40)
new = rng.normal(58, 10, 40)
result = stats.ttest_ind(new, old)
welch = stats.ttest_ind(new, old, equal_var=False)
print(round(float(new.mean() - old.mean()), 2))
print(round(float(result.statistic), 3), round(float(result.pvalue), 4))
print(round(float(welch.pvalue), 4), result.pvalue < 0.05)
```

```text
4.33
1.988 0.0503
0.0505 False
```

- We generated the data, so we know the truth: the new design's mean **really
  is** 6 points higher. In the sample the difference came out at 4.33.
- `ttest_ind` answers "if the two groups had the same mean, how likely would a
  difference this large be?": p = 0.0503. With a 0.05 threshold, "not
  significant".
- So with a real difference present, the test **missed** it. Groups of 40,
  against a spread of 10, are not enough to show a difference of 6
  confidently. "Not significant" ≠ "no difference".
- `equal_var=False` (Welch's test) does not assume the two groups have equal
  spread; if you are not sure, it is the safe choice. Here the result is
  almost the same.

## A confidence interval says more than p

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(9)
old = rng.normal(52, 10, 40)
new = rng.normal(58, 10, 40)
res = stats.ttest_ind(new, old)
low, high = res.confidence_interval(confidence_level=0.95)
print(round(float(low), 2), round(float(high), 2))
mean_ci = stats.t.interval(0.95, df=len(new) - 1,
                           loc=new.mean(), scale=stats.sem(new))
print([round(float(v), 2) for v in mean_ci])
```

```text
-0.01 8.66
[53.39, 58.96]
```

- The 95% confidence interval of the difference runs from −0.01 to 8.66. This
  single line tells more than the p-value: the difference **could be zero,
  or 8.7 points**. The data cannot tell them apart; more people are needed.
- Because the interval contains zero, p came out above 0.05; the two are two
  faces of the same calculation.
- `stats.t.interval` gives the interval of a single mean: the new design's
  mean is most likely between 53.4 and 59.0.

## Categorical data: chi-square

```python
import numpy as np
from scipy import stats

table = np.array([[90, 60],
                  [45, 105]])
res = stats.chi2_contingency(table)
print(round(float(res.statistic), 2), res.dof, f"{res.pvalue:.2e}")
print(res.expected_freq.round(1).tolist())
print((table[:, 0] / table.sum(axis=1)).round(2).tolist())
```

```text
26.07 1 3.29e-07
[[67.5, 82.5], [67.5, 82.5]]
[0.6, 0.3]
```

- The rows are two ads, the columns "clicked / did not click". The question:
  does the click rate depend on the ad?
- `expected_freq` is the counts expected under independence (67.5 and 82.5
  in each row). The gap between observed and expected is large: p = 3.29e-07.
- The rates are 60% and 30%: the difference is both significant **and
  large**. Always look at both.

## Relationships: pearsonr and spearmanr

```python
import numpy as np
from scipy import stats

x = np.arange(1, 21)
y = x ** 3
r, p = stats.pearsonr(x, y)
rho, p2 = stats.spearmanr(x, y)
print(round(float(r), 3), round(float(rho), 3))
rng = np.random.default_rng(10)
a = rng.normal(size=30)
b = rng.normal(size=30)
print(round(float(stats.pearsonr(a, b).pvalue), 3))
```

```text
0.922 1.0
0.026
```

- `pearsonr` measures a **linear** relationship: y = x³ is a perfect
  relationship but not a straight line, r = 0.922. `spearmanr` looks at
  **ranks**: as x grows y always grows, ρ = 1.0.
- Then two **unrelated** random arrays: p = 0.026. "Significant" with no
  relationship at all. The 0.05 threshold already accepts one false alarm in
  every twenty tries when there is no relationship.

## Many tests, many false alarms

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(11)
false_alarms = 0
for test in range(100):
    a = rng.normal(0, 1, 30)
    b = rng.normal(0, 1, 30)
    if stats.ttest_ind(a, b).pvalue < 0.05:
        false_alarms += 1
print(false_alarms)
print(round(0.05 / 100, 4))
```

```text
9
0.0005
```

- 100 times, two groups were drawn from **the same** distribution; in truth
  there is no difference. Still, 9 tests said "significant".
- That is why looking at twenty measures and reporting the one that hit is
  misleading. The simplest correction (Bonferroni): divide the threshold by
  the number of tests, 0.0005 for 100 tests.
- Better still: write down what you will look at before seeing the data.

## Summary

- A distribution object: `pdf`/`pmf`, `cdf`, `sf`, `ppf`, `rvs(random_state=)`.
- The median for skewed data; `describe`, `sem`, `iqr`.
- `ttest_ind(..., equal_var=False)`; "not significant" does not mean no
  difference.
- A confidence interval shows the size of the difference and its uncertainty
  together.
- `chi2_contingency` for a categorical table; `pearsonr` linear, `spearmanr`
  rank relationships.
- Many tests produce false alarms; correct the threshold, write the
  hypothesis in advance.
