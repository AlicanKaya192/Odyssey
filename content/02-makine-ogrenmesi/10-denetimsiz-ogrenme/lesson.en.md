# Unsupervised Learning

Every section so far had a `y`: a price, pass/fail, fraud. The model
predicted and we compared against the right answer.

In this section **there is no `y`.**

We have four columns for 350 customers — `spend`, `visits`, `items`,
`returns` — and no list where anyone labelled "this customer is of that
type". The question is: **how many groups do these people fall into, and
what separates the groups?**

## What changes

| | Supervised | Unsupervised |
|---|---|---|
| Input | `X` and `y` | `X` only |
| Output | A prediction | Structure (groups, axes) |
| Metric | Accuracy, MAE, F1 | Silhouette, explained variance |
| A right answer | Exists | **Does not** |
| Train/test | Essential | Usually meaningless |

The last two rows matter. **With no right answer, the sentence "the model
is 92% correct" cannot be written.** The metrics you have tell you how
*tidy* the result is, not how *right* it is.

That makes unsupervised learning not easier but **harder**: the only judge
of whether the result is useful is you.

## K-means

The most common clustering method. The idea is three steps:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>pick <code>k</code> centres<br>at random</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>assign each row<br>to the nearest</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>move centres<br>to the mean</span>
  </div>
  <figcaption>It loops until the centres stop moving. That is where the name comes from: k means.</figcaption>
</figure>

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

`fit_predict` — because there is no separate test set to predict on; the
model learns from and labels the same data.

**`n_clusters` is not a hyperparameter but an input.** You tell the model
"find four groups" and it finds four. Say three and it finds three. It has
no notion of how many groups the data holds.

## The first result

Scaled and run with `k=4`, the cluster sizes come out **79, 102, 70, 99**.
Look at the means:

| Cluster | `spend` | `visits` | `items` | `returns` |
|---|---|---|---|---|
| 0 | 428.2 | 15.2 | 23.4 | 3.3 |
| 1 | 45.8 | 3.2 | 4.2 | 0.3 |
| 2 | 63.9 | **19.3** | 6.4 | 2.6 |
| 3 | 180.2 | 8.4 | 11.3 | 1.1 |

**This table is the section's real output.** The cluster numbers say
nothing; the means say everything:

- **Cluster 1** — comes rarely, spends little. 102 of the 350.
- **Cluster 3** — mid-level, regular. 99 people.
- **Cluster 0** — spends a lot, buys a lot. 79 people.
- **Cluster 2** — **the interesting one.** Its spend is as low as cluster
  1's (63.9) yet it visits 19 times a month and makes 2.6 returns. Someone
  who comes often, browses a lot, buys little and sends back what they buy.

Cluster 2 could not have been found by eye in this data. That is exactly
what clustering is for: **seeing what four columns say at once.**

## Scaling is mandatory here too

K-means rests on distance — just like KNN. Run without scaling:

| | Silhouette |
|---|---|
| Scaled | **0.517** |
| Unscaled | **0.202** |

The unscaled cluster sizes: **175, 47, 95, 33.**

The table explains what happened: `spend` has a spread of 155 and `returns`
of 1.5. In the distance computation `spend` crushes everything.

The result: the model **puts both low-spend groups into one heap of 175** —
the frequent browsers disappear — and in exchange splits the high spenders
in two **by spend alone** (481 and 348).

Instead of four real groups it finds four slices of one column.

## Choosing `k`

If `k` is an input, where does it come from? There are two tools.

**First: inertia.** The sum of squared distances from each record to its
own centre. It necessarily falls as `k` grows — it would be zero if `k`
equalled the record count. What you look for is **where it slows down**:

```
k=2   695.9
k=3   388.8      <- a large drop
k=4   265.6      <- a large drop
k=5   212.7      <- slowing
k=6   189.6
k=7   167.3
```

This is called the **elbow method**: the point where the curve bends. Here
the elbow sits between 3 and 4.

**Second: the silhouette.** For each record, a ratio of "how close to its
own cluster, how far from the nearest other". Between −1 and +1; higher is
better.

```
k=2   0.514
k=3   0.525      <- the highest
k=4   0.517
k=5   0.489
```

**Here is the honest part: the silhouette says `k=3`, while the data was
generated from four groups.** The difference is 0.008 — no larger than the
measurement noise.

The silhouette is not wrong; it answers its own question correctly. Its
question is "how tidy are the clusters", not "how many real groups are
there". Cluster 1 and cluster 2 (the low spenders and the frequent
browsers) sit close together in space; merging into three raises the
silhouette slightly while **losing a distinction that matters to the
business.**

**The conclusion:** `k` is not a measurement result but a decision. The two
tools narrow the range (3 to 4, not 2 to 5) and a person reading the table
of means picks the rest.

## K-means always finds clusters

This section's most important warning. Apply `KMeans` to 350 rows of purely
random data with no structure at all:

```
k=2   silhouette 0.169
k=3   silhouette 0.176
k=4   silhouette 0.181
k=5   silhouette 0.185
```

**The model returns four clusters, the silhouette is positive, and it rises
with `k`.** There are no groups there at all.

Two lessons follow:

1. **Returning clusters is not proof that clusters exist.** The algorithm
   partitions whatever you give it.
2. **Maximising the silhouette is not a method.** It rises even on noise.
   To compare you need a reference — 0.52 on the real data, 0.18 on noise:
   the threefold gap is the actual information.

The test of whether the clusters are real is not a number: **does the table
of means tell a meaningful story?** For cluster 2 it did.

## Cluster numbers are arbitrary

Run the same data with a different `random_state`:

```
seed 0   [45.8, 428.2, 63.9, 180.2]
seed 1   [180.2, 428.2, 63.9, 45.8]
seed 2   [63.9, 45.8, 180.2, 428.2]
```

**The same groups, different numbers.** There is no such thing as "cluster
0"; on the next run it lands on a different group.

This is why two clusterings are not compared by their labels. The right
tool:

```python
from sklearn.metrics import adjusted_rand_score
print(adjusted_rand_score(labels_a, labels_b))
```

The **adjusted Rand score** ignores the numbers and asks "are these two
records in the same cluster in both". 1.0 is the same grouping, 0 is as
similar as chance.

The ARI between the scaled and unscaled clusterings is **0.602** — two
genuinely different groupings, not merely shifted numbers.

## Principal component analysis (PCA)

The second unsupervised method is not clustering but **dimension
reduction**: turning four columns into two while losing as little
information as possible.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
Z = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)   # [0.662 0.223]
```

**The first component carries 66.2% of the data's variance and the second
22.3%.** Together **88.5%**. We turned four columns into two and lost 11.5%
of the information.

What are the components? Look at their weights:

```
component 1   [ 0.531,  0.426,  0.540,  0.495]
component 2   [-0.471,  0.659, -0.425,  0.403]
                spend  visits   items  returns
```

**In the first component all four are positive and close to each other:**
that axis is "overall activity". The further right, the more a customer
does of everything.

**In the second, `visits` and `returns` are positive while `spend` and
`items` are negative:** that axis is precisely "comes often but buys
little". What separates cluster 2 is written in the second component.

PCA found that axis without seeing a single label.

**PCA's cost is interpretability.** The new columns are called `PC1` and
`PC2`; they are mixtures of the four original ones. A sentence like "as
spend rises, this happens" can no longer be written.

## PCA + clustering

Run `KMeans` again on top of the two components:

```
silhouette in the full space   0.517
silhouette in PCA space        0.652
ARI between the two            1.000
```

**ARI 1.000: the grouping is identical.** Two of the four columns were
thrown away and not one customer moved.

**But do not be fooled by the higher silhouette.** 0.652 does not show the
clusters are better, only that they were **measured in fewer dimensions**.
The two discarded dimensions were the noise that blurred the clusters
together; drop them and the same groups merely *look* tidier. Silhouettes
from spaces of different dimension are not comparable.

PCA's real benefit here is **drawing**: you cannot put four-dimensional
data on paper, but you can put two.

## What for when

| Need | Method |
|---|---|
| Splitting customers into groups | K-means |
| Drawing four-dimensional data | PCA |
| Reducing many correlated columns | PCA |
| Finding outlying behaviour | Not clustering; anomaly detection |
| The groups are known in advance | Not clustering; classification |

The last row is often skipped: **if you have labels, do not cluster.**
Supervised learning is always stronger; unsupervised methods are what you
reach for when there are *no* labels.

## What we left out

- **K-means' assumptions.** It looks for round clusters of similar size and
  similar density. Give it two crescent-shaped groups and it will cut both
  down the middle.
- **DBSCAN.** It works on density; it needs no `k`, finds the clusters
  itself, and can mark records belonging to no cluster as **noise**. Far
  better on shapes that are not round.
- **Hierarchical clustering.** It merges records one by one into a tree (a
  dendrogram); you pick `k` afterwards by looking at the tree.
- **t-SNE and UMAP.** Far stronger than PCA for visualisation, but since
  they do not preserve distances you do not cluster on top of them — they
  are for looking only.

This section in one sentence: **in unsupervised learning the algorithm
always gives an answer; you are the one who decides whether the answer
means anything.**
