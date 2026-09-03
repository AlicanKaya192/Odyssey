In supervised learning the question does not arise: you check the test set
to see whether the model is right. In clustering there is no test set to
check, so the question falls entirely to you.

This note collects five ways to answer it.

## 1. Measure what noise scores

The silhouette cannot be read on its own. Is 0.52 good? There is no way to
know — good against what?

Generate random data of the same shape with the same number of columns and
cluster it with the same `k`:

```python
import numpy as np
rng = np.random.default_rng(0)
noise = rng.normal(0, 1, X_scaled.shape)
```

Measured: 0.517 on the real data, 0.181 on noise. **The threefold gap** is
the actual information.

If the two values sit close together, your clusters are probably arbitrary
partitions the algorithm handed you.

## 2. Read the table, not the number

A clustering result is not a number but a table:

| Cluster | `spend` | `visits` | `items` | `returns` |
|---|---|---|---|---|
| 0 | 428.2 | 15.2 | 23.4 | 3.3 |
| 1 | 45.8 | 3.2 | 4.2 | 0.3 |
| 2 | 63.9 | 19.3 | 6.4 | 2.6 |
| 3 | 180.2 | 8.4 | 11.3 | 1.1 |

The question to ask: **can you give every row a name?**

- 0 → "the big customer"
- 1 → "the rare visitor"
- 2 → "browses a lot, buys little"
- 3 → "the steady middle"

If you can, the clusters are saying something. If the rows' means look
alike and no name comes to mind, there is no structure.

**This is not eyeballing.** Being unable to name them means the clusters do
not separate from one another; numerical metrics sometimes miss that.

## 3. Change the seed

```python
for seed in (0, 1, 2, 3):
    labels = KMeans(n_clusters=4, random_state=seed, n_init=10).fit_predict(X_scaled)
```

**Cluster numbers changing is normal.** What to look at is the grouping
itself:

```python
from sklearn.metrics import adjusted_rand_score
print(adjusted_rand_score(labels_0, labels_1))
```

If the ARI across seeds is near 1.0 the structure is solid. If it is around
0.6-0.7 the algorithm finds a different partition every time — that
instability is a sign the structure is weak.

## 4. Shake the data

The same method as section 08: drop 10% of the records and cluster again.
If the remaining records keep their groups, the structure is real.

```python
sample = df.sample(frac=0.9, random_state=seed)
```

When clustering is unstable, the same customer lands in different groups
from round to round.

## 5. Tie it to something outside

The strongest test. If you have information you did not use in the
clustering — the signup date, the city, what they did the following month —
check whether the clusters differ on it.

If cluster 2 ("browses a lot, buys little") is real, its customers should
also show a high return rate the following month. If they do, the cluster
has caught something.

**That information is never fed into the clustering**, or the test loses its
meaning.

## When clustering is the wrong tool

| Symptom | What you probably need |
|---|---|
| You already have labels | Classification |
| You are looking for "unusual" records | Anomaly detection |
| The groups are defined by a business rule | `groupby`, not clustering |
| The clusters are crescent- or ring-shaped | DBSCAN |
| A different result on every seed | No structure; the wrong question |

**The fourth row is k-means' best-known limit.** It looks for round
clusters of similar size. Give it two nested rings and it will cut both
down the middle — mathematically correct, nonsense in practice.

## Presenting the result

When explaining a clustering to a stakeholder:

- **Use names, not cluster numbers.** "Cluster 2" says nothing; "the group
  that visits often and buys little" says something.
- **Give the sizes.** A cluster of 70 and a cluster of 200 call for
  different decisions.
- **State the uncertainty.** "The silhouette points to `k=3` and the elbow
  to somewhere between 3 and 4; we chose four because the fourth group
  behaves differently in business terms" is honest and defensible.
- **Never say "X% accurate".** No such number exists, and being unable to
  answer when asked is worse.

## In one sentence

**Clustering is a tool for exploring, not for proving.** It shows you where
to look; you are the one who looks and decides.
