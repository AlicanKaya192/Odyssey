In section 06, skipping the scaling dropped KNN **below the baseline**: 0.64
against 0.92. What happens to a tree on the same data?

**What you need to do:**

1. Build the same flow and split it.
2. Train **two trees**, both with `max_depth=3` and `random_state=42`:
   - one on the **raw** data
   - one on the **scaled** data
3. Print the two accuracies side by side (three decimals).
4. Print `same` if the results are equal, `different` otherwise.
5. Print the difference scaling made for KNN in section 06: **0.92 - 0.64**,
   to two decimals.

**Expected output:**

```
0.8 0.8
same
0.28
```

**The two numbers are identical.** Not one decimal moves.

**Why:** the tree asks `income <= 137500`. After scaling that question
becomes `income_scaled <= 0.42`. **The threshold changes, the ordering does
not** — and a tree cares only about ordering. Since which records fall above
the threshold never changes, neither does the tree.

**The third line shows the contrast:** on the same data, the same scaling
operation made a difference of **0.28** for KNN.

<br>

| Model | Unscaled | Scaled | Difference |
|---|---|---|---|
| KNN | 0.64 | 0.92 | **0.28** |
| Tree | 0.80 | 0.80 | **0.00** |

**The lesson: there is no rule saying "always scale".** Scaling is a step
that depends on what the model looks at:

- **Anything using distance** (KNN, SVM, clustering) → compulsory
- **Anything using thresholds** (trees, forests, gradient boosting) →
  unnecessary

Scaling for a tree does no harm and no good; it is a wasted step.

**For the same reason trees are robust to outliers:** a record a hundred
times larger is still in the "above the threshold" group, and that is all.
