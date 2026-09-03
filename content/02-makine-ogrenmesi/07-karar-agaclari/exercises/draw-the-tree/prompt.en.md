You have read the rules as text. Now you will **draw** the tree itself — and
measure how much work each column did.

**What you need to do:**

1. Build the same flow and train the tree with **`max_depth=2`**
   (`random_state=42`).
2. Print each column's **importance**: one line each, **the column name and
   the value** (three decimals).
3. Print the name of the **most important** column.
4. Draw the tree with `plot_tree`, passing `feature_names`, the class names
   `stays` and `leaves`, and coloured boxes (`filled=True`).
5. Save it as `chart.png`.

**Expected output:**

```
age 0.0
income 0.454
visits 0.546
visits
```

The tree drawing will appear **in the results panel** after you run it.

**Each box in the drawing has five lines:**

| Line | What it means |
|---|---|
| `visits <= 18.5` | This node's question |
| `gini = 0.425` | Impurity: 0 pure, 0.5 the most mixed |
| `samples = 150` | How many records reached this node |
| `value = [104, 46]` | The breakdown by class |
| `class = stays` | The majority class |

**Look at the numbers: `age`'s importance is exactly 0.0.**

A tree of depth 2 has only three splits and none of them used `age`. But
that does **not mean age is unimportant** — only "its turn never came in
this tree". Raise the depth to 3 and `age` joins in, with an importance of
0.169.

**Feature importance has three traps:**

1. **Importance is not causation.** "`visits` is the most important" does not
   yield "if we persuade the customer to visit more they will stay". Perhaps
   the customers who visit rarely are the ones who already decided to leave;
   then the visit count is a **consequence**, not a cause.

2. **Correlated columns share importance.** If two columns are nearly the
   same the tree picks one and the other gets near-zero importance. The
   `age = 0.0` here is partly that — though its real cause is the depth
   limit.

3. **High-cardinality columns inflate.** A continuous numeric column offers
   thousands of possible thresholds and the tree is luckier at stumbling on
   a good split there. The extreme case: put a **customer id** in the data
   and the tree can separate every record with it, making that column look
   the most important — though it carries no information at all.

A more reliable measure is `permutation_importance`: it shuffles a column
and sees how far the score falls, and it can be measured on the test set.
