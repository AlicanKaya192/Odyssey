## Split measures

| Measure | Formula | Use |
|---|---|---|
| Gini | `1 − Σ pₖ²` | classification (scikit-learn's default) |
| Entropy | `−Σ pₖ log₂ pₖ` | classification (`criterion="entropy"`) |
| Squared errors | `Σ (y − ȳ)²` | regression |

## Settings (with scikit-learn's names)

| Setting | Effect |
|---|---|
| `max_depth` | at most how many questions; small → a simple tree |
| `min_samples_split` | the minimum samples to split a node |
| `min_samples_leaf` | the minimum samples in a leaf; stops leaves for noise |
| `ccp_alpha` | cost-complexity pruning: large → more pruning |

## Pluses and minuses

- Readable, needs no scaling or other transformation, learns non-linear
  boundaries and interactions by itself.
- Unstable: a small change in the data can grow a completely different tree;
  its boundaries are parallel to the axes; a deep tree overfits easily.

## Common mistakes

- Not limiting the depth: 100% in training, low on the test.
- Taking the tree's first chosen feature as "the most important cause": the
  greedy choice may use only one of several similar features.
- Expecting a smooth curve from a regression tree: the prediction is stepped.
