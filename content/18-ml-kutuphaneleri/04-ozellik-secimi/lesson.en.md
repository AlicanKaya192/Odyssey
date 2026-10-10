# Feature Selection

Not every column in a table is useful: some never change, some are noise
unrelated to the target. Needless columns slow the model down, make it harder
to interpret and prepare the ground for overfitting on small data.
`sklearn.feature_selection` removes columns in three ways: by a statistic per
column (**filter**), by a model's importance scores (**embedded**) and by
training the model again and again (**wrapper**). All are transformers, so the
previous section's rule applies: selection goes **inside the pipeline**.

## Columns that never change: VarianceThreshold

```python
import numpy as np
from sklearn.feature_selection import VarianceThreshold

X = np.array([[0, 1.0, 5.0], [0, 2.0, 5.0], [0, 3.0, 5.1], [0, 4.0, 5.0]])
vt = VarianceThreshold(threshold=0.01).fit(X)
print(vt.variances_.round(4).tolist(), vt.get_support().tolist())
```

```text
[0.0, 1.25, 0.0019] [False, True, False]
```

- A column whose variance stays below the threshold is dropped: the first
  column is always 0, the third almost constant (0.0019). It does not look at
  the target; there is no leakage risk.
- The threshold depends on the scale: on unscaled data a column with small
  units may be dropped unfairly. Usually it is used only to drop constant
  columns (`threshold=0`).

## This section's data

The next blocks use the same synthetic data: 20 columns, but only **the first
4** are related to the target (`n_informative=4`, `shuffle=False`); the other
16 are noise. We will see which method finds this.

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
kb = SelectKBest(f_classif, k=4).fit(X, y)
print(sorted(kb.get_support(indices=True).tolist()))
mi = SelectKBest(mutual_info_classif, k=4).fit(X, y)
print(sorted(mi.get_support(indices=True).tolist()))
print(kb.scores_[:6].round(1).tolist())
```

```text
[0, 1, 2, 3]
[0, 1, 2, 3]
[282.0, 99.1, 383.7, 77.5, 0.3, 0.0]
```

- The **filter** method scores each column against the target **on its own**
  and keeps the best `k`. `f_classif` looks at differences of means (ANOVA
  F), `mutual_info` at non-linear relationships too. Both found 0–3.
- The scores (`scores_`) separate by a wide margin: informative columns
  77–384, noise near zero.
- Its weakness: it judges columns **one by one**. It cannot tell apart two
  columns that only matter together, or two columns that copy each other.

## By the model's importance: SelectFromModel

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
l1 = LogisticRegression(penalty="l1", C=0.05, solver="liblinear")
sfm = SelectFromModel(l1).fit(X, y)
print(sfm.get_support(indices=True).tolist())
forest = RandomForestClassifier(n_estimators=100, random_state=8)
sft = SelectFromModel(forest, max_features=4, threshold=-float("inf")).fit(X, y)
print(sorted(sft.get_support(indices=True).tolist()))
```

```text
[0, 1, 2, 3]
[0, 1, 2, 3]
```

- The **embedded** method: a model is trained, columns with a low coefficient
  or importance score are dropped.
- L1-penalised logistic regression (in the linear models section) pushes the
  coefficients of needless columns **exactly to zero**; the non-zero ones are
  selected. The smaller `C`, the fewer columns remain.
- The best 4 columns by the forest's importance scores (`max_features=4`;
  `threshold=-inf` means "no threshold, only a count"). Both give 0–3.

## Elimination by training: RFECV

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
rfe = RFECV(LogisticRegression(), step=1, cv=5).fit(X, y)
print(rfe.n_features_, rfe.get_support(indices=True).tolist())
print(rfe.ranking_[:8].tolist())
```

```text
3 [0, 1, 2]
[1, 1, 1, 2, 14, 13, 12, 16]
```

- The **wrapper** method: the model is trained, the weakest column is dropped,
  it is trained again... (`RFE`, recursive feature elimination). `RFECV`
  chooses where to stop with cross-validation.
- Here it chose 3 columns: column 3 is informative but weak (filter score
  77.5); by cross-validation, keeping it did not raise the score. `ranking_` is
  the order of elimination: 1 for the selected, large numbers for those
  dropped early.
- It is the most expensive method: 20 columns × 5 folds ≈ a hundred
  trainings. On data with many columns, reduce with a filter first.

## How many columns?

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
for k in [2, 4, 10, 20]:
    pipe = make_pipeline(SelectKBest(f_classif, k=k), LogisticRegression())
    print(k, round(cross_val_score(pipe, X, y, cv=5).mean(), 3))
```

```text
2 0.868
4 0.87
10 0.868
20 0.852
```

- The selection is inside the pipeline, `k` is compared with
  cross-validation.
- 4 columns are slightly better than 20 (0.870 against 0.852): the 16 noise
  columns misled the model a little. The gap is small; 500 rows are enough to
  withstand the noise. With fewer rows and more columns the gap grows.
- `k` is a hyperparameter; instead of trying by hand, it will be searched with
  `GridSearchCV` in the next section (`selectkbest__k`).

## Summary

- Constant columns: `VarianceThreshold`; it does not look at the target.
- Filter `SelectKBest(f_classif / mutual_info_classif, k=)`: fast, judges
  columns one by one.
- Embedded `SelectFromModel(L1 or a forest)`; wrapper `RFECV`: expensive but
  judges columns together.
- Selection always inside the pipeline; how many columns to keep is chosen
  with cross-validation.
