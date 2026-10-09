## Steps

| Step | Code |
|---|---|
| Centre | `Xc = X - X.mean(axis=0)` |
| Covariance | `C = Xc.T @ Xc / (n - 1)` |
| Eigenvectors | `vals, vecs = np.linalg.eigh(C)`, sort from large to small |
| Or SVD | `U, S, Vt = np.linalg.svd(Xc, full_matrices=False)`, variance `S**2 / (n - 1)` |
| Project | `Z = Xc @ vecs[:, :k]` |
| Rebuild | `X ≈ Z @ vecs[:, :k].T + mean` |

## scikit-learn

| Name | Meaning |
|---|---|
| `PCA(k)` | `k` components; `PCA(0.95)` the smallest `k` keeping 95% of the variance |
| `components_` | the components (one per row) |
| `explained_variance_` | each component's variance (eigenvalue) |
| `explained_variance_ratio_` | its share of the total variance |
| `transform` / `inverse_transform` | project / rebuild |

## When?

- Many related features: dimensionality reduction, noise reduction.
- Visualisation: reduce to 2 or 3 components and plot.
- Before a model: fewer features, faster training (accuracy may drop a bit).

## Common mistakes

- Not scaling: the feature with the large unit takes over the first
  component.
- Fitting PCA on all data and splitting afterwards: test information leaks;
  fit only on training data inside a `Pipeline`.
- Reading meaning into a component's sign: `v` and `−v` are the same axis.
- Expecting non-linear structure: PCA only finds linear directions.
- Taking high variance for "important": a direction unrelated to the target
  can also be very spread out.
