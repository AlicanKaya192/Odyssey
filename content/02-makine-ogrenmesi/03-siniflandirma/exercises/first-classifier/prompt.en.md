For the first time the target is a **category**: did the student pass (`1`)
or fail (`0`). The flow is the same; the model and the measure change.

`students.csv` holds 160 students; the columns are `hours` (hours studied),
`prev_score` (previous mark), `attendance` (attendance percentage) and
`passed`.

**What you need to do:**

1. Import everything you need and read the file. The model is
   **`LogisticRegression`** (pass `max_iter=1000` or you get a warning).
2. Take the three columns into `X` and `passed` into `y`.
3. Split: a quarter for testing, `random_state=42`, and **`stratify=y`**.
4. Print the training and test counts side by side.
5. Build the **baseline**: predict the most frequent class for every test
   record and compute its accuracy.
6. Train the model and compute its accuracy. Print the baseline's and the
   model's accuracy **side by side** (three decimals).
7. Print `better` if the model beat the baseline, otherwise `worse`.

**Expected output:**

```
120 40
0.675 0.85
better
```

**`stratify=y` is new.** It keeps the class proportions the same in training
and test. Without it a random split might leave 30 passes and 10 fails in
the test set and a different ratio in training — the measurement would then
depend on the luck of the split. In classification it is passed almost
always.

**The second line is what this exercise is about.** The baseline is
**67.5%** — because most students pass, and even a line saying "everyone
passed" gets two thirds right.

The model's 85% only takes on meaning next to it. When the classes are
imbalanced, accuracy on its own says almost nothing: had one class been 95%,
a line that learns nothing would be **95% correct**.
