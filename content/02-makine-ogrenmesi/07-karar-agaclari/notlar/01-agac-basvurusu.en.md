## Building it

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model = DecisionTreeRegressor(max_depth=3, random_state=42)
```

| Parameter | What it does | Default |
|---|---|---|
| `max_depth` | How many questions deep it may go | `None` (unlimited) |
| `min_samples_leaf` | The fewest records a leaf may hold | 1 |
| `min_samples_split` | The fewest records needed to split | 2 |
| `max_features` | How many features to try per split | All |
| `criterion` | `gini` / `entropy` (classification), `squared_error` (regression) | `gini` |
| `ccp_alpha` | Pruning strength; larger shrinks the tree | 0.0 |
| `class_weight` | Weights for the classes on imbalanced data | `None` |

**Why `random_state` is needed:** when two splits are equally good the tree
picks between them at random. Without it you can get a different tree on
every run.

## Reading a tree

**As text:**

```python
from sklearn.tree import export_text
print(export_text(model, feature_names=list(X.columns)))
```

**As a drawing:**

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11, 5))
plot_tree(model, feature_names=list(X.columns),
          class_names=["stays", "leaves"],
          filled=True, rounded=True, fontsize=9, ax=ax)
fig.savefig("chart.png")
```

Each box has four lines:

| Line | What it means |
|---|---|
| `visits <= 18.5` | This node's question (absent in leaves) |
| `gini = 0.425` | Impurity: 0 pure, 0.5 the most mixed |
| `samples = 150` | How many records reached this node |
| `value = [104, 46]` | The breakdown by class |
| `class = stays` | The majority class — the prediction, if it is a leaf |

## Reaching into the tree's structure

```python
print(model.get_depth())              # the actual depth
print(model.get_n_leaves())           # the number of leaves
print(X.columns[model.tree_.feature[0]])          # the root split's feature
print(round(model.tree_.threshold[0], 2))         # the root split's threshold
```

The `tree_.feature` and `tree_.threshold` arrays follow node order; the first
element is always the root.

## Feature importance

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(float(value), 3))
```

They add up to 1 and say how much the splits made on that column reduced
impurity.

**Three traps:**

| Trap | The consequence |
|---|---|
| Importance is not causation | "The most important column" does not show it is the cause |
| Correlated columns | One gets chosen, its twin gets near-zero importance |
| High-cardinality columns | Continuous numeric columns inflate; an id column climbs to the top |

A more reliable method is `permutation_importance`: it shuffles one column
and sees how far the score falls.

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10,
                                random_state=42)
```

## Limiting complexity

| Route | How it works |
|---|---|
| `max_depth` | Crude but clear; limits how many questions get asked |
| `min_samples_leaf` | A floor on the records in a leaf; blocks memorising a single record |
| `min_samples_split` | Stops small nodes from splitting |
| `ccp_alpha` | Grows the tree then cuts it back; the most flexible route |

```python
DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, random_state=42)
```

Using two together is common: the depth sets an upper bound and
`min_samples_leaf` stops deep branches from narrowing to a single record.

## No scaling needed

A tree asks `income <= 137500`. After scaling that becomes
`income_scaled <= 0.42` — **the threshold changes, the ordering does not.**

The measured result: unscaled 0.80, scaled 0.80. Identical.

For the same reason:

- Outliers do not upset a tree (an extreme value is merely "above the
  threshold").
- The columns' units can be a mixture (years, currency, counts).
- Transforms like a logarithm change nothing.

**Categorical columns still have to be encoded:** sklearn's tree does not
work with text, so `pd.get_dummies` is needed.

## Regression trees

```python
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor(max_depth=3, random_state=42)
```

The same logic, with two differences:

- **Variance** is reduced instead of impurity (`criterion="squared_error"`).
- A leaf holds the **mean** of the records in that group instead of a class.

This has a consequence: a regression tree produces **stepped** predictions.
Every record landing in a leaf gets the same number, so it cannot draw a
continuous curve.

It was measured in section 05: on the car data the tree's MAE was 64 and
linear regression's 16.5. That is exactly why — imitating a linear
relationship in steps is expensive.

## Common mistakes

- **Not limiting the depth.** The default is `None`; the tree memorises the
  training data.
- **Choosing the depth from the test table.** Cross validation is needed.
- **Not passing `random_state`.** There is randomness in equal splits.
- **Taking feature importance for causation.** The most common and most
  expensive interpretation mistake.
- **Leaving an id/number column in the data.** The tree can separate every
  record with it.
- **Spending time on scaling.** It does no harm and no good.
- **Trusting a single tree.** Change a few rows and the tree changes;
  ensemble methods exist for this.
