## Two tests, two assumptions

| | ADF | KPSS |
|---|---|---|
| Stands for | Augmented Dickey–Fuller | Kwiatkowski–Phillips–Schmidt–Shin |
| Starting assumption | **Not** stationary (has a unit root) | Stationary |
| Small p (< 0.05) | Stationary | Not stationary |
| Large p | No decision: non-stationarity could not be rejected | No decision: stationarity could not be rejected |
| Statistic | The more negative, the more stationary | The larger, the less stationary |

When a test **fails to reject** its assumption, it has not proved it. A large
ADF p-value does not mean "not stationary", it means "I could not show that it
is stationary". That is why you use the two tests together: one looks from one
side, the other from the opposite side.

## The returned values

```python
from statsmodels.tsa.stattools import adfuller, kpss

stat, pvalue, used_lags, n_obs, critical, icbest = adfuller(x)
stat, pvalue, used_lags, critical = kpss(x, regression="c", nlags="auto")
```

- `stat`: the test statistic.
- `pvalue`: the p-value.
- `used_lags`: the number of lags the test took into account.
- `critical`: the critical values, `{"1%": ..., "5%": ..., "10%": ...}`. In
  ADF, a statistic **smaller** (more negative) than the critical value means
  stationary; in KPSS, a **larger** one means not stationary.

The series must not contain `NaN`: `dropna()` after differencing.

## Reading the two together

| ADF | KPSS | Reading | What to do |
|---|---|---|---|
| Stationary | Stationary | Stationary | Carry on |
| Not stationary | Not stationary | Not stationary | Difference |
| Not stationary | Stationary | May be stationary around a straight line (trend-stationary) | Remove the trend or difference; plot |
| Stationary | Not stationary | May become stationary once differenced | Difference; plot |

The last two rows are the "tests disagree" case. Most of the time it shows the
transformation is incomplete: a season, a growing variance or a level shift.

## The `regression` option

| Value | What the test looks for stationarity around |
|---|---|
| `"c"` (default) | A constant level |
| `"ct"` | A straight trend line |

A series that comes out "stationary" with `"ct"` is **trend-stationary**: the
level drifts, but the drift is a straight line and deviations return to it. In
practice knowing the distinction is enough; for most business series
differencing is the safe route.

## The p-value of KPSS

KPSS reads its p-value off a table, and the table only covers 0.01–0.10. If
the statistic is outside the table:

- p = 0.01 means "at most 0.01" (a strong rejection),
- p = 0.10 means "at least 0.10" (no rejection),

and statsmodels prints an `InterpolationWarning`. It is not an error. To
silence it:

```python
import warnings

warnings.simplefilter("ignore")
```

## When the tests go wrong

**A season.** Neither test looks for a season. A seasonal series can come out
"stationary". Look at the plot and the seasonal plot.

**A level shift.** A series that moves to another level in one day but is
stationary in both periods (like 2 September in the web traffic) can look like
a random walk to ADF. Rather than differencing, the shift has to be modelled
(Section 21).

**A short series.** With 30–40 observations the tests have little power: ADF
says "could not reject" to almost anything. With three years of monthly data,
do not lean too hard on a test result.

**A very long series.** With thousands of observations even the smallest
deviation comes out "significant". However small p is, look at the size of the
effect.

**A series that returns slowly.** It returns to its mean, but very slowly: ADF
cannot tell it from a random walk. Longer data is needed.

**Outliers.** A few large spikes can pull the result either way. Clean them
first (Section 13).

## What a p-value is and is not

A p-value: the probability of seeing a result this extreme **if the assumption
were true**.

- p = 0.03 does **not** mean "the series is stationary with 97% probability".
- 0.05 is not a magic line; 0.049 and 0.051 are the same information.
- A test is a decision tool, not a measurement. It does not answer "how
  stationary".

The solid route: the plot + the mean and standard deviation of the two halves
+ the two tests. If all four say the same thing, the decision is clear.
