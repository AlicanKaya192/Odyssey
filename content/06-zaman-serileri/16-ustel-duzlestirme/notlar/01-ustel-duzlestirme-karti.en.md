## One class, the whole family

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    train,
    trend=None,              # None, "add", "mul"
    damped_trend=False,      # only with a trend
    seasonal=None,           # None, "add", "mul"
    seasonal_periods=None,   # length of the season (number of rows)
)
fit = model.fit()
```

| Trend | Season | Common name | When |
|---|---|---|---|
| None | None | Simple exponential smoothing | A noisy level with no trend or season |
| `"add"` | None | Holt | A linear trend |
| `"add"` + damping | None | Damped Holt | A trend that will not last for ever |
| `"mul"` | None | Exponential trend | Percentage growth |
| None | `"add"` | Seasonal smoothing | Level + a season of constant size |
| `"add"` | `"add"` | Additive Holt–Winters | Trend + a season of constant size |
| `"add"` | `"mul"` | Multiplicative Holt–Winters | Trend + a season growing with the level |
| `"mul"` | `"mul"` | Fully multiplicative | Percentage growth + a proportional season |

`train` must carry a regularly spaced index (`asfreq`), contain no `NaN`, and
be at least **two full seasons** long.

## The result object

| Attribute | Content |
|---|---|
| `fit.params` | The coefficients and initial values (a dictionary) |
| `fit.params["smoothing_level"]` | `α` |
| `fit.params["smoothing_trend"]` | `β` |
| `fit.params["smoothing_seasonal"]` | `γ` |
| `fit.params["damping_trend"]` | `φ` |
| `fit.level`, `fit.trend`, `fit.season` | The values of the components over the training period |
| `fit.fittedvalues` | The one-step forecasts on the training data |
| `fit.resid` | The residuals on the training data |
| `fit.forecast(h)` | The forecast of the next `h` steps (a series with a date index) |
| `fit.aic` | An information criterion: smaller is better |

The coefficient of an unused component comes back as `nan`.

## The update equations

For an additive trend and an additive season (season length $m$):

$$\ell_t = \alpha\,(y_t - s_{t-m}) + (1 - \alpha)(\ell_{t-1} + b_{t-1})$$

$$b_t = \beta\,(\ell_t - \ell_{t-1}) + (1 - \beta)\,b_{t-1}$$

$$s_t = \gamma\,(y_t - \ell_t) + (1 - \gamma)\,s_{t-m}$$

$$\hat{y}_{t+h} = \ell_t + h\,b_t + s_{t+h-m}$$

All three follow the same pattern: **new information × coefficient + old
estimate × (1 − coefficient)**.

- The level is pulled towards the observation with the seasonal share removed.
- The slope is pulled towards the latest change in the level.
- The seasonal share is pulled towards the deviation of the observation from
  the level.

With a multiplicative season, division replaces subtraction and multiplication
replaces addition.

The forecast with a damped trend:

$$\hat{y}_{t+h} = \ell_t + (\phi + \phi^2 + \dots + \phi^h)\,b_t$$

`φ = 1` is undamped; with `φ = 0.9` the effect of the slope falls to a third
in ten steps.

## Giving a coefficient yourself

```python
fit = model.fit(smoothing_level=0.2, optimized=False)
fit = model.fit(smoothing_level=0.2)     # alpha fixed, the rest is found
```

When? When forecasting many series with the same settings, or when you do not
trust the coefficient found on a very short series. Typical hand choices:
`α` 0.1–0.3, `β` 0.05–0.2, `γ` 0.1–0.3.

## Choosing a model

Three routes, in order of reliability:

1. **A rolling origin** (Section 15): the out-of-sample error of the
   candidates. The most reliable; the most expensive.
2. **An information criterion:** `fit.aic`. It rewards fit and penalises the
   number of coefficients. Only models fitted **on the same data with the same
   transformation** can be compared.
3. **By the structure:** is there a trend, do the waves grow (Section 10)?

Do not choose by the training error (`fit.resid`): it always shrinks as you
add components.

## Quick smoothing with pandas

```python
s.ewm(alpha=0.2, adjust=False).mean()       # the level of simple exponential smoothing
s.ewm(span=10, adjust=False).mean()         # alpha = 2 / (span + 1)
s.ewm(halflife=5, adjust=False).mean()      # the weight halves in 5 steps
```

`adjust=False` is the update rule of the lesson. For a one-step forecast,
`shift(1)`: `s.ewm(alpha=0.2, adjust=False).mean().shift(1)`.

Compared with a moving average (Section 07):

| | `rolling(n).mean()` | `ewm(alpha=a).mean()` |
|---|---|---|
| Weights | The last `n` observations equal, before that zero | All, decaying exponentially |
| A value leaving the window | A sudden effect | No effect: its weight has already shrunk |
| `NaN` at the start | `n − 1` of them | None |
| Rough equivalence | `n` | `α = 2 / (n + 1)` |
