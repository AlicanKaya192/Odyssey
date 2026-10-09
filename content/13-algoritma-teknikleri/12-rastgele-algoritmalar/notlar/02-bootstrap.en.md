Ten students have an average score of 80. If we had chosen ten other students,
how much would the average change? The way to estimate this without collecting
new data is the **bootstrap**: draw new samples of the same size from the data
you have **with replacement**, take the mean of each, and look at how widely
these means spread.

```python
import random
import statistics

random.seed(0)
scores = [72, 85, 90, 64, 78, 88, 95, 70, 81, 77]
means = []
for _ in range(10_000):
    resample = random.choices(scores, k=len(scores))   # with replacement
    means.append(statistics.mean(resample))
means.sort()
print(statistics.mean(scores))
print(means[250], means[9750])                          # the middle 95%
```

```text
80
74.2 85.6
```

The middle 95% of the means of ten thousand resamples lies roughly in this
range: a **confidence interval** showing how unsteady the mean is for a class
of ten. No formula is needed; only sampling with replacement and some
computing power.

A random forest uses the same idea: each tree is trained on a bootstrap sample
of the data, and the trees making different errors makes the average sturdier.
The rows that never enter the sample (about a third) become that tree's
**out-of-bag** validation data.
