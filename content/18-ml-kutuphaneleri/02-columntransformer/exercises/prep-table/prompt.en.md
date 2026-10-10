`prep_table(rows)` should build a DataFrame from `[size, city, id]` rows and
prepare it with a `ColumnTransformer`: `size` filled with the median and
scaled, `city` encoded with `OneHotEncoder(handle_unknown="ignore",
sparse_output=False)`, `id` kept out of the model. Return `[shape, names]`:
shape as a list, names from `get_feature_names_out()`. The starter code has no
city part.

**Expected output:**

```
[4, 4]
num__size
cat__city_Ankara
cat__city_Bursa
cat__city_Izmir
```
