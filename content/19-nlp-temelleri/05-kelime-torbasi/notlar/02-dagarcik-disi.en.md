The vocabulary is learned from the training data. How many of the words in
the test data are missing from it? Let us measure on the same kind of text
and on another kind:

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews, make_tickets

reviews = [r["text"] for r in make_reviews(2000)]
tickets = [t["text"] for t in make_tickets(500)]
vectorizer = CountVectorizer().fit(reviews[:1000])
analyze = vectorizer.build_analyzer()


def oov_share(texts):
    tokens = [w for t in texts for w in analyze(t)]
    unseen = sum(w not in vectorizer.vocabulary_ for w in tokens)
    return round(unseen / len(tokens), 3)


print(oov_share(reviews[1000:]), oov_share(tickets))
```

```text
0.005 0.633
```

- The vocabulary built from the first 1000 reviews knows 99.5% of the words
  in the next 1000 reviews: the same kind of text, the same words.
- The same vocabulary **does not know 63%** of the words in the support
  tickets. "refund", "invoice" and "password" never appeared in the reviews;
  the model will silently drop them.

## What does it mean?

A model decides only with the words it saw in training. If you apply a
classifier trained on product reviews to support tickets, it decides
without seeing most of each ticket; without measuring accuracy you might
think it "works". This situation is called **domain shift**.

A checklist:

- Train the model on data that looks like the text you will use it on.
- Measure the out-of-vocabulary share on new data. If it suddenly rises (a
  new product, a new season, new slang), the model has gone stale.
- Methods that cope with unseen words: character n-grams (04), subword
  tokenisation (the second module).
