# Clustering and Near Duplicates

In this section we do two more jobs with unlabelled text. First
**clustering**: splitting similar documents into groups. Unlike topic
modelling, each document falls into a single cluster. Then finding **near
duplicates**: copies of the same text repeated with small differences. On
review sites, in news feeds and when collecting training data, these copies
distort results. Comparing all pairs becomes impossible on large data; for
that we build two ideas from scratch, **MinHash** and **LSH**
(locality-sensitive hashing).

## Clustering the tickets with K-Means

Let us apply the K-Means you met in ML Algorithms to TF-IDF vectors. The
preprocessing is the same as in 12:

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
categories = np.array([t["category"] for t in tickets])
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
tfidf = TfidfVectorizer(stop_words=stop, token_pattern=r"[a-z]{2,}", min_df=5)
X = tfidf.fit_transform(texts)
words = tfidf.get_feature_names_out()
kmeans = KMeans(n_clusters=5, n_init=10, random_state=0).fit(X)
for i, center in enumerate(kmeans.cluster_centers_):
    size = (kmeans.labels_ == i).sum()
    print(i, size, " ".join(words[center.argsort()[::-1][:5]]))
table = pd.crosstab(pd.Series(kmeans.labels_, name="cluster"),
                    pd.Series(categories, name="category"))
print(table)
print(round(table.max(axis=1).sum() / len(categories), 3))
```

```text
0 415 account email address log access
1 547 order card refund invoice money
2 122 arrived box parcel damaged open
3 419 delivered order address does got
4 497 app error page order history
category  account  billing  refund  shipping  technical
cluster                                                
0             347       48       1         9         10
1              52      259     174        53          9
2               2        1       0       119          0
3               2        2       7       401          7
4               7        8       2        11        469
0.798
```

- A cluster's **centre** (`cluster_centers_`) is the mean TF-IDF vector of
  the documents in the cluster. Its largest words describe the cluster.
- Purity is 0.798: on the same data NMF's heaviest topic gave 0.692. Since
  each ticket falls into one cluster, clustering is more natural for short,
  single-topic texts.
- Billing and refund merged again into **a single money cluster** (1): 259
  billing, 174 refund. Clustering also looks at words; two categories that
  use the same words do not separate.
- Because `TfidfVectorizer` scales rows to unit length (`norm="l2"`),
  Euclidean distance gives the same ordering as cosine similarity here;
  that is why K-Means can be used on text directly.

## Exact duplicates

Let us move to the reviews. First the identical ones: texts that stay the
same after lowercasing and collapsing spaces.

```python
from collections import Counter

from text_data import make_reviews

reviews = [r["text"] for r in make_reviews(1000)]


def normalize(text):
    return " ".join(text.lower().split())


groups = Counter(normalize(t) for t in reviews)
repeated = {t: n for t, n in groups.items() if n > 1}
print(len(repeated), sum(repeated.values()))
print(groups.most_common(2))
```

```text
9 26
[('exactly what i needed.', 6), ('my brother loves it too.', 3)]
```

Finding exact duplicates is easy and fast: a dictionary (or hash table) is
enough, and each text is processed once. But "Exactly what I needed." and
"Exactly what I needed!!" count as different texts.

## Jaccard similarity

Let us think of two texts as **sets of pieces**. As pieces we take character
5-grams (shingles). **Jaccard similarity** is the size of the intersection of
two sets divided by the size of their union: 1 is identical, 0 is no shared
piece.

```python
from itertools import combinations


def shingles(text, n=5):
    text = normalize(text)
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)


print(round(jaccard(shingles("Exactly what I needed."),
                    shingles("Exactly what I needed!!")), 2))
S = [shingles(t) for t in reviews]
all_pairs = list(combinations(range(len(S)), 2))
near = {(i, j) for i, j in all_pairs if jaccard(S[i], S[j]) >= 0.8}
exact = [(i, j) for i, j in near if normalize(reviews[i]) == normalize(reviews[j])]
print(len(all_pairs), len(near), len(near) - len(exact))
```

```text
0.85
499500 46 15
```

- The similarity of the two "Exactly what I needed" reviews is 0.85: the
  exclamation marks change a few pieces, the rest is the same.
- 1000 reviews make 499,500 pairs. Of the 46 pairs above the threshold (0.8),
  15 are not exact copies: reviews with sentences swapped, written in
  capitals or with an exclamation added at the end.
- The problem is scale: the number of pairs grows as n²/2. On this computer
  the pairs of 1000 reviews take a few seconds; 2000 reviews take four times
  as long, and a million reviews are 500 billion pairs. We need to find
  similar ones without comparing every pair.

## MinHash: squeezing a set into a short signature

The idea of **MinHash**: give each piece of the set a number with a hash
function and take the **smallest**. The probability that two sets' smallest
values are the same is exactly their Jaccard similarity. Build a 64-number
**signature** with 64 different hash functions, and the share of equal
numbers estimates Jaccard.

```python
import zlib

NUM = 64


def minhash(shingle_set):
    return [min(zlib.crc32(f"{seed}:{s}".encode()) for s in shingle_set)
            for seed in range(NUM)]


def estimate(sig_a, sig_b):
    return sum(a == b for a, b in zip(sig_a, sig_b)) / NUM


pairs = [("Exactly what I needed.", "Exactly what I needed!!"),
         ("The strap is great.", "The strap is weak."),
         ("Waste of money.", "Arrived early and well packed.")]
for a, b in pairs:
    sa, sb = shingles(a), shingles(b)
    print(round(jaccard(sa, sb), 2), round(estimate(minhash(sa), minhash(sb)), 2))
signatures = [minhash(s) for s in S]
```

```text
0.85 0.92
0.45 0.42
0.0 0.0
```

- On the left the real Jaccard, on the right the estimate from the 64-number
  signature. The estimate is close but not exact: with 64 numbers its
  standard deviation is at most 0.06 (when the similarity is 0.5); the first
  pair is off by 0.07. More numbers narrow it.
- We use `zlib.crc32` as the hash function and get 64 different functions by
  putting the `seed` in front of the text. The second note explains why
  Python's own `hash()` is not used.
- A signature is much smaller than a set and is computed **once per
  review**. But comparing signatures pair by pair is still n² work.

## LSH: comparing only candidate pairs

**LSH** splits the signature into **bands**: 64 numbers = 8 bands × 8
numbers. If any band of two reviews is exactly the same, they become a
**candidate pair**. Identical bands fall into the same bucket; only reviews in
the same bucket are compared.

```python
from collections import defaultdict

BANDS, ROWS = 8, 8
buckets = defaultdict(list)
for idx, sig in enumerate(signatures):
    for b in range(BANDS):
        buckets[(b, tuple(sig[b * ROWS:(b + 1) * ROWS]))].append(idx)
candidates = set()
for members in buckets.values():
    candidates.update(combinations(members, 2))
found = {(i, j) for i, j in candidates if jaccard(S[i], S[j]) >= 0.8}
print(len(candidates), len(found), round(len(found) / len(near), 3))
for s in [0.5, 0.7, 0.8, 0.9]:
    print(s, round(1 - (1 - s ** ROWS) ** BANDS, 3))
```

```text
77 44 0.957
0.5 0.031
0.7 0.378
0.8 0.77
0.9 0.989
```

- Instead of 499,500 pairs we compared only 77 candidate pairs with the real
  Jaccard and found 44 of the 46 pairs above the threshold (95.7%). The two
  missed pairs are the ones unlucky in their signatures.
- The table below is theoretical: the probability that a pair with Jaccard s
  becomes a candidate is `1 - (1 - s^r)^b`. Pairs at 0.5 similarity almost
  never become candidates, those at 0.9 almost always do. With the number of
  bands and rows you move the sharp step of this S curve to the threshold you
  want: more bands, more candidates (fewer misses, more work).
- Search engines, training-data cleaning and plagiarism checks find near
  duplicates among millions of documents with this idea.

## Summary

- K-Means puts each document into one cluster; for short tickets it gave
  purer groups than the topic model (0.798). It still does not know the
  categories.
- For exact duplicates, normalisation + a dictionary is enough.
- For near duplicates, Jaccard similarity: the intersection / union of
  character n-gram sets. Comparing all pairs grows as n².
- MinHash squeezes a set into a short signature; the share of equal numbers
  estimates Jaccard.
- LSH splits the signature into bands and compares only candidate pairs that
  share a band; it finds almost all similar pairs with very little work.
