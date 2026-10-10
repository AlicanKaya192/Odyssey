The prices of three products over three days sit in a matrix: rows are days,
columns products. With broadcasting, every calculation is one line:

```python
import numpy as np

prices = np.array([[100, 50, 20], [110, 45, 22], [121, 54, 21]], dtype=float)
change = (prices[1:] / prices[:-1] - 1) * 100
print(change.round(1).tolist())
low, high = prices.min(axis=0), prices.max(axis=0)
print(((prices - low) / (high - low)).round(2).tolist())
weights = np.array([0.5, 0.3, 0.2])
print((prices * weights).sum(axis=1).tolist(), (prices @ weights).tolist())
share = prices / prices.sum(axis=1, keepdims=True)
print(share.sum(axis=1).round(10).tolist())
```

```text
[[10.0, -10.0, 10.0], [10.0, 20.0, -4.5]]
[[0.0, 0.56, 0.0], [0.48, 0.0, 1.0], [1.0, 1.0, 0.5]]
[69.0, 72.9, 80.9] [69.0, 72.9, 80.9]
[1.0, 1.0, 1.0]
```

## Line by line

| Calculation | How it spread |
|---|---|
| Daily percentage change | `prices[1:]` / `prices[:-1]`: the same shape, shifted by a day |
| Min-max scaling (0–1) | `(3, 3)` − `(3,)`: each column's minimum from every row |
| Weighted basket value | `(3, 3)` × `(3,)`, then the row sum; or the matrix product `@` |
| Share within the day | the row total as `(3, 1)` with `keepdims=True`; each row's shares add up to 1 |

## Two ways, the same result

`(prices * weights).sum(axis=1)` and `prices @ weights` gave the same numbers.
The first is broadcasting + a sum, the second a matrix-vector product. For
big matrices `@` is faster (it goes to a linear algebra library) and states
the intent more clearly: "each row's dot product with the weights". The
matrix product is the subject of the next section (linalg).

## Watch out

- The percentage change has no value for the first day: the result has 2
  rows.
- In min-max scaling, if a column is constant (`high == low`) it divides by
  zero; guard it with `np.where(high > low, ..., 0)`.
