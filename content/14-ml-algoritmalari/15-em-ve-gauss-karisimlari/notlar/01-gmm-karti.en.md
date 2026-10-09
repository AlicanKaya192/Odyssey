## The model

Density: `p(x) = Σⱼ πⱼ · N(x; μⱼ, Σⱼ)`, the shares `πⱼ` sum to 1.

## EM steps

| Step | What is computed |
|---|---|
| E | `rᵢⱼ = πⱼ N(xᵢ; μⱼ, Σⱼ) / Σₗ πₗ N(xᵢ; μₗ, Σₗ)` |
| M | `Nⱼ = Σᵢ rᵢⱼ`, `πⱼ = Nⱼ / n` |
| M | `μⱼ = Σᵢ rᵢⱼ xᵢ / Nⱼ` |
| M | `Σⱼ = Σᵢ rᵢⱼ (xᵢ − μⱼ)(xᵢ − μⱼ)ᵀ / Nⱼ` |

The log-likelihood `Σᵢ ln p(xᵢ)` never decreases in a round; stop when the
increase becomes very small.

## Covariance types (`covariance_type`)

| Type | Shape | Parameters |
|---|---|---|
| `spherical` | round, one variance per component | fewest |
| `diag` | ellipse parallel to the axes | medium |
| `tied` | all components the same ellipse | medium |
| `full` | each component its own tilted ellipse | most |

## Compared with k-Means

| | k-Means | GMM |
|---|---|---|
| Assignment | hard (one cluster) | soft (probability) |
| Cluster shape | round | ellipse (`full`) |
| Measure | inertia | log-likelihood, BIC |
| Speed | fast | slower |

k-Means can be thought of as the hard-assignment version of a GMM whose
variances are all equal and very small.

## Common mistakes

- Choosing the number of components by log-likelihood: the largest `k`
  always wins; use BIC or AIC.
- A single start: EM gets stuck in a local optimum (`n_init`).
- A component collapsing onto one point: its variance goes to zero and the
  likelihood to infinity; scikit-learn adds a small `reg_covar` to the
  diagonal.
- Not scaling: different units distort the covariance too.
