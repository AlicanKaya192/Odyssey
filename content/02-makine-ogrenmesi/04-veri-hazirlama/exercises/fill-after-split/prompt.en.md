You are going to fill the missing values — but **after splitting**. That is
this section's rule, and this whole exercise circles it.

**What you need to do:**

1. Read the file. Take the three **numeric** columns into `X` (`age`, `km`,
   `engine`) and `price` into `y`.
2. **Split first**: a quarter for testing, `random_state=42`. The missing
   values are still there; the split does not mind.
3. Compute the fill value from the **training data only**: the mean of the
   `engine` column.
4. Print that value and the `engine` mean over **all the data** side by side
   (three decimals).
5. Fill the gaps in both training and test using **the same value**.
6. Print how many gaps remain in each set, side by side.
7. Train the model and print the MAE (two decimals).

**Expected output:**

```
1.458 1.457
0 0
32.58
```

**The first line is what this exercise is about.** The two means are almost
identical: **1.458** and **1.457**. A difference of one part in a thousand.

So why bother?

**Because the rule is not about the size of the difference.** A mean
computed over all the data carries information from the test rows. Today the
difference is 0.001; on other data, with an outlier landing on the test
side, it could be 0.3.

Apply the rule as "no need when the difference is small" and you will never
see the day the difference is large — because measuring it requires doing
both computations anyway.

**The "same value" in step five matters too.** Filling the test set with its
own mean would move the two sets into different worlds; the model would be
examined on something other than what it was trained on.
