## Three tools

| | `seasonal_decompose` | `STL` | `MSTL` |
|---|---|---|---|
| Method | Moving average | LOESS (local smoothing) | STL applied in turn |
| Model | Additive or multiplicative | Additive only | Additive only |
| Trend at the ends | `NaN` (half a period) | Defined | Defined |
| Season | Fixed | May change over time | May change over time |
| Outliers | Not robust | `robust=True` | `stl_kwargs={"robust": True}` |
| Number of periods | One | One | Several |
| Speed | Very fast | Fast | Slower |

All of them live in `statsmodels.tsa.seasonal`.

## The calls

```python
from statsmodels.tsa.seasonal import MSTL, STL, seasonal_decompose

r = seasonal_decompose(s, model="additive", period=7)
r = seasonal_decompose(p, model="multiplicative", period=12)

r = STL(s, period=7, robust=True).fit()
r = MSTL(s, periods=(7, 365)).fit()

r.observed, r.trend, r.seasonal, r.resid
fig = r.plot()
```

With `MSTL`, `r.seasonal` is a table: one column per period (`seasonal_7`,
`seasonal_365`).

If the frequency of the index is known (`asfreq("D")`, `asfreq("MS")`),
statsmodels can guess the period itself, but it does not always pick the one
you want. **Write `period` yourself.**

## Choosing the period

| Data frequency | Pattern | `period` |
|---|---|---|
| Hourly | Daily | 24 |
| Hourly | Weekly | 168 |
| Daily | Weekly | 7 |
| Daily | Yearly | 365 |
| Weekly | Yearly | 52 |
| Monthly | Yearly | 12 |
| Quarterly | Yearly | 4 |

The data must hold at least **two full cycles** of the period; three or more
for a reliable pattern.

## The trend with an even period: the 2×12 average

When the period is odd (7) a centred window has a middle point. When it is
even (12) it does not: the window looks either 6 months back and 5 ahead, or
the other way round. The classical fix is to take a 2-term average on top of
the 12-term one:

```python
trend = p.rolling(12).mean().rolling(2).mean().shift(-6)
```

The result is a symmetric average spread over 13 months in which the two end
months get half weight. This is exactly what `seasonal_decompose` does for an
even period (measured); `p.rolling(12, center=True).mean()` does **not** give
the same result.

## Additive or multiplicative: deciding

1. Plot the series. Do the waves grow as the level rises?
2. Compute `max - min` and `max / min` per year. Which one is constant? A
   constant difference means additive, a constant ratio multiplicative.
3. Try both and group the residual by year. If the size of the residual
   changes from year to year, that model is wrong.

If the series contains zero or negative values, the multiplicative model
cannot be used. If unsure: take the logarithm and decompose additively.

## Units in the multiplicative model

| Component | Additive | Multiplicative |
|---|---|---|
| Trend | Unit of the series | Unit of the series |
| Seasonal | Unit of the series, sums to 0 | A ratio, averages 1 |
| Residual | Unit of the series, around 0 | A ratio, around 1 |

A multiplicative residual of 1.03 means the observation is 3% above what was
expected.

## The settings of STL

```python
STL(s, period=7, seasonal=7, trend=None, robust=False)
```

- `seasonal`: how fast the season may change (an odd number, at least 7). A
  small value: the season changes freely from year to year. A large value: an
  almost fixed season, close to the classical method.
- `trend`: the length of the trend smoother (an odd number). The larger, the
  smoother the trend. Left empty, it is computed from the period.
- `robust`: lowers the weight of outlier days. Turn it on when there are
  outliers; `fit.weights` shows which days were turned down.

## The strength of the components

How marked is the season? A measure between 0 and 1:

$$F_S = \max\left(0,\; 1 - \frac{\operatorname{Var}(\text{residual})}{\operatorname{Var}(\text{seasonal} + \text{residual})}\right)$$

The same formula for the trend, with the trend in place of the season.

```python
strength = 1 - r.resid.var() / (r.seasonal + r.resid).var()
```

In the daily sales the strength of the weekly season is 0.92 and that of the
trend 0.91: both are very marked. Below 0.3 is weak and may not be worth
separating. It is handy when classifying many series (hundreds of products):
which ones are seasonal and which are not.

## Adjusting

```python
adjusted = s - r.seasonal        # additive
adjusted = p / r.seasonal        # multiplicative
detrended = s - r.trend          # detrended: only pattern and noise
```
