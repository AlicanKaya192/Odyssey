You learned four model families: linear, KNN, tree-based and ensemble.
Which suits this data?

**The answer comes from measurement** — and in this section choosing the
right **metric** is your job too.

**What you need to do:**

1. Prepare and split the data (no `followup_calls`, `stratify=y`).
2. Set up a `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
3. Take four models in turn:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `knn` — `KNeighborsClassifier(n_neighbors=15)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Print one line each: **the name, the CV average precision, the CV
   spread, the test ROC AUC, the test average precision** (three decimals).
   Use `scoring="average_precision"` for the cross validation.
5. Print average precision's **baseline** (the positive rate).
6. On the last line print the CV winner.

**Expected output:**

```
logreg 0.542 0.04 0.724 0.462
knn 0.406 0.065 0.672 0.344
forest 0.429 0.043 0.662 0.309
boosting 0.455 0.026 0.71 0.411
0.195
logreg
```

**Why average precision rather than accuracy?** You saw it in the second
exercise: the baseline is 0.805 and all four models will score near it.
Accuracy **cannot tell any model from another** on this problem — section
09's lesson that "a metric whose spread is near zero is not steady but
blind".

Average precision is sensitive to the minority class and its baseline is
**0.195**. 0.542 is about three times that.

**The result is counterintuitive: the simplest model wins.** Logistic
regression leads both in CV (0.542) and on the test (0.462). The forest
scores 0.429, boosting 0.455 and KNN 0.406.

That is the same lesson as the car data in the first exercise:
**complexity is not an advantage in itself.** With eight features and 600
training rows there is no extra structure for the ensembles to learn.

**Do not forget the spreads:** 0.040 for logreg and 0.026 for boosting. The
0.087 gap between the means is more than twice those spreads, so the
difference is real — the check you learned in section 08.

**And note the gap between ROC AUC and average precision:** 0.724 and 0.462
for logreg. The same model, the same probabilities. As you measured in
section 09, ROC comes out optimistic on imbalanced data.
