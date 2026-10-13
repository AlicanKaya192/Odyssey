# Similarity and Search

Once text is turned into numbers, every document is a **vector**: a point in
a space with many dimensions. That lets us ask a new question: how **similar**
are two documents? Search engines, "similar products", finding duplicate
support tickets and the semantic search of the second module all rest on
this question. This section compares two measures of similarity, builds a
small search engine over help articles, measures how good the search is and
writes BM25, the classic formula of search engines, from scratch.

## Distance or angle?

Take three documents with the seven-word vocabulary of section 05: "the
battery is great", the same sentence repeated three times, and "great price
great sound".

```python
import numpy as np

a = np.array([1, 0, 1, 1, 0, 0, 1])
b = 3 * a
c = np.array([0, 0, 2, 0, 1, 1, 0])


def cosine(x, y):
    return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))


print(np.linalg.norm(a - b).round(3), cosine(a, b).round(3))
print(np.linalg.norm(a - c).round(3), cosine(a, c).round(3))
```

```text
4.0 1.0
2.449 0.408
```

- **Euclidean distance** (`np.linalg.norm(a - b)`) is the length of the
  straight line between two points. The distance to the same sentence
  repeated three times (b) is 4; to c, which is about something else, 2.449.
  By Euclid, a is closer to c: wrong.
- **Cosine similarity** is the cosine of the angle between two vectors: the
  dot product divided by the product of the lengths. 1 if they point the same
  way, 0 if they share no word. a and b point the same way: 1. a and c share
  only "great": 0.408.
- In text, length carries no meaning; direction does. That is why text
  similarity is almost always measured with the cosine.

## Cosine with TF-IDF

We saw in section 06 that TF-IDF rows have unit length. For unit vectors the
cosine **is the dot product itself**; no denominator is needed.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ["the battery is great", "the battery died", "great price great sound"]
X = TfidfVectorizer().fit_transform(docs)
print((X @ X.T).toarray().round(3).tolist())
print(np.allclose((X @ X.T).toarray(), cosine_similarity(X)))
```

```text
[[1.0, 0.476, 0.337], [0.476, 1.0, 0.0], [0.337, 0.0, 1.0]]
True
```

`X @ X.T` is a table of every document's similarity with every document:
the diagonal is 1 (every document is fully similar to itself), the first and
second documents share "the battery" for 0.476, the first and third share
"great" for 0.337; the third document shares no word with the second: 0.
`cosine_similarity` gives the same table and works on vectors that are not
normalised too.

## A search engine

`make_articles()` in `text_data.py` gives 15 articles of a help centre; three
articles for each support category. Let us compare a question with the
articles:

```python
from text_data import make_articles

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]
vectorizer = TfidfVectorizer().fit(texts)
A = vectorizer.transform(texts)


def search(query, k=3):
    scores = cosine_similarity(vectorizer.transform([query]), A).ravel()
    best = np.argsort(scores)[::-1][:k]
    return [(articles[i]["title"], round(float(scores[i]), 3)) for i in best]


for title, score in search("I forgot my password"):
    print(score, title)
```

```text
0.338 Resetting your password
0.106 Locked accounts and login problems
0.0 Refund or replacement for a damaged item
```

- The vectoriser is `fit` on the articles: the vocabulary and the IDF come
  from the documents being searched. The query is only `transform`ed.
- The first result is the right article. The scores may look low (0.338),
  but what matters is the **ranking**: the absolute cosine score depends on
  the lengths of the document and the query.
- The third result scores **0**: it shares no word with the query and is
  only there to fill the list. A real search engine does not show results
  that score 0.

## Vocabulary mismatch

```python
for title, score in search("money back for broken item", k=2):
    print(score, title)
```

```text
0.294 Refund or replacement for a damaged item
0.109 How refunds work
```

The right article ("Refund or replacement for a damaged item") was found,
but only thanks to the words "item" and "for": the query says "money back"
and "broken", the article "refund" and "damaged". A bag of words and TF-IDF
only match **the same words**; they know nothing of synonyms. This is called
**vocabulary mismatch**. The embeddings of the second module exist to solve
it.

## Measuring search

We cannot tell whether a search engine is good by looking at single queries.
Let us use 1000 support tickets as queries: if the category of the top
article matches the ticket's category, it is a hit. This measure is called
**precision@1** (the hit rate of the first result).

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_tickets

tickets = make_tickets(1000)
queries = [t["text"] for t in tickets]
truth = np.array([t["category"] for t in tickets])
cats = np.array([a["category"] for a in articles])


def precision_at_1(vec):
    vec.fit(texts)
    scores = cosine_similarity(vec.transform(queries), vec.transform(texts))
    return round(float((cats[scores.argmax(axis=1)] == truth).mean()), 3)


print("count", precision_at_1(CountVectorizer()))
print("tfidf", precision_at_1(TfidfVectorizer()))
print("tfidf+stop", precision_at_1(TfidfVectorizer(stop_words="english")))
```

```text
count 0.678
tfidf 0.784
tfidf+stop 0.809
```

- 67.8% with counts; 78.4% with TF-IDF. IDF kept words found everywhere,
  such as "the", "my" and "I", from inflating the score.
- A stop list is a bit better for this task (80.9%): here negation does not
  matter, the topic does (the rule of section 03: depending on the task).
- It is not 100% because some tickets also contain a sentence from another
  category, and some are written with words that never appear in the
  articles.

## BM25

The classic formula search engines have used for decades is **BM25**. It is
similar to TF-IDF with two differences: repeating a word stops adding much to
the score after a point (saturation, `k1`), and long documents are penalised
relative to the average length (`b`).

```python
import math
from collections import Counter

analyze = CountVectorizer().build_analyzer()
tokens = [analyze(t) for t in texts]
avg_len = sum(len(t) for t in tokens) / len(tokens)
df = Counter(w for t in tokens for w in set(t))
N = len(tokens)


def bm25(query, k1=1.5, b=0.75):
    scores = []
    for doc in tokens:
        tf = Counter(doc)
        norm = k1 * (1 - b + b * len(doc) / avg_len)
        score = 0.0
        for w in analyze(query):
            if w in tf:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                score += idf * tf[w] * (k1 + 1) / (tf[w] + norm)
        scores.append(score)
    return scores


S = np.array([bm25(q) for q in queries])
print("bm25", round(float((cats[S.argmax(axis=1)] == truth).mean()), 3))
```

```text
bm25 0.755
```

- `tf[w] * (k1 + 1) / (tf[w] + norm)` approaches `k1 + 1` as the word's
  count in the document grows, but never passes it: a word appearing 10 times
  is worth at most 2.5 times one appearing once.
- `norm` takes the document's length into account; `b = 0.75` is the
  strength of that effect: the same count is worth less in a long document.
- On this data BM25 (75.5%) did not beat TF-IDF (78.4%). The articles are
  short and close in length; BM25's length correction gains nothing here. On
  documents of very different lengths (web pages, books) BM25 usually comes
  out ahead. Always **measure on your own data** which method is better; a
  formula known as "the best method" is not the best on every data set.

## Summary

- Documents are vectors; text similarity is measured with the **cosine**,
  not with distance (direction matters, not length).
- TF-IDF rows have unit length: cosine = dot product, `X @ X.T`.
- Search: `fit` + `transform` the documents, only `transform` the query,
  rank by cosine.
- A bag of words knows no synonyms (broken / damaged): vocabulary mismatch.
- Evaluate search with a measure such as precision@1 on real queries. On
  this data TF-IDF reached 78.4%, 80.9% with a stop list, BM25 75.5%.
