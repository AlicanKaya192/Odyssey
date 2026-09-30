## The recipe

1. **Plot.** Trend, season, growing waves, outlier days, level shifts.
2. **Transform.** The logarithm if the waves grow. Repair outlier days
   (Section 13).
3. **Difference.** With a season, `D = 1`; if a drift remains, `d = 1`. If the
   standard deviation rose, undo it (Section 11).
4. **ACF and PACF.** On the differenced series (Section 12).
5. **Candidates.** Two or three small models.
6. **AIC.** The smallest; among close ones, the one with fewest coefficients.
7. **Residual.** Ljung–Box, the ACF, the biggest misses.
8. **Test.** A rolling origin; against the baseline and the other models.

## From ACF and PACF to a candidate

In the correlogram of the differenced series:

| What you see | Candidate |
|---|---|
| The PACF cuts off after 1, the ACF decays | `p = 1` |
| The PACF cuts off after 2 | `p = 2` |
| The ACF cuts off after 1, the PACF decays | `q = 1` |
| Both decay | `p = 1`, `q = 1` |
| Both in the band | `p = 0`, `q = 0` |
| Only a negative bar at `m` in the ACF | `Q = 1` |
| Decaying bars at `m`, `2m`, `3m` in the ACF; only at `m` in the PACF | `P = 1` |
| Around −0.5 at lag 1, after `d = 1` | `q = 1` (or over-differencing) |

After a seasonal difference the commonest outcome is `Q = 1`, `P = 0`.

## A small search

Instead of writing the candidates by hand, a small grid:

```python
import itertools
import warnings

warnings.simplefilter("ignore")

rows = []
for p, q in itertools.product(range(3), range(3)):
    fit = ARIMA(train, order=(p, 1, q), seasonal_order=(0, 1, 1, 7)).fit()
    rows.append({"order": (p, 1, q), "aic": fit.aic, "terms": p + q})

table = pd.DataFrame(rows).sort_values("aic")
print(table.head(5))
```

- `d` and `D` do **not** go into the grid: the AIC cannot be compared across
  different differencing.
- The AICs of the best few rows are very close (under 2 points): choose the
  one with **fewest terms** among them.
- The grid is a first screening. The final decision is in the residual and on
  the rolling origin.

## AIC and BIC

| | AIC | BIC |
|---|---|---|
| Penalty | 2 per coefficient | `ln(n)` per coefficient |
| Tendency | Slightly larger models | Small models |
| When | When the aim is forecasting | When the aim is finding the "true" structure |

Both are **relative**: a single AIC value tells you nothing. It can be
negative; the smaller (more negative) one is better.

How big should the difference be?

| Difference in AIC | Reading |
|---|---|
| 0–2 | Indistinguishable; choose the simpler |
| 2–10 | The smaller is better, but not certain |
| More than 10 | A clear difference |

## Checking the residual

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

skip = d + D * m                       # the start-up effect
resid = fit.resid.iloc[skip:]

print(round(resid.mean(), 2))
print(acf(resid, nlags=2 * m).round(2).tolist()[1:])
print(acorr_ljungbox(resid, lags=[2 * m], model_df=p + q + P + Q))
```

- **Drop the first values.** In a model that differences, the first
  `d + D × m` residuals come from the start-up of the model and are very
  large; they spoil the test.
- **`model_df`:** the number of coefficients of the model. The test corrects
  its degrees of freedom accordingly.
- **p > 0.05:** no memory left.

| In the residual | What to do |
|---|---|
| Lag 1 outside the band | Raise `p` or `q` by one |
| Lag `m` outside the band | Raise `P` or `Q` by one |
| Slowly decaying positive bars | Raise `d` |
| The width grows over time | The logarithm |
| A few giant values | Outlier days; Section 13 |
| Misses always on the same dates | The calendar; Section 18 |

## Signs of too much model

- The p-value of a coefficient is above 0.05.
- The AR and MA coefficients are close and opposite in sign.
- A coefficient is stuck at ±1.
- Adding a term lowers the AIC by less than 2.
- Warnings: failed to converge, non-invertible starting values.
- The training error falls while the rolling-origin error rises.

If you see one, **remove** a term and look again.

## When the AIC and the test error disagree

It happens; like the (1,0,0)(0,1,1)₇ example in the lesson. Three possible
reasons:

1. **The model is set up wrongly** yet fits well one step ahead (the needed
   difference was not taken, say). The residual test catches this.
2. **A difference in horizon.** The AIC measures the one-step fit; you are
   using 28 steps ahead. At a long horizon the effect of the differencing and
   the constant grows.
3. **Chance.** A single split. Look at the rolling origin.

The rule: the AIC **weeds out**, the rolling origin **chooses**.
