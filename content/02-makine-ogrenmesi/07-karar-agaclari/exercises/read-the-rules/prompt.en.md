Linear regression's coefficients are abstract. A tree's rules can be
**turned into sentences** — and that is a tree's most valuable quality.

**What you need to do:**

1. Build the same flow and train a tree with **`max_depth=2`**
   (`random_state=42`).
2. Print the rules with `export_text`. Do not forget the column names, or it
   writes `feature_0` and the like.
3. Print the **root split's** feature and threshold side by side (the
   threshold to two decimals).
4. Print the **number of leaves and the depth** side by side.

**Expected output:**

```
|--- visits <= 18.50
|   |--- income <= 137500.00
|   |   |--- class: 1
|   |--- income >  137500.00
|   |   |--- class: 0
|--- visits >  18.50
|   |--- income <= 41500.00
|   |   |--- class: 0
|   |--- income >  41500.00
|   |   |--- class: 0
visits 18.5
4 2
```

**Turn the root question into a sentence:** "Does this customer visit fewer
than 18.5 times a month?" The tree tried every feature and every possible
threshold, took the question that separates the group best — and `visits`
won.

**Now look at the bottom two leaves: both say `class: 0`.**

The split does not change the label. So why did the tree split?

**Because the tree optimises impurity, not the label.** The left leaf holds
20 records split 11 to 9 (almost half and half); the right holds 75 split 74
to 1 (almost pure). Both have the same majority class but entirely different
**confidence**.

The difference shows up when you call `predict_proba`: the left leaf says
55%, the right one 99%. Someone using only `predict` treats those two
records as the same — when one is nearly certain and the other a coin flip.

**When reading a rule you always look at two things together:** the rule
itself and **how many records it rests on**. A rule from a leaf of 3 records
may carry nothing that generalises.
