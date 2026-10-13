Using a text model needs two things: the vectoriser (vocabulary, IDF) and
the model (weights). A Pipeline keeps both in one object, so it is saved to a
single file.

```python
import os

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LogisticRegression(max_iter=1000))]).fit(texts, labels)
joblib.dump(pipe, "review_model.joblib")
print(round(os.path.getsize("review_model.joblib") / 1024), "KB")
loaded = joblib.load("review_model.joblib")
new = ["The battery died after two days.", "Totally worth the money."]
print(loaded.predict(new).tolist())
print(bool((loaded.predict(texts) == pipe.predict(texts)).all()))
```

```text
131 KB
['negative', 'positive']
True
```

- The file is 131 KB: the vocabulary, the IDF values and the weights of each
  class.
- The loaded Pipeline takes raw text directly, and every prediction is the
  same as the saved one's.

## Things to watch (from ML Libraries)

- **Version:** the scikit-learn version that saves the file and the one that
  loads it should be the same; if they differ it warns and results may
  change.
- **Security:** `joblib.load` can run code stored in the file. Only load
  files you saved yourself or trust.
- **The final model:** retrain the final model on all the
  training data (test included if needed, once the measuring is done) and
  save it; you must have measured on a separate test set before.
