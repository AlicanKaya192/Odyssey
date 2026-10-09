If the data is split across several machines or parts, each part computes its
own `(n, mean, M2)` triple; then the triples are merged without moving the data
itself (Chan's formula). `M2` is the sum of squared deviations, and the
variance is `M2 / n`.

```python
import numpy as np


def summarize(part):
    mean = part.mean()
    return len(part), mean, ((part - mean) ** 2).sum()


def merge(a, b):
    n_a, mean_a, m2_a = a
    n_b, mean_b, m2_b = b
    n = n_a + n_b
    delta = mean_b - mean_a
    mean = mean_a + delta * n_b / n
    m2 = m2_a + m2_b + delta ** 2 * n_a * n_b / n
    return n, mean, m2


rng = np.random.default_rng(5)
data = rng.normal(100, 15, size=10_000)
total = summarize(data[:3000])
for start in range(3000, 10_000, 3500):
    total = merge(total, summarize(data[start:start + 3500]))
n, mean, m2 = total
print(n, round(mean, 4), round(m2 / n, 4))
print(round(data.mean(), 4), round(data.var(), 4))
```

```text
10000 100.3233 227.6291
100.3233 227.6291
```

The summaries of three parts were merged; the result is the same as computed
on the whole data. Systems like Spark and DuckDB compute `AVG` and `VAR`
aggregates in a similar way: each machine its own summary, merged at the end. It
is the variance version of the "partial sums + merging" idea in the Big Data
path.
