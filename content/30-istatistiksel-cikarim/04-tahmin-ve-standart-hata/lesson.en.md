# Estimation and Standard Error

In a real job you hold one sample and need to write a sentence like: "Users
stay 8.4 minutes on average, **give or take this much**." The first part is
the estimate, the second how reliable the estimate is. In this section we
learn to compute both from a single sample, and what a "good estimate"
means.

## Estimator and estimate

- **Estimator**: a **rule** that produces a number from a sample. "Take the
  sample mean" is an estimator.
- **Estimate**: the **number** that rule gives on the sample you hold.
- **Point estimate**: a single number for the unknown parameter. In the next
  section we will turn it into an interval.

Whether an estimator is good cannot be seen from one number; you look at
how the rule behaves **over thousands of samples**. Three properties are
wanted:

| Property | Question |
|---|---|
| Unbiasedness | Does it land in the right place on average? |
| Consistency | Does it approach the truth as the sample grows? |
| Efficiency | How little does it wobble with the same data? |

## The standard error from one sample

The central limit theorem gave the standard error of the mean as
$\sigma / \sqrt{n}$. But we do not know $\sigma$ (the population's
deviation). The fix is simple: put the sample's deviation $s$ in its place.

$$SE = \dfrac{s}{\sqrt{n}}$$

```python
import numpy as np
from ab_data import make_population

users = make_population()
sample = users.sample(n=100, random_state=21)
x = sample["minutes"]
se = x.std() / np.sqrt(len(x))
print(round(x.mean(), 2), round(x.std(), 2), round(se, 3))
```

```text
8.38 4.86 0.486
```

This sample says "the mean is 8.38 minutes, the standard error
0.486". The true mean is 9.04 and the true standard error
$6.13 / \sqrt{100} \approx 0.613$. The single sample underestimated both the
mean and the deviation a little. Is that bad luck or a flaw of the method?
Let us look with thousands of samples.

## How reliable is the standard error estimate?

```python
import numpy as np
from ab_data import make_population

users = make_population()
x_all = users["minutes"].to_numpy()
rng = np.random.default_rng(22)
samples = rng.choice(x_all, size=(4000, 100))
means = samples.mean(axis=1)
ses = samples.std(axis=1, ddof=1) / np.sqrt(100)
print(round(x_all.std() / np.sqrt(100), 3), round(means.std(), 3),
      round(ses.mean(), 3))
print(round(np.percentile(ses, 5), 3), round(np.percentile(ses, 95), 3))
```

```text
0.613 0.618 0.606
0.464 0.797
```

- The first line has three numbers: the true standard error from the
  formula, how much the 4000 means really wobbled, and the average of the
  standard errors each sample computed **for itself**. All three are around
  0.61: the method is right.
- The second line is the spread of the individual estimates: 90% of samples
  found the standard error between 0.464 and 0.797. Our
  estimate (0.486) is inside that range: ordinary bad luck.
- In skewed data the few long sessions are not in every sample, so single
  estimates lean towards being below the truth, while on average they are
  close. In small, skewed samples the standard error is an "estimate" too.

## The square-root rule: the price of precision

The standard error shrinks with $\sqrt{n}$. So halving the error takes
**four times** the data. The sample needed to reach a desired standard
error:

$$n = \left(\dfrac{\sigma}{SE_{target}}\right)^2$$

```python
import math
from ab_data import make_population

users = make_population()
sigma = users["minutes"].std()
for target in [1.0, 0.5, 0.25]:
    print(target, math.ceil((sigma / target) ** 2))
```

```text
1.0 38
0.5 151
0.25 601
```

- For a precision of 1 minute, 38 people are enough.
- For half a minute 151, for a quarter minute 601
  people: four times more at every halving.
- `math.ceil` rounds up: the number of people must be whole, and "a little
  short" misses the target.
- In a real job $\sigma$ is unknown; it is estimated from past data or a
  small pilot sample.

## Efficiency: the mean or the median?

In bell-shaped data both the mean and the median estimate the centre without
bias. Which one wobbles less?

```python
import numpy as np
from ab_data import make_population

users = make_population()
y = users["load_ms"].to_numpy()
rng = np.random.default_rng(23)
samples = rng.choice(y, size=(4000, 100))
sd_mean = samples.mean(axis=1).std()
sd_median = np.median(samples, axis=1).std()
ratio = (sd_median / sd_mean) ** 2
print(round(sd_mean, 2), round(sd_median, 2), round(ratio, 2))
```

```text
11.98 14.83 1.53
```

- On the same 100-person samples the median wobbled more than the mean.
- The last number is the ratio of the variances: for the median to be as
  precise as the mean you need about 1.53 times the data. For a
  normal distribution the theoretical value is $\pi / 2 \approx 1.57$.
- In bell-shaped data the mean is more **efficient**. In data full of
  outliers the picture can flip; then the robustness of the median is worth
  more.

## A biased estimator: the sample maximum

Let us estimate the slowest page load time by the largest of 100 users:

```python
import numpy as np
from ab_data import make_population

users = make_population()
y = users["load_ms"].to_numpy()
rng = np.random.default_rng(24)
maxes = rng.choice(y, size=(2000, 100)).max(axis=1)
print(y.max(), round(maxes.mean(), 1), (maxes < y.max()).mean())
```

```text
1324 1150.0 0.999
```

The true slowest value is 1324 ms; the sample maximum is
1150.0 ms on average and 99.9% of samples stayed below the
truth. Even as the sample grows, this estimator approaches the truth **from
below**; it can never go above it. That is exactly the definition of bias:
missing in the same direction on average.

## The same for proportions

```python
import numpy as np
from ab_data import make_population

users = make_population()
sample = users["bought"].sample(n=400, random_state=25)
p_hat = sample.mean()
print(round(p_hat, 4), round(np.sqrt(p_hat * (1 - p_hat) / 400), 4))
```

```text
0.1325 0.017
```

This 400-person sample says "the share of buyers is 0.1325, the
standard error 0.017". The true share is 0.114: the estimate is
about 1.1 standard errors away from it. Whether that is ordinary
or surprising we will ask in the next section with a confidence interval,
and later with a hypothesis test.

## Summary

- An estimator is a rule, an estimate the number it gives. A good estimator
  is unbiased, consistent and efficient; we measure that by simulation.
- The standard error is estimated from one sample as $s / \sqrt{n}$; with
  small, skewed samples that estimate wobbles too.
- Doubling precision takes four times the data:
  $n = (\sigma / SE_{target})^2$.
- In bell-shaped data the mean is more efficient than the median; the
  sample maximum is a biased estimator.
