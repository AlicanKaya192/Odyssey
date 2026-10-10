`lasso_columns(alpha)` should train `Lasso(alpha=alpha)` on all the data and return
the indices of the columns with a **non-zero** coefficient as a list. The
starter code only counts positive coefficients; a column with a negative
coefficient is selected too.

**Expected output:**

```
[9, 18, 20, 21, 29]
15
```
