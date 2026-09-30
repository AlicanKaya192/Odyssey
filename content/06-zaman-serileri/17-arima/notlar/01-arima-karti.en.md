## Setting up

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(
    train,
    order=(p, d, q),
    seasonal_order=(P, D, Q, m),     # omitted when there is no season
).fit()
```

`train` must carry a regularly spaced date index (`asfreq`); then `forecast`
produces the dates itself.

## The result object

| Attribute | Content |
|---|---|
| `fit.params` | The coefficients: `const`, `ar.L1`, `ma.L1`, `ar.S.L12`, `ma.S.L12`, `sigma2` |
| `fit.pvalues` | The p-value of each coefficient |
| `fit.summary()` | The whole table; `.tables[1]` for the coefficients only |
| `fit.aic`, `fit.bic` | Information criteria; smaller is better |
| `fit.resid` | One-step residuals on the training data |
| `fit.fittedvalues` | One-step forecasts on the training data |
| `fit.forecast(h)` | The next `h` steps |
| `fit.get_forecast(h)` | Forecast + interval: `.predicted_mean`, `.conf_int()` (Section 20) |

## Familiar faces

Most of the methods you have seen so far are special cases of the ARIMA
family:

| ARIMA | The same thing as |
|---|---|
| (0,0,0) | White noise; the forecast is the mean |
| (0,1,0) | A random walk; the forecast is naive |
| (0,1,0) + constant | Drift |
| (0,1,1) | Simple exponential smoothing |
| (0,2,2) | Holt (additive trend) |
| (0,0,0)(0,1,0)ₘ | Seasonal naive |
| (0,1,1)(0,1,1)ₘ | Very close to additive Holt–Winters |
| (1,0,0) | AR(1): a series returning to its mean |

In simple exponential smoothing `α = 1 + θ`: if the MA coefficient is −0.8
then `α = 0.2`.

## Reading the coefficients

| Coefficient | Meaning |
|---|---|
| `ar.L1 = 0.7` | 70% of today's deviation carries over to tomorrow |
| `ar.L1` ≈ 1 | Almost a random walk; raise `d` by one |
| `ar.L1 < 0` | The series goes up and down in turn |
| `ma.L1 = −0.8`, `d = 1` | 20% of a surprise is lasting; the level adapts slowly |
| `ma.L1` ≈ −1 | Differenced too much; lower `d` by one |
| `ma.S.L12 = −0.9`, `D = 1` | The seasonal pattern is very stable |
| `ar.L1` and `ma.L1` close, opposite in sign | They cancel; remove both |

## The shape of the forecast

| Model | The forecast at a long horizon |
|---|---|
| `d = 0`, with a constant | Returns to the mean |
| `d = 1`, no constant | Flat: stays at the last level |
| `d = 1`, with a constant | A line: goes on at a fixed slope |
| `d = 2` | A line: goes on at the last slope |
| `D = 1` | Repeats the pattern of the last season |
| `d = 1`, `D = 1` | Pattern + last level; carries a trend |

At a long horizon the forecast is decided not by the AR and MA terms but by
**the differencing and the constant**. AR and MA shape only the first few
steps.

## Constant and trend

```python
ARIMA(train, order=(1, 0, 0))                # d = 0: a constant is there by default
ARIMA(train, order=(0, 1, 1), trend="t")     # d = 1: drift (a linear trend)
ARIMA(train, order=(1, 0, 0), trend="n")     # no constant
```

With `d ≥ 1` no constant is added by default; if a trend is wanted,
`trend="t"`.

## A multiplicative series

```python
import numpy as np

fit = ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
forecast = np.exp(fit.forecast(12))
```

Error measures are computed on the **back-transformed** forecast, not on the
logarithm. The AICs of models with and without the logarithm cannot be
compared (different data).

## Speed

| Case | What to do |
|---|---|
| A long season (`m = 365`) | ARIMA is not suitable; Fourier terms (Section 18) |
| Many rolling origins | A small order; if needed the last `n` observations via `train.iloc[-n:]` |
| Large `p`, `q` | Slow and unnecessary; keep them below 2 |

On a daily series of a thousand observations with `m = 7`, a small seasonal
model fits in under half a second.

## `ARIMA` and `SARIMAX`

`statsmodels.tsa.statespace.sarimax.SARIMAX` is the older, more detailed
interface to the same model. You will see it in other sources; `order` and
`seasonal_order` mean the same. External variables (`exog`) exist in both.
