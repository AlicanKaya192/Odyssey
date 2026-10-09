The k-means++ start rests on a simple idea: choose the first centroid at
random, and each next one from points **far from the existing centroids**.
Distance is not fully decisive but a probability: a point's chance of being
chosen is proportional to its **squared distance** to the nearest centroid.
Far points are more likely, but a single outlier is not chosen every time.

With the lesson's `X` and `kmeans`, let us compare 100 random starts with 100
k-means++ starts:

```python
def kmeans_pp(X, k, rng):
    C = [X[rng.integers(len(X))]]
    while len(C) < k:
        # each point's squared distance to its nearest centroid
        d = ((X[:, None, :] - np.array(C)[None]) ** 2).sum(axis=2).min(axis=1)
        C.append(X[rng.choice(len(X), p=d / d.sum())])
    return np.array(C)


for name in ("random", "k-means++"):
    r = np.random.default_rng(0)
    stuck, rounds = 0, []
    for _ in range(100):
        if name == "random":
            start = X[r.choice(len(X), 3, replace=False)]
        else:
            start = kmeans_pp(X, 3, r)
        history = kmeans(X, start)[2]
        stuck += history[-1] > 549
        rounds.append(len(history))
    print(name, stuck, np.mean(rounds))
```

```text
random 4 5.78
k-means++ 1 4.34
```

k-means++ cut the stuck runs from 4 to 1 and the mean number of rounds from
5.78 to 4.34: centroids that start well settle faster. But getting stuck is
not zero; that is why scikit-learn uses k-means++ together with `n_init` and
keeps the best of several tries.

k-means++ is not only a good start; it also has a guarantee: the expected
inertia is at most `O(log k)` times the best solution. A random start has no
such bound.
