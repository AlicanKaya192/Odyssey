# Chunking and Vector Search

The strongest measure against hallucination was giving the model the text to
base its answer on. But sending all of a company's documents in every call is
not possible: they do not fit in the context window and every token is paid
for (07). The solution is to split the documents into small **chunks** and,
for every question, find and send only the **relevant** chunks. This section
builds the search half of this setup; the next section connects it to the
model (RAG).

## Data: a shop's help articles

`doc_data.py`, which the exercises also use, holds 14 short help articles of a
fictional outdoor shop (shipping, returns, warranty, tent care…) and 27
questions. For every question it is written which article gives the answer
and a short phrase that must appear in a correct answer (`key`); the answers
to the last three questions are **not** in the articles.

```python
import re
import numpy as np
from doc_data import DOCS, QUESTIONS
from llm_client import count_tokens

print(len(DOCS), "articles,", len(QUESTIONS), "questions")
print(DOCS[0]["title"])
print(DOCS[0]["text"][:60], "...")
print(QUESTIONS[3])
```

```text
14 articles, 27 questions
Shipping costs and delivery times
Orders over 50 euros ship for free. Smaller orders pay a shi ...
{'q': 'How long do I have to send something back?', 'doc': 'returns', 'key': '30 days'}
```

## Three ways of chunking

```python
def by_article():
    return [(d["id"], d["title"] + ". " + d["text"]) for d in DOCS]


def by_sentence():
    return [(d["id"], s) for d in DOCS
            for s in re.split(r"(?<=\.) ", d["text"])]


def by_window(size, overlap, title=False):
    chunks = []
    for d in DOCS:
        words = d["text"].split()
        head = d["title"] + ": " if title else ""
        for i in range(0, max(len(words) - overlap, 1), size - overlap):
            chunks.append((d["id"], head + " ".join(words[i:i + size])))
    return chunks


for _, text in by_window(12, 4)[:3]:
    print(text)
```

```text
Orders over 50 euros ship for free. Smaller orders pay a shipping
orders pay a shipping fee of 4.90 euros. Standard delivery takes 3
Standard delivery takes 3 to 5 working days. Express delivery costs 9.90
```

- **One chunk per article:** the meaning stays whole but the chunks are large.
- **One chunk per sentence:** small and clear, but a sentence sometimes cannot
  be understood on its own.
- **A fixed window:** every chunk is a set number of words; consecutive chunks
  **overlap** by a few words so that a fact split at a border stays whole in at
  least one chunk. Above, windows of 12 words overlap by 4: every chunk starts
  with the last four words of the one before. `title=True` adds the article's
  title to the start of every chunk.

## Vector search

We turn every chunk into a **vector**: TF-IDF, which you know from the NLP
path. The chunks with the highest **cosine similarity** between their vectors
and a question's vector count as the most relevant. Since TF-IDF vectors
already have length 1, the cosine is the dot product of the two vectors.

```python
from sklearn.feature_extraction.text import TfidfVectorizer


class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        texts = [text for _, text in chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query, k=3):
        q = self.vectorizer.transform([query])
        scores = (self.matrix @ q.T).toarray().ravel()
        best = np.argsort(-scores)[:k]
        return [(self.chunks[i], round(float(scores[i]), 3)) for i in best]


index = Index(by_sentence())
for (doc, text), score in index.search("Do gift cards expire?"):
    print(score, doc)
    print("  " + text)
```

```text
0.383 giftcards
  Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
0.284 refunds
  Purchases paid with a gift card are refunded as a new gift card.
0.26 loyalty
  Points expire if you make no purchase for 12 months.
```

The most relevant chunk is the sentence that carries the question's words
"gift cards" and gives the answer ("valid for 3 years"). In real systems the
vectors usually come from an **embedding model** trained on large amounts of
text (document embeddings in the NLP path), and for millions of chunks
**vector databases** work with approximate nearest neighbour search. The idea
is the same: the vectors closest to the question.

## Which chunking is better?

As the measure we look at how many of the 24 answerable questions have the
correct answer phrase (`key`) in one of the first `k` chunks. Next to it, the
average number of tokens these `k` chunks will take to the model:

```python
answerable = [q for q in QUESTIONS if q["doc"]]


def evaluate(chunks, k=3):
    index = Index(chunks)
    hits, tokens = 0, 0
    for q in answerable:
        found = index.search(q["q"], k)
        hits += any(q["key"] in text for (_, text), _ in found)
        tokens += sum(count_tokens(text) for (_, text), _ in found)
    return round(hits / len(answerable), 2), round(tokens / len(answerable))


for name, chunks in [("article", by_article()),
                     ("sentence", by_sentence()),
                     ("window 12", by_window(12, 0)),
                     ("window 12/4", by_window(12, 4)),
                     ("window 12/4+title", by_window(12, 4, True)),
                     ("window 24/8", by_window(24, 8)),
                     ("window 24/8+title", by_window(24, 8, True))]:
    print(f"{name:18} chunks {len(chunks):2}  key@3 {evaluate(chunks)}")
```

```text
article            chunks 14  key@3 (1.0, 225)
sentence           chunks 52  key@3 (0.71, 50)
window 12          chunks 53  key@3 (0.42, 54)
window 12/4        chunks 69  key@3 (0.5, 56)
window 12/4+title  chunks 69  key@3 (0.58, 75)
window 24/8        chunks 33  key@3 (0.88, 106)
window 24/8+title  chunks 33  key@3 (0.88, 125)
```

The whole article always brings the key (1.0) but takes 225 tokens per
question. Sentences are four times cheaper (50 tokens) but stop at 0.71.
Windows of 12 words split the facts between chunks (0.42); an overlap of 4
words raises this to 0.50, adding the title to 0.58. Windows of 24 words with
an overlap of 8 reach 0.88 with half the tokens of the articles; there the
title adds nothing but tokens. Because these articles are short, sending the
whole article is a good option too; for documents several pages long it is
not. The best setting depends on the data and is not chosen without
measuring.

## What does the search miss?

```python
index = Index(by_window(24, 8, True))
for q in answerable:
    found = index.search(q["q"], 3)
    if not any(q["key"] in text for (_, text), _ in found):
        print(q["q"], "->", found[0][0][0])
```

```text
How much does shipping cost for a 30 euro order? -> payment
How long do I have to send something back? -> warranty
When will I get my money back? -> shipping
```

Even with the best setting three questions are missed, and all three are of
the same kind: the question uses other words than the article. "Send
something back" does not find the returns article, "money back" does not find
the refunds article; "30 euro order" goes to the payment article, which
contains "orders over 300 euros". TF-IDF only matches identical words; it even
counts "cost" and "costs" as different. Embedding models put words close in
meaning on close vectors, so they find such questions better; in practice word
search and embedding search are often used together (**hybrid search**).

## Summary

- Documents are split into chunks; for every question only the relevant chunks
  are found and sent to the model.
- The chunks are turned into vectors; those with the highest cosine similarity
  to the question are chosen. In real systems the vectors come from an
  embedding model.
- Chunk size is a trade-off: a large chunk keeps the information whole but
  takes many tokens; a small chunk is cheap but can split the information.
  Overlap and adding the title reduce splitting.
- Search based on matching words misses questions that ask about the same
  thing in other words.
- Chunking and search are chosen by **measuring** with real questions.
