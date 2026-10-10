## Scaling

| Class | When |
|---|---|
| `StandardScaler()` | the default; mean 0, deviation 1 |
| `RobustScaler()` | with outliers (median, quartiles) |
| `MinMaxScaler()` | when a 0–1 range is needed (images, neural networks) |
| `MaxAbsScaler()` | sparse data (keeps zeros) |
| — | tree models need no scaling |

## Missing values

| Code | What it does |
|---|---|
| `SimpleImputer(strategy="median")` | the median for numbers |
| `SimpleImputer(strategy="most_frequent")` | the most frequent for categories |
| `SimpleImputer(strategy="constant", fill_value=0)` | a constant |
| `add_indicator=True` | adds a "was missing" column |
| `KNNImputer(n_neighbors=5)` | the mean of similar rows |

## Categories

| Code | When |
|---|---|
| `OneHotEncoder(handle_unknown="ignore")` | unordered, few values |
| `OrdinalEncoder(categories=[[...]])` | ordered (size, level) |
| `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` | −1 for unknown |
| `TargetEncoder()` | many values (with cross fitting) |

## Creating features

| Code | What it does |
|---|---|
| `PolynomialFeatures(degree=2, include_bias=False)` | squares and interactions |
| `KBinsDiscretizer(n_bins=5, encode="ordinal")` | splits numbers into ranges |
| `FunctionTransformer(np.log1p)` | your own formula |
| `get_feature_names_out()` | the new column names |

## Errors

| Symptom | Cause |
|---|---|
| `Found unknown categories ['Van']` | no `handle_unknown="ignore"` |
| `Input X contains NaN` | the model does not accept missing values; fill first |
| `could not convert string to float` | a text column was not encoded |
| Sizes behave like S < XL < L | `OrdinalEncoder` alphabetical order |
| A suspiciously high training score | target encoding done by hand (leakage) |
