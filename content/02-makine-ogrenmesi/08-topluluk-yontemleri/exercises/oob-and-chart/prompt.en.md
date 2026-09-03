Bagging has a pleasant by-product: each tree **never sees** roughly **a
third** of the training data — the rows that missed its bootstrap sample.
Those rows are a ready-made test set for that tree.

sklearn collects this into the **out-of-bag score**: an estimate without
setting aside a separate validation set.

**What you need to do:**

1. Prepare and split the data.
2. Try these tree counts: **10, 25, 50, 100, 200**. Pass `oob_score=True` to
   each model.
3. Print one line each: **the count, the OOB score, the test score** (three
   decimals). Collect both in lists.
4. Draw both curves on one chart (labelled `oob` and `test`, with
   `marker="o"`), label the axes `trees` and `accuracy`, add a title and a
   `legend`, and save as `chart.png`.
5. Print the difference between the OOB and test score **at the largest tree
   count** (absolute value, three decimals).

**Expected output:**

```
10 0.873 0.86
25 0.873 0.9
50 0.88 0.88
100 0.893 0.9
200 0.887 0.9
0.013
```

Your chart will appear **in the results panel** after you run it.

**The two curves run close together.** OOB estimates the test score well —
and it does so **without touching the test set at all**.

**Why that is valuable:** cross validation retrains the model for every
fold; 5 folds means 5 trainings. OOB is computed from trees you **already
trained**, at no extra cost. On large data that is a real difference.

**But it does not replace the test set.** OOB comes from the training data;
it can be used for model choice and tuning, while the final report is still
made on the untouched test set.

**It is unreliable with few trees:** with 10 trees each row is out-of-bag for
only 3-4 of them, which makes for a noisy estimate. As the count grows OOB
steadies — you can see that in the chart.

**One condition:** `oob_score` only works with `bootstrap=True`. Without
sampling with replacement there are no left-out rows.
