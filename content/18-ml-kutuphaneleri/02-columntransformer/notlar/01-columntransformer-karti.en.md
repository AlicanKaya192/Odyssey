## Building

| Code | What it does |
|---|---|
| `ColumnTransformer([("name", transformer, columns), ...])` | a treatment per group |
| `("num", make_pipeline(SimpleImputer(), StandardScaler()), [...])` | several steps in a part |
| `("drop_me", "drop", ["id"])` | drop a column explicitly |
| `("keep", "passthrough", ["x"])` | pass a column through as it is |
| `remainder="drop"` (default) / `"passthrough"` | the columns not listed |
| `make_column_selector(dtype_include="number")` | select by type |
| `make_column_selector(pattern="^price_")` | select by name |
| `make_column_transformer((tr, cols), ...)` | names the parts itself |

## Reading

| Code | Gives |
|---|---|
| `ct.get_feature_names_out()` | output column names (`part__column`) |
| `verbose_feature_names_out=False` | without the prefix |
| `ct.set_output(transform="pandas")` | a DataFrame output |
| `ct.named_transformers_["num"]` | a fitted part |
| `ct.transformers_` | the list of fitted parts |

## Errors

| Symptom | Cause |
|---|---|
| A column never entered the model | not listed, `remainder="drop"` |
| An ID number became a feature | selection by type or `passthrough` |
| `Some column names are not columns of the dataframe` | a wrong or missing column name |
| The output columns are in an unexpected order | the order of the parts is the output order |
| An error on an unknown category | no `handle_unknown` on the part's `OneHotEncoder` |
