`prep_frame(rows)` should build a `ColumnTransformer` that fills `size` with the
median and one-hot encodes `city` (`verbose_feature_names_out=False`), and
make the output a DataFrame with `set_output(transform="pandas")`. Return
`[columns, size_value_of_the_third_row]` (a `float`).

**Expected output:**

```
size
city_Ankara
city_Bursa
city_Izmir
95.0
```
