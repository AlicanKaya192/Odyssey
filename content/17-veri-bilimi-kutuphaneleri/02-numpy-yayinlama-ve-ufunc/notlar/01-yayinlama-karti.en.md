## The rule

Shapes are compared **from the right**; on every axis the sizes are **equal**
or one of them is **1**. A missing axis is added at the front as 1.

| A | B | Result |
|---|---|---|
| `(3, 4)` | `(4,)` | `(3, 4)` |
| `(3, 4)` | `(3,)` | **error** |
| `(3, 4)` | `(3, 1)` | `(3, 4)` |
| `(3, 1)` | `(1, 4)` | `(3, 4)` |
| `(5, 1, 2)` | `(1, 3, 2)` | `(5, 3, 2)` |

## Patterns

| Task | Code |
|---|---|
| Centring by column | `X - X.mean(axis=0)` |
| A ratio by row | `X / X.sum(axis=1, keepdims=True)` |
| A column vector | `v[:, np.newaxis]` or `v.reshape(-1, 1)` |
| Every pair | `a[:, None] - b[None, :]` |
| Seeing the shape in advance | `np.broadcast_shapes(s1, s2)` |

## ufuncs

| Code | What it does |
|---|---|
| `np.add.reduce(a)` | the sum (the same as `sum`) |
| `np.add.accumulate(a)` | the cumulative sum |
| `np.multiply.outer(a, b)` | the product of every pair |
| `np.maximum(a, b)` | the larger one, item by item |
| `f(a, out=b)` | write the result into an existing array |
| `f(a, where=mask, out=...)` | compute only within the mask |
| `np.vectorize(f)` | convenience; no speed gain |
