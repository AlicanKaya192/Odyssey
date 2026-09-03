## K-means

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

| Parameter | What it does | Default |
|---|---|---|
| `n_clusters` | How many clusters to look for | 8 |
| `n_init` | How many different starts to try | `auto` |
| `random_state` | The seed for the initial centres | `None` |
| `max_iter` | The maximum number of rounds | 300 |
| `init` | How the start is chosen (`k-means++` is smart) | `k-means++` |

**Why `n_init` exists:** the initial centres are random, and a poor start
gets stuck in a poor result. The model runs from scratch `n_init` times and
keeps the one with the lowest inertia.

What a fitted model gives you:

```python
model.labels_           # each record's cluster number
model.cluster_centers_  # the centres (in the SCALED space)
model.inertia_          # the sum of squared distances to the centres
model.predict(new)      # assigns new records to the nearest centre
```

**`cluster_centers_` lives in the scaled space.** To read it in the
original units:

```python
print(scaler.inverse_transform(model.cluster_centers_).round(1))
```

## Scaling

Mandatory — k-means rests on distance.

```python
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)
```

Measured: the scaled silhouette is 0.517, the unscaled 0.202. The unscaled
model puts two real groups into a single heap of 175.

Here `fit_transform` is applied to all the data; **section 04's leakage
rule does not apply**, because there is no target to predict and no test
set to compare against.

## Reading a cluster profile

This table is the section's real output:

```python
df["cluster"] = labels
print(df.groupby("cluster").mean().round(1))
print(df["cluster"].value_counts().sort_index())
```

The cluster numbers are meaningless; the means and the sizes are what
matter.

## Choosing `k`

```python
for k in range(2, 9):
    m = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    print(k, round(float(m.inertia_), 1),
          round(float(silhouette_score(X_scaled, m.labels_)), 3))
```

| Tool | What it says | Its limit |
|---|---|---|
| Inertia (the elbow) | Where the curve bends | It always falls as `k` grows |
| Silhouette | How tidy the clusters are | Positive on noise too |

Measured: the elbow sits between 3 and 4, the silhouette peaks at `k=3`
(0.525), and the data was generated from four groups. **The two tools
narrow the range; they do not make the decision.**

## The silhouette

```python
from sklearn.metrics import silhouette_score
print(round(float(silhouette_score(X_scaled, labels)), 3))
```

Between −1 and +1. A rough reading:

| Value | Meaning |
|---|---|
| Above 0.7 | Very distinct clusters (rare on real data) |
| 0.5 - 0.7 | Reasonable structure |
| 0.25 - 0.5 | Weak; look carefully |
| Below 0.25 | Treat as no structure |

**Never read it without a reference:** even random noise gives 0.18. You
have to measure what noise scores on your own data and compare.

## Comparing two clusterings

```python
from sklearn.metrics import adjusted_rand_score
print(round(float(adjusted_rand_score(labels_a, labels_b)), 3))
```

The cluster numbers change with the seed, so labels cannot be compared
directly. ARI asks "are these two records in the same cluster in both".

| ARI | Meaning |
|---|---|
| 1.0 | Exactly the same grouping |
| Around 0.6 | Partly overlapping |
| Around 0 | As similar as chance |

## PCA

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
Z = pca.fit_transform(X_scaled)

print(pca.explained_variance_ratio_)   # [0.662 0.223]
print(pca.components_)                 # each component's weights
```

| Parameter | What it does |
|---|---|
| `n_components` | How many components to keep |
| `n_components=0.9` | As many as carry 90% of the variance |
| `random_state` | The seed, if a randomised solver is used |

**Scaling before PCA is mandatory.** Since it works on variance, on
unscaled data the column with the largest units takes over every component.

How many components to keep:

```python
import numpy as np
print(np.cumsum(pca.explained_variance_ratio_).round(3))
# [0.662 0.885 0.973 1.   ]
```

A threshold between 85% and 95% is common.

**The components are not original columns but mixtures.** `PC1` came out as
"overall activity" and `PC2` as "comes often but buys little" — but that
reading was done by hand from the weight table; PCA gives no such names.

## Common mistakes

- **Not scaling.** It spoils the result for both k-means and PCA.
- **Taking `n_clusters` for a hyperparameter.** The model does not know how
  many groups there are; you tell it.
- **Reading meaning into cluster numbers.** They move when the seed
  changes.
- **Maximising the silhouette.** It rises on noise too; it is not a
  criterion on its own.
- **Treating returned clusters as proof of structure.** The algorithm
  partitions any data.
- **Comparing silhouettes from spaces of different dimension.** 0.652 after
  PCA against 0.517 in the full space — the same clusters, a different
  measurement space.
- **Clustering when you have labels.** With labels, classification is
  always stronger.
- **Not passing `random_state`.** The result changes on every run.
