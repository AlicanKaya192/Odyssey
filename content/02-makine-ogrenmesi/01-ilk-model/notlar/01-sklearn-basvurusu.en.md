Everything used in this section, where you can find it without searching.

## Imports

sklearn is not one piece; everything comes from its own subpackage.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
```

| Subpackage | What is inside |
|---|---|
| `sklearn.model_selection` | Splitting and validation tools |
| `sklearn.linear_model` | Linear models |
| `sklearn.tree` | Decision trees |
| `sklearn.neighbors` | KNN |
| `sklearn.metrics` | Measures |
| `sklearn.preprocessing` | Scaling, encoding |

`import sklearn` on its own is not enough — you import by subpackage name.

## The three steps

```python
model = LinearRegression()          # build
model.fit(X_train, y_train)         # learn
prediction = model.predict(X_test)  # predict
```

| Call | What it does | What it returns |
|---|---|---|
| `Model()` | Builds it; it knows nothing yet | The model object |
| `fit(X, y)` | Derives the rule from data | The model itself |
| `predict(X)` | Applies the rule | An array of predictions |
| `score(X, y)` | Measures (R² for regression) | A single number |

Because `fit` returns the model itself, `model = LinearRegression().fit(X, y)`
fits on one line.

## Values that appear after training

Every name ending in an underscore does **not exist** before `fit` is called.

| Value | What it is |
|---|---|
| `coef_` | The coefficients (slope). An array of one for a single feature |
| `intercept_` | The intercept |
| `feature_names_in_` | The column names used in training |
| `n_features_in_` | How many features it was trained on |

```python
model.fit(X_train, y_train)
print(model.coef_[0], model.intercept_)
```

## `train_test_split`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
```

| Parameter | What it does |
|---|---|
| `test_size` | The share kept for testing (0.2 - 0.3 is common) |
| `train_size` | The alternative; you do not pass both |
| `random_state` | Fixes the split so the result is reproducible |
| `shuffle` | `True` by default; turning it off keeps the order |
| `stratify` | Keeps class proportions on both sides (classification) |

**The return order is fixed:** `X_train, X_test, y_train, y_test`. Getting
it wrong raises no error — it gives a wrong result.

## Measures

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, prediction)
mse = mean_squared_error(y_test, prediction)
rmse = mse ** 0.5
r2 = r2_score(y_test, prediction)
```

| Measure | Unit | How to read it |
|---|---|---|
| MAE | The target's unit | How many units I am off on average |
| MSE | The unit squared | Punishes large errors more |
| RMSE | The target's unit | MSE made readable |
| R² | Unitless | 1 perfect, 0 as good as the baseline, negative worse |

**The order is always `(actual, predicted)`.** Reversing it changes nothing
for MAE but gives a wrong answer for R².

## The shape of `X` and `y`

```python
X = df[["area"]]            # one feature   - double brackets
X = df[["area", "age"]]     # many features
y = df["price"]             # the target    - single brackets
```

| Error | Cause |
|---|---|
| `Expected 2D array, got 1D array` | `X` taken with single brackets |
| `Found input variables with inconsistent numbers of samples` | `X` and `y` differ in length |
| `X has 2 features, but ... expecting 1` | Training and prediction columns differ |
| `This LinearRegression instance is not fitted yet` | `predict` before `fit` |

## The baseline

```python
baseline = y_train.mean()
baseline_mae = mean_absolute_error(y_test, [baseline] * len(y_test))
```

sklearn has a ready-made one too:

```python
from sklearn.dummy import DummyRegressor

dummy = DummyRegressor(strategy="mean")
dummy.fit(X_train, y_train)
print(mean_absolute_error(y_test, dummy.predict(X_test)))
```

`DummyRegressor` carries the same three steps — a baseline is a model too.

## Changing model

```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

model = LinearRegression()
model = DecisionTreeRegressor(max_depth=3, random_state=42)
model = KNeighborsRegressor(n_neighbors=5)
```

`fit`, `predict` and `score` are the same for all three. Only the
construction line and that model's hyperparameters change.
