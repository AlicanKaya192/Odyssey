A model makes its "negative" decision from a probability: when it passes
0.5. This **threshold** can be changed, and it directly sets the trade-off
between precision and recall. Let us reduce the task to two classes: is a
review negative?

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
is_negative = labels == "negative"
X_train, X_test, y_train, y_test = train_test_split(
    texts, is_negative, test_size=0.25, random_state=0, stratify=is_negative)
vectorizer = TfidfVectorizer().fit(X_train)
model = LogisticRegression(max_iter=1000)
model.fit(vectorizer.transform(X_train), y_train)
proba = model.predict_proba(vectorizer.transform(X_test))[:, 1]
for threshold in [0.2, 0.3, 0.5, 0.7]:
    pred = proba >= threshold
    p = precision_score(y_test, pred)
    r = recall_score(y_test, pred)
    print(threshold, round(p, 3), round(r, 3), int(pred.sum()))
```

```text
0.2 0.723 0.878 119
0.3 0.851 0.816 94
0.5 0.985 0.684 68
0.7 1.0 0.459 45
```

The columns: threshold, precision, recall, the number of reviews called
"negative".

- The default threshold is 0.5: precision 0.985 (almost no false alarms), but
  only 68.4% of the negatives are caught.
- Lowering the threshold to 0.2 catches 87.8% of the negatives, but 27.7% of
  those called "negative" are not.
- Threshold 0.7: only the very sure ones; precision 1.0, recall 0.459.

## How to choose the threshold?

Look at the cost of the errors. If a person reviews the negative reviews and
missing one is expensive, choose a low threshold (high recall); if the
person's time is limited, a high threshold (high precision). Choose the
threshold on **validation data**, not on test data. `TunedThresholdClassifierCV`
from ML Libraries does this with cross-validation.
