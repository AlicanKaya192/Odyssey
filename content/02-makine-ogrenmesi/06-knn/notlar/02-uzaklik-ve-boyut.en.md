The whole of KNN rests on one operation: **how similar are two records?**
This note is about how that is computed and where it breaks.

## Euclidean distance

The straight-line distance between two points:

```
d = ((x1 - x2)^2 + (y1 - y2)^2 + ...) ^ 0.5
```

```python
def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
```

Squaring does two jobs: it removes the sign and it foregrounds large
differences. The second is the source of the scaling problem — a gap of
100,000 in one column crushes a gap of 40 in another **once squared**.

## Other distances

| Measure | How | When |
|---|---|---|
| Euclidean (`p=2`) | Straight line | The default; continuous numeric columns |
| Manhattan (`p=1`) | Along the axes | More robust to outliers, steadier in many dimensions |
| Cosine | The angle between | Text/vector data; when **direction** matters, not magnitude |
| Hamming | In how many positions they differ | Binary or categorical columns |

```python
KNeighborsClassifier(n_neighbors=5, metric="manhattan")
```

**Why cosine for text:** two documents on the same subject have similar word
proportions but can differ wildly in length. Euclidean calls the long
document distant; cosine, looking only at direction, finds them close.

## Why scaling is compulsory

An example, with numbers. Two customers:

```
A: income 50,000, visits 10
B: income 51,000, visits 45
```

The Euclidean distance:

```
((51000 - 50000)^2 + (45 - 10)^2) ^ 0.5
= (1,000,000 + 1,225) ^ 0.5
= 1000.6
```

**The gap of 35 in visits adds 1,225 to the sum; the gap of 1,000 in income
adds 1,000,000.** The result comes almost entirely from income — even though
the visit count may matter far more for whether a customer leaves.

After scaling both columns have mean 0 and standard deviation 1, and the
differences become comparable.

The measured result: accuracy **0.64 → 0.92**.

## The curse of dimensionality

As the number of features grows, distance loses its meaning. A simple
experiment shows it:

```python
import numpy as np

rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    points = rng.random((500, d))
    first = points[0]
    distances = np.sqrt(((points[1:] - first) ** 2).sum(axis=1))
    ratio = distances.min() / distances.max()
    print(d, round(float(ratio), 3))
```

As the dimension grows, **the ratio between the nearest and the furthest
neighbour approaches 1.** Every point is almost equally far from every
other, and choosing the "nearest" turns into a coin flip.

### Why it happens

Every new feature adds another term to the distance. As the number of terms
grows the sums resemble one another — much as the totals pile up around the
average when you roll many dice.

### What to do

| Route | How |
|---|---|
| Feature selection | Remove columns weakly related to the target (on the training side!) |
| Dimension reduction | Reduce to a few components with PCA (section 10) |
| Domain knowledge | Combine columns into a few meaningful features |
| Change model | Trees do not suffer from this |

**A rough measure:** with more than fifteen features, do not use KNN without
comparing it to the baseline. At thirty columns simpler models are usually
better.

## The shape of the decision boundary

`k` decides how **smooth** the boundary is:

| `k` | Boundary | Risk |
|---|---|---|
| 1 | Fragmented, full of islands | Memorises the noise |
| 5-15 | Wavy but whole | Usually good |
| Very large | Almost straight | Misses real detail |

In a measured example `k=1` and `k=15` gave **the same test accuracy**
(0.90) but entirely different boundaries: one had carved islands around
individual points, the other drew a single smooth curve.

**The same number, a different model.** This is the most concrete example of
why looking at one measure is not enough.

## Categorical columns

Because KNN works with numbers, categorical columns are encoded first
(section 04). But there is a subtlety: **one-hot columns enter the distance
as 0 or 1**, while scaled numeric columns run between -3 and +3.

So the categorical columns carry less weight than the numeric ones. When
that needs balancing, the encoded columns get scaled too, or a weighted
distance measure is used.

A column with many categories (a city, say) also feeds the curse of
dimensionality, since one-hot turns it into dozens of columns.

## Missing values

In a distance computation a missing value is undefined: there is no distance
between `NaN` and any number. sklearn raises an error.

There are two routes: fill them as in section 04, or use **`KNNImputer`** —
a tool that fills a missing value from its nearest neighbours' values.

```python
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=5)
imputer.fit(X_train)
X_train = imputer.transform(X_train)
```

Being a KNN itself, **it wants scaling too** and **it too is applied after
the split**.
