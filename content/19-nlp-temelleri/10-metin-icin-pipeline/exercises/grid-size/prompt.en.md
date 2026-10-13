A parameter grid is a dictionary: the key is `step__parameter`, the value the
list of values to try.

- `count_fits(grid, folds)`: how many models are trained? The product of all
  the value counts × the number of folds (final refit excluded).
- `step_names(grid)`: the step names in the grid (the part before `__`),
  unique and sorted.

**Expected output:**

```
60
['model', 'tfidf']
```
