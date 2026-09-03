When a model is not good enough there are two routes: **collect more data**
or **change the model**. Instead of guessing which will work, you are going
to measure it.

The method: train the model again and again on growing portions of the
training data, watching both errors.

**What you need to do:**

1. Prepare and split the data (`random_state=42`).
2. Try these sizes in turn: **10, 20, 30, 45, 60, 79**.
3. For each size, train the model on the **first that many rows** of the
   training data and measure two errors:
   - the **training** error on that portion
   - the error on the **always the same** test set
4. Print one line per size: **the size, the training error, the test
   error**.
5. Draw both curves on one chart, label them, add a `legend`. The axes are
   `training size` and `MAE`; add a title and save as `chart.png`.
6. Print `no` if the gap between the two errors at the last size is **below
   1**, `yes` otherwise. (The question: would more data help?)

**Expected output:**

```
10 10.1 19.4
20 11.8 18.59
30 13.87 18.22
45 15.45 18.01
60 16.33 16.75
79 15.52 15.69
no
```

Your chart will appear **in the results panel** after you run it.

**The two curves move towards each other**, which can be surprising:

- **The training error rises** (10.10 → 15.52). Memorising ten records is
  easy, 79 is not. As the set grows the model sits a harder exam.
- **The test error falls** (19.40 → 15.69). A model that has seen more
  examples generalises better.
- **In the end they meet:** 15.52 and 15.69, a gap of 0.17.

**The `no` you printed is a decision.** Once the curves have met the model is
no longer memorising; what this data has to give has been taken. Collecting a
hundred more cars will not change the number.

Had a gap remained (training 5, test 18, say) the answer would be `yes`: the
model is memorising and more data would damp it.

**This chart buys an expensive decision cheaply.** "Should we collect data or
change the model" can be weeks of work; a learning curve answers it in
seconds.

The answer here is on the "model or feature" side: to do better you need a
new column or a different method.
