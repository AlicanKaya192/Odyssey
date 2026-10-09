A GMM learns not only clusters but also the data's **density**: for every
point it answers "how likely is this value in this data". This is a simple
way to find outliers (anomalies): a point with very low density is suspect.

With the lesson's `x`:

```python
g = GaussianMixture(2, n_init=5, random_state=0).fit(x[:, None])
scores = g.score_samples(x[:, None])       # each point's log-density
threshold = np.percentile(scores, 1)       # the lowest 1%
print(round(threshold, 2), int((scores < threshold).sum()))
for v in (0.0, 4.0, 9.0, -5.0):
    s = g.score_samples([[v]])[0]
    print(v, round(float(s), 2), s < threshold)
```

```text
-4.05 5
0.0 -1.46 False
4.0 -2.2 False
9.0 -8.71 True
-5.0 -12.68 True
```

We put the threshold at the data's lowest 1% log-density (−4.05); 5 points of
the training data are below it. Of the new values, 0 and 4 are in the middle of
the components, with high log-densities (−1.46 and −2.2). 9 and −5 are far
below the threshold (−8.71 and −12.68): both count as outliers. −5 comes out
more anomalous than 9 because the left component is narrow (variance 1.12) and
the right one wide: to the right the density falls more slowly.

Choosing the threshold is a decision: 1% means accepting that one in every
hundred points of clean data is also flagged as "anomalous". In a real
application the threshold is chosen by the cost of a false alarm.
