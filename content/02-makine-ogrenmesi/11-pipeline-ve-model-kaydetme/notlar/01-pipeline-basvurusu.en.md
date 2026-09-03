## The smallest form

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

The step names are strings you choose. The last step must be an
**estimator** and the earlier ones **transformers**.

The shortcut:

```python
from sklearn.pipeline import make_pipeline
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
```

It generates the names itself (`standardscaler`, `logisticregression`) —
quick, but it makes `GridSearchCV` keys unreadable.

## ColumnTransformer

```python
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ("num", numeric_steps, ["tenure", "monthly", "support"]),
    ("cat", text_steps, ["city", "plan"]),
])
```

| Parameter | What it does | Default |
|---|---|---|
| `transformers` | (name, transformer, columns) triples | — |
| `remainder` | What happens to unlisted columns | `"drop"` |
| `verbose_feature_names_out` | Prefix the output names | `True` |

**`remainder="drop"` is the default:** a column you did not list is
**silently discarded**. When a new column is added it never reaches the
model and nobody notices. `remainder="passthrough"` passes them through
untouched.

Instead of listing columns by hand you can select them by type:

```python
from sklearn.compose import make_column_selector

ColumnTransformer([
    ("num", numeric_steps, make_column_selector(dtype_include="number")),
    ("cat", text_steps, make_column_selector(dtype_exclude="number")),
])
```

## Imputing

```python
from sklearn.impute import SimpleImputer

SimpleImputer(strategy="median")          # numeric
SimpleImputer(strategy="most_frequent")   # text
SimpleImputer(strategy="constant", fill_value="unknown")
```

`strategy`: `"mean"`, `"median"`, `"most_frequent"`, `"constant"`.

Remember from section 04: the median is less affected by outliers than the
mean.

## Encoding

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

OneHotEncoder(handle_unknown="ignore")
OrdinalEncoder()   # only for genuinely ordered categories
```

**`handle_unknown="ignore"` is almost always what you want.** When a value
unseen during training arrives, the default behaviour is to raise; `ignore`
sets all that row's columns to zero.

`drop="first"` drops the first category — it reduces collinearity for
linear models and is pointless for trees.

## Reaching the steps

```python
pipe.named_steps["model"].coef_
pipe.named_steps["prepare"].get_feature_names_out()
pipe[-1]                 # the last step
pipe[:-1].transform(X)   # preprocessing only
```

`get_feature_names_out()` gives the column names after preprocessing; it is
the only correct source when reading coefficients.

## Cross validation

```python
cross_val_score(pipe, X_train, y_train, cv=skf, scoring="f1")
```

Given a pipeline, every step is retrained **inside each fold**. Leakage
stops being a matter of care.

Measured: with 200 noise columns added and `SelectKBest` run outside the
cross validation the CV score is 0.780; inside the pipeline, 0.716.

## GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
search = GridSearchCV(pipe, grid, cv=skf, scoring="accuracy", n_jobs=-1)
search.fit(X_train, y_train)
```

**The key format:** the step names and the parameter name are joined by
**two underscores**. The same rule holds however many levels deep.

```python
search.best_params_      # the best settings
search.best_score_       # their CV mean
search.best_estimator_   # the pipeline retrained on all the training data
search.cv_results_       # the detail for every point
search.predict(X_test)   # predicts with best_estimator_
```

Since `refit=True` is the default, `best_estimator_` comes ready.

When the grid grows, `RandomizedSearchCV` tries a random subset (`n_iter`
of them) through the same interface.

## Saving

```python
import joblib

joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

`joblib` is used rather than `pickle`: it is faster with large NumPy arrays
and produces smaller files.

Compression:

```python
joblib.dump(pipe, "model.joblib", compress=3)
```

Slower, but noticeably smaller.

**Saved:** every step, the learned numbers, the column order.
**Not saved:** the library versions, the training data, the threshold you
chose, the scores you measured. A text file next to it covers those.

**Security:** `joblib.load` constructs the Python objects inside the file; a
file from a source you do not trust can run code.

## Common mistakes

- **Calling `fit_transform` outside the pipeline and then
  `cross_val_score`.** A silent leak; measured at 6.4 points.
- **Forgetting `remainder`.** Unlisted columns are silently discarded.
- **Not passing `handle_unknown`.** In production it dies on the first
  unexpected category.
- **Saving only the last step.** `joblib.dump(pipe, ...)` rather than
  `joblib.dump(model, ...)`; otherwise what the preprocessing learned is
  lost.
- **Writing a single underscore.** `model__C`, not `model_C`.
- **Taking `GridSearchCV`'s score as the final report.** `best_score_`
  comes from cross validation on the training side and is optimistic
  because a search was run; the final report is on the test set.
- **Leaving no version note.** The file may not open under a different
  scikit-learn version.
