You learned four model families: linear, KNN, tree-based and ensemble.
Which suits this data?

**The answer comes from measurement** — and in this section choosing the
right **metric** is your job too.

**What you need to do:**

1. Prepare and split the data (no `followup_calls`, `stratify=y`). Encode
   the text columns with `OneHotEncoder(handle_unknown="ignore",
   drop="if_binary")`: the two-valued columns (`sex`, `smoker`) become a
   single column. Opening a two-valued column into two gives the same
   information twice.
2. Set up a `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
3. Take four models in turn:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `knn` — `KNeighborsClassifier(n_neighbors=15)`
   - `forest` — `RandomForestClassifier(n_estimators=200, min_samples_leaf=30, random_state=42)`
     (`min_samples_leaf=30` leaves at least 30 rows in every leaf. In very
     small leaves two splits can get exactly the same score and the
     processor breaks that tie differently; with large leaves the result is
     the same on every computer.)
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Print one line each: **the name, the CV average precision, the CV
   spread, the test ROC AUC, the test average precision** (three decimals).
   Use `scoring="average_precision"` for the cross validation.
5. Print average precision's **baseline** (the positive rate).
6. On the last line print the CV winner.

**Expected output:**

```
logreg 0.541 0.038 0.723 0.46
knn 0.379 0.025 0.637 0.299
forest 0.518 0.067 0.709 0.39
boosting 0.462 0.024 0.71 0.411
0.195
logreg
```

**Why average precision rather than accuracy?** You saw it in the second
exercise: the baseline is 0.805 and all four models will score near it.
Accuracy **cannot tell any model from another** on this problem — section
09's lesson that "a metric whose spread is near zero is not steady but
blind".

Average precision is sensitive to the minority class and its baseline is
**0.195**. 0.541 is about three times that.

**The result is counterintuitive: the simplest model wins.** Logistic
regression leads both in CV (0.541) and on the test (0.46). The forest
scores 0.518, boosting 0.462 and KNN 0.379.

That is the same lesson as the car data in the first exercise:
**complexity is not an advantage in itself.** With eight features and 600
training rows there is no extra structure for the ensembles to learn.

**Do not forget the spreads:** 0.038 for logreg and 0.024 for boosting. The
0.079 gap between the means is more than twice those spreads, so the
difference is real — the check you learned in section 08. The forest is close
to logreg (0.518) but its spread is 0.067: the 0.023 gap is far below it, so
CV cannot tell the two apart. On the test logreg leads (0.46 to 0.39).

**And note the gap between ROC AUC and average precision:** 0.723 and 0.46
for logreg. The same model, the same probabilities. As you measured in
section 09, ROC comes out optimistic on imbalanced data.
