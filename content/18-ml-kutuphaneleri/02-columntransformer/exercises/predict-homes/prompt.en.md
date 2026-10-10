`predict_homes(rows, prices, new_rows)` should build a **single** object that
predicts prices from a raw `[size, city, id]` table: `make_pipeline(prep,
LinearRegression())`. The preparation: `size` filled with the median, `city`
with `OneHotEncoder(handle_unknown="ignore")`, `id` dropped. Train it with
`rows` and `prices` and return the predictions for `new_rows` as a list
rounded to 1 place. New rows may have a missing size or an unseen city.

**Expected output:**

```
[1966.7, 2055.6]
```
