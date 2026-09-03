The previous exercise produced `18.5`. Is that good or bad?

The answer is not in the number but in **what you compare it against**. Now
you will build that comparison and measure the model against it.

**What you need to do:**

1. Read the file, take `area` and `price`, and split the data **the same
   way** (a quarter for testing, `random_state=42`).
2. Build the baseline: the mean price of the **training** data. Print it to
   two decimals.
3. Compute the baseline's mean absolute error on the test set — by
   predicting that same number for every test record.
4. Train the model and compute its mean absolute error.
5. Print the two errors **side by side**: the baseline first, then the model
   (two decimals).
6. Print `better` if the model beat the baseline, `worse` if it did not.

**Expected output:**

```
312.87
82.29 18.5
better
```

**The first line** is the baseline's prediction: it says 312.87 for every
house. A poor prediction, but a prediction — and one that can be measured.

**The second line** is the heart of it. 82.29 is the error you reach having
learned nothing; 18.5 is the error you reach by looking at the area. The gap
is **what the model added**: 77% of the error.

Had the model given 85, the output would be `worse` and those three lines of
code would have to go. The baseline exists precisely to make that decision
possible.

**Order matters:** the baseline is computed **before** the model. Computed
afterwards, you have already seen the model's number and it becomes easy to
adjust your expectation to it.
