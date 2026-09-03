A decision tree's most praised quality is being **readable**. That is true,
but being readable and being read correctly are not the same thing. This
note is about the second.

## Reading a node

```
visits <= 18.5
gini = 0.425
samples = 150
value = [104, 46]
class = stays
```

| Line | Turned into a sentence |
|---|---|
| `visits <= 18.5` | "Do they visit fewer than 18.5 times a month?" |
| `samples = 150` | 150 records reached this node |
| `value = [104, 46]` | 104 stay, 46 leave |
| `gini = 0.425` | Moderately mixed |
| `class = stays` | The majority is "stays" |

**`samples` is the most often skipped line.** If a leaf holds 3 records, its
rule was built by looking at three people; it may carry nothing that
generalises.

When reading a rule you always ask "how many records is this based on".

## Two leaves with the same label

Sometimes a split gives the same class on both sides:

```
|--- income <= 41500 --> class: 0    (samples 20, value [11, 9])
|--- income >  41500 --> class: 0    (samples 75, value [74, 1])
```

The split does not change the label. Why did the tree split?

Because the tree optimises **impurity, not the label**. The left leaf is 11
to 9 (gini 0.495, almost the most mixed), the right is 74 to 1 (gini 0.026,
almost pure). Their majorities are the same but their **confidence** is
entirely different.

The difference shows up when you call `predict_proba`:

```python
model.predict_proba(X_test)
```

55% for a record landing in the left leaf, 99% for the right one.

**The practical consequence:** someone who only uses `predict` and never
looks at `predict_proba` treats those two records as the same. Threshold
tuning (section 03) uses exactly this difference.

## Feature importance: three traps

### 1. Importance is not causation

`visits` coming out as the most important column does not yield "if we
encourage customers to visit more they will not leave". The model sees
things varying together, not why.

Perhaps the customers who visit rarely are the ones who have already decided
to leave. In that case the visit count is a **consequence**, not a cause.

### 2. Correlated columns share importance

If two columns are nearly the same (floor area and room count, say) the tree
picks one; the other gets near-zero importance.

The wrong conclusion: "room count does not affect the price." The right one:
"the tree did not need it because floor area already carried the same
information."

The way to check: remove columns one at a time and see how far the model
worsens.

### 3. High-cardinality columns inflate

A continuous numeric column offers thousands of possible thresholds; a
two-category column offers one. The tree is luckier at stumbling on a good
split in the first.

The extreme case: put a **customer id** in the data and the tree can
separate every record with it, making that column look the most important —
though it carries no information at all.

**Columns like ids, sequence numbers and timestamps are removed before the
data reaches the model.**

## A more reliable measure

Instead of `feature_importances_` you can use **permutation importance**:

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test,
                                n_repeats=10, random_state=42)

for name, value in zip(X.columns, result.importances_mean):
    print(name, round(float(value), 3))
```

What it does is simple: it **shuffles** a column's values and sees how far
the model's score falls. A large fall means that column really is being
used.

It has two advantages:

- **It can be measured on the test set**, so it shows information that
  actually generalises.
- **High-cardinality columns do not inflate**, because the measurement looks
  at the score rather than the number of splits.

It has a limit too: it still misleads with correlated columns. Shuffle one
and the score does not fall, because the other carries the same
information — and both look "unimportant".

## Instability

Remove a few rows from the data and retrain, and **even the root split can
change**.

The cause is greediness: the first split decides between two candidates by a
hair, and when that flips the whole tree beneath it is reshaped.

**This has two consequences:**

- Presenting a single tree's rules as "a discovered truth" is wrong.
  Tomorrow another tree may give other rules.
- Feature importance is unstable too: today `visits`, ten rows later
  `income` can come out most important.

There is a way to measure the stability: train several trees with different
`random_state` values or different subsamples and see whether the root split
changes.

**The fix is ensemble methods:** the average of many trees damps a single
tree's instability. That is the next section.

## When presenting a rule

Tree rules can be explained to stakeholders and that is a real advantage.
But three things are said together:

| What is said | Why |
|---|---|
| The rule | "Those who visit fewer than 18 times and earn little leave" |
| How many records it rests on | `samples` — a rule from 5 records does not generalise |
| How certain it is | The `value` breakdown — 11 to 9 and 74 to 1 are not the same |

Stating only the rule, without the confidence and the number it rests on, is
misleading.

And always: **this is a rule, not an explanation of a cause.**
