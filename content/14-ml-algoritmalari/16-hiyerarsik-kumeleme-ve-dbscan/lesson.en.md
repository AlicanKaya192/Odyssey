# Hierarchical Clustering and DBSCAN

k-Means and GMMs look for clusters around a centre; they struggle with shapes
like half-moons and with noisy data, and they want `k` in advance. In this
section we look at two different ideas. **Hierarchical clustering** merges
points step by step and builds a **tree**; we choose `k` afterwards by cutting
the tree at a height. **DBSCAN** defines a cluster as a **dense region**:
points close to each other form a cluster whatever its shape, and those in
sparse regions are **noise**. We write both from scratch and compare them with
SciPy and scikit-learn.

## Clustering by merging

Agglomerative hierarchical clustering works like this:

1. Every point is a cluster on its own.
2. Merge the two clusters closest to each other.
3. Repeat step 2 until one cluster remains.

"The distance between two clusters" can be defined in several ways; this is
called the **linkage**:

- **single:** the distance between the two closest points of the clusters.
- **complete:** the distance between their two farthest points.
- **average:** the mean distance over all pairs of points.
- **ward:** the pair whose merge increases the within-cluster sum of squared
  distances least (similar to k-Means' measure).

```python
import numpy as np
from scipy.cluster.hierarchy import linkage

X = np.array([[1.0, 1.0], [1.5, 1.2], [1.2, 1.9], [5.0, 5.0], [5.6, 5.2],
              [5.2, 6.1], [9.0, 1.0], [8.4, 1.6]])


def agglomerate(X, method="single"):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    clusters = {i: [i] for i in range(len(X))}        # cluster id -> points
    merges, nxt = [], len(X)
    while len(clusters) > 1:
        best = None
        keys = sorted(clusters)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                block = D[np.ix_(clusters[a], clusters[b])]
                d = {"single": block.min(), "complete": block.max(),
                     "average": block.mean()}[method]
                if best is None or d < best[0]:
                    best = (d, a, b)
        d, a, b = best
        clusters[nxt] = clusters.pop(a) + clusters.pop(b)   # new cluster id
        merges.append((a, b, round(float(d), 3)))
        nxt += 1
    return merges


for a, b, d in agglomerate(X):
    print(a, b, d)
for method in ("single", "complete", "average"):
    ours = [m[2] for m in agglomerate(X, method)]
    print(method, ours[-2:], ours == linkage(X, method)[:, 2].round(3).tolist())
```

```text
0 1 0.539
3 4 0.632
2 8 0.762
6 7 0.849
5 9 0.985
11 12 4.561
10 13 4.904
single [4.561, 4.904] True
complete [6.36, 8.0] True
average [5.385, 6.442] True
```

Each line is one merge: which two clusters, at what distance. New clusters are
numbered 8, 9, 10... (SciPy's convention). The first five merges are below 1,
inside the clusters; the last two are above 4.5 and join the clusters to each
other. For all three linkages every merge distance equals SciPy's `linkage`
result. The last merges depend on the linkage: the final merge is at 4.904
with single and at 8.0 with complete.

These merges are drawn as a **dendrogram** (a tree diagram). Cutting the tree
horizontally at a height gives the clusters: cutting anywhere between 1 and
4.5 leaves three clusters.

<figure class="fig">
<svg viewBox="0 0 480 250" width="480" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="40" y1="220.0" x2="460" y2="220.0"/><text class="dim" x="32" y="224.0" font-size="11" text-anchor="end">0</text><line class="grid" x1="40" y1="181.5" x2="460" y2="181.5"/><text class="dim" x="32" y="185.5" font-size="11" text-anchor="end">1</text><line class="grid" x1="40" y1="143.1" x2="460" y2="143.1"/><text class="dim" x="32" y="147.1" font-size="11" text-anchor="end">2</text><line class="grid" x1="40" y1="104.6" x2="460" y2="104.6"/><text class="dim" x="32" y="108.6" font-size="11" text-anchor="end">3</text><line class="grid" x1="40" y1="66.2" x2="460" y2="66.2"/><text class="dim" x="32" y="70.2" font-size="11" text-anchor="end">4</text><line class="grid" x1="40" y1="27.7" x2="460" y2="27.7"/><text class="dim" x="32" y="31.7" font-size="11" text-anchor="end">5</text><polyline class="curve" points="107.1,220.0 107.1,199.3 164.3,199.3 164.3,220.0"/><polyline class="curve" points="392.9,220.0 392.9,195.7 450.0,195.7 450.0,220.0"/><polyline class="curve" points="50.0,220.0 50.0,190.7 135.7,190.7 135.7,199.3"/><polyline class="curve" points="221.4,220.0 221.4,187.4 278.6,187.4 278.6,220.0"/><polyline class="curve" points="335.7,220.0 335.7,182.1 421.4,182.1 421.4,195.7"/><polyline class="curve" points="250.0,187.4 250.0,44.6 378.6,44.6 378.6,182.1"/><polyline class="curve" points="92.9,190.7 92.9,31.4 314.3,31.4 314.3,44.6"/><line class="curve2" x1="40" y1="123.8" x2="460" y2="123.8" stroke-dasharray="6 4"/><text class="ink" x="107.1" y="238" font-size="12" text-anchor="middle">0</text><text class="ink" x="164.3" y="238" font-size="12" text-anchor="middle">1</text><text class="ink" x="50.0" y="238" font-size="12" text-anchor="middle">2</text><text class="ink" x="392.9" y="238" font-size="12" text-anchor="middle">3</text><text class="ink" x="450.0" y="238" font-size="12" text-anchor="middle">4</text><text class="ink" x="335.7" y="238" font-size="12" text-anchor="middle">5</text><text class="ink" x="221.4" y="238" font-size="12" text-anchor="middle">6</text><text class="ink" x="278.6" y="238" font-size="12" text-anchor="middle">7</text></svg>
<figcaption>The single-linkage dendrogram of the eight points. The height of each horizontal line is the merge distance. The orange dashed line cuts the tree at 2.5: three branches, three clusters ({0, 1, 2}, {3, 4, 5}, {6, 7}).</figcaption>
</figure>

## The linkage matters

Let us try the two half-moons that could not be split in the k-Means section;
and let us also add 20 random **noise** points to the same data:

```python
from sklearn.datasets import make_moons
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score

Xm, ym = make_moons(300, noise=0.06, random_state=0)
rng = np.random.default_rng(16)
Xn = np.vstack([Xm, rng.uniform(-1.5, 2.5, (20, 2))])   # 20 noise points
for link in ("single", "complete", "average", "ward"):
    clean = AgglomerativeClustering(2, linkage=link).fit_predict(Xm)
    noisy = AgglomerativeClustering(2, linkage=link).fit_predict(Xn)
    print(link, round(adjusted_rand_score(ym, clean), 3),
          round(adjusted_rand_score(ym, noisy[:300]), 3))
```

```text
single 1.0 0.0
complete 0.197 0.132
average 0.425 0.0
ward 0.297 0.297
```

On clean data **single** linkage finds the two moons perfectly (1.0): along a
moon every point is close to its neighbour, so the chain never breaks. The
others still look for round clusters. But once 20 noise points are added,
single (and average) drop to 0: the noise points build bridges between the
moons, the tree gathers almost everything into one cluster, and the "second
cluster" is just 4 distant noise points. This is single linkage's known
weakness: **chaining**.

## DBSCAN: clusters by density

DBSCAN asks for two numbers: a radius `eps` and a minimum number of points
`min_samples`. It splits the points into three kinds:

- **Core:** at least `min_samples` points (itself included) within radius
  `eps`.
- **Border:** not a core point but a neighbour of one.
- **Noise:** neither; it joins no cluster, its label is `−1`.

A cluster is a chain of core points closer than `eps` to each other, plus
their border neighbours. No `k` is given; the number of clusters comes from
the data.

```python
from sklearn.cluster import DBSCAN, KMeans


def dbscan(X, eps, min_samples):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    neigh = [np.where(row <= eps)[0] for row in D]       # itself included
    core = np.array([len(nb) >= min_samples for nb in neigh])
    labels = np.full(len(X), -1)                         # -1: noise
    c = 0
    for i in range(len(X)):
        if labels[i] != -1 or not core[i]:
            continue
        labels[i] = c                                    # a new cluster
        stack = [i]
        while stack:
            p = stack.pop()
            if not core[p]:
                continue                                 # border: no spread
            for q in neigh[p]:
                if labels[q] == -1:
                    labels[q] = c
                    stack.append(q)
        c += 1
    return labels, core


labels, core = dbscan(Xn, 0.2, 5)
ref = DBSCAN(eps=0.2, min_samples=5).fit(Xn)
noise = int((labels == -1).sum())
print((labels == ref.labels_).all(), labels.max() + 1, int(core.sum()), noise)
moons = round(adjusted_rand_score(ym, labels[:300]), 3)
print(moons, int((labels[300:] == -1).sum()))
km = KMeans(2, n_init=10, random_state=0).fit(Xn)
print(round(adjusted_rand_score(ym, km.labels_[:300]), 3))
```

```text
True 2 302 15
1.0 15
0.221
```

Our DBSCAN matches scikit-learn on every label. It found 2 clusters (nobody
told it 2), and 302 of the 320 points are core points. 15 points are noise and
all of them come from the 20 added noise points; the other 5 happened to land
on the moons. The moons are separated perfectly (1.0). On the same data
k-Means stays at 0.221.

<figure class="fig">
<svg viewBox="0 0 480 300" width="480" xmlns="http://www.w3.org/2000/svg"><circle class="dot" cx="255.1" cy="221.9" r="3" fill-opacity=".85"/><circle class="dot" cx="220.4" cy="203.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="270.1" cy="160.4" r="3" fill-opacity=".85"/><circle class="dot" cx="273.2" cy="221.0" r="3" fill-opacity=".85"/><circle class="dot" cx="290.5" cy="214.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="131.6" cy="173.7" r="3" fill-opacity=".85"/><circle class="dot" cx="287.6" cy="219.7" r="3" fill-opacity=".85"/><circle class="dot" cx="251.5" cy="214.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="239.7" cy="126.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="153.6" cy="129.6" r="3" fill-opacity=".85"/><circle class="dot" cx="340.3" cy="167.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.0" cy="164.2" r="3" fill-opacity=".85"/><circle class="dot" cx="219.7" cy="203.1" r="3" fill-opacity=".85"/><circle class="dot" cx="305.2" cy="222.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.6" cy="161.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="199.9" cy="115.4" r="3" fill-opacity=".85"/><circle class="dot" cx="329.1" cy="184.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="175.7" cy="118.2" r="3" fill-opacity=".85"/><circle class="dot" cx="280.9" cy="226.2" r="3" fill-opacity=".85"/><circle class="dot" cx="209.1" cy="172.2" r="3" fill-opacity=".85"/><circle class="dot" cx="230.7" cy="200.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="173.1" cy="122.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="141.3" cy="151.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="144.1" cy="154.6" r="3" fill-opacity=".85"/><circle class="dot" cx="273.4" cy="228.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="149.5" cy="144.1" r="3" fill-opacity=".85"/><circle class="dot" cx="233.3" cy="207.8" r="3" fill-opacity=".85"/><circle class="dot" cx="346.2" cy="168.7" r="3" fill-opacity=".85"/><circle class="dot" cx="291.8" cy="222.1" r="3" fill-opacity=".85"/><circle class="dot" cx="340.7" cy="158.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="178.3" cy="118.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="226.0" cy="117.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.4" cy="175.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="142.4" cy="146.1" r="3" fill-opacity=".85"/><circle class="dot" cx="259.7" cy="220.8" r="3" fill-opacity=".85"/><circle class="dot" cx="204.5" cy="150.0" r="3" fill-opacity=".85"/><circle class="dot" cx="211.6" cy="188.7" r="3" fill-opacity=".85"/><circle class="dot" cx="213.3" cy="197.1" r="3" fill-opacity=".85"/><circle class="dot" cx="342.7" cy="149.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.1" cy="175.5" r="3" fill-opacity=".85"/><circle class="dot" cx="278.5" cy="230.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="184.4" cy="116.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="191.5" cy="118.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="256.5" cy="141.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="230.7" cy="128.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="139.7" cy="166.9" r="3" fill-opacity=".85"/><circle class="dot" cx="287.9" cy="225.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="221.5" cy="119.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="274.2" cy="177.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="247.9" cy="125.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="203.0" cy="121.5" r="3" fill-opacity=".85"/><circle class="dot" cx="250.8" cy="216.9" r="3" fill-opacity=".85"/><circle class="dot" cx="206.9" cy="186.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="157.8" cy="130.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="218.3" cy="118.6" r="3" fill-opacity=".85"/><circle class="dot" cx="316.5" cy="208.8" r="3" fill-opacity=".85"/><circle class="dot" cx="207.5" cy="176.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="265.8" cy="161.2" r="3" fill-opacity=".85"/><circle class="dot" cx="349.8" cy="171.2" r="3" fill-opacity=".85"/><circle class="dot" cx="201.2" cy="157.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="138.8" cy="164.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="124.9" cy="171.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="220.3" cy="113.4" r="3" fill-opacity=".85"/><circle class="dot" cx="341.5" cy="153.3" r="3" fill-opacity=".85"/><circle class="dot" cx="343.2" cy="168.9" r="3" fill-opacity=".85"/><circle class="dot" cx="269.2" cy="216.4" r="3" fill-opacity=".85"/><circle class="dot" cx="316.0" cy="204.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="152.0" cy="137.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="278.0" cy="161.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="243.2" cy="123.2" r="3" fill-opacity=".85"/><circle class="dot" cx="204.8" cy="157.4" r="3" fill-opacity=".85"/><circle class="dot" cx="277.9" cy="219.8" r="3" fill-opacity=".85"/><circle class="dot" cx="329.1" cy="180.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="262.8" cy="151.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="136.4" cy="180.8" r="3" fill-opacity=".85"/><circle class="dot" cx="315.7" cy="209.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="256.9" cy="137.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="171.0" cy="118.9" r="3" fill-opacity=".85"/><circle class="dot" cx="223.8" cy="207.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="134.7" cy="165.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="147.6" cy="144.5" r="3" fill-opacity=".85"/><circle class="dot" cx="205.1" cy="166.2" r="3" fill-opacity=".85"/><circle class="dot" cx="323.6" cy="201.9" r="3" fill-opacity=".85"/><circle class="dot" cx="260.1" cy="223.6" r="3" fill-opacity=".85"/><circle class="dot" cx="289.3" cy="220.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="200.9" cy="106.1" r="3" fill-opacity=".85"/><circle class="dot" cx="253.0" cy="215.1" r="3" fill-opacity=".85"/><circle class="dot" cx="278.3" cy="226.6" r="3" fill-opacity=".85"/><circle class="dot" cx="320.0" cy="212.4" r="3" fill-opacity=".85"/><circle class="dot" cx="281.5" cy="216.5" r="3" fill-opacity=".85"/><circle class="dot" cx="333.1" cy="173.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="243.3" cy="122.7" r="3" fill-opacity=".85"/><circle class="dot" cx="338.4" cy="190.9" r="3" fill-opacity=".85"/><circle class="dot" cx="223.5" cy="207.8" r="3" fill-opacity=".85"/><circle class="dot" cx="202.0" cy="155.1" r="3" fill-opacity=".85"/><circle class="dot" cx="203.3" cy="162.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="168.9" cy="124.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="230.2" cy="128.2" r="3" fill-opacity=".85"/><circle class="dot" cx="224.2" cy="196.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="266.6" cy="162.3" r="3" fill-opacity=".85"/><circle class="dot" cx="332.2" cy="179.1" r="3" fill-opacity=".85"/><circle class="dot" cx="308.5" cy="208.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="144.3" cy="153.3" r="3" fill-opacity=".85"/><circle class="dot" cx="214.6" cy="179.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="209.0" cy="115.2" r="3" fill-opacity=".85"/><circle class="dot" cx="277.3" cy="223.1" r="3" fill-opacity=".85"/><circle class="dot" cx="302.8" cy="219.8" r="3" fill-opacity=".85"/><circle class="dot" cx="247.4" cy="219.8" r="3" fill-opacity=".85"/><circle class="dot" cx="346.7" cy="168.2" r="3" fill-opacity=".85"/><circle class="dot" cx="260.6" cy="218.0" r="3" fill-opacity=".85"/><circle class="dot" cx="206.8" cy="163.5" r="3" fill-opacity=".85"/><circle class="dot" cx="204.2" cy="160.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="250.8" cy="139.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="181.7" cy="121.1" r="3" fill-opacity=".85"/><circle class="dot" cx="309.4" cy="219.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="220.9" cy="125.2" r="3" fill-opacity=".85"/><circle class="dot" cx="215.3" cy="175.0" r="3" fill-opacity=".85"/><circle class="dot" cx="341.8" cy="179.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="154.3" cy="141.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="266.4" cy="159.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="265.3" cy="140.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="139.6" cy="178.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="267.9" cy="167.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="233.9" cy="119.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="195.6" cy="114.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="160.3" cy="133.3" r="3" fill-opacity=".85"/><circle class="dot" cx="212.6" cy="189.9" r="3" fill-opacity=".85"/><circle class="dot" cx="234.7" cy="209.6" r="3" fill-opacity=".85"/><circle class="dot" cx="204.4" cy="168.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="281.5" cy="177.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="174.5" cy="122.2" r="3" fill-opacity=".85"/><circle class="dot" cx="214.2" cy="167.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="227.6" cy="116.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="206.1" cy="116.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="134.9" cy="168.2" r="3" fill-opacity=".85"/><circle class="dot" cx="241.0" cy="222.4" r="3" fill-opacity=".85"/><circle class="dot" cx="322.2" cy="199.4" r="3" fill-opacity=".85"/><circle class="dot" cx="336.8" cy="185.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="254.4" cy="132.3" r="3" fill-opacity=".85"/><circle class="dot" cx="326.3" cy="192.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="275.3" cy="167.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="162.5" cy="131.2" r="3" fill-opacity=".85"/><circle class="dot" cx="266.1" cy="226.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="273.9" cy="180.9" r="3" fill-opacity=".85"/><circle class="dot" cx="208.3" cy="161.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="144.0" cy="156.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="262.3" cy="152.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="256.3" cy="141.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="202.1" cy="114.6" r="3" fill-opacity=".85"/><circle class="dot" cx="345.4" cy="154.2" r="3" fill-opacity=".85"/><circle class="dot" cx="251.2" cy="227.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.7" cy="158.9" r="3" fill-opacity=".85"/><circle class="dot" cx="313.3" cy="212.5" r="3" fill-opacity=".85"/><circle class="dot" cx="296.6" cy="216.5" r="3" fill-opacity=".85"/><circle class="dot" cx="326.5" cy="186.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="191.6" cy="119.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="227.7" cy="123.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="265.8" cy="185.5" r="3" fill-opacity=".85"/><circle class="dot" cx="288.7" cy="222.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="170.1" cy="124.7" r="3" fill-opacity=".85"/><circle class="dot" cx="222.2" cy="195.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="191.7" cy="115.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="276.1" cy="167.1" r="3" fill-opacity=".85"/><circle class="dot" cx="234.4" cy="213.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="231.5" cy="131.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="256.0" cy="130.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="271.2" cy="164.8" r="3" fill-opacity=".85"/><circle class="dot" cx="199.9" cy="159.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="243.3" cy="119.4" r="3" fill-opacity=".85"/><circle class="dot" cx="355.7" cy="161.6" r="3" fill-opacity=".85"/><circle class="dot" cx="284.2" cy="222.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="139.3" cy="149.8" r="3" fill-opacity=".85"/><circle class="dot" cx="241.2" cy="212.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="226.9" cy="119.1" r="3" fill-opacity=".85"/><circle class="dot" cx="222.8" cy="203.0" r="3" fill-opacity=".85"/><circle class="dot" cx="269.7" cy="228.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="133.8" cy="153.2" r="3" fill-opacity=".85"/><circle class="dot" cx="255.5" cy="212.0" r="3" fill-opacity=".85"/><circle class="dot" cx="316.8" cy="211.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="244.5" cy="129.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="153.7" cy="134.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="136.3" cy="162.6" r="3" fill-opacity=".85"/><circle class="dot" cx="343.7" cy="162.2" r="3" fill-opacity=".85"/><circle class="dot" cx="257.6" cy="224.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="134.3" cy="190.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="157.6" cy="130.6" r="3" fill-opacity=".85"/><circle class="dot" cx="296.6" cy="210.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="160.8" cy="122.4" r="3" fill-opacity=".85"/><circle class="dot" cx="268.5" cy="220.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="171.6" cy="123.4" r="3" fill-opacity=".85"/><circle class="dot" cx="260.7" cy="221.2" r="3" fill-opacity=".85"/><circle class="dot" cx="205.2" cy="169.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="255.9" cy="142.8" r="3" fill-opacity=".85"/><circle class="dot" cx="214.7" cy="183.8" r="3" fill-opacity=".85"/><circle class="dot2" cx="151.0" cy="139.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="279.0" cy="197.1" r="3" fill-opacity=".3"/><circle class="dot2" cx="180.6" cy="124.2" r="3" fill-opacity=".85"/><circle class="dot" cx="336.8" cy="184.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="178.2" cy="123.3" r="3" fill-opacity=".85"/><circle class="dot" cx="342.0" cy="149.9" r="3" fill-opacity=".85"/><circle class="dot" cx="313.5" cy="201.5" r="3" fill-opacity=".85"/><circle class="dot" cx="291.4" cy="221.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="220.5" cy="116.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="240.8" cy="133.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="238.2" cy="125.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="189.8" cy="114.8" r="3" fill-opacity=".85"/><circle class="dot" cx="345.0" cy="151.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="136.2" cy="182.1" r="3" fill-opacity=".85"/><circle class="dot" cx="249.1" cy="213.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="268.8" cy="154.9" r="3" fill-opacity=".85"/><circle class="dot" cx="301.9" cy="219.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="132.7" cy="179.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="125.5" cy="180.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="193.8" cy="112.5" r="3" fill-opacity=".85"/><circle class="dot" cx="215.1" cy="194.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="166.8" cy="123.7" r="3" fill-opacity=".85"/><circle class="dot" cx="243.2" cy="227.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="140.6" cy="158.2" r="3" fill-opacity=".85"/><circle class="dot" cx="328.6" cy="199.6" r="3" fill-opacity=".85"/><circle class="dot" cx="346.5" cy="150.8" r="3" fill-opacity=".85"/><circle class="dot" cx="232.5" cy="210.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="269.9" cy="178.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="206.9" cy="114.5" r="3" fill-opacity=".85"/><circle class="dot" cx="239.5" cy="213.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="183.8" cy="119.6" r="3" fill-opacity=".85"/><circle class="dot" cx="209.5" cy="186.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="145.7" cy="148.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="127.1" cy="178.4" r="3" fill-opacity=".85"/><circle class="dot" cx="320.5" cy="202.7" r="3" fill-opacity=".85"/><circle class="dot" cx="334.9" cy="184.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="135.0" cy="174.5" r="3" fill-opacity=".85"/><circle class="dot" cx="324.5" cy="212.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="182.6" cy="121.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="191.8" cy="117.8" r="3" fill-opacity=".85"/><circle class="dot" cx="339.4" cy="179.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="273.3" cy="162.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="146.7" cy="144.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="162.2" cy="127.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="258.0" cy="140.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="227.4" cy="118.7" r="3" fill-opacity=".85"/><circle class="dot" cx="205.5" cy="177.4" r="3" fill-opacity=".85"/><circle class="dot" cx="287.5" cy="215.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="217.5" cy="111.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="278.8" cy="189.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="140.9" cy="147.0" r="3" fill-opacity=".85"/><circle class="dot" cx="335.7" cy="193.0" r="3" fill-opacity=".85"/><circle class="dot" cx="220.7" cy="192.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="249.7" cy="141.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="162.8" cy="127.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="138.7" cy="159.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="196.9" cy="121.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="268.4" cy="165.5" r="3" fill-opacity=".85"/><circle class="dot" cx="321.7" cy="204.9" r="3" fill-opacity=".85"/><circle class="dot" cx="287.4" cy="220.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="251.0" cy="138.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="137.1" cy="158.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="226.2" cy="121.2" r="3" fill-opacity=".85"/><circle class="dot" cx="317.9" cy="212.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="131.8" cy="159.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="263.4" cy="145.3" r="3" fill-opacity=".85"/><circle class="dot" cx="216.3" cy="191.9" r="3" fill-opacity=".85"/><circle class="dot" cx="212.5" cy="168.4" r="3" fill-opacity=".85"/><circle class="dot" cx="201.3" cy="147.7" r="3" fill-opacity=".85"/><circle class="dot" cx="305.8" cy="212.0" r="3" fill-opacity=".85"/><circle class="dot" cx="239.4" cy="225.7" r="3" fill-opacity=".85"/><circle class="dot2" cx="268.8" cy="150.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="258.8" cy="132.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="142.1" cy="150.6" r="3" fill-opacity=".85"/><circle class="dot" cx="215.8" cy="206.0" r="3" fill-opacity=".85"/><circle class="dot" cx="335.9" cy="176.6" r="3" fill-opacity=".85"/><circle class="dot" cx="331.6" cy="193.6" r="3" fill-opacity=".85"/><circle class="dot2" cx="134.1" cy="178.7" r="3" fill-opacity=".85"/><circle class="dot" cx="330.7" cy="189.0" r="3" fill-opacity=".85"/><circle class="dot" cx="211.6" cy="184.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="170.0" cy="115.8" r="3" fill-opacity=".85"/><circle class="dot" cx="239.7" cy="210.1" r="3" fill-opacity=".85"/><circle class="dot" cx="306.6" cy="215.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="147.6" cy="137.0" r="3" fill-opacity=".85"/><circle class="dot" cx="324.7" cy="198.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="213.2" cy="116.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="261.4" cy="152.7" r="3" fill-opacity=".85"/><circle class="dot" cx="211.7" cy="175.2" r="3" fill-opacity=".85"/><circle class="dot" cx="341.1" cy="170.8" r="3" fill-opacity=".85"/><circle class="dot" cx="213.4" cy="186.8" r="3" fill-opacity=".85"/><circle class="dot" cx="336.7" cy="169.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="247.9" cy="129.2" r="3" fill-opacity=".85"/><circle class="dot" cx="234.3" cy="204.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="181.9" cy="121.9" r="3" fill-opacity=".85"/><circle class="dot2" cx="208.4" cy="120.4" r="3" fill-opacity=".85"/><circle class="dot2" cx="196.0" cy="127.6" r="3" fill-opacity=".85"/><circle class="dot" cx="302.3" cy="222.2" r="3" fill-opacity=".85"/><circle class="dot" cx="337.1" cy="186.7" r="3" fill-opacity=".85"/><circle class="dot" cx="249.6" cy="223.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="280.6" cy="173.5" r="3" fill-opacity=".85"/><circle class="dot" cx="230.0" cy="206.0" r="3" fill-opacity=".85"/><circle class="dot" cx="311.9" cy="207.7" r="3" fill-opacity=".85"/><circle class="dot" cx="222.0" cy="204.3" r="3" fill-opacity=".85"/><circle class="dot2" cx="152.0" cy="149.2" r="3" fill-opacity=".85"/><circle class="dot2" cx="244.4" cy="120.0" r="3" fill-opacity=".85"/><circle class="dot" cx="211.2" cy="179.0" r="3" fill-opacity=".85"/><circle class="dot2" cx="258.0" cy="170.5" r="3" fill-opacity=".85"/><circle class="dot2" cx="124.5" cy="193.8" r="3" fill-opacity=".3"/><path class="curve3" d="M269.4,282.0 L277.4,290.0 M269.4,290.0 L277.4,282.0"/><path class="curve3" d="M340.9,47.0 L348.9,55.0 M340.9,55.0 L348.9,47.0"/><path class="curve3" d="M106.5,61.5 L114.5,69.5 M106.5,69.5 L114.5,61.5"/><path class="curve3" d="M146.1,91.7 L154.1,99.7 M146.1,99.7 L154.1,91.7"/><path class="curve3" d="M137.7,92.8 L145.7,100.8 M137.7,100.8 L145.7,92.8"/><path class="curve3" d="M364.6,10.0 L372.6,18.0 M364.6,18.0 L372.6,10.0"/><path class="curve3" d="M281.2,241.9 L289.2,249.9 M281.2,249.9 L289.2,241.9"/><circle class="dot" cx="209.4" cy="213.6" r="3" fill-opacity=".3"/><path class="curve3" d="M363.8,203.6 L371.8,211.6 M363.8,211.6 L371.8,203.6"/><circle class="dot2" cx="256.4" cy="177.1" r="3" fill-opacity=".85"/><circle class="dot2" cx="137.1" cy="183.5" r="3" fill-opacity=".85"/><path class="curve3" d="M311.2,171.3 L319.2,179.3 M311.2,179.3 L319.2,171.3"/><path class="curve3" d="M285.7,123.8 L293.7,131.8 M285.7,131.8 L293.7,123.8"/><path class="curve3" d="M115.5,82.0 L123.5,90.0 M115.5,90.0 L123.5,82.0"/><path class="curve3" d="M284.2,61.7 L292.2,69.7 M284.2,69.7 L292.2,61.7"/><path class="curve3" d="M136.0,13.0 L144.0,21.0 M136.0,21.0 L144.0,13.0"/><path class="curve3" d="M338.9,33.1 L346.9,41.1 M338.9,41.1 L346.9,33.1"/><path class="curve3" d="M365.5,112.7 L373.5,120.7 M365.5,120.7 L373.5,112.7"/></svg>
<figcaption>DBSCAN (eps = 0.2, min_samples = 5): two clusters in purple and orange, faint points are border points (3 of them), crosses are noise (15 of them).</figcaption>
</figure>

## Choosing eps

DBSCAN's weak spot is `eps`: too small and everything is noise or broken
clusters, too large and everything is one cluster.

```python
for eps in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0):
    lab = DBSCAN(eps=eps, min_samples=5).fit_predict(Xn)
    print(eps, lab.max() + 1, int((lab == -1).sum()))
```

```text
0.05 10 263
0.1 11 34
0.2 2 15
0.3 1 13
0.5 1 8
1.0 1 0
```

At `eps = 0.05`, 263 of the 320 points are noise and the rest are scattered
into 10 small clusters. At 0.1 there are still 11 clusters. 0.2 is the right
place: 2 clusters. From 0.3 on the two moons merge and one cluster remains; at
1.0 there is no noise either. It is also assumed that all clusters have the
**same density**: for two clusters, one dense and one sparse, a single `eps`
may not exist. One way to choose `eps` is in the lesson note.

## Summary

- Hierarchical clustering builds a tree by merging the closest clusters; `k`
  is chosen afterwards by cutting the tree.
- Linkage: single (closest), complete (farthest), average, ward. Single finds
  long shapes but chains through noise.
- DBSCAN: core, border, noise; it finds the number of clusters from the data,
  has no shape limit and separates noise.
- DBSCAN's settings are `eps` and `min_samples`; it struggles with clusters of
  different densities.
- Both methods rest on distance: scale first.
