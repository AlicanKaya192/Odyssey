## Settings

| Setting | What it changes | scikit-learn |
|---|---|---|
| `k` | small: complex boundary; large: flat boundary | `n_neighbors` |
| Weight | equal votes or `1 / distance` | `weights="uniform"` / `"distance"` |
| Distance | Euclidean, Manhattan, cosine… | `metric` |
| Search structure | brute force, KD-tree, ball tree | `algorithm` |

## Cost

- Training: none (storing the data).
- Prediction: `O(n · d)` per query with brute force; a KD-tree speeds it up in
  low dimensions, its benefit fades in high dimensions.
- Memory: all the training data.

## When good, when bad?

- Good: few dimensions, data with local structure, problems with irregular
  boundaries, a quick baseline.
- Bad: many dimensions (the curse of dimensionality), very large data (slow
  prediction), features on mixed scales (standardise first).

## Common mistakes

- Forgetting to standardise: the feature with the large unit rules the
  distance.
- Choosing `k` by training accuracy: `k = 1` always looks perfect.
- An even `k` with two classes: votes can tie; an odd number reduces ties.
