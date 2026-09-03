In the previous exercise you saw you cannot choose `k` from the test table.
Section 05's rule: a hyperparameter is chosen **with cross validation**.

But this exercise holds a trap, and the trap is the lesson.

**What you need to do:**

1. Prepare, split and scale the data. Build a `StratifiedKFold` (5 folds,
   `shuffle=True`, `random_state=42`).
2. Cross validate **on the training data only** for these values of `k`:
   **1, 3, 5, 7, 9, 15, 25**.
3. Print one line per `k`: **k, the CV mean, the CV spread** (three
   decimals).
4. Find the `k` with the **highest mean**.
5. Compute the **noise threshold**: subtract that k's own spread from the
   best mean. Among the `k` values above the threshold, take the
   **largest**.
6. Print the test accuracy for both choices: the CV winner first, then your
   robust `k`. One line each: **k, test accuracy**.

**Expected output:**

```
1 0.913 0.04
3 0.893 0.039
5 0.9 0.052
7 0.873 0.057
9 0.88 0.062
15 0.893 0.053
25 0.88 0.054
1 0.82
25 0.92
```

**Look at the first seven lines.** The highest mean is at `k=1`: 0.913. The
choice looks settled.

**Now look at the spread: 0.040.** The gap between the best and worst mean is
also 0.040 (0.913 - 0.873). So **every value of `k` sits inside the others'
noise.** Cross validation cannot separate them here.

Section 05's sentence: *"Before saying 'this model is better', the difference
has to exceed the spread."* When it does not, the choice is made on another
ground — and for KNN that ground is clear: **a larger `k` is more robust**,
because it does not hang on a single neighbour.

**The last two lines show the result:**

```
CV winner       k=1   ->  test 0.820
robust choice   k=25  ->  test 0.920
```

**The naive choice costs ten points.**

**This does not mean cross validation failed** — quite the opposite. Because
it gave the spread as well, we could say "this difference is meaningless".
Someone looking only at the mean would pick `k=1` and never learn why they
lost.
