In the second exercise we said a pipeline prevents leakage. Now you will
measure **how much** it prevents.

For scaling and imputing the effect is usually small. But it grows when a
step **looks at the target**. Feature selection is exactly such a step.

**What you need to do:**

1. Prepare, split and preprocess the data (nine columns).
2. With `numpy.random.default_rng(7)`, generate **200 columns of entirely
   random** noise and append them to the nine. Print the total column
   count.
3. **The wrong way:** pick the best 15 columns with
   `SelectKBest(f_classif, k=15)` on all the training data, then run
   `cross_val_score` on those 15.
4. **The right way:** put the selector and the model in a `Pipeline` and
   run `cross_val_score` on all 209 columns.
5. Print the two CV means and the gap between them (three decimals).
6. Print **how many of the 15 columns picked the wrong way are noise** (the
   first nine columns are real, the rest noise).

**Expected output:**

```
209
0.78
0.716
0.064
8
```

**A 6.4-point gap, entirely fabricated.**

What happened: the selector looked at **all the training data** and said
"these 15 columns resemble the target most". Picking 15 out of 209, it is
easy to find noise columns that happen to resemble the target. Validated on
that same data, those columns look good — because the selection was made on
it in the first place.

**The last line proves it: 8 of the 15 selected columns are pure noise.**
There is no information in them; they merely resemble `churn` in this
particular sample of 450 rows.

**The right way makes the selection inside each fold.** The noise columns
picked in the first fold do not help on that fold's validation part —
different rows live there. The trick falls apart and the real score
surfaces: 0.716.

**The general rule:** every step that looks at the target belongs inside
the pipeline. Feature selection, target encoding, outlier removal — all of
them.

**A warning:** the correct 0.716 is lower than the 0.738 from the second
exercise. The reason is simple — 200 noise columns genuinely make the
model's job harder. Adding noise hurts; the point is that **a bad
measurement makes that harm invisible.**
