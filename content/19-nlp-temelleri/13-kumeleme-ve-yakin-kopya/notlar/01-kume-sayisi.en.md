In K-Means you give the number of clusters. A common measure is the
**silhouette score**: for each document, the difference between "how close
it is to its own cluster" and "how far it is from the nearest other
cluster", between −1 and 1. A value near 1 means clearly separated clusters.

```python
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import silhouette_score
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
X = TfidfVectorizer(stop_words=stop, token_pattern=r"[a-z]{2,}",
                    min_df=5).fit_transform(texts)
for k in [3, 5, 8, 10]:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    score = silhouette_score(X, kmeans.labels_, metric="cosine")
    print(k, round(score, 3), round(kmeans.inertia_))
```

```text
3 0.07 1715
5 0.123 1599
8 0.152 1484
10 0.195 1398
```

- The silhouette scores are very low (0.07–0.20): the tickets do not form
  clearly separated clusters. This is common with text; documents share many
  words and clusters overlap.
- The score rises with k and there is no peak in the middle. The sum of
  distances within clusters (`inertia_`) always falls too. Neither shows the
  "right" k on this data.
- In practice choose k by use: if the support team has five groups, 5; if a
  finer breakdown is wanted, 10. Look at each cluster's words and a few of
  its examples and decide whether it makes sense.
