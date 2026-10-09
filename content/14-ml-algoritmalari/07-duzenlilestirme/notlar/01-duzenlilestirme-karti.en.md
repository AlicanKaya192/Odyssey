## Three penalties

| Method | Penalty | Effect | scikit-learn |
|---|---|---|---|
| Ridge (L2) | `α Σ w²` | shrinks weights, does not zero them | `Ridge` |
| Lasso (L1) | <code>α Σ &#124;w&#124;</code> | sets some weights exactly to zero | `Lasso` |
| Elastic Net | a mix of both | selection + stability under collinearity | `ElasticNet` |

## The scale of `α` in scikit-learn

A setting with the same name is not on the same scale in every model:

- `Ridge`: `‖y − Xw‖² + α ‖w‖²` (the **sum** of errors).
- `Lasso`: `‖y − Xw‖² / (2n) + α ‖w‖₁` (half the **mean** of errors).
- `LogisticRegression`: `C = 1 / α`; a large `C` means little regularisation,
  `C=np.inf` none.

When writing from scratch and comparing, these scales must match; in the lesson
they did.

## Why standardise first?

The penalty is applied to all weights with the same factor. If a feature is
measured in millimetres instead of metres, its weight becomes a thousand times
smaller and the penalty barely affects it. Standardisation brings every feature
to the same scale.

## Common mistakes

- Penalising the intercept: the model cannot hit the mean. Centre first.
- Choosing `α` by the training error: it always comes out as `α = 0`.
- Taking Lasso's selected features as the certain truth: of two collinear
  features it can choose one almost at random.
