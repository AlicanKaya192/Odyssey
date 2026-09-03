## Cross validation

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf,
                         scoring="neg_mean_absolute_error")

print([round(-s, 2) for s in scores])
print(round(-scores.mean(), 2), round(scores.std(), 2))
```

| Parameter | What it does |
|---|---|
| `n_splits` | How many pieces to cut into (5 and 10 are common) |
| `shuffle` | Shuffle before cutting; needed for sorted files |
| `random_state` | With `shuffle=True`, fixes the result |

**How many folds:** 5 is fast and usually enough. 10 is more reliable but
twice as expensive. With very little data the number of folds can go up to
the number of records (`LeaveOneOut`).

## Kinds of fold

| Class | When |
|---|---|
| `KFold` | Regression, the ordinary case |
| `StratifiedKFold` | Classification; each fold keeps the class proportions |
| `TimeSeriesSplit` | Time series; the past trains, the future tests |
| `GroupKFold` | So that records of the same group (same patient, same customer) are not separated |

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

**For classification `cross_val_score` already uses `StratifiedKFold` by
default** — but pass `cv=kf` with an explicit `KFold` and you have turned
that protection off with your own hand.

## Score names

`scoring` takes a string and works on the rule that **larger is better**.
That is why error measures come back negative.

| `scoring` | What it gives |
|---|---|
| `neg_mean_absolute_error` | -MAE |
| `neg_root_mean_squared_error` | -RMSE |
| `r2` | R² (larger is already better) |
| `accuracy` | Accuracy |
| `precision`, `recall`, `f1` | Classification measures |
| `roc_auc` | The area under the curve |

```python
print(round(-scores.mean(), 2))    # error measures: flip the sign
print(round(scores.mean(), 3))     # r2 and accuracy: do not
```

## More information: `cross_validate`

```python
from sklearn.model_selection import cross_validate

result = cross_validate(model, X, y, cv=kf,
                        scoring=["neg_mean_absolute_error", "r2"],
                        return_train_score=True)

print(result["test_neg_mean_absolute_error"])
print(result["train_neg_mean_absolute_error"])
```

`return_train_score=True` gives you **the training scores as well** — which
is exactly what you need to see overfitting.

You can take several measures in one run; each comes back under a
`test_<name>` key.

## The learning curve

By hand:

```python
sizes = [10, 20, 30, 45, 60, 79]
for n in sizes:
    model.fit(X_train[:n], y_train[:n])
    train_error = mean_absolute_error(y_train[:n], model.predict(X_train[:n]))
    test_error = mean_absolute_error(y_test, model.predict(X_test))
```

With sklearn:

```python
from sklearn.model_selection import learning_curve

sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=kf, scoring="neg_mean_absolute_error",
    train_sizes=[0.2, 0.4, 0.6, 0.8, 1.0])
```

`learning_curve` runs **cross validation** at every size, so it is more
reliable than the hand-written version; in exchange it is slower.

## Reading it

| What you see | Diagnosis | What to do |
|---|---|---|
| Training low, test high, a large gap | Overfitting | Simplify the model, add data, regularise |
| Both high and close together | Underfitting | Complicate the model, add features |
| Both low and close together | Good | Nothing |
| The curves have met but are still high | You have hit the data's limit | A new **feature** or a different model |
| The gap between the curves is not closing | Too little data | **More data** will help |

## The order for choosing settings

```python
# 1. Put the test set aside
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 2. Choose the settings on the TRAINING side with cross validation
best_score, best_depth = None, None
for depth in (2, 3, 5, 8, None):
    scores = cross_val_score(
        DecisionTreeRegressor(max_depth=depth, random_state=42),
        X_train, y_train, cv=kf, scoring="neg_mean_absolute_error")
    if best_score is None or scores.mean() > best_score:
        best_score, best_depth = scores.mean(), depth

# 3. Train on all the training data with the chosen setting
model = DecisionTreeRegressor(max_depth=best_depth, random_state=42)
model.fit(X_train, y_train)

# 4. Look at the test set ONCE
print(mean_absolute_error(y_test, model.predict(X_test)))
```

The number in step four is the number that goes in the report. Changing a
setting and looking again after that spends the test set.

## Common mistakes

- **Choosing a setting by looking at the test set.** The test is now
  training data.
- **Cross validating on all the data and then testing on that same data.**
  Leakage; the test set must stay apart.
- **Looking only at the mean.** The spread (std) says how much the number
  moves; small differences can vanish inside it.
- **Using `KFold` for classification.** On imbalanced data a fold may get no
  records of the minority class at all.
- **Using `shuffle=True` without `random_state`.** Different folds and a
  different result on every run.
- **Random folds on a time series.** The future leaks into the past.
