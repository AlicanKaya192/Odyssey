# numpy.random and linalg

Two jobs repeat all the time in data science: **producing random numbers**
(splitting data, simulations, initialising models) and **linear algebra**
(matrix products, solving equations, least squares). NumPy has two
submodules for them: `numpy.random` and `numpy.linalg`. This section covers
the right way to use both and their common mistakes. The mathematics itself
is in the Mathematics path; here is the code.

## Generator: reproducible randomness

```python
import numpy as np

rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))
print(rng.random(3).round(3), rng.normal(0, 1, 2).round(3))
first = np.random.default_rng(42).integers(1, 7, size=5)
again = np.random.default_rng(42).integers(1, 7, size=5)
print((first == again).all())
```

```text
[1 5 4 3 3]
[0.697 0.094 0.976] [ 0.128 -0.316]
True
```

- **`np.random.default_rng(seed)`** builds a **generator**. The numbers come
  from its methods: `integers` (the stop is not included: a 1–6 die),
  `random` (a 0–1 decimal), `normal(mean, deviation, count)`.
- The same seed → the same numbers. That is how an experiment or a data split
  can be repeated.
- The old style `np.random.seed(42)` + `np.random.rand()` uses a **global**
  state: a call elsewhere in the program shifts the sequence. In new code,
  each job uses its own generator (the same idea as `random.Random` in Python
  Beginner).

## Picking, shuffling, independent streams

```python
import numpy as np

rng = np.random.default_rng(0)
print(rng.choice(["a", "b", "c"], size=5, p=[0.6, 0.3, 0.1]))
print(rng.choice(10, size=4, replace=False))
rng = np.random.default_rng(0)
x = np.arange(6)
print(rng.permutation(x), x)
rng.shuffle(x)
print(x)
child1, child2 = np.random.default_rng(5).spawn(2)
print(child1.integers(100), child2.integers(100))
```

```text
['b' 'a' 'a' 'a' 'b']
[4 7 8 6]
[3 2 5 4 0 1] [0 1 2 3 4 5]
[4 5 1 2 0 3]
22 53
```

- **`choice(..., p=...)`** picks with probabilities; **`replace=False`** picks
  without repeats (no one is chosen twice).
- **`permutation(x)`** returns a shuffled **copy** and does not touch `x`;
  **`shuffle(x)`** shuffles `x` **itself**.
- **`spawn(n)`** derives n generators independent of each other: each
  parallel job gets its own stream, with no overlap.

## Matrix products and solving equations

```python
import numpy as np

A = np.array([[2.0, 1], [1, 3]])
b = np.array([3.0, 5])
print(A @ np.array([1, 2]), A * np.array([1, 2]))
x = np.linalg.solve(A, b)
print(x.round(3), np.allclose(A @ x, b))
print(np.linalg.inv(A).round(3).tolist(), round(float(np.linalg.det(A)), 6))
```

```text
[4. 7.] [[2. 2.]
 [1. 6.]]
[0.8 1.4] True
[[0.6, -0.2], [-0.2, 0.4]] 5.0
```

- **`@`** is the matrix product (`np.matmul`): `[2·1 + 1·2, 1·1 + 3·2] = [4, 7]`.
  **`*`** multiplies item by item: it spread the vector over each row and
  gave a 2 × 2 matrix. Very different results; mixing them up is a silent
  error.
- **`np.linalg.solve(A, b)`** solves the equation `A x = b`: `2x + y = 3`,
  `x + 3y = 5` → `x = 0.8`, `y = 1.4`. Checked with `np.allclose`.
- `np.linalg.inv(A) @ b` gives the same result but is **slower and less
  accurate**; unless the inverse is explicitly needed, `solve` is used.
- If `det` is zero (or very small), the matrix has no inverse.

## Singular matrices and the condition number

```python
import numpy as np

S = np.array([[1.0, 2], [2, 4]])
try:
    np.linalg.solve(S, [1, 2])
except np.linalg.LinAlgError as error:
    print("LinAlgError:", error)
print(np.linalg.matrix_rank(S))
A = np.array([[2.0, 1], [1, 3]])
almost = np.array([[1, 1], [1, 1.0001]])
print(round(float(np.linalg.cond(A)), 3), np.linalg.cond(almost) > 1e4)
```

```text
LinAlgError: Singular matrix
1
2.618 True
```

- The second row of `S` is twice the first: the equations say the same thing
  and there is no single solution. NumPy raises **`LinAlgError: Singular
  matrix`**; the rank is 1.
- Sneakier is an **almost** singular matrix: no error, but the result is very
  sensitive to small changes in the input. **`np.linalg.cond`** (the condition
  number) measures this: 2.6 is healthy, above 10,000 is dangerous. Two very
  similar features in a regression (multicollinearity) are exactly this.

## Length, eigenvalues, least squares

```python
import numpy as np

print(np.linalg.norm([3, 4]))
print(np.linalg.eigvalsh(np.array([[2.0, 1], [1, 2]])))
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]], dtype=float)
y = np.array([2.1, 3.9, 6.2, 7.8])
coef, residuals, rank, _ = np.linalg.lstsq(X, y, rcond=None)
print(coef.round(3), rank)
```

```text
5.0
[1. 3.]
[0.15 1.94] 2
```

- **`norm`** is the length of a vector (`√(3² + 4²) = 5`).
- **`eigvalsh`** gives the eigenvalues of a symmetric matrix (real numbers,
  sorted). For a general matrix, `eig`; for a symmetric matrix, `eigh` /
  `eigvalsh` is both faster and keeps the results out of the complex number
  type.
- **`lstsq(X, y)`** finds, when the equations have no exact solution (4
  points, 2 unknowns), the solution that makes the error smallest: least
  squares. With an `X` whose first column is 1, this is fitting a line:
  `y ≈ 0.15 + 1.94 x`. This is the inside of linear regression (with
  scikit-learn in the ML Libraries module).

## Summary

- `rng = np.random.default_rng(seed)`; `integers`, `random`, `normal`,
  `choice(p=, replace=)`, `permutation` (a copy) / `shuffle` (in place),
  `spawn`.
- Your own generator instead of the global `np.random.seed`.
- `@` is the matrix product, `*` item by item.
- `solve(A, b)` (better than taking the inverse), `inv`, `det`,
  `matrix_rank`.
- A singular matrix raises `LinAlgError`; `cond` tells you about an almost
  singular one.
- `norm`, `eigvalsh` for symmetric matrices, least squares with `lstsq`.
