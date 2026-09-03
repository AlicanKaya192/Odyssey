The `km` column runs from 10,000 to 300,000 and `engine` from 1.0 to 2.0.
Both are numbers but they do not live in the same world. In this exercise
you will measure **which model** that gap affects, and **how much**.

**What you need to do:**

1. Read the file and drop the rows with gaps (`dropna`). This section is
   about scaling; you solved the gaps in the previous exercise.
2. Take the three numeric columns into `X` and `price` into `y`. Split
   (`random_state=42`).
3. Fit a `StandardScaler` **on training** and apply it to **both**.
4. Train **KNN** (`n_neighbors=5`) twice: on raw data and on scaled data.
   Print the two MAEs side by side (two decimals).
5. Train **linear regression** twice as well: raw and scaled. Print the two
   MAEs side by side.
6. Print `same` if linear regression's two results are identical,
   `different` otherwise.

**Expected output:**

```
171.49 51.48
34.63 34.63
same
```

**The first line: a factor of three.** Unscaled, KNN is really only looking
at `km`. The gap between 1.0 and 2.0 in `engine` is nothing next to a
250,000 gap in `km`. In a distance computation the small column behaves as
if it were not there.

**The second line: no difference at all.** Linear regression learns a
separate coefficient per column and tunes it to that column's scale. If `km`
is in large numbers, its coefficient comes out small; the result does not
change.

**The lesson is not "always scale" but "know what each model looks at":**

| Affected | Not affected |
|---|---|
| KNN, SVM, clustering, neural networks | Decision tree, random forest |
| **Anything using distance** | **Anything using thresholds** |

A tree asks "is km above 150,000"; the column's scale does not change that
question.

**Watch the `fit` / `transform` distinction.** The scaler learns the
training set's mean and standard deviation; calling `fit_transform` on the
test set would be leakage and would also put the two sets on different
scales.
