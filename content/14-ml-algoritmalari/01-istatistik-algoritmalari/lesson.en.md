# Statistics Algorithms

Mean, variance, percentiles, correlation and histograms: the first lines of
every data analysis. The formulas look simple, but computing them has two
traps: **floating-point error** and **edge cases**. In this section we write
each from scratch and compare it with NumPy's result.

## The easy way to compute variance wrongly

Variance can also be written as "the mean of the squares minus the square of
the mean": `E[x²] − (E[x])²`. It is computed in one pass and is right on paper.
But if the numbers are large and close to each other, it subtracts two huge
numbers and floating-point precision runs out.

```python
import numpy as np

rng = np.random.default_rng(1)
x = 1e9 + rng.normal(0, 1, size=100_000)       # around a billion, sd 1


def naive_var(values):
    n = len(values)
    s = sum(values)
    s2 = sum(v * v for v in values)
    return s2 / n - (s / n) ** 2               # huge - huge


def two_pass_var(values):
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)


print(round(naive_var(x.tolist()), 4), round(two_pass_var(x.tolist()), 4),
      round(float(np.var(x)), 4))
```

```text
256.0 0.9931 0.9931
```

The true variance is about 1; the one-pass formula found 256. The values of
`x²` are around 10¹⁸, and the roughly 16 significant digits of a `float` cannot
carry the small difference between them (**catastrophic cancellation**). The
two-pass way is right because it subtracts the mean first and works with small
numbers.

## Variance on streaming data: Welford

Two passes need the data to be readable twice. If the data streams (sensors,
logs) or does not fit in memory, **Welford's algorithm** computes soundly in
one pass, updating the mean and the sum of squared deviations with every new
value.

```python
class RunningStats:
    def __init__(self):
        self.n, self.mean, self.m2 = 0, 0.0, 0.0

    def add(self, value):
        self.n += 1
        delta = value - self.mean               # distance from the old mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)  # relative to the old and new mean

    def var(self):
        return self.m2 / self.n


stats = RunningStats()
for v in x:
    stats.add(float(v))
print(round(stats.mean - 1e9, 6), round(stats.var(), 4))
print(np.isclose(stats.var(), np.var(x)))
```

```text
-0.004581 0.9931
True
```

One pass, constant memory, the same result as NumPy. The "running mean" of the
batch normalisation layer in neural networks is kept with a similar update.

## Percentiles

The `q`-th percentile is the value below which `q%` of the data lies. If the
position `(n − 1) · q / 100` in the sorted list is not a whole number, **linear
interpolation** is done between the two neighbouring values; this is NumPy's
default.

```python
def percentile(values, q):
    s = sorted(values)
    pos = (len(s) - 1) * q / 100
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


data = [7, 1, 3, 9, 4, 6, 2]
for q in (0, 25, 50, 90, 100):
    print(q, round(percentile(data, q), 2), round(float(np.percentile(data, q)), 2))
```

```text
0 1.0 1.0
25 2.5 2.5
50 4.0 4.0
90 7.8 7.8
100 9.0 9.0
```

The median (the 50th percentile) is 4; the 90th percentile lies between two
values, 7.8. The definition of a percentile is not unique: in NumPy other
methods can be chosen with `method`; on small data the results differ.

## Correlation

Pearson correlation measures the **linear** relation of two variables between
−1 and 1: the dot product of the deviations from the mean, divided by the
product of the lengths of the two deviation vectors.

```python
def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    da, db = a - a.mean(), b - b.mean()
    return (da @ db) / np.sqrt((da @ da) * (db @ db))


hours = rng.uniform(0, 10, 50)
score = 40 + 5 * hours + rng.normal(0, 8, 50)
print(round(pearson(hours, score), 4), round(np.corrcoef(hours, score)[0, 1], 4))
xs = np.linspace(-3, 3, 61)
print(round(pearson(xs, xs ** 2), 4))
```

```text
0.8329 0.8329
0.0
```

There is a strong linear relation between study hours and score: 0.83. But
the second line matters: `y = x²` is a perfect relation, yet the correlation is
**0**. Correlation sees only linear relations; "no correlation" does not mean
"no relation".

<figure class="fig">
<svg viewBox="0 0 360 240" width="360" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="30" y1="218" x2="330" y2="218"/><line class="grid" x1="180" y1="10" x2="180" y2="225"/><polyline class="curve" points="30.0,20.0 35.0,33.0 40.0,45.5 45.0,57.6 50.0,69.3 55.0,80.5 60.0,91.3 65.0,101.6 70.0,111.5 75.0,121.0 80.0,130.0 85.0,138.6 90.0,146.7 95.0,154.4 100.0,161.7 105.0,168.5 110.0,174.9 115.0,180.8 120.0,186.3 125.0,191.4 130.0,196.0 135.0,200.2 140.0,203.9 145.0,207.2 150.0,210.1 155.0,212.5 160.0,214.5 165.0,216.0 170.0,217.1 175.0,217.8 180.0,218.0 185.0,217.8 190.0,217.1 195.0,216.0 200.0,214.5 205.0,212.5 210.0,210.1 215.0,207.2 220.0,203.9 225.0,200.2 230.0,196.0 235.0,191.4 240.0,186.3 245.0,180.8 250.0,174.9 255.0,168.5 260.0,161.7 265.0,154.4 270.0,146.7 275.0,138.6 280.0,130.0 285.0,121.0 290.0,111.5 295.0,101.6 300.0,91.3 305.0,80.5 310.0,69.3 315.0,57.6 320.0,45.5 325.0,33.0 330.0,20.0" fill="none"/><line class="curve3" x1="30" y1="166.7" x2="330" y2="166.7"/><text class="dim" x="334" y="222" font-size="12">x</text><text class="dim" x="186" y="18" font-size="12">y = x²</text></svg>
<figcaption>y = x²: a perfect relation. But the best-fitting line (dashed) is flat; the fall on the left half cancels the rise on the right half and the Pearson correlation is 0.</figcaption>
</figure>

## Histogram

A histogram splits the range of values into bins of equal width and counts the
values falling into each. There are two edge cases: values outside the range
are not counted, and a value exactly equal to the upper bound goes into the
last bin.

```python
def histogram(values, bins, low, high):
    counts = [0] * bins
    width = (high - low) / bins
    for v in values:
        if v < low or v > high:
            continue                           # outside the range
        i = min(int((v - low) / width), bins - 1)   # upper bound: last bin
        counts[i] += 1
    return counts


vals = rng.normal(0, 1, 1000)
print(histogram(vals, 6, -3, 3))
print(np.histogram(vals, bins=6, range=(-3, 3))[0].tolist())
```

```text
[19, 127, 333, 333, 152, 30]
[19, 127, 333, 333, 152, 30]
```

The same counts. About two thirds of a thousand values from a normal
distribution are in the two middle bins (between −1 and 1).

## Summary

- `E[x²] − (E[x])²` breaks with catastrophic cancellation on large, close
  numbers; subtract the mean first or use Welford.
- Welford: one pass, constant memory, a sound variance.
- Percentile: position `(n − 1) · q / 100` in the sorted list, linear
  interpolation in between.
- Pearson correlation measures only linear relations; 0 with `x²`.
- In a histogram, out-of-range values and the upper bound are the two edge
  cases.
