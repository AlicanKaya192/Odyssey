The residual is not "rubbish", it is a **diagnostic tool**. In a good
decomposition the residual is boring: around zero, patternless, the same width
in every period. If it is not boring, it is telling you something.

## Five questions

```python
r = seasonal_decompose(s, model="additive", period=7)
e = r.resid.dropna()
```

**1. Is its mean zero?**

```python
print(round(e.mean(), 3))
```

It should be very close to zero in the additive model and to 1 in the
multiplicative one. If not, the trend has missed the level.

**2. Is there a pattern by calendar?**

```python
print(e.groupby(e.index.dayofweek).mean().round(1).tolist())
print(e.groupby(e.index.month).mean().round(1).tolist())
```

Every group should be close to zero. If a particular day or month keeps coming
out positive or negative, there is a season that was not separated: the period
is wrong, or a second period is needed.

**3. Does its width change over time?**

```python
print(e.abs().groupby(e.index.year).mean().round(1).tolist())
```

If it grows from year to year (or, as in the passenger series, is large at the
ends and small in the middle), the model is additive but the series is
multiplicative.

**4. Do neighbouring days resemble each other?**

```python
print(round(e.corr(e.shift(1)), 2))
```

It should be close to zero. If it is high, there is still usable information
in the residual: yesterday's surprise tells you about today. Section 12
(autocorrelation) is the full version of this question and the starting point
of ARIMA.

**5. Which days are the extremes?**

```python
print(e.abs().sort_values(ascending=False).head(5))
```

These are events: a campaign, a holiday, an outage, a data error. Compare them
with the calendar (the holiday list from Section 04). If the same date comes
up every year, it is not an event but a season that was not separated.

## From symptom to diagnosis

| What you see in the residual | What it means | What to do |
|---|---|---|
| A slow wave | The trend is too stiff, or a second season | A shorter trend window; MSTL |
| Always the same sign on particular days | A season not separated | Fix `period`, add a second period |
| The width grows with the level | Multiplicative structure | `model="multiplicative"` or the logarithm |
| Isolated large spikes | Events | `robust=True`; mark the events (Sections 13, 21) |
| Residuals of the opposite sign around a spike | The outlier pulled the trend | `STL(..., robust=True)` |
| Always positive after some date | A level shift | Change point (Section 21) |
| Neighbouring days are alike | Remaining dependence | It can be modelled: Sections 12 and 17 |

## Finding unusual days with the residual

The rolling z-score of Section 07 looked at the raw series; with a strong
weekly pattern every Saturday came out a little "unusual". In the residual the
pattern has already been removed:

```python
fit = STL(s, period=7, robust=True).fit()
z = (fit.resid - fit.resid.mean()) / fit.resid.std()
unusual = z[z.abs() > 3]
```

`robust=True` is essential here: without it the outlier day itself distorts
the trend and the season and shrinks its own residual. Section 21 takes this
idea all the way.

## A decomposition is not a forecast

A decomposition explains **the past**. To extend it into the future you have
to think about each component separately:

- **Seasonal**: it repeats; it can be copied as is into next week.
- **Trend**: it has to be extended; how to extend it is a modelling choice.
- **Residual**: by definition the unpredictable part; it gives the size of the
  uncertainty.

The baseline forecasts of Section 14 and the exponential smoothing of
Section 16 are precisely ways of carrying these three components forward.
