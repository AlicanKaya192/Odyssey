Accuracy came out at 85%. But **which** 85%? In this exercise you will open
that number up.

**What you need to do:**

1. Build the same flow as the previous exercise (same split, same model).
2. Compute the **confusion matrix** and print it, turned into a list with
   `.tolist()`.
3. Extract the four numbers from the matrix and print them **side by side on
   one line**: TN, FP, FN, TP.
4. Compute accuracy from those four: `(TN + TP) / total`. Print it to three
   decimals.
5. Which kind of error is more common? Print `FP` if false positives
   outnumber false negatives, `FN` otherwise.

**Expected output:**

```
[[8, 5], [1, 26]]
8 5 1 26
0.85
FP
```

**How to read the matrix:** rows are **actual**, columns **predicted**. The
top-left corner is always TN.

```
                 predicted 0   predicted 1
actual 0              8             5      <- 5 false positives
actual 1              1            26      <- 1 false negative
```

**The last line is the finding.** The model said "passed" to a failing
student 5 times but said "failed" to a passing student only once. It
**leans towards saying "passed"**.

Is that good or bad? It depends not on the model but on what the decision is
used for:

- For a **scholarship**, giving one to someone undeserving (FP) is
  expensive — this model is bad.
- For a **support class**, missing someone who needs it (FN) is expensive —
  this model is good.

The same four numbers, two different conclusions. Accuracy said 85% and hid
that distinction entirely.
