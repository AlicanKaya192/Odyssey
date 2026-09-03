`predict` gives you a `0` or a `1`. But inside the model there is a
**probability**, and `predict` cuts it at **0.5**.

That 0.5 is not the result of a calculation but a default. In this exercise
you will change it — without retraining the model.

**What you need to do:**

1. Build the same flow and train the model.
2. Take the **positive class's probability** for the test set.
3. Try three thresholds in turn: **0.3, 0.5, 0.7**.
4. For each, cut the probability at that threshold to produce predictions.
5. Print one line per threshold: **the threshold, precision, recall** — the
   three side by side, the ratios to three decimals.

**Expected output:**

```
0.3 0.818 1.0
0.5 0.839 0.963
0.7 0.889 0.889
```

**Read the table top to bottom:** as the threshold rises, precision goes up
(0.818 → 0.889) and recall goes down (1.0 → 0.889).

**At 0.3 recall is 1.000.** The model does not miss a single student who
passed. The price is precision falling to 0.818: it calls more failing
students "passed".

**At 0.7 precision is 0.889.** The model now speaks more cleanly but misses
three students who passed.

**This is a trade, not an improvement.** Moving the threshold reduces one
error and raises the other; nothing is gained overall. Real improvement only
comes from a better model or better features.

**So which one do you pick?** It depends on the problem:

- Finding who needs a support class → **lower** the threshold, miss nobody.
- Automatic scholarship approval → **raise** it, avoid wrong approvals.

**Important:** the threshold is a hyperparameter too. It is chosen on a
**validation** set, not on the test set — we look at all three on the test
set here because the subject is the trade-off itself, not the choice.
