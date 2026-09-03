The previous section ended with a single tree being unstable. The fix:
**build many trees and ask them all.**

In this exercise you will put three models side by side — and see once more
why one number is not enough.

**What you need to do:**

1. Prepare and split the data (`random_state=42`, `stratify=y`).
   **No scaling** — all of these are tree-based.
2. Print the baseline (the most frequent class, three decimals).
3. Take three models in turn:
   - `tree` — `DecisionTreeClassifier(max_depth=2, random_state=42)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Print one line each: **the name, the test accuracy, the CV mean, the CV
   spread** (`StratifiedKFold`, 5 folds, `shuffle=True`, `random_state=42`,
   on the **training** data only).
5. Print the **test winner** and the **CV winner** side by side.
6. Print `different` if they differ, `same` if they agree.

**Expected output:**

```
0.7
tree 0.96 0.827 0.049
forest 0.9 0.867 0.063
boosting 0.88 0.873 0.053
tree boosting
different
```

**Read the test column and the tree wins: 0.96.** It beats both the forest
and boosting. So what is all this ensemble business for?

**Read the CV column: the order reverses.** The tree is **last** at 0.827
and boosting first at 0.873.

Which do you believe? Remember section 05: on a test set of 50 records, one
record moves the accuracy by 0.02. In section 07's depth sweep the test
column jumped 0.82 → 0.96 → 0.80; **0.96 is the peak of that jumping**, not
a real advantage.

CV is the mean of five separate measurements. The spreads are close too
(0.049-0.063), so the 0.046 between them sits at the edge of the noise — but
at least it does not rest on a single draw.

**The last line is this module's most repeated lesson:** one number does not
settle a question about a model.
