Section 07 ended saying "a single tree is unstable" without measuring it.
Now you will — and see how far a forest damps it.

**The method:** take out a different 10% of the training data each time and
retrain both models. The test set never changes, so the scores are
comparable.

**What you need to do:**

1. Prepare and split the data.
2. Run six rounds with `seed` from **0 to 5**. In each round:
   - Sample **90%** of the training data with that seed and match the
     labels.
   - Train a **tree** (`max_depth=3`, `random_state=42`).
   - Train a **forest** (`n_estimators=200`, `random_state=42`).
   - Keep both test accuracies and **the tree's root threshold**.
3. Print the three lists on separate lines: the tree scores, the forest
   scores, the root thresholds.
4. On the last line print the two ranges side by side: the tree's
   (highest − lowest) and the forest's (two decimals).

**Expected output:**

```
[0.92, 0.88, 0.78, 0.8, 0.8, 0.84]
[0.9, 0.84, 0.86, 0.9, 0.9, 0.92]
[16.5, 15.5, 16.5, 18.5, 28.5, 18.5]
0.14 0.08
```

**The first line: the tree wanders between 0.78 and 0.92.** The same model,
the same test set. The only thing that changed is which 10% dropped out —
and the score moves by 14 points.

**The third line is more troubling.** The root split's threshold climbs from
15.5 to 28.5. So the model's **rule** changes: in one round "those who visit
fewer than 16 times a month", in another "fewer than 28".

Imagine presenting that to a stakeholder as "the rule we discovered". Ten
rows later you would have found a different rule.

**The second line: the forest ranges from 0.84 to 0.92.** An 8-point range
instead of 14. The same noise, damped by half.

**Why it damps:** a single tree's error is largely random — this row dropped
so the threshold moved. Averaged, random errors cancel. A hundred trees see
a hundred different samples, err in a hundred different places, and the
average steadies.

**It does not eliminate, it reduces.** 0.08 is still not zero; an ensemble is
not magic but statistics.
