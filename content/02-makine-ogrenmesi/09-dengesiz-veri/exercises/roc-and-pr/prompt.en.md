Precision, recall and F1 all hang on a single threshold. There are two ways
to measure a model's **ranking ability** — whether it can put the risky
transactions at the top of the list.

**What you need to do:**

1. Prepare, split and scale the data. Train the logistic regression and a
   `RandomForestClassifier(n_estimators=200, random_state=42)` (the forest on
   the unscaled data).
2. Print one line each: **the name, ROC AUC, average precision** (three
   decimals).
3. Print average precision's **baseline** — the value a random model would
   get, that is the positive rate (three decimals).
4. Draw the logistic regression's two curves **side by side**:
   - ROC on the left (`roc_curve`), axes `fpr` and `tpr`, title `ROC`.
   - The precision-recall curve on the right, axes `recall` and
     `precision`, title `PR`.
   - Save as `chart.png`.
5. On the last line print the difference between ROC AUC and average
   precision (for the logistic regression, three decimals).

**Expected output:**

```
logreg 0.908 0.525
forest 0.834 0.426
0.056
0.383
```

**ROC AUC is 0.908.** The chance of giving a randomly chosen fraud a higher
probability than a randomly chosen normal transaction is 90.8%. That sounds
excellent.

**Average precision is 0.525.** The same model, the same probabilities. The
gap is **0.383** — the number on the last line.

**Why so wide?** The ROC curve divides the false positive count by 354
negatives; even 38 false alarms make the rate only 0.107. The
precision-recall curve instead compares false alarms with **the positives**,
and there 38 false alarms look large next to 14 catches.

**The baselines differ too.** A random model's ROC AUC is 0.5, while its
average precision is the positive rate — here **0.056**. So 0.525 is
actually nine times the baseline. Not a bad number, merely not as rosy as
0.908.

**The rule:** do not report ROC AUC alone on imbalanced data. Give both
numbers; the second is far more honest about the minority class.

You can see it in the chart too: the ROC curve hugs the top left corner
while the PR curve falls away quickly as recall grows.
