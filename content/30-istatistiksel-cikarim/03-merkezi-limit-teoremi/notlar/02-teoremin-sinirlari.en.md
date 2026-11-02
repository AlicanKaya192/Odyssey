The central limit theorem is powerful but not unconditional. It breaks in
three situations.

## 1. When the values are not independent

Counting ten sessions of the same user as ten separate people makes the
sample look bigger than it is. Those ten sessions resemble each other: they
carry the same person's habits. The real information is not ten people's
worth but a little more than one person's. The standard error formula takes
$n = 10$ and underestimates the wobble.

**Check:** What does a row represent? A person or an event? Is the unit
picked at random (the user) the same as the unit measured (the session)?

## 2. When the variance is not finite

Some distributions have tails so heavy that their variance is infinite.
The best known is the **Cauchy distribution**. Even as the sample grows, the
means do not gather:

```python
import numpy as np

rng = np.random.default_rng(8)
for n in [10, 1000]:
    means = rng.standard_cauchy(size=(2000, n)).mean(axis=1)
    q1, q3 = np.percentile(means, [25, 75])
    print(n, round(q3 - q1, 2))
```

```text
10 2.12
1000 2.04
```

The width of the middle half of the means (the IQR) is about 2 with 10
people and with 1000 people alike. With normal data the same experiment
would narrow 10 times for a sample 100 times larger. Such an extreme case
is rare in real data, but heavy-tailed metrics (revenue data where a few
users spend huge amounts) show a similar slowness.

## 3. When the sample is small and the data skewed

The theorem says "as $n$ grows". With small $n$ the means of skewed data
are skewed too; in this section we saw that the spend means of 30 people
never missed downwards.

**Check:** Draw the means by simulation. If you cannot, use the bootstrap
(second module) or methods that do not rely on a distribution
(non-parametric tests).
