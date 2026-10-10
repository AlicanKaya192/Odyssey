`df` has a `city` column of `category` dtype and an `x1` column with gaps.
`category_model(min_leaf)` should use both columns **without preprocessing**
(`categorical_features="from_dtype"`) and return `[is_categorical_,
test_score]` (the score with 3 places). The starter code does not use the
city at all.

**Expected output:**

```
[[True, False], 0.739]
```
