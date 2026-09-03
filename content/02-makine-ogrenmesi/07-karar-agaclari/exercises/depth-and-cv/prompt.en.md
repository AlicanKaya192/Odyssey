Depth is a tree's complexity knob. You will see a table familiar from
section 05 — and this time you will make the choice correctly.

**What you need to do:**

**Part one — the depth table:**

1. Try these depths: **1, 2, 3, 5, 8, `None`**.
2. Measure the training and test accuracy for each.
3. Print one line: **depth, training, test**. Write `none` for `None`.

**Part two — cross validation:**

4. Build a `StratifiedKFold` (5 folds, `shuffle=True`, `random_state=42`).
5. Cross validate **on the training data only** for these depths:
   **1, 2, 3, 5, `None`**.
6. Print one line each: **depth, CV mean, CV spread**.
7. Print the depth with the highest mean.

**Expected output:**

```
1 0.807 0.82
2 0.88 0.96
3 0.933 0.8
5 0.993 0.88
8 1.0 0.88
none 1.0 0.88
1 0.753 0.062
2 0.827 0.049
3 0.773 0.057
5 0.813 0.086
none 0.82 0.091
2
```

**Look at the training column in the first table:** 0.807 → 1.000. With no
depth limit the tree puts each record in its own leaf and memorises. The
same table as section 05's overfitting one.

**The test column jumps:** 0.82 → 0.96 → 0.80 → 0.88. On a test set of 50
records one record moves it by 0.02; this table is full of noise and **you
do not choose a depth from it**.

**Look at the second table.** The best mean is at **depth 2** (0.827) and it
also has the smallest spread (0.049). The difference is meaningful against
the spread: `none` comes second at 0.820 but with a spread of 0.091, far
less stable.

**This is the opposite of section 06.** There every `k` sat inside the noise
and cross validation could not separate them; here it separates them
comfortably.

**The same tool, two different outcomes** — which is why you look at the
spread every time. The mean alone is enough neither to say "I chose" nor "I
could not".

One more nicety: the depth you chose, 2, also gives the best result on the
test set (0.96). But you learned that **after** choosing; had you chosen by
looking at the test set, the measurement would not have been honest.
