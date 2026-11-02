# Comparing Proportions

The most common question in A/B tests is not about a mean but about a
**proportion**: did the new checkout button increase the share of buyers?
The share who sign up, who click, who come back ... In all of them each
user has a single yes/no (1/0). In this section we learn to compare two
proportions, to build the confidence interval of the difference, and why a
different test is needed when the counts are small.

## The data: the checkout button test

```python
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
print(k.to_dict(), n.to_dict())
pa, pb = k["A"] / n["A"], k["B"] / n["B"]
print(round(pa, 4), round(pb, 4), round(pb - pa, 4), round((pb - pa) / pa, 3))
```

```text
{'A': 472, 'B': 560} {'A': 4000, 'B': 4000}
0.118 0.14 0.022 0.186
```

- Each group has 4,000 users. With the old button (A) the share of buyers
  is 0.118, with the new one (B) 0.140.
- The **absolute difference**: 0.022, that is about 2.2 percentage
  points.
- The **relative lift**: the difference divided by A, 18.6%. "Sales
  rose 19%" is a relative lift; do not confuse it with "percentage points".

## The two-proportion z-test

$H_0$: the two groups' true proportions are equal. If $H_0$ is true we can
think of the two groups as one pool; the common proportion $\hat{p}$ comes
from both groups combined. The standard error of the difference and the
test statistic:

$$SE = \sqrt{\hat{p}(1-\hat{p})\left(\dfrac{1}{n_A} + \dfrac{1}{n_B}\right)} \qquad z = \dfrac{\hat{p}_B - \hat{p}_A}{SE}$$

```python
import numpy as np
from scipy import stats
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
pa, pb = k["A"] / n["A"], k["B"] / n["B"]
pool = k.sum() / n.sum()
se = np.sqrt(pool * (1 - pool) * (1 / n["A"] + 1 / n["B"]))
z = (pb - pa) / se
print(round(pool, 4), round(se, 5), round(z, 3))
print(round(2 * stats.norm.sf(abs(z)), 4))
```

```text
0.129 0.0075 2.935
0.0033
```

- The common proportion is 0.1290, the standard error of the
  difference 0.0075. The difference is about 2.9 times the standard
  error.
- The two-sided p = 0.0033: `2 * sf(|z|)`, because we look at both
  tails.

`statsmodels` runs the same test in one line:

```python
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_checkout_test

test = make_checkout_test()
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
z, p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])
print(round(z, 3), round(p, 4))
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"],
                                       method="newcomb")
print(round(low, 4), round(high, 4))
```

```text
2.935 0.0033
0.0073 0.0367
```

- z and p are the same as ours by hand.
- The 95% confidence interval of the difference is 0.0073 to
  0.0367: the new button very likely raises the share of buyers by
  between 0.7 and 3.7 percentage points. `method="newcomb"` is the
  two-proportion counterpart of the Wilson interval from the single
  proportion section; it is reliable with small samples too.
- We generated the data: the true difference is 13.0 − 11.4 = 1.6 percentage
  points. The interval contains it; the observed 2.2 is a bit large by
  chance.

## When counts are small: Fisher's exact test

The z-test relies on the central limit theorem: it assumes proportions are
distributed in a bell shape. When groups are small and events rare (a few
purchases), that assumption weakens. Say in a small pilot test 3 and 11 out
of 40 people each bought:

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

table = [[3, 37], [11, 29]]
z, p_z = proportions_ztest([11, 3], [40, 40])
fisher = stats.fisher_exact(table)
print(round(p_z, 4), round(fisher.pvalue, 4))
```

```text
0.0186 0.0367
```

**Fisher's exact test** uses no approximate distribution; it counts all the
possible arrangements of the 2×2 table. Here the z-test gave p =
0.0186, Fisher p = 0.0367. Which one behaves correctly? Let us
simulate small tests where the true difference is zero (both 8%) 10,000
times:

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(131)
p_z, p_f = [], []
for _ in range(10000):
    a, b = rng.binomial(40, 0.08), rng.binomial(40, 0.08)
    if a + b == 0:
        p_z.append(1.0)
        p_f.append(1.0)
        continue
    p_z.append(proportions_ztest([b, a], [40, 40])[1])
    p_f.append(stats.fisher_exact([[a, 40 - a], [b, 40 - b]]).pvalue)
p_z, p_f = np.array(p_z), np.array(p_f)
print(round((p_z < 0.05).mean(), 4), round((p_f < 0.05).mean(), 4))
```

```text
0.0616 0.0157
```

- With no difference the z-test gave false alarms 6.2% of the time:
  above the promised 5%.
- Fisher: 1.6%, far below 5%. Fisher is **conservative**: it gives
  fewer false alarms than it promises, and pays for that with lost power.
- Rule: Fisher for small tables where an expected count in some cell falls
  below 5; the z-test for A/B tests with thousands of users.

## When reporting

- Give the two proportions, the absolute difference (percentage points) and
  the relative lift together.
- Write the confidence interval for the absolute difference: "+2.2
  percentage points (95% CI: 0.7 to 3.7)".
- A relative lift looks huge on small base rates: going from 1% to 2% is a
  "100% lift" but only 1 percentage point.

## Summary

- A proportion is the mean of 0/1 data; two proportions are compared with
  the z-test (`proportions_ztest`).
- For the difference's confidence interval:
  `confint_proportions_2indep(..., method="newcomb")`.
- With small counts the z-test may not keep its promise; Fisher's exact test
  is safe but conservative.
- Do not confuse the absolute difference with the relative lift.
