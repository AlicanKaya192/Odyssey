# Preprocessing

Models want numbers, complete numbers and mostly numbers on a similar scale.
Real data comes with missing values, text categories and columns in very
different units. `sklearn.preprocessing` and `sklearn.impute` provide the
transformers that close this gap. They all follow the previous section's
contract: `fit` on the training data, `transform` everywhere. This section
covers scalers, filling missing values, encoding categories and creating new
features, together with what each one does **when chosen wrongly**.

## Three scalers, one outlier

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

income = np.array([[30.0], [35.0], [40.0], [45.0], [500.0]])
for scaler in [StandardScaler(), MinMaxScaler(), RobustScaler()]:
    out = scaler.fit_transform(income).ravel().round(2)
    print(type(scaler).__name__, out.tolist())
```

```text
StandardScaler [-0.54, -0.51, -0.49, -0.46, 2.0]
MinMaxScaler [0.0, 0.01, 0.02, 0.03, 1.0]
RobustScaler [-1.0, -0.5, 0.0, 0.5, 46.0]
```

| Scaler | What it does | With an outlier |
|---|---|---|
| `StandardScaler` | subtract the mean, divide by the deviation | the outlier pulls the mean and deviation; the four normal values got squeezed into −0.54…−0.46 |
| `MinMaxScaler` | make the minimum 0 and the maximum 1 | the four values got crushed into 0–0.03 |
| `RobustScaler` | subtract the median, divide by the interquartile range | the normal values spread over −1…0.5, the outlier alone at 46 |

- On data with outliers `RobustScaler` keeps the differences between the
  other values. Without outliers `StandardScaler` is the default choice.
- Models based on distance or slope (KNN, SVM, regularised linear models,
  neural networks) are sensitive to scale; **tree models are not**, scaling is
  unnecessary for them.

## Filling missing values

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[1.0, 7.0], [np.nan, 8.0], [3.0, np.nan], [100.0, 9.0]])
for strategy in ["mean", "median"]:
    imp = SimpleImputer(strategy=strategy)
    filled = imp.fit_transform(X)[:, 0].round(2).tolist()
    print(strategy, filled, imp.statistics_.round(2).tolist())
flagged = SimpleImputer(strategy="median", add_indicator=True).fit_transform(X)
print(flagged.shape, flagged[:, 2:].astype(int).tolist())
```

```text
mean [1.0, 34.67, 3.0, 100.0] [34.67, 8.0]
median [1.0, 3.0, 3.0, 100.0] [3.0, 8.0]
(4, 4) [[0, 0], [1, 0], [0, 1], [0, 0]]
```

- `SimpleImputer` fills a missing value with a statistic of the column; the
  statistic is in `statistics_`, learned **from the training data**.
- The first column has an outlier like 100: the mean filled the gap with
  34.67 (like no real value), the median with 3.
- `add_indicator=True` adds a "this was missing" column for each column with
  gaps (the last two columns). A value **being missing** can carry
  information (the customer did not state an income); do not lose it by
  filling.
- To fill with a constant, `strategy="constant", fill_value=0`; on a
  categorical column, `strategy="most_frequent"`.

## Categories: OneHotEncoder

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

train = pd.DataFrame({"city": ["Izmir", "Ankara", "Izmir", "Bursa"]})
enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
print(enc.fit_transform(train).astype(int).tolist())
print(enc.get_feature_names_out().tolist())
print(enc.transform(pd.DataFrame({"city": ["Van"]})).astype(int).tolist())
strict = OneHotEncoder().fit(train)
try:
    strict.transform(pd.DataFrame({"city": ["Van"]}))
except ValueError as error:
    print("ValueError:", str(error).split(" in column")[0])
```

```text
[[0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 1, 0]]
['city_Ankara', 'city_Bursa', 'city_Izmir']
[[0, 0, 0]]
ValueError: Found unknown categories ['Van']
```

- Each category becomes a 0/1 column. There is **no** order: no fake relation
  like Ankara < Izmir is created.
- `get_feature_names_out` gives the names of the new columns; needed when
  reading model results.
- A category never seen in training (Van) always arrives in production. The
  default setting fails and stops; `handle_unknown="ignore"` turns it into a
  row with every column 0.
- `sparse_output=False` makes the result an ordinary array; with many
  categories the default sparse matrix saves memory.

## Ordered categories: OrdinalEncoder

```python
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

sizes = pd.DataFrame({"size": ["M", "S", "XL", "L"]})
auto = OrdinalEncoder().fit(sizes)
print(auto.categories_[0].tolist(), auto.transform(sizes).ravel().tolist())
ordered = OrdinalEncoder(categories=[["S", "M", "L", "XL"]]).fit(sizes)
print(ordered.transform(sizes).ravel().tolist())
```

```text
['L', 'M', 'S', 'XL'] [1.0, 2.0, 3.0, 0.0]
[1.0, 0.0, 3.0, 2.0]
```

- `OrdinalEncoder` gives each category a single number. Left alone, it picks
  the order **alphabetically**: L=0, M=1, S=2, XL=3. Meaningless for sizes; a
  linear model learns "S is smaller than XL but larger than L".
- With `categories=[[...]]` you give the order: S=0, M=1, L=2, XL=3.
- For a category without order (city), `OneHotEncoder`; for an ordered one
  (size, education level), `OrdinalEncoder` with its order given. Tree models
  can also work well with ordinal codes on unordered categories.

## Creating new features

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

X = np.array([[2.0, 3.0]])
poly = PolynomialFeatures(degree=2, include_bias=False).fit(X)
print(poly.get_feature_names_out(["a", "b"]).tolist(), poly.transform(X).tolist())
```

```text
['a', 'b', 'a^2', 'a b', 'b^2'] [[2.0, 3.0, 4.0, 6.0, 9.0]]
```

- `PolynomialFeatures` adds squares and **interactions** (`a b`): a linear
  model can learn curves and "two features together" effects.
- The column count grows fast: 10 features become 65 columns at degree two.
  It is used with regularisation (the linear models section).
- Tools such as `KBinsDiscretizer` for splitting numbers into ranges and
  `FunctionTransformer(np.log1p)` for your own formula use the same
  interface.

## Summary

- Scaling: `StandardScaler` without outliers, `RobustScaler` with them;
  unnecessary for trees.
- Missing values: `SimpleImputer` (median with outliers), `add_indicator=True`
  for the missingness itself.
- Unordered categories `OneHotEncoder(handle_unknown="ignore")`, ordered ones
  `OrdinalEncoder(categories=[[...]])`.
- All are `fit` on the training data; what they learn sits in fields like
  `statistics_`, `categories_`, `mean_`.
