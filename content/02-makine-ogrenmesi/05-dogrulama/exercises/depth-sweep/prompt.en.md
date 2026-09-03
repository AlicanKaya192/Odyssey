So far you have only looked at the test score. In this exercise you will put
**the training score** beside it — and see something entirely different about
the model.

A decision tree's `max_depth` tunes complexity directly.

**What you need to do:**

1. Prepare the data: read, drop the rows with gaps, encode the categories,
   split (`random_state=42`).
2. Try these depths in turn: **1, 2, 3, 5, 8 and `None`** (no limit).
3. Train the model at each depth and measure **two** errors: on the training
   set and on the test set.
4. Print one line per depth: **the depth, the training error, the test
   error** — the three side by side, errors to two decimals. Print `none`
   instead of `None`.

**Expected output:**

```
1 99.68 96.65
2 72.72 58.47
3 51.34 65.3
5 18.25 53.83
8 0.19 56.83
none 0.0 59.06
```

**Look at the two columns separately.**

**The training column falls to zero.** With no depth limit the tree
memorises every record in its own branch and makes no error at all on the
training data. That is not an achievement: the model **remembers** the data,
it does not learn the rule.

**The test column does not fall.** It wanders between 53 and 96 and never
drops below 50. The gap is -3.03 at depth 1 and **59.06** with no limit —
that gap is overfitting itself.

**Now look carefully at the test column:** 96.65 → 58.47 → 65.30 → 53.83 →
56.83 → 59.06. Not a smooth curve; it **jumps**.

Which depth is best? Reading the table and saying "5" is easy. But the test
set has 27 records; are those five-unit differences a real advantage, or an
accident of which 27 cars landed in the test set?

The next exercise measures exactly that.
