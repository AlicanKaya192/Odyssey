`predict()` really compares the probability with **0.5**. That number is a
default sklearn chose, not something that came from the data.

On imbalanced data 0.5 is almost never the right place: the model already
gives positives low probabilities.

**What you need to do:**

1. Prepare, split and scale the data. Train a
   `LogisticRegression(max_iter=1000)`.
2. Get the positive class's probability with `predict_proba`.
3. Try these thresholds in turn: **0.5, 0.4, 0.3, 0.2, 0.1, 0.05**.
4. Print one line per threshold: **the threshold, precision, recall, F1 and
   the number of frauds caught** (three decimals).
5. On the last line print **the threshold giving the highest F1** and that
   F1 value side by side.

**Expected output:**

```
0.5 0.75 0.286 0.414 6
0.4 0.6 0.286 0.387 6
0.3 0.5 0.286 0.364 6
0.2 0.5 0.333 0.4 7
0.1 0.342 0.619 0.441 13
0.05 0.262 0.762 0.39 16
0.1 0.441
```

**F1 peaks at a threshold of 0.10: 0.441.** At the default 0.5 it was 0.414.

**Why that line matters:** the model never changed. The same coefficients,
the same probabilities, no retraining. All that changed is **where the
decision is made** — and the number of frauds caught went from 6 to 13.

**What happens at 0.05?** Recall climbs to 0.762 (16 caught) but precision
falls to 0.262 and F1 comes back down. "Lower the threshold, raise recall"
is not an unlimited strategy.

**A warning:** here you chose the threshold **by looking at the test set**.
In a real project that would be exactly section 05's leakage — a threshold
is chosen on a validation set or with cross validation, and the test set
only gives the final report.

**A second warning:** F1 treats precision and recall as equally important.
The business usually does not. If a miss costs 400 and a false alarm 5, the
expected cost picks 0.05, not the 0.10 that F1 named.

**Choosing a threshold is a business decision, not a model decision.**
