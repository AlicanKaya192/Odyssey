In the previous exercise you saw a single split give anything between 16.16
and 21.56. The fix: measure not once but **five times**, and average.

Cross validation cuts the data into five pieces and makes each piece the
test in turn. Every record is tested exactly once and used for training
exactly four times.

**What you need to do:**

1. Prepare the data; again **do not split it**, cross validation does the
   cutting itself.
2. Build a `KFold`: **5 folds**, `shuffle=True`, `random_state=42`.
3. Measure a linear regression with `cross_val_score`, using
   `scoring="neg_mean_absolute_error"`.
4. Flip the sign of the scores, round to two decimals and print the list.
5. Print the **mean and the spread** (standard deviation) side by side (two
   decimals).
6. In the previous exercise `random_state=2` gave **17.07**. Print `inside`
   if that number falls **between** the lowest and highest fold, `outside`
   otherwise.

**Expected output:**

```
[14.97, 15.96, 19.29, 19.63, 12.64]
16.5 2.65
inside
```

**Two numbers come out, and the second is worth at least as much as the
first.**

- **16.50** is the model's expected error — the mean of five measurements,
  far sturdier than a single split.
- **2.65** is how much that number moves. The folds range from 12.64 to
  19.63.

**The third line is a check.** The 17.07 from a single split falls inside the
folds' range — so that number was not wrong, it was just **one draw**.

**The practical consequence:** if two models have means of 16.5 and 17.2 with
a spread of 2.65, the 0.7 between them sits inside the noise. Before saying
"this model is better", the difference has to exceed the spread.

**The `neg_` prefix looks odd but has a reason:** sklearn treats every score
as "larger is better". For an error that is backwards, so the sign is
flipped.

**Why `float()` is needed:** put NumPy numbers straight into a list and the
output shows `[np.float64(14.97), ...]`. `float()` cleans that up.
