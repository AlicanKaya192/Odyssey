# Document Embeddings and Semantic Search

In section 07 of NLP Fundamentals we matched support tickets to help-centre
articles with TF-IDF and left a problem open: **vocabulary mismatch**. The
ticket says "package", the article "parcel"; with no shared word the TF-IDF
similarity is 0. In this section we build **document vectors** from word
vectors and move search from word overlap to **similarity of meaning**. This
is called **semantic search**.

## Word vectors from ticket texts

This time let us learn the vectors from the support tickets' own language:
20,000 tickets **separate** from the ones we will evaluate on (a different
seed) plus the articles. The method is the PPMI + SVD of section 01.

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
articles = make_articles()
article_texts = [a["title"] + " " + a["text"] for a in articles]
train_texts = [t["text"] for t in make_tickets(20000, seed=1)] + article_texts
docs = [TOKEN.findall(t.lower()) for t in train_texts]
counts = Counter(w for d in docs for w in d)
vocab = sorted(w for w in counts if counts[w] >= 3)
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for d in docs:
    ids = [index.get(w) for w in d]
    for i, a in enumerate(ids):
        for j in range(max(0, i - 4), min(len(ids), i + 5)):
            if a is not None and j != i and ids[j] is not None:
                M[a, ids[j]] += 1
with np.errstate(divide="ignore", invalid="ignore"):
    P = np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))
P = np.nan_to_num(np.maximum(P, 0))
U, S, _ = np.linalg.svd(P)
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(len(vocab))
for word in ["parcel", "refund", "password"]:
    sims = E @ E[index[word]]
    print(word, [vocab[i] for i in np.argsort(-sims)[1:5]])
```

```text
454
parcel ['arrived', 'box', 'pracel', 'parecl']
refund ['rfeund', 'refnud', 'reufnd', 'insetad']
password ['paswsord', 'psasword', 'passwrod', 'reset']
```

- 454 words. The neighbours of "parcel" are "arrived", "box" and two
  misspelled forms of itself: "pracel", "parecl".
- The nearest neighbours of "refund" and "password" are typos too. Nobody
  said "rfeund really means refund"; the misspelled word appears **in the
  same contexts** as the right one, so its vector landed close. For TF-IDF,
  "rfeund" and "refund" were two unrelated columns.
- `nan_to_num`: the row of a word left with no context gives 0/0 = `nan`; we
  turn it into 0.

## A document vector: the average of word vectors

The simplest way to get a document's vector is the average of the vectors of
its (non-stop, known) words:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def embed(text):
    words = [w for w in TOKEN.findall(text.lower())
             if w in index and w not in ENGLISH_STOP_WORDS]
    if not words:
        return np.zeros(E.shape[1])
    v = np.mean([E[index[w]] for w in words], axis=0)
    return v / np.linalg.norm(v)


a = "Where is my order? It has not arrived yet."
b = "The parcel arrived damaged."
c = "The app crashes on my phone."
tfidf = TfidfVectorizer(stop_words="english").fit(article_texts)
for x, y in [(a, b), (a, c)]:
    vx, vy = tfidf.transform([x]), tfidf.transform([y])
    lexical = cosine_similarity(vx, vy)[0, 0]
    print(round(float(lexical), 3), round(float(embed(x) @ embed(y)), 3))
```

```text
0.0 0.723
0.0 0.129
```

- TF-IDF was built with the articles' vocabulary; "arrived" is not in it (the
  article says "arrives"). So the TF-IDF similarity of the two shipping
  tickets is 0. With embeddings it is 0.723; shipping and an app error get
  0.129.
- The average embedding is noisy at sentence level: even two unrelated
  tickets can get a similarity of 0.1–0.5. Look at the ranking rather than
  single values; search uses the ranking anyway.

## Measuring search

As in NLP Fundamentals: 2000 tickets, 15 articles; a hit if the first
article's category matches the ticket's (precision@1).

```python
tickets = make_tickets(2000)
labels = np.array([t["category"] for t in tickets])
categories = np.array([a["category"] for a in articles])
queries = [t["text"] for t in tickets]
lexical = cosine_similarity(tfidf.transform(queries),
                            tfidf.transform(article_texts))
A = np.array([embed(t) for t in article_texts])
semantic = np.array([embed(q) for q in queries]) @ A.T
for name, scores in [("tfidf", lexical), ("embedding", semantic)]:
    hits = categories[scores.argmax(axis=1)] == labels
    print(name, round(float(hits.mean()), 3))
zero = lexical.max(axis=1) == 0
hits = categories[semantic.argmax(axis=1)] == labels
print(int(zero.sum()), round(float(hits[zero].mean()), 3))
```

```text
tfidf 0.804
embedding 0.819
5 1.0
```

- Search with embeddings scores 81.9%, TF-IDF 80.4%. The gap is small; for
  most tickets the shared words are enough.
- 5 tickets share **no** words with the articles; TF-IDF is blind to them
  (every score is 0). The embeddings sent all five to the right article.

## Combining the two

The two methods are good at different things: TF-IDF at exact word matches
(order numbers, product names), embeddings at meaning. **Hybrid search** adds
the two scores with weights:

```python
for alpha in [0.0, 0.3, 0.5, 0.7, 1.0]:
    mixed = alpha * lexical + (1 - alpha) * semantic
    accuracy = (categories[mixed.argmax(axis=1)] == labels).mean()
    print(alpha, round(float(accuracy), 3))
```

```text
0.0 0.819
0.3 0.839
0.5 0.832
0.7 0.826
1.0 0.804
```

- `alpha = 0` is embeddings only, `1` TF-IDF only. The mix beats both: 83.9%
  at 0.3.
- This is the most common setup in real search systems too: combining the
  scores of a fast word search (such as BM25) and a semantic search. We chose
  `alpha` on the test data here; in real work it is chosen on validation
  data.

## Summary

- In vectors learned from ticket texts, typos became neighbours of the right
  form: "rfeund" ≈ "refund".
- The simplest document vector is the average of word vectors; even two
  tickets with no shared word can come out similar.
- Semantic search slightly beat TF-IDF (81.9% against 80.4%) and also found
  the tickets with no shared words.
- Hybrid search combined the strengths of both: 83.9%.
