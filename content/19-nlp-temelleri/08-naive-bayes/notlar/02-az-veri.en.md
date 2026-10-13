Naive Bayes has two strengths: it learns quickly from little data, and what
it learns can be read. Let us measure both:

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
nb = MultinomialNB().fit(vectorizer.transform(X_train), y_train)
words = vectorizer.get_feature_names_out()
log_prob = dict(zip(nb.classes_, nb.feature_log_prob_))
diff = log_prob["negative"] - log_prob["positive"]
print([str(words[i]) for i in np.argsort(diff)[::-1][:5]])
print([str(words[i]) for i in np.argsort(diff)[:5]])
for n in [50, 100, 200, 500, 1500]:
    model = MultinomialNB().fit(vectorizer.transform(X_train[:n]), y_train[:n])
    print(n, round(model.score(vectorizer.transform(X_test), y_test), 3))
```

```text
['terrible', 'honest', 'hate', 'of', 'waste']
['works', 'no', 'expected', 'well', 'totally']
50 0.738
100 0.816
200 0.842
500 0.864
1500 0.866
```

## What did the model learn?

`feature_log_prob_` is the table of $\log P(w \mid c)$ for every class (the
`log_lik` we computed by hand in the lesson). The difference between two
classes shows how strongly a word points to each:

- For negative: "terrible", "honest", "hate", "of", "waste".
- For positive: "works", **"no"**, "expected", "well", "totally".

"no" pointing to positive reviews looks surprising: the data holds the phrase
"I expected it to be bad, but no". The lesson of section 05 holds again: a
model learns association, not meaning. That is why you should **always look**
at the learned words; an odd word often shows a phrase in the data, or a
leak.

## How much data is needed?

The last lines are a **learning curve**: test accuracy as the training data
grows.

- With 50 reviews, 73.8%: it already beats the baseline (66%).
- With 200 reviews 84.2%, with 500 reviews 86.4%; with 1500, 86.6%. The curve
  flattens after 500.

A flat curve says "more data will not help this model". To do better you
must change the model or the features (word pairs took it to 88.8%; linear
models come in section 09). A learning curve is the cheapest way to decide
whether to spend effort on collecting data or on the model.
