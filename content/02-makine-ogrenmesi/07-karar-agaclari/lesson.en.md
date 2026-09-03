# Decision Trees

KNN asked "who resembles this record most". A decision tree asks something
entirely different: **"which question separates the group best?"**

No distances, no neighbours. Only thresholds and branches.

## A tree is a sequence of questions

The model looks like this:

```
visits <= 18.5 ?
├── yes -> income <= 137500 ?
│          ├── yes -> leaves
│          └── no  -> stays
└── no  -> ...
```

When a new customer arrives you answer the root question, descend that
branch, answer the next question and arrive at a **leaf**. The leaf's label
is the prediction.

**This structure has two consequences:**

- **The model is readable.** Linear regression's coefficients are abstract;
  a tree's rules turn into sentences: "if they visit fewer than 18 times a
  month and earn under 137,500, they leave."
- **The rule is sharp.** Between 18.5 visits and 18.6 visits there is a
  chasm for the model; in reality there is none. The stepped nature of trees
  comes from this.

## How a split is chosen

At each step the tree does this: it **tries every feature and every possible
threshold**, measures how well each one separates the group, and takes the
best.

"Separating well" is measured by a number: **impurity**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">gini = 0</span><span class="anat-body">the group holds a single class — <b>pure</b></span></div>
    <div class="anat-row"><span class="anat-label">gini = 0.5</span><span class="anat-body">two classes half and half — <b>the most mixed</b></span></div>
    <div class="anat-row"><span class="anat-label">a good split</span><span class="anat-body">the two subgroups' impurity is <b>lower</b> than before the split</span></div>
  </div>
  <figcaption>At each step the tree takes the question that reduces impurity most. It does not look ahead — this is called "greedy".</figcaption>
</figure>

`entropy` can be used instead of `gini`; the results are usually very close.
For regression the measure changes: **variance** (MSE) is reduced instead of
impurity.

**Being greedy is a limit:** the tree takes the best split available now
without considering two steps ahead. Sometimes a "slightly bad now, very
good later" split is missed.

## Reading a tree

A trained tree's rules can be written out as text:

```python
from sklearn.tree import export_text
print(export_text(model, feature_names=list(X.columns)))
```

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
```

**Look at the bottom two leaves: both say `class: 0`.**

The split does not change the label. So why did the tree split at all?

Because the tree optimises **impurity**, not the label. The left leaf holds
20 records split 11 to 9 (gini 0.495, almost the most mixed state); the
right leaf holds 75 records split 74 to 1 (gini 0.026, almost pure). Both
have the same majority class but entirely different **confidence**.

That difference shows up when you call `predict_proba`: the left leaf says
55%, the right one 99%.

## Scaling changes nothing

In section 06, skipping the scaling dropped KNN below the baseline: 0.64
against 0.92. On the same data, a tree gives:

```
tree, unscaled   0.80
tree, scaled     0.80
```

**Identical.** Not one decimal moves.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>KNN</h4>
      <p>Computes distances.<br>The columns' scale changes <b>everything</b>: 0.64 → 0.92</p>
    </div>
    <div class="versus-side">
      <h4>Tree</h4>
      <p>Asks "is this value above the threshold".<br>Scaling moves the threshold, <b>not the answer</b>: 0.80 → 0.80</p>
    </div>
  </div>
  <figcaption>Scaling is not an "always do it" step; it depends on what the model looks at.</figcaption>
</figure>

The reason is simple: the question `income <= 137500` becomes
`income_scaled <= 0.42` after scaling. The threshold changes, the
**ordering** does not — and a tree cares only about ordering.

For the same reason trees are robust to outliers: a record a hundred times
larger is still in the "above the threshold" group, and that is all.

## Depth: a familiar knob

```
depth   training   test
    1      0.807   0.820
    2      0.880   0.960
    3      0.933   0.800
    5      0.993   0.880
    8      1.000   0.880
 none      1.000   0.880
```

You saw the same table in section 05: **the training accuracy climbs to
1.000** while the test accuracy stalls. With no depth limit the tree puts
each record in its own leaf and memorises.

**The test column jumps again:** 0.82 → 0.96 → 0.80 → 0.88. On a test set of
50 records one record moves it by 0.02, and this table is full of noise.

So the depth is not chosen from here. With cross validation:

```
depth   CV mean   CV std
    1     0.753    0.062
    2     0.827    0.049
    3     0.773    0.057
    5     0.813    0.086
 none     0.820    0.091
```

The best is **depth 2** (0.827) and it also has the smallest spread (0.049).
This time the choice is comfortable: the difference is meaningful against
the spread, and the chosen value is also the best on test (0.96).

**The opposite of section 06.** There every `k` sat inside the noise and
cross validation could not separate them; here it can. The same tool, two
different outcomes — which is why **you look at the spread every time**.

**A second knob: `min_samples_leaf`.** It says how many records a leaf must
hold at least. It blocks memorising without limiting depth: if a leaf must
hold at least 5 records, no branch can form around a single one.

## Feature importance

A tree can say how much each column earned its keep:

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(value, 3))
```

```
age      0.169
income   0.398
visits   0.433
```

These numbers say how much the splits made on that column reduced impurity,
and they add up to 1.

**But they have three traps:**

**1. Importance is not causation.** The rule from earlier modules holds
here. "The most important variable is `visits`" does not mean raising the
visit count keeps the customer.

**2. Correlated columns share importance.** If two columns are nearly the
same, the tree picks one and the other gets near-zero importance. The
conclusion "this column is useless" gets drawn — when only its twin was
chosen.

**3. High-cardinality columns get inflated.** A continuous numeric column
offers thousands of possible thresholds; a categorical one offers a few. The
tree is luckier at finding a good split by chance in the first, and its
importance comes out higher than it should.

The extreme case of the third trap: put a **customer id** in the data and
the tree can separate every record with it, making that column look the most
important of all.

## A tree's real weakness: instability

Remove a few rows from the data and retrain, and you can get an **entirely
different tree**. Even the root split can change.

The cause is greediness: the first split decides a threshold by a hair, and
when that decision flips, everything beneath it changes. A small change in
the data reshapes the whole tree.

**This lowers a single tree's reliability.** Today the model says "the most
important column is `visits`"; ten rows later it can say "the most important
column is `income`".

The fix is in the next section: **build many trees and average them.**
Random forests and gradient boosting do exactly that, turning the
instability from a disadvantage into an advantage.

## Tree or KNN

Three models' results on the same data:

```
baseline               0.70
decision tree (d=3)    0.80
KNN (k=25, scaled)     0.92
```

**On this data KNN wins.** The tree beats the baseline but falls behind KNN.

That does not mean trees are bad — it depends on the data. Trees work with
stepped rules; when the boundary is smooth and curved they have to imitate
it in steps. We saw the same in section 05: on the car data the tree's error
was 64 and linear regression's 16.5.

**Choosing a model is a matter of measurement.** Which one wins depends on
the shape of the data, and there is no way to know in advance.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>When a tree is good</h4>
      <p>Rules are sharp and stepped<br>Many categorical columns<br>Interpretability matters<br>Scaling is not possible</p>
    </div>
    <div class="versus-side">
      <h4>When KNN is good</h4>
      <p>Boundaries are smooth and curved<br>Few numeric features<br>Local similarity is meaningful<br>The data is small</p>
    </div>
  </div>
  <figcaption>Neither assumes anything about the shape of the boundary, but they capture different shapes with different ease.</figcaption>
</figure>

## A tree's advantages

| Advantage | Why |
|---|---|
| No scaling needed | It looks at ordering, not distance |
| Robust to outliers | An extreme value is merely "above the threshold" |
| Readable | The rules turn into sentences |
| Categorical and numeric together | Both can live in the same tree |
| Captures interactions | Combined rules like "young **and** rarely visiting" come naturally |

The last row matters: linear regression gives each column its own
coefficient, and what happens when "being young" meets "visiting rarely" has
to be stated separately. A tree builds that by itself, because its branches
are already nested conditions.

## What we skipped in this section

- **Pruning.** With the `ccp_alpha` parameter the tree is grown first and
  its useless branches cut afterwards; a more flexible route than limiting
  depth.
- **Regression trees.** `DecisionTreeRegressor` works on the same logic,
  except a leaf holds a **mean** instead of a class and variance is reduced
  instead of impurity.
- **Handling categorical columns directly.** sklearn still wants them
  encoded; some libraries (LightGBM among them) take categories as they are.

The next section solves this section's weakness: a single tree's instability
disappears in the average of **many trees**.
