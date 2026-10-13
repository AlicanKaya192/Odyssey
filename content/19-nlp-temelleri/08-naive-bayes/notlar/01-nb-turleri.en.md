scikit-learn has three Naive Bayes classes for text; they differ in how they
count a word.

| Class | Input | The idea | When |
|---|---|---|---|
| `MultinomialNB` | Word counts (or TF-IDF) | Each word counts with its repetitions | The default choice |
| `ComplementNB` | Word counts | Learns each class from the documents **outside** it | Imbalanced classes |
| `BernoulliNB` | Presence (0/1) | A word **not** appearing is information too | Short texts |

## Let us compare

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
for model in [MultinomialNB(), ComplementNB(), BernoulliNB()]:
    model.fit(A, y_train)
    pred = model.predict(B)
    neutral = round(float((pred[y_test == "neutral"] == "neutral").mean()), 3)
    print(type(model).__name__, round(model.score(B, y_test), 3), neutral)
```

```text
MultinomialNB 0.866 0.847
ComplementNB 0.846 0.861
BernoulliNB 0.864 0.819
```

- The second number is the overall accuracy, the third the share of
  **neutral** reviews found neutral. Neutral is the class with the fewest
  examples.
- `ComplementNB` is a little behind in overall accuracy (84.6%) but it finds
  the minority class, neutral, best (86.1%). On imbalanced data accuracy
  alone misleads; in section 09 we meet per-class measures (precision,
  recall).
- All three are close: in Naive Bayes the real gain comes not from the type
  but from the features (word pairs, cleaning).

## Naive Bayes with TF-IDF

`MultinomialNB` also works with TF-IDF values (as long as they are not
negative). In theory it was designed for counts, but in practice TF-IDF
often gives similar or slightly better results. Choose with validation.
