Before building a model you build a **baseline**: the simplest prediction
that learns nothing. For regression that is predicting the mean of the
training data for everything.

**What you need to do:**

1. Compute the mean of the training prices — that is the baseline.
2. Print the baseline, rounded to two decimals.
3. Compute the **absolute error** for each test price and print the list
   (each to two decimals).
4. Print the mean of those errors — this is called **MAE**.

**Expected output:**

```
297.5
[2.5, 97.5, 82.5]
60.83
```

**Why absolute values:** if one prediction is off by +40 and another by -40,
adding the errors gives zero and the model looks perfect. The absolute value
measures the **size** of the mistake rather than its direction.

**What this number is for:** 60.83 is the line your first model has to beat.
If a model gives 55 it has learned something; if it gives 65 it has not, and
it is worse than the mean.
