In the previous exercise you saw `k` change the answer. Now you will measure
**what** `k` tunes.

It should feel familiar from section 05: you will read two scores together.

**What you need to do:**

1. Prepare and scale the data (as in the previous exercise).
2. Try these values of `k` in turn: **1, 3, 5, 9, 15, 25**.
3. Measure two accuracies per `k`: on the **training** set and on the
   **test** set.
4. Print one line per `k`: **k, the training accuracy, the test accuracy** —
   accuracies to three decimals.

**Expected output:**

```
1 1.0 0.82
3 0.94 0.86
5 0.94 0.92
9 0.927 0.9
15 0.92 0.88
25 0.927 0.92
```

**The first line: at `k=1` the training accuracy is 1.000.**

Not surprising once you think about it: every training point's **own nearest
neighbour is itself**. The distance is zero. The model reads that point's
label off itself and never errs.

On test it drops to 0.82 — a textbook example of section 05's overfitting
table: **perfect on training, weak on test.**

**As `k` grows**, the training accuracy falls (the model can no longer
memorise) and the test accuracy generally rises. But not on a smooth curve:
0.82 → 0.86 → 0.92 → 0.90 → 0.88 → 0.92, it jumps.

That jumping should be familiar — you saw it in section 05 and the cause is
the same: on a test set of 50 records, one record changing sides moves the
accuracy by 0.02.

**This is why you cannot choose `k` from this table.** How it is chosen comes
in the next exercise.
