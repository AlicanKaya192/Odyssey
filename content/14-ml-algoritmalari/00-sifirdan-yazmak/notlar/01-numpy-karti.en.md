## Used most in this module

| Job | NumPy |
|---|---|
| Seeded generator | `rng = np.random.default_rng(0)` |
| Normal / uniform distribution | `rng.normal(mean, sd, size)`, `rng.uniform(a, b, size)` |
| Shape | `X.shape`, `X.ndim`, `len(X)` |
| Per column | `X.mean(axis=0)`, `X.std(axis=0)`, `X.sum(axis=0)` |
| Per row | `X.sum(axis=1)` |
| Matrix product | `X @ w`, `X.T @ X` |
| Selecting by condition | `X[y == 1]`, `np.where(c, a, b)` |
| Position of the largest | `np.argmax(v)`, `np.argsort(v)` |
| Counting | `np.bincount(y)`, `np.unique(y, return_counts=True)` |
| Comparing | `np.allclose(a, b)`, `(a == b).all()` |
| Rounding, to a list | `a.round(3)`, `a.tolist()` |

## The broadcasting rule

The shapes of two arrays are compared **from the end**; each dimension must be
equal or 1. `(200, 2) - (2,)` works (the vector goes to every row),
`(200, 2) - (200,)` does not; subtracting per row needs `(200, 1)`:
`v[:, None]` or `v.reshape(-1, 1)`.

## Common mistakes

- Mixing up `axis`: `axis=0` gives a result per column (length = number of
  features), `axis=1` per row (length = number of samples).
- `ddof`: NumPy and scikit-learn divide by `n` by default (`ddof=0`); pandas'
  `std()` divides by `n − 1` (`ddof=1`).
- Comparing floating-point numbers with `==`: use `np.allclose`.
- An unseeded generator: a different result on every run; the experiment cannot
  be repeated.
