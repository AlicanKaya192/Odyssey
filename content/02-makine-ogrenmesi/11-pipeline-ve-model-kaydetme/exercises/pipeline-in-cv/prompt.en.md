A pipeline's real gain does not show in a single line. It appears when you
hand a pipeline to section 05's `cross_val_score`.

**What you need to do:**

1. Prepare and split the data. Write a **function that builds** the
   preprocessor (each model must get its own copy).
2. Set up a `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
3. Build two pipelines and take them in turn:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
4. Print one line each: **the name, the CV mean, the CV spread, the test
   accuracy** (three decimals). Cross validate with the **raw `X_train`** —
   the pipeline does the preparation itself.
5. On the last line print the CV winner and the test winner side by side.

**Expected output:**

```
logreg 0.738 0.037 0.793
forest 0.689 0.027 0.753
logreg logreg
```

**Note what you handed `cross_val_score`: the raw `X_train`.** Unfilled
missing values, unencoded text columns, unscaled numbers.

`cross_val_score` opens five folds and **retrains every step of the
pipeline inside each one.** The first fold's median comes from that fold's
training part; the second fold's from the second.

**Try doing that by hand:** `fit_transform` the scaler once and hand the
result to `cross_val_score`, and the scaler has seen all the training data.
That data is then split into five folds, and each fold's "validation" part
consists of rows the scaler has already seen. **A silent leak** — and
nobody notices.

A pipeline makes this **structurally impossible**. In the third exercise
you will measure how large that leak can get.

**As for the results:** logistic regression leads in both columns. This
data is largely linear — churn falls as `tenure` rises and climbs as
`support` rises — and the forest cannot exploit that smoothness.

**The spreads matter too:** 0.037 and 0.027. The 0.049 gap between the
means sits above those spreads, so the difference is real.
