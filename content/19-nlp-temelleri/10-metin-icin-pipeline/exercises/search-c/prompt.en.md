`search_C(values)` should search only the model's `C` (from `values`) on the
ready `pipe` with a **5-fold** `GridSearchCV` (`scoring="f1_macro"`, training
data only). Return `[best C, test macro F1]`; F1 is measured on the test data
and rounded to 3 places.

**Expected output:**

```
[1, 0.874]
```
