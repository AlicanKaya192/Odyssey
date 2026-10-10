## numpy.random

| Code | Gives |
|---|---|
| `rng = np.random.default_rng(42)` | a seeded generator |
| `rng.integers(1, 7, size=5)` | integers 1–6 (the stop excluded) |
| `rng.random(3)` | 0–1 decimals |
| `rng.normal(mean, sd, count)` | a normal distribution |
| `rng.choice(a, size=, p=, replace=)` | picking |
| `rng.permutation(x)` | a shuffled copy |
| `rng.shuffle(x)` | shuffles `x` in place |
| `rng.spawn(n)` | n independent generators |

## numpy.linalg

| Code | What it does |
|---|---|
| `A @ B` | the matrix product (`*` is item by item) |
| `np.linalg.solve(A, b)` | `A x = b` |
| `np.linalg.inv(A)` | the inverse (`solve` unless needed) |
| `np.linalg.det(A)` | the determinant |
| `np.linalg.matrix_rank(A)` | the rank |
| `np.linalg.cond(A)` | the condition number (danger if large) |
| `np.linalg.norm(v)` | the length |
| `np.linalg.eigh(A)` / `eigvalsh` | eigenvalues/vectors of a symmetric matrix |
| `np.linalg.lstsq(X, y, rcond=None)` | least squares |

## Errors

| Symptom | Cause |
|---|---|
| Different numbers on every run | no seed |
| Another call shifted the sequence | the global `np.random.seed` |
| `LinAlgError: Singular matrix` | rows are multiples of each other |
| A meaninglessly large result | almost singular (large `cond`) |
| An unexpected matrix shape | `@` was needed instead of `*` |
