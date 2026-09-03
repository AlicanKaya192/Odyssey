You will reduce the confusion matrix's four numbers to two meaningful
ratios — and build both from the formula.

**What you need to do:**

1. Build the same flow and extract the four numbers from the confusion
   matrix.
2. Compute **precision**: `TP / (TP + FP)`. Print it to three decimals.
3. Compute **recall**: `TP / (TP + FN)`. Print it to three decimals.
4. Compute **F1**: `2 x precision x recall / (precision + recall)`. Print it
   to three decimals.
5. Print the three values sklearn gives **side by side on one line** (same
   order, three decimals).

**Expected output:**

```
0.839
0.963
0.897
0.839 0.963 0.897
```

**What separates the two ratios is their denominator:**

- **Precision 0.839** — the denominator `TP + FP` is **your predictions**.
  "Of the 31 people I called passing, 26 really did."
- **Recall 0.963** — the denominator `TP + FN` is **what actually exists**.
  "Of the 27 people who passed, I found 26."

The same `TP`, two different denominators, two different questions.

**Recall came out higher than precision.** The model casts a wide net: it
misses almost nobody who passed, but sweeps up some who failed. The 5 false
positives in the confusion matrix are exactly that.

**Why is F1 a harmonic mean?** With an ordinary average, a model that calls
exactly one person passing and gets it right (precision 1.0, recall 0.037)
would score 0.52 and look tolerable. The harmonic mean gives **0.071**: if
either is very low, so is the result.
