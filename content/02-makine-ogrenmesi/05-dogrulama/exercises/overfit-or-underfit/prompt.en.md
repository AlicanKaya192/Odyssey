Overfitting and underfitting call for **opposite fixes**: one asks you to
simplify the model, the other to complicate it. A wrong diagnosis sends you
the wrong way.

In this exercise you put the diagnosis into code.

**What you need to do:**

1. Prepare and split the data as usual.
2. Train two models: **`simple`** (depth 1) and **`complex`** (depth
   `None`).
3. Measure the training and test error for each.
4. Make the diagnosis:
   - If the gap between test and training error is **above 20** →
     `overfit`
   - Otherwise, if the training error is **above 50** → `underfit`
   - If neither → `ok`
5. Print one line per model: **the name, the training error, the test error,
   the diagnosis**.

**Expected output:**

```
simple 99.68 96.65 underfit
complex 0.0 59.06 overfit
```

**Two lines, two different diseases.**

In the `simple` model both errors are around 100 — the model is so simple it
cannot even explain the training data. That is **underfitting**, and the fix
is to complicate the model.

In the `complex` model the training error is **zero** and the test error 59.
The model memorised the data and generalised nothing. That is
**overfitting**, and the fix is to simplify it.

**Notice:** had you been looking at the test score alone you would have seen
96.65 and 59.06, said "the second is better", and moved on. With the
training score beside it, two entirely different problems appear — and they
have different cures.

The thresholds here (20 and 50) are numbers chosen for this data; in a real
project you look at how the two scores stand **relative to each other**
rather than at a fixed cut-off.
