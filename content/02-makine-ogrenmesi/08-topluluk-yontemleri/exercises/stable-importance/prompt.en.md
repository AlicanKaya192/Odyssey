In section 07 the tree gave `age` an importance of **0.0**, and we talked
about why concluding "this column is useless" would be wrong. Now you will
see what the forest says.

**What you need to do:**

1. Prepare and split the data.
2. Train two models: `tree` (`max_depth=2`) and `forest` (200 trees), both
   with `random_state=42`.
3. Print one line each: **the name and the three importance values** side by
   side (in column order `age`, `income`, `visits`; three decimals).
4. On the last line print how many columns got **exactly zero** importance,
   side by side: the tree's count first, then the forest's.

**Expected output:**

```
tree 0.0 0.454 0.546
forest 0.232 0.344 0.424
1 0
```

**The tree says 0.0 for `age`; the forest says 0.232.**

The tree is not wrong: a tree of depth 2 has only three splits, and `visits`
and `income` won earlier. `age` was never even tried.

**The forest has 200 trees** and each tries only a subset of the features at
every split (`max_features`). That means `age` competes **on its own** many
times — when `visits` is hidden for that split, its turn comes. Its real
contribution surfaces that way.

**The last line sums it up: one zero column in the tree, none in the
forest.**

**The lesson:** a single tree saying "this column does not matter" cannot be
trusted. Zero importance can mean "its turn never came" rather than "it
contributes nothing".

**But the three traps still stand:**

1. Importance is not **causation** — a forest does not change that.
2. Correlated columns still share importance.
3. High-cardinality columns still inflate.

The more reliable route is again `permutation_importance`: it shuffles a
column, sees how far the score falls, and can be measured on the test set.
