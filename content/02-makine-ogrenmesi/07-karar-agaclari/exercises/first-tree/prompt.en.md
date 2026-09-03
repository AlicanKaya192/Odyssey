KNN asked "who resembles this record most". A decision tree asks something
entirely different: **"which question separates the group best?"**

You will put three models side by side on the same data.

**What you need to do:**

1. Read `customers.csv`, take the three columns into `X` and `churn` into
   `y`, split (`random_state=42`, `stratify=y`).
2. Build the **baseline**: the most frequent class.
3. Train a **decision tree**: `max_depth=3`, `random_state=42`. **Do not
   scale** — you will see why in the next exercise.
4. Train a **KNN**: `k=25` on **scaled** data (the robust choice from
   section 06).
5. Print the three accuracies **side by side on one line**: baseline, tree,
   KNN.
6. Print `better` if the tree beats the baseline, `worse` otherwise.
7. Which model is better? Print `knn` or `tree`.

**Expected output:**

```
0.7 0.8 0.92
better
knn
```

**The tree beats the baseline** (0.80 against 0.70) — so it has learned
something.

**But it loses to KNN** (0.92). That does not mean trees are bad; it means
this one suits **this data** less well.

The reason lies in how a tree works: it builds stepped rules (`visits <=
18.5` and so on). When the boundary is smooth and curved it has to imitate
it in steps, losing a little at every step.

We saw the reverse in section 05: on the car data the tree's error was 64
and linear regression's 16.5. There too the data was linear and the tree was
struggling with steps.

**The lesson: choosing a model is a matter of measurement.** Which one wins
depends on the shape of the data and there is no way to know in advance.
Trees have advantages of their own — you will see them in the next
exercises.
