## Methods

| Method | Prediction | Strength | Weakness |
|---|---|---|---|
| Global mean | `μ` | simple | no personalisation |
| Bias baseline | `μ + b_u + b_i` | fast, robust | blind to taste |
| User-based CF | deviations of similar users | explainable ("people like you") | slow with many users |
| Item-based CF | your ratings of similar items | items change little, precomputed | new items |
| Matrix factorisation | `μ + b_u + b_i + p_u · q_i` | most accurate, scales | hidden dimensions are not interpretable |
| Content-based | the item's features (genre, author) | new items can be recommended | recommends more of the same |

## Measures

| Measure | What it measures |
|---|---|
| RMSE | the error of rating prediction |
| precision@k | how many of the `k` recommended items hit |
| recall@k | how many of the relevant items were recommended |
| Coverage | how much of the catalogue was ever recommended |

## The matrix factorisation step (one rating)

- `err = r − (μ + b_u + b_i + p_u · q_i)`
- `b_u += lr (err − λ b_u)`, `b_i += lr (err − λ b_i)`
- `p_u += lr (err q_i − λ p_u)`, `q_i += lr (err p_u − λ q_i)` (both with
  the old values)

## Common mistakes

- Taking empty cells for a rating of 0: missing data is not "disliked".
- Adding test ratings to training before measuring (leakage).
- Looking only at RMSE: users see the list, not the error.
- Piling everything onto popular items: personalisation and diversity are
  lost.
