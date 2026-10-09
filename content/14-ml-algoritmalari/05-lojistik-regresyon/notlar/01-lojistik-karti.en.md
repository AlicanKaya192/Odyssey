## Formulas

| What | Formula |
|---|---|
| Sigmoid | `σ(z) = 1 / (1 + e⁻ᶻ)` |
| Probability | `p = σ(A w)` |
| Log loss | `−mean(y log p + (1 − y) log(1 − p))` |
| Gradient | `Aᵀ (p − y) / n` |
| Decision | 1 if `p ≥ threshold` |
| Softmax | `pₖ = e^(zₖ) / Σ e^(zⱼ)` |

## Interpreting a weight

`wᵢ` is how much the **log-odds** (`log(p / (1 − p))`) grows when `xᵢ` goes up by
one unit. `e^(wᵢ)` is the odds ratio: if `wᵢ = 0.7`, `e^0.7 ≈ 2`, so the odds
double. If the features were standardised, the weights can be compared with
each other.

## With scikit-learn

- `LogisticRegression()` regularises by default (`C=1`); for an unregularised
  comparison use `C=np.inf`.
- `predict_proba(X)[:, 1]` is the probability of class 1; `predict` uses a
  threshold of 0.5.
- With several classes softmax (multinomial) is used.

## Common mistakes

- `np.log(0)`: if a probability is exactly 0 or 1 the loss is infinite; in
  practice `np.clip(p, 1e-12, 1 - 1e-12)`.
- For a large negative `z`, `np.exp(-z)` overflows; it warns but the sigmoid
  still goes to 0. In softmax, subtract the largest.
- If a perfect line separates the classes, unregularised weights grow without
  limit; gradient descent never stops.
