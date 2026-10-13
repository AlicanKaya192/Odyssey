# Capstone Project: A Semantic Search Engine

In this section we put the module's pieces together and build a small but
complete product: a **search engine** that reads a customer support ticket
and suggests the most suitable help centre article. What we will use:

- word vectors learned from unlabelled tickets (01, 04, 12),
- **hybrid search** combining word matching with TF-IDF and meaning
  similarity with embeddings (04),
- evaluation that measures ranking (14),
- and a must for a real product: being able to say **"I don't know"** when
  it is not sure.

## 1. Word vectors

As in 04: 50-dimensional vectors with PPMI + SVD from 20,000 unlabelled
tickets and 15 articles.

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
articles = make_articles()
article_texts = [a["title"] + " " + a["text"] for a in articles]
corpus = [t["text"] for t in make_tickets(20000, seed=1)] + article_texts
docs = [TOKEN.findall(t.lower()) for t in corpus]
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
U, S, _ = np.linalg.svd(np.nan_to_num(np.maximum(P, 0)))
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(len(articles), len(vocab))
```

```text
15 454
```

## 2. The engine

We write the engine as a class: when it is built it computes the TF-IDF and
embedding vectors of the articles **once** (the index), and at query time it
only computes the query's vectors and compares. The score is the weighted
sum of the two similarities: `alpha` is the share of word matching.

```python
class SearchEngine:
    def __init__(self, texts, alpha=0.3):
        self.alpha = alpha
        self.tfidf = TfidfVectorizer(stop_words="english").fit(texts)
        self.lexical = self.tfidf.transform(texts)
        self.semantic = np.array([self.embed(t) for t in texts])

    @staticmethod
    def embed(text):
        words = [w for w in TOKEN.findall(text.lower())
                 if w in index and w not in ENGLISH_STOP_WORDS]
        if not words:
            return np.zeros(E.shape[1])
        v = np.mean([E[index[w]] for w in words], axis=0)
        return v / np.linalg.norm(v)

    def scores(self, queries):
        lexical = (self.tfidf.transform(queries) @ self.lexical.T).toarray()
        semantic = np.array([self.embed(q) for q in queries]) @ self.semantic.T
        return self.alpha * lexical + (1 - self.alpha) * semantic


engine = SearchEngine(article_texts)
scores = engine.scores(["my pakage never arrived"])[0]
for i in np.argsort(-scores)[:3]:
    print(round(float(scores[i]), 3), articles[i]["title"])
```

```text
0.56 Lost, late or damaged parcels
0.364 Refund or replacement for a damaged item
0.275 Partial refunds
```

A query written with the misspelled "pakage" and "never", which does not
appear in the articles, brings the parcel article to the top.

## 3. Measuring

2000 tickets, each with a known category. An article counts as right if it
is in the ticket's category (each category has 3 articles). Three measures:

- **P@1**: is the first result right?
- **MRR** (mean reciprocal rank): the mean of one over the rank of the
  first right result. 1 at first place, 0.5 at second, 0.33 at third.
- **R@3**: is there at least one right article among the first three
  results?

```python
tickets = make_tickets(2000)
queries = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
categories = np.array([a["category"] for a in articles])


def evaluate(scores):
    order = np.argsort(-scores, axis=1)
    hits = categories[order] == labels[:, None]
    first = hits.argmax(axis=1)
    return (round(float(hits[:, 0].mean()), 3),
            round(float(np.mean(1 / (first + 1))), 3),
            round(float(hits[:, :3].any(axis=1).mean()), 3))


for alpha in [1.0, 0.0, 0.3]:
    engine.alpha = alpha
    print(alpha, *evaluate(engine.scores(queries)))
engine.alpha = 0.3
```

```text
1.0 0.804 0.875 0.93
0.0 0.819 0.89 0.956
0.3 0.839 0.901 0.956
```

- TF-IDF alone (`alpha = 1`) gives P@1 80.4%, embeddings alone 81.9%, hybrid
  search 83.9%. Hybrid is ahead on MRR and R@3 too.
- R@3 is 95.6%: there is almost always a right article among the first
  three. If a product shows three suggestions instead of one result, the
  user's need is mostly met.

## 4. Saying "I don't know"

Anything gets typed into a real search box. Right now the engine suggests an
article for every query, even for a sentence that has nothing to do with
support. A simple cure: suggest no article when the highest score is below a
**threshold**. Let us choose the threshold so that it rejects only 5% of real
tickets, and test it with two kinds of unrelated text: product reviews and
small-world sentences.

```python
from corpus_data import make_corpus
from text_data import make_reviews

threshold = float(np.quantile(engine.scores(queries).max(axis=1), 0.05))
reviews = [r["text"] for r in make_reviews(500)]
world = make_corpus(500)
print(round(threshold, 3))
for name, texts in [("reviews", reviews), ("world", world)]:
    top = engine.scores(texts).max(axis=1)
    print(name, round(float((top < threshold).mean()), 3))


def answer(query):
    scores = engine.scores([query])[0]
    if scores.max() < threshold:
        return "no matching article"
    return articles[int(scores.argmax())]["title"]


for text in ["i was charged twice", "we flew to dublin in ireland",
             "the parcel arrived on time , great service"]:
    print(answer(text))
```

```text
0.408
reviews 0.552
world 0.952
Double charges and pending payments
no matching article
Lost, late or damaged parcels
```

- 95.2% of the small-world sentences are rejected: their words are far from
  the language of support.
- But only 55.2% of the product reviews. Reviews mentioning delivery
  ("Delivery took 18 days") use the words of parcel tickets; in the last
  example a happy customer is sent to the lost parcel article. Separating
  unrelated text **close** to the domain is much harder than separating
  distant text.
- Raising the threshold rejects more unrelated text but also misses real
  tickets (the first note). The product decides which mistake is more
  expensive: a wrong article, or a customer left without an answer?

## Summary

- Search engine = index (the articles' vectors, once) + similarity at query
  time + ranking.
- Hybrid search, combining word matching and meaning similarity, did better
  than either: P@1 83.9%, MRR 0.901, R@3 95.6%.
- Saying "I don't know" with a threshold is possible, but unrelated text
  close to the domain (product reviews) easily passes the threshold.
- Next steps: looking at where the errors gather (the second note), stronger
  pretrained vectors (12), and reranking the first results with a more
  expensive model.
