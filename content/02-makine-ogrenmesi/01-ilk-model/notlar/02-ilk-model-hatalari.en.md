Everybody building a model for the first time hits a few of these. Most are
one-line mistakes, but their messages say nothing at first glance.

## 1. `Expected 2D array, got 1D array instead`

```python
X = df["area"]          # Series - one-dimensional
model.fit(X, y)         # error
```

**Translation:** "you did not hand X over as a table."

```python
X = df[["area"]]        # DataFrame - two-dimensional
```

The same applies when asking for a prediction for a single number:

```python
model.predict(95)       # error
model.predict([[95]])   # correct
```

## 2. `This ... instance is not fitted yet`

```python
model = LinearRegression()
print(model.coef_)      # error - it has not learned yet
```

Values ending in an underscore come into existence **after** `fit` is
called. The same holds for `predict`.

## 3. Getting `train_test_split`'s return order wrong

```python
X_train, y_train, X_test, y_test = train_test_split(X, y)   # wrong
```

The correct order is `X_train, X_test, y_train, y_test`. Write it wrong and
**no error is raised** — the code runs and the model gives nonsense. That
makes it one of the more dangerous mistakes.

An easy check: `len(X_train)` must be larger than `len(X_test)`.

## 4. Not passing `random_state`

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
```

The code runs, but every run gives a different MAE. Comparing two models
becomes impossible: you cannot tell whether the difference came from the
model or from the split.

## 5. Building the baseline after the model

Computing the baseline after seeing the model's MAE is not technically
wrong, but it works against human nature: once you have seen the number,
you adjust your expectation to it.

The baseline is built **first**. Building a model with the line to beat
already drawn is a different job from drawing the line after seeing the
result.

## 6. Measuring on the training data

```python
model.fit(X_train, y_train)
print(model.score(X_train, y_train))    # meaningless
print(model.score(X_test, y_test))      # correct
```

The training score tells you how much the model memorised, not how much it
learned. It is not worthless though: seeing **both scores together**
reveals overfitting (training 0.99, test 0.62).

## 7. Comparing coefficients with each other

```python
print(model.coef_)      # [ 2.77 -3.35]
```

"3.35 is bigger, so age matters more" is **wrong**. A coefficient depends on
its column's unit: area ranges from 45 to 165, age from 0 to 30. Two numbers
in different units are not comparable.

Comparing them requires scaling first — that is section 4.

## 8. Taking a coefficient for a cause

If the model says "age -3.35", that is an **association**. The sentence
"ageing a house lowers its price" does not come out of the model; what comes
out is "houses that are older come out cheaper".

## 9. Passing column names differently in training and prediction

```python
model.fit(df[["area", "age"]], y)
model.predict(df[["age", "area"]])      # different order - wrong result
```

The column **order** must match the order the model learned. Working with
pandas, sklearn may warn you — but not in every case; using the same list in
both places is the safe habit.

## 10. Calling a measure with its arguments reversed

```python
mean_absolute_error(prediction, y_test)   # makes no difference for MAE
r2_score(prediction, y_test)              # wrong result for R2
```

The order is always `(actual, predicted)`. MAE forgives it because it is
symmetric; R² does not — and the wrong answer arrives without an error.

## 11. Not matching the measure to the kind of problem

Calling `accuracy_score` for regression, or `mean_absolute_error` for
classification. Sometimes it raises an error, sometimes it produces a
meaningless number.

A numeric target takes MAE/RMSE/R², a categorical one accuracy/precision/
recall.

## 12. Feeding data with missing values straight into a model

```
ValueError: Input contains NaN
```

sklearn does not work with missing values (apart from a few tree-based
models). You have to fill them or drop those rows before the model — and
that decision must come **after** the split, or it becomes leakage. That is
section 4.
