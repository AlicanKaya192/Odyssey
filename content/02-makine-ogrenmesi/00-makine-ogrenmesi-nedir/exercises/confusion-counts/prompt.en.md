"80% correct" is a number, but **which** 80%? In this exercise you will
open that number up.

You have the true state of ten patients (`1` ill, `0` not) and a model's
predictions.

**What you need to do:**

1. Compute four counts:
   - **TP** — actual 1, predicted 1 (found the ill patient)
   - **TN** — actual 0, predicted 0 (correctly left the healthy one alone)
   - **FP** — actual 0, predicted 1 (a false alarm)
   - **FN** — actual 1, predicted 0 (**missed an ill patient**)
2. Print all four **side by side on one line**: TP, TN, FP, FN.
3. Compute accuracy as `(TP + TN) / total` and print it to two decimals.

**Expected output:**

```
4 4 1 1
0.8
```

**The two mistakes are not the same thing.** An FP is an unnecessary test.
An FN is **a patient who slips through**. Accuracy blends both into one
number, says "80%", and erases the difference.

These four counts are called the **confusion matrix**, and they are what you
actually look at in classification. That is section 3.
