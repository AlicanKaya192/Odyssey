## Formulas

| What | Formula |
|---|---|
| Score | `f(x) = w·x + b`, class `sign(f(x))` |
| Hinge loss | `max(0, 1 − y f(x))`, `y ∈ {−1, +1}` |
| Objective | `λ/2 ‖w‖² + mean(hinge)` or `½‖w‖² + C Σ hinge` |
| Link | `C = 1 / (λ n)` |
| Margin width | `2 / ‖w‖` |

## Kernels

| Kernel | `K(a, b)` | Boundary |
|---|---|---|
| Linear | `a·b` | flat |
| Polynomial | `(a·b + 1)ᵈ` | a degree-`d` curve |
| RBF (Gaussian) | `exp(−γ ‖a − b‖²)` | flexible, local |

If `γ` is large, each point affects only its very close neighbourhood (a complex
boundary, a risk of overfitting); if small, the boundary flattens.

## When?

- Medium-size data, many features (like text), a clear boundary.
- On very large data a kernel SVM is slow; a linear SVM (`LinearSVC`) or SGD is
  preferred.
- Probabilities do not come out naturally; `SVC(probability=True)` produces
  them with an extra calibration.

## Common mistakes

- Not scaling: distances and inner products slide towards the large-unit
  feature.
- Leaving labels as 0/1: the hinge loss needs `−1/+1`.
- Trying `C` and `γ` separately: they should be searched together (a grid).
