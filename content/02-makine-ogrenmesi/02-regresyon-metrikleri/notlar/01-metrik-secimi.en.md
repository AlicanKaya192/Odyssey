Which measure to use when comes down to a single question: **in this
problem, is one large error more expensive than the sum of several small
ones?**

## A comparison

| Measure | Unit | Reaction to large errors | To outliers | Readability |
|---|---|---|---|---|
| MAE | The target's unit | Proportional | Robust | High |
| MSE | The unit squared | Disproportionate (squared) | Sensitive | Low |
| RMSE | The target's unit | Disproportionate (squared) | Sensitive | Medium |
| R² | None | Disproportionate (square-based) | Sensitive | Medium |
| MAPE | Percentage | Proportional | Robust | High |

## Questions that decide it

**1. Is one large error a disaster?**

- Yes → **RMSE**. Flight times, drug dosages, critical stock levels.
- No → **MAE**. Total cost, average daily sales.

**2. Will you explain the result to someone non-technical?**

- Yes → **MAE** or **MAPE**. "We are off by 18 thousand on average."
- No → R² can be added as well.

**3. Will you compare two different problems?**

- Yes → **R²**. Being unitless, it is the only comparable measure.
- No → Measures with units are more informative.

**4. Does the target contain zeros or near-zeros?**

- Yes → **Do not use MAPE.** The division blows up or the percentage flies
  off.
- No → MAPE is an option.

**5. Does the target's scale vary a lot between records?**
(some are 10 units, others 10,000)

- Yes → **MAPE** or a logarithmic transform. MAE gets swamped by the errors
  on the large records.
- No → MAE / RMSE are enough.

## The code

```python
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score,
)

mae = mean_absolute_error(y_test, prediction)
mse = mean_squared_error(y_test, prediction)
rmse = mse ** 0.5
mape = mean_absolute_percentage_error(y_test, prediction)
r2 = r2_score(y_test, prediction)
```

`mean_absolute_percentage_error` returns a **ratio** (0.08), not a
percentage. Multiply by 100 to get percent.

## Computing them by hand

Knowing the formulas pays off more than knowing the error messages.

```python
errors = [a - p for a, p in zip(actual, predicted)]
n = len(errors)

mae = sum(abs(e) for e in errors) / n
mse = sum(e ** 2 for e in errors) / n
rmse = mse ** 0.5

mean = sum(actual) / n
ss_res = sum(e ** 2 for e in errors)
ss_tot = sum((a - mean) ** 2 for a in actual)
r2 = 1 - ss_res / ss_tot
```

`ss_res` is the model's error and `ss_tot` the baseline's. R² comes from the
ratio between them — **the baseline is built into the measure.**

## The same result seen four ways

The four numbers below describe the same predictions from the same model:

```
MAE   18.50
RMSE  22.86
R²     0.943
MAPE   0.063
```

None is more "correct" than the others. They answer different questions:

- MAE: how far off am I?
- RMSE: do I have any large errors?
- R²: where am I relative to the baseline?
- MAPE: how far off am I in proportion?

**RMSE is always greater than or equal to MAE.** A large gap between them
means there are a few large errors. That is the reason for writing both: the
gap itself carries information.

## Common mistakes

- **Taking `mean_squared_error` for RMSE.** sklearn returns the square; you
  take the root.
- **Reversing the arguments.** The order is always `(actual, predicted)`.
  MAE forgives it, R² does not.
- **Comparing numbers from different test sets.** Two models' MAEs are
  comparable only if they were measured **on the same split**.
- **Using a regression measure for classification.** With a categorical
  target MAE is meaningless; accuracy, precision and recall belong there.
