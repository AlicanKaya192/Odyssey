## The calls

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf

values = acf(x, nlags=20)            # array: values[0] = 1, values[k] = lag k
values = pacf(x, nlags=20)

fig = plot_acf(x, lags=20)           # the correlogram, band included
fig = plot_pacf(x, lags=20)
fig = plot_acf(x, lags=20, zero=False)   # hide the lag 0 bar

table = acorr_ljungbox(x, lags=[10, 20])   # columns: lb_stat, lb_pvalue
```

`x` must not contain `NaN`. If you differenced, `dropna()`.

## The confidence band

$$\pm \frac{1.96}{\sqrt{n}}$$

| Observations | Band |
|---|---|
| 50 | ±0.277 |
| 100 | ±0.196 |
| 250 | ±0.124 |
| 500 | ±0.088 |
| 1000 | ±0.062 |
| 5000 | ±0.028 |

The band drawn by `plot_acf` **widens** a little as the lag grows (it accounts
for the correlation at earlier lags); a constant ±1.96/√n is a good first
approximation.

On a very long series the band is very narrow: a correlation of 0.05 comes out
"significant" but is useless in practice. **Significant** and **large** are
not the same thing.

## How many lags?

- With a season, at least two cycles: 14–21 for daily data, 24–36 for monthly,
  48 and 336 for hourly.
- The upper limit: a quarter of the number of observations. Distant lags are
  computed from few pairs and are unreliable.

## From shape to diagnosis

| What you see in the ACF | What it means | What to do |
|---|---|---|
| All high, decaying very slowly | Trend / random walk | `diff()` |
| Slowly decaying peaks at `m`, `2m`, `3m` | A strong season | `diff(m)` |
| The first few lags high, decaying fast | Short memory (AR type) | Look at the PACF |
| Only lag 1 (or the first `q`) outside the band | MA type | `q` is that number |
| Decaying in waves, changing sign | AR with a negative coefficient, or AR(2) | Look at the PACF |
| Lag 1 around −0.5, the rest zero | Differenced too much | Undo one difference |
| After a seasonal difference, only a negative bar at `m` | A seasonal MA term | Section 17: `Q = 1` |
| All inside the band | White noise | No memory to model |

## ACF and PACF together

| ACF | PACF | Process |
|---|---|---|
| Decays slowly | Cuts off after lag `p` | AR(p) |
| Cuts off after lag `q` | Decays slowly | MA(q) |
| Decays slowly | Decays slowly | Both: ARMA |
| All in the band | All in the band | White noise |

"Cuts off": every bar after that lag is inside the band. "Decays": the bars
shrink step by step.

On real data the shapes are never as clean as in the textbook. The ACF and
PACF give **candidates**; you make the final decision by comparing models
(Sections 15 and 17).

## Ljung–Box

```python
acorr_ljungbox(x, lags=[10])
```

| | |
|---|---|
| Assumption | The autocorrelation of the first `m` lags is zero (white noise) |
| Small p (< 0.05) | There is memory: structure left to model |
| Large p | No memory was found |
| Choosing `lags` | 10 without a season; `2m` with one (14 for daily, 24 for monthly) |

When applying it to the residual of a model, you give the number of parameters
of the model as `model_df`; the test corrects its degrees of freedom
accordingly (Section 17).

## Other uses of autocorrelation

- **Finding the period:** the first large peak of the ACF is the length of the
  season.
- **Choosing features:** the ACF and PACF tell you which lags to give a
  machine learning model (Section 19): those beyond the band.
- **Checking residuals:** after every model.
- **Sampling frequency:** if lag 1 is 0.99, consecutive observations carry
  almost the same information; sampling less often loses nothing.
