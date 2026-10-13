The model knows five categories. But what if a customer asks something that
fits none of them? A classifier cannot say "I do not know"; it has to put
every ticket into one of the five categories. Let us see this and build an
"I am not sure" gate by looking at **how confident** the model is:

```python
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_tickets

MASKS = [(r"\bORD-\d+\b", " ordernum "), (r"\$[\d,]+(?:\.\d{2})?", " amount "),
         (r"\S+@\S+", " email "), (r"\b\d{4}-\d{2}-\d{2}\b", " date "),
         (r"\bE\d{3,4}\b", " errcode ")]


def mask(text):
    for pattern, placeholder in MASKS:
        text = re.sub(pattern, placeholder, text)
    return " ".join(text.lower().split())


tickets = make_tickets(4000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer(preprocessor=mask, ngram_range=(1, 2))
pipe = Pipeline([("tfidf", vectorizer), ("model", LinearSVC(C=3))])
pipe.fit(X_train, y_train)
limit = np.percentile(pipe.decision_function(X_test).max(axis=1), 5)
print(round(limit, 2))
new = ["Do you sell gift cards?", "What are your opening hours?",
       "Is this jacket waterproof?", "My order ORD-12345 has not arrived."]
scores = pipe.decision_function(new).max(axis=1)
for text, label, score in zip(new, pipe.predict(new), scores):
    print(f"{label:<10} {score:6.2f} {'unsure' if score < limit else 'ok'}")
```

```text
0.37
account     -0.21 unsure
account     -0.34 unsure
account     -0.37 unsure
shipping     0.69 ok
```

- `decision_function` gives a score for each category; the largest is the
  predicted category. The larger the score, the more confident the model.
- We set the limit from known tickets: 95% of the test tickets score above
  0.37. A new ticket scoring lower counts as "not sure". (To keep it short we
  took the limit from the test data; in real work this is a setting too and
  is chosen on a separate validation set.)
- The three out-of-scope questions were still put into a category, but their
  scores are below the limit: the system can send them to a person. The real
  shipping ticket passes easily.
- This is a threshold, not a guarantee: an out-of-scope ticket that happens
  to contain a category's strong words ("card", "order") can get a high
  score. Where to put the limit is a trade-off: raise it and more tickets go
  to people; lower it and more get routed wrongly.
