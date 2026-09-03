The data is 600 subscribers. Two text columns (`city`, `plan`), three
numeric ones (`tenure`, `monthly`, `support`) and the target `churn`. Three
columns have missing values.

In section 04 you did this by hand: take the median from the training data,
use it on the test set too, fit the encoder on training... Six steps and
four "from training" warnings.

In this exercise a **single object** will do the same job.

**What you need to do:**

1. Read the data. Print the missing-value counts as a dict.
2. Take everything but `churn` as `X` and the `churn` column as `y`, then
   split (`test_size=0.25`, `random_state=42`, `stratify=y`).
3. Build a `ColumnTransformer`:
   - for the **numeric** columns: impute with the median, then scale
   - for the **text** columns: impute with the most frequent value, then
     `OneHotEncoder(handle_unknown="ignore")`
4. Join it with `LogisticRegression(max_iter=1000)` into a `Pipeline` and
   fit it.
5. Print the baseline and the pipeline's test accuracy side by side (three
   decimals).
6. Print the **number of columns** after preprocessing and the **column
   names**.

**Expected output:**

```
{'city': 24, 'plan': 0, 'tenure': 0, 'monthly': 48, 'support': 30, 'churn': 0}
0.573 0.793
9
['num__tenure', 'num__monthly', 'num__support', 'cat__city_Ankara', 'cat__city_Bursa', 'cat__city_Izmir', 'cat__plan_basic', 'cat__plan_plus', 'cat__plan_pro']
```

**The baseline is 0.573 and the model 0.793.** A real 22-point gain.

But this exercise is not about the score. **It is about what the line
`pipe.fit(X_train, y_train)` did:**

- Computed the numeric columns' median **from the training data only**
- Computed the text columns' mode **from the training data only**
- Fitted the encoder **on the training data only**
- Fitted the scaler **on the training data only**
- Trained the model

When `pipe.predict(X_test)` was called, no step **learned again**; each
applied what it had learned during training.

**Section 04's rule — "split first, touch afterwards" — is no longer a
matter of care.** There is no way to run a pipeline in the wrong order.

**Look at the column list:** the three numeric columns stayed as they were
and the two text columns opened into six (3 cities + 3 plans). Nine in
total. Those names are the only correct source when reading coefficients.

**Why `handle_unknown="ignore"` is there:** if a city unseen during
training turns up in the test set, `OneHotEncoder` **raises an error** by
default. `ignore` sets all that row's city columns to zero. Without this
setting a production model dies on the first unexpected value.
