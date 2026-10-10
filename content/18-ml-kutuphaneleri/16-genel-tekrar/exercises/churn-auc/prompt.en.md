`churn_auc(c)` returns the pipeline's 5-fold mean AUC on the churn data (3 places).
The `monthly` column has gaps; the starter code only scales the number columns
and fails. Build the number part as **fill with the median + scale**
(`make_pipeline(SimpleImputer(strategy="median"), StandardScaler())`).

**Expected output:**

```
0.777
0.771
```
