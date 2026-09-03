You are about to run a hyperparameter sweep: which setting is better? You
will measure it with cross validation. But `cross_val_score` computes
**accuracy** by default.

Let us measure what that means on imbalanced data.

**What you need to do:**

1. Prepare, split (`stratify=y`) and scale the data.
2. Set up a `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
3. Try these five metrics in turn: **accuracy, recall, f1, roc_auc,
   average_precision**. Cross validate a
   `LogisticRegression(max_iter=1000)` on the **training** data for each.
4. Print one line per metric: **the metric's name, the mean, the spread**
   (three decimals).
5. On the last line print the name of the **narrowest**-spread metric and
   the **widest** one, side by side.

**Expected output:**

```
accuracy 0.952 0.008
recall 0.317 0.188
f1 0.397 0.183
roc_auc 0.93 0.028
average_precision 0.521 0.144
accuracy recall
```

**Accuracy's spread is 0.008.** All five folds give nearly the same number.

That looks like a good thing — steady, reliable. It is not. **In a
hyperparameter sweep this metric can say nothing:** whatever setting you
try, the result stays around 0.95. You cannot rank anything.

**Recall's spread is 0.188** — twenty-three times as much. The reason is
plain: each fold holds only ~17 positives, and a few escaping moves the
number noticeably.

That is **noise**, yes. But there is a real signal inside it; accuracy has
no signal at all.

**`roc_auc` and `average_precision` sit between the two:** they are
sensitive to the minority class (0.930 and 0.521 are very different from
each other) yet their spreads are narrower (0.028 and 0.144), since they do
not hang on individual records.

**In practice:** hyperparameter searches on imbalanced data usually use
`average_precision`. `GridSearchCV` takes the same `scoring` parameter.

**The general rule:** a metric whose spread is near zero is not steady but
**blind**.
