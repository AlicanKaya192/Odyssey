# ColumnTransformer

In a real table each column needs a different treatment: numbers are filled
and scaled, text categories are one-hot encoded, an ID number never enters the
model. Doing these separately and gluing them with `np.hstack` is long and
dangerous: the column order gets mixed up, and the same steps are written
again for the test data. `ColumnTransformer` attaches its own transformer to
each group of columns and `fit`s / `transform`s them all **like a single
transformer**.

## This section's data

```python
import numpy as np
import pandas as pd

homes = pd.DataFrame({
    "size": [80.0, 120.0, np.nan, 95.0, 150.0],
    "rooms": [2, 3, 3, 2, 4],
    "city": ["Izmir", "Ankara", "Izmir", "Bursa", "Ankara"],
    "heating": ["gas", "gas", "electric", None, "gas"],
    "id": [101, 102, 103, 104, 105],
})
print(homes.dtypes.astype(str).to_dict())
print(homes.isna().sum().to_dict())
```

```text
{'size': 'float64', 'rooms': 'int64', 'city': 'str', 'heating': 'str', 'id': 'int64'}
{'size': 1, 'rooms': 0, 'city': 0, 'heating': 1, 'id': 0}
```

- Two number columns (one with a gap), two text columns (one with a gap) and
  an ID column. The section's other blocks use this `homes` table.

## A separate treatment per column group

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
categorical = make_pipeline(SimpleImputer(strategy="most_frequent"), onehot)
prep = ColumnTransformer([("num", numeric, ["size", "rooms"]),
                          ("cat", categorical, ["city", "heating"])])
out = prep.fit_transform(homes)
print(out.shape)
print(*prep.get_feature_names_out(), sep="\n")
print(out[2].round(2).tolist())
```

```text
(5, 7)
num__size
num__rooms
cat__city_Ankara
cat__city_Bursa
cat__city_Izmir
cat__heating_electric
cat__heating_gas
[-0.13, 0.27, 0.0, 0.0, 1.0, 1.0, 0.0]
```

- Each part is a triple: **name**, **transformer**, **columns**. For numbers,
  the two steps "fill, then scale" became one transformer with
  `make_pipeline` (we will see Pipeline in detail in the next section).
- The output has 7 columns: 2 scaled numbers + 3 cities + 2 heating types. The
  names have the form `part__column`; you can read where each column came
  from.
- In the third row, the home with the missing size: filled with the median and
  scaled (−0.13), the Izmir and electric columns are 1.
- `fit` happens once; on the test data `transform` is called on the same
  object. What each part learned (median, mean, categories) is stored inside.

## Columns not in the list: remainder

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

drop = ColumnTransformer([("num", StandardScaler(), ["rooms"])])
keep = ColumnTransformer([("num", StandardScaler(), ["rooms"])],
                         remainder="passthrough")
print(drop.fit_transform(homes[["rooms", "id"]]).shape)
print(keep.fit_transform(homes[["rooms", "id"]]).shape)
print(keep.get_feature_names_out().tolist())
```

```text
(5, 1)
(5, 2)
['num__rooms', 'remainder__id']
```

- The default is `remainder="drop"`: a column not in the list is **silently
  dropped**. Forgetting to add a column raises no error; the model just never
  sees that information.
- `remainder="passthrough"` passes the rest through as they are. If there is a
  column that must not enter the model, like an ID number, that is dangerous
  too; the safest is to list the wanted columns **explicitly**.

## Selecting by type and pandas output

```python
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

numbers = make_column_selector(dtype_include="number")
texts = make_column_selector(dtype_include=object)
onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), numbers),
                          ("cat", onehot, texts)],
                         verbose_feature_names_out=False)
prep.set_output(transform="pandas")
out = prep.fit_transform(homes.drop(columns="heating"))
print(type(out).__name__, out.columns.tolist())
print(out.loc[2, "size"])
```

```text
DataFrame ['size', 'rooms', 'id', 'city_Ankara', 'city_Bursa', 'city_Izmir']
107.5
```

- `make_column_selector(dtype_include="number")` selects columns by type; when
  a new number column is added, the code does not need to change.
- But careful: **`id` is a number too**, so it was selected as a feature. If an
  ID number enters the model, the model may learn from order or chance. When
  selecting by type, such columns are dropped beforehand.
- `set_output(transform="pandas")` makes the output a DataFrame with column
  names; `verbose_feature_names_out=False` removes the `part__` prefix from
  the names. Reading intermediate results becomes much easier.

## Summary

- `ColumnTransformer([(name, transformer, columns), ...])` applies its own
  treatment to each column group and behaves as a single transformer.
- For several steps, give a part `make_pipeline(...)`.
- The default `remainder="drop"` silently drops what is not listed.
- `make_column_selector` selects by type; watch out for number columns like
  IDs.
- `get_feature_names_out` and `set_output(transform="pandas")` make the result
  readable.
