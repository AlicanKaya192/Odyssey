The car data you met in section 05: 120 listings with `age`, `km`,
`engine` (numeric, 14 missing), `fuel`, `gearbox` (text) and the target
`price`.

This exercise runs a regression project **from start to finish**.

**What you need to do:**

1. Read the data, take the five columns as `X` and `price` as `y`. Split
   (`test_size=0.25`, `random_state=42` — regression has no `stratify`).
2. Build the preprocessor: median + scaling for the numeric columns,
   `OneHotEncoder(handle_unknown="ignore")` for the text ones.
3. Measure the **baseline**: predict the training mean for everything.
   Print MAE, RMSE and R² on one line (MAE/RMSE to one decimal, R² to
   three).
4. Take three models in turn: `linear` (`LinearRegression`), `tree`
   (`DecisionTreeRegressor(max_depth=3, random_state=42)`), `forest`
   (`RandomForestRegressor(n_estimators=200, random_state=42)`).
   Print one line each: **the name, the cross-validation MAE, the CV
   spread, the test MAE, the test R²**.
5. On the last line print the **CV winner** and the **test winner** side by
   side (the lowest MAE wins).

**Expected output:**

```
137.3 154.7 -0.02
linear 16.6 2.8 16.2 0.984
tree 69.3 10.2 65.7 0.746
forest 42.3 15.1 44.2 0.883
linear linear
```

**Why the first line is written:** the baseline's MAE is 137.3 and its R²
−0.02. A negative R² means "worse than the mean" — an expected result here,
since the baseline *is* the mean and a small deviation on the test set
pushes it below zero.

**Now look at the real lesson: the simplest model wins.**

Linear regression's MAE is **16.2**; the forest's is 44.2 and the tree's
65.7. The simplest model beats the most complex one **fourfold**.

That contradicts the intuition "a more complex model is better", and the
reason was measured in section 07: **when the relationship really is
linear**, trees try to imitate it with steps and lose. An ensemble does not
rescue it either — the forest improves on the tree (65.7 → 44.2) but comes
nowhere near the linear model. The problem is not the number of trees but
that a tree does not suit the data.

**Look at the spreads too:** 15.1 for the forest against 2.8 for the linear
model. The forest is not only worse but **less stable** — expected with a
training set of 90 rows.

**The last line:** on this data CV and the test agree on the winner. In
section 08 they did not. Agreement gives confidence; disagreement is the
warning to **never trust one number**.
