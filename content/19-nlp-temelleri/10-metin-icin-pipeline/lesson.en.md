# Pipelines for Text

So far we have `fit` the vectoriser and the model separately and remembered
the rule "build the vectoriser on training data only" by hand every time. A
**Pipeline** joins the two into one object: raw text goes in, a prediction
comes out. This is not only convenient; it prevents leakage in
cross-validation and parameter search by itself, and when you save and use
the model it makes forgetting the vectoriser impossible. This section covers
building a Pipeline for text, cross-validation, searching the settings of
the vectoriser and the model together, and combining different features. It
is the use on text of the Pipeline you met in ML Libraries.

## Building a Pipeline

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
pipe = Pipeline([("tfidf", TfidfVectorizer()),
                 ("model", LogisticRegression(max_iter=1000))])
pipe.fit(X_train, y_train)
print(round(pipe.score(X_test, y_test), 3))
print(pipe.predict(["not good at all", "love it"]).tolist())
```

```text
0.88
['positive', 'positive']
```

- `Pipeline` chains the steps in order: each step has a name (`"tfidf"`,
  `"model"`) and an object. `fit` runs `fit_transform` on the vectoriser and
  `fit` on the model; `predict` only `transform`s with the vectoriser.
- The input is now **raw text**: `pipe.predict(["not good at all"])`. When
  predicting it is impossible to forget calling the vectoriser.
- The result is the same as the model built separately in section 09: 88%.
  But note: this model found "not good at all" **positive**. Single-word
  logistic regression trusted the weight of "good"; the Naive Bayes of
  section 08 said negative. One example proves nothing, but it is a reminder
  of why word pairs matter.

## Cross-validation

A single train/test split can be lucky or unlucky. **Cross-validation**
splits the training data into k parts; each time it uses one part for
validation and the rest for training, and gives the mean of the k scores.

```python
from sklearn.model_selection import cross_val_score

cv = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1_macro")
print(cv.round(3).tolist(), round(cv.mean(), 3))
leaky_X = TfidfVectorizer().fit_transform(X_train)
leaky = cross_val_score(LogisticRegression(max_iter=1000), leaky_X, y_train,
                        cv=5, scoring="f1_macro")
print(round(leaky.mean(), 3))
```

```text
[0.874, 0.896, 0.857, 0.842, 0.89] 0.872
0.874
```

- The macro F1 of the five folds moves between 0.842 and 0.896: a single
  split's score can be off by ±0.03. The mean is 0.872.
- When the Pipeline is passed to `cross_val_score`, the vectoriser is refit
  **in every fold** on that fold's training part only.
- The second try is the leaky way: the vectoriser was built once on all the
  training data, then cross-validated. The words and IDF of the validation
  part leaked into the model in every fold. On this data the gap is small
  (0.874 against 0.872), because the vocabulary is small and the words appear
  everywhere. On real data, where rare words and thresholds such as `min_df`
  matter, the gap grows. With a Pipeline the question never comes up.

## Parameter search

The vectoriser's settings (n-grams, `sublinear_tf`) and the model's `C` can
be searched together. A parameter's name is written as `step__parameter`:

```python
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(pipe, {
    "tfidf__ngram_range": [(1, 1), (1, 2)],
    "tfidf__sublinear_tf": [False, True],
    "model__C": [1, 10],
}, cv=5, scoring="f1_macro")
grid.fit(X_train, y_train)
print(grid.best_params_)
print(round(grid.best_score_, 3))
print(round(f1_score(y_test, grid.predict(X_test), average="macro"), 3))
```

```text
{'model__C': 10, 'tfidf__ngram_range': (1, 2), 'tfidf__sublinear_tf': True}
0.888
0.868
```

- 2 × 2 × 2 = 8 settings, each in 5 folds: 40 models were trained. The best is
  word pairs, `sublinear_tf=True` and `C=10`.
- **Careful:** `best_score_` (0.888) is higher than the test score (0.868).
  Choosing the best of eight settings means fitting the validation score to
  lucky folds; the chosen setting's score is optimistic. Always measure real
  performance on test data never used in the search (the lesson about the
  optimistic `best_score_` in ML Libraries).
- `grid` can be used like a Pipeline refit on all the training data with the
  best setting: `grid.predict(...)`.

## Combining features

`FeatureUnion` produces different features from the same text and puts them
side by side: word n-grams and character n-grams.

```python
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC

words = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                  ("model", LinearSVC())])
both = Pipeline([
    ("features", FeatureUnion([
        ("words", TfidfVectorizer(ngram_range=(1, 2))),
        ("chars", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))),
    ])),
    ("model", LinearSVC()),
])
for name, model in [("words", words), ("words+chars", both)]:
    model.fit(X_train, y_train)
    macro = f1_score(y_test, model.predict(X_test), average="macro")
    print(name, round(model.score(X_test, y_test), 3), round(macro, 3))
```

```text
words 0.916 0.874
words+chars 0.912 0.863
```

Adding character n-grams **did not help** on this data (91.6% against
91.2%). Character n-grams shine on text with many typos and varied suffixes;
our reviews have a small vocabulary and the words repeat already. Not every
addition pays off; measure every feature you combine.

## Text and another column

Besides the text we may have other information: which product a review is
about. `ColumnTransformer` applies its own transformer to each column:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

products = [r["product"] for r in reviews]
frame = pd.DataFrame({"text": texts, "product": products})
F_train, F_test, f_train, f_test = train_test_split(
    frame, labels, test_size=0.25, random_state=0, stratify=labels)
mixed = Pipeline([
    ("columns", ColumnTransformer([
        ("text", TfidfVectorizer(ngram_range=(1, 2)), "text"),
        ("product", OneHotEncoder(handle_unknown="ignore"), ["product"]),
    ])),
    ("model", LinearSVC()),
])
mixed.fit(F_train, f_train)
print(round(mixed.score(F_test, f_test), 3))
```

```text
0.914
```

- The text column is given to `TfidfVectorizer` as a **single column name**
  (`"text"`): a vectoriser expects a list of texts, not a table. The
  categorical column is given as a list (`["product"]`).
- The product type added nothing (91.4%): in this data the product has
  nothing to do with the sentiment. In real data (some products drawing more
  complaints, for example) it can help.

## Summary

- A Pipeline joins the vectoriser and the model: raw text goes in, a
  prediction comes out; forgetting the vectoriser becomes impossible.
- `cross_val_score(pipe, ...)` refits the vectoriser in every fold; leakage is
  prevented by itself.
- `GridSearchCV` searches the vectoriser's and the model's settings together
  (`tfidf__ngram_range`, `model__C`); `best_score_` is optimistic, make the
  final measurement on the test data.
- `FeatureUnion` combines different features of the same text,
  `ColumnTransformer` different columns. On this data neither paid off:
  measure every addition.
