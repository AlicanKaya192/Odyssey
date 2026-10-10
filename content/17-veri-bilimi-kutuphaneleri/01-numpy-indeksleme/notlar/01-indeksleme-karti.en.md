## Selecting

| Code | Gives | View / copy |
|---|---|---|
| `m[i, j]` | one item | — |
| `m[i]`, `m[:, j]` | a row, a column | view |
| `m[1:, ::2]` | a slice | view |
| `m[[0, 2]]` | a list of rows | copy |
| `m[[0, 2], [1, 3]]` | the **pairs** (0,1) and (2,3) | copy |
| `m[np.ix_([0, 2], [1, 3])]` | a sub-matrix | copy |
| `m[m > 5]` | a mask, a flat array | copy |
| `m[..., 0]` | 0 on the last axis (Ellipsis) | view |

## Assignment

| Code | Result |
|---|---|
| `m[m > 5] = 0` | `m` changes |
| `m[[0, 1], 0] = 0` | `m` changes |
| `m[m > 5][0] = 0` | `m` does not change (written to a copy) |

## Conditions and positions

| Code | What it does |
|---|---|
| `(a > 0) & (a < 5)`, <code>&#124;</code>, `~` | combine masks (parentheses required) |
| `np.where(c, a, b)` | a value by condition |
| `np.where(c)[0]`, `np.nonzero(a)[0]` | positions |
| `np.argsort(a)`, `a.argmax(axis=...)` | the sorting order, where the largest is |
| `np.unique(a, return_counts=True)` | distinct values and their counts |
| `np.isin(a, list)` | is it in the list |
| `np.clip(a, low, high)` | clamp |
| `a[:, np.newaxis]` | a new axis |
