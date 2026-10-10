`keep_all_but_id(rows)` should build a `ColumnTransformer`: the `id` column is
dropped explicitly (`("drop_id", "drop", ["id"])`), everything else passes
through as it is (`remainder="passthrough"`,
`verbose_feature_names_out=False`). Return the output column names. The
starter code passes everything through; `id` is in the output too.

**Expected output:**

```
['size', 'city']
```
