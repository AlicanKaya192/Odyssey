In error analysis the most instructive examples are the mistakes the model is
**most sure** about: either the model learned something fundamentally wrong,
or the label is doubtful.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer().fit(X_train)
model = LogisticRegression(max_iter=1000)
model.fit(vectorizer.transform(X_train), y_train)
proba = model.predict_proba(vectorizer.transform(X_test))
pred = model.classes_[proba.argmax(axis=1)]
wrong = np.flatnonzero(pred != y_test)
sure = wrong[np.argsort(proba[wrong].max(axis=1))[::-1][:4]]
for i in sure:
    print(y_test[i], "->", pred[i], round(float(proba[i].max()), 2))
    print("  ", X_test[i][:60])
```

```text
negative -> positive 0.94
   The lid is awful. But arrived early and well packed.
neutral -> positive 0.88
   NOTHING SPECIAL ABOUT THE BUTTONS. MY HUSBAND LOVES IT TOO.
negative -> positive 0.87
   the seat is not sturdy at all. but totally worth the money.
neutral -> positive 0.81
   Delivery took 11 days. My friend loves it too.
```

- `wrong` holds the indices of the wrongly predicted test examples;
  `proba[wrong].max(axis=1)` is the model's confidence for each. We print the
  four most confident mistakes.
- **Mixed reviews:** "The lid is awful. But arrived early and well packed."
  Its stars are low (negative), but half of the text is positive and the
  model trusted "But arrived early". A person would hesitate too.
- "the seat is not sturdy at all. but totally worth the money." Labelled
  negative, but the last sentence is strongly positive.
- When neutral reviews end with a positive sentence ("My husband loves it
  too"), the model drifts to positive.

## What did we learn?

These mistakes show the limit of the **task** more than of the model: a
review's stars do not tell the whole tone of its text. In real data, too,
labels are noisy. If such examples come up often:

- review the labels again (label noise),
- redefine the task (sentiment per sentence, or a "mixed" class),
- or accept that the model is unsure in these cases and manage it with a
  threshold.
