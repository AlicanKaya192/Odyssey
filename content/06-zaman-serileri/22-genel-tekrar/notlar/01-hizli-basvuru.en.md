All the tools of the track, in working order. For detail go back to the notes
of the section concerned.

## Reading dates

| Job | Code |
|---|---|
| Turn text into dates | `pd.to_datetime(s, format="%d.%m.%Y")` |
| See broken values | `pd.to_datetime(s, errors="coerce")` → `NaT` |
| Convert while reading | `pd.read_csv(f, index_col="date", parse_dates=True)` |
| Set / convert a time zone | `.dt.tz_localize("Europe/Istanbul")`, `.dt.tz_convert("UTC")` |
| Parts | `.dt.year`, `.dt.month`, `.dt.dayofweek`, `.dt.hour` |
| Formatted text | `.dt.strftime("%Y-%m-%d")` |

## A regular index

| Job | Code |
|---|---|
| Make it the index, sort | `df.set_index("date").sort_index()` |
| Drop duplicates | `df.drop_duplicates()`, `s[~s.index.duplicated()]` |
| A regular frequency | `s.asfreq("D")` |
| A date range | `pd.date_range("2024-01-01", periods=28, freq="D")` |
| Slice | `s.loc["2024-03"]`, `s.loc["2024-03-01":"2024-03-15"]` |
| Periods | `s.index.to_period("M")` |

Frequency aliases: `h` hour, `D` day, `B` business day, `W-SUN` week, `MS` /
`ME` month start / end, `QS` quarter, `YS` year.

## Summarising and shifting

| Job | Code |
|---|---|
| Downsample | `s.resample("MS").sum()` (a flow), `.mean()` / `.last()` (a state) |
| Upsample | `s.resample("h").ffill()`, `.interpolate()` |
| Weekday profile | `s.groupby(s.index.dayofweek).mean()` |
| Carry the past | `s.shift(1)`, `s.shift(7)` |
| Change | `s.diff()`, `s.diff(7)`, `s.pct_change()` |
| Rolling window | `s.rolling(7).mean()`; in a feature `s.shift(1).rolling(7).mean()` |
| Expanding / exponential | `s.expanding().mean()`, `s.ewm(alpha=0.3).mean()` |
| Long → wide | `df.pivot(index="date", columns="store", values="sales")` |

## Diagnosis

| Question | Code |
|---|---|
| Components | `STL(s, period=7, robust=True).fit()` → `.trend`, `.seasonal`, `.resid` |
| Stationary? | `adfuller(s)[1]` (small p: stationary), `kpss(s)[1]` (small p: not) |
| Autocorrelation | `acf(s, nlags=30)`, `pacf(s, nlags=30)`, `plot_acf(s)` |
| Is the residual white noise? | `acorr_ljungbox(resid, lags=[14])` (large p: yes) |
| Tame the variance | `np.log(s)`; back with `np.exp` |

## Missing values and outliers

| Job | Code |
|---|---|
| Count the gaps | `s.isna().sum()` |
| A short gap | `s.interpolate(limit=3)` |
| A seasonal series | fill with `pd.concat([s.shift(7), s.shift(-7)], axis=1).mean(axis=1)` |
| Robust score | `0.6745 * (r - r.median()) / (r - r.median()).abs().median()` |

## Baselines and validation

| Job | Code |
|---|---|
| Naive | `train.iloc[-1]` |
| Seasonal naive | repeat the last `m` values |
| MAE / RMSE | `np.abs(e).mean()`, `np.sqrt((e ** 2).mean())` |
| MASE | MAE / the seasonal naive MAE on the training data |
| Rolling origin | a list of cuts; at each `train = s.loc[:cut]`, the next `h` days the test |
| scikit-learn | `TimeSeriesSplit(n_splits=5)`; no shuffled `KFold` |

## Models

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA

fit = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7).fit()
forecast = fit.forecast(28)

fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7), exog=x_train).fit()
result = fit.get_forecast(28, exog=x_future)
result.predicted_mean
result.conf_int(alpha=0.2)
```

Calendar features (always known in the future):

```python
angle = 2 * np.pi * index.dayofyear / 365.25
x["sin1"], x["cos1"] = np.sin(angle), np.cos(angle)      # yearly Fourier
x["dow"] = index.dayofweek                               # or weekday dummies
x["t"] = (index - start).days                            # trend
```

Lag features always with `shift`; if the horizon is `h` the newest lag is `h`.

## Intervals

| Job | Code |
|---|---|
| Empirical | `np.quantile(errors, [0.1, 0.9])` of rolling-origin errors |
| Coverage | `((actual >= low) & (actual <= high)).mean()` |
| Pinball | `np.mean(np.maximum(q * d, (q - 1) * d))`, `d = actual - forecast` |
| Which quantile | cost short / (cost short + cost over) |

## Anomalies and changes

| Job | Code |
|---|---|
| Live expectation | `pd.concat([s.shift(7 * k) for k in (1, 2, 3, 4)], axis=1).median(axis=1)` |
| Run length | `same = s.diff() == 0`; `same.groupby((~same).cumsum()).sum() + 1` |
| CUSUM | `total = max(0, total + z - k)`; alarm if `total > h` |
| Day of a change | sum of squares of the two pieces for every cut; the smallest, and its gain |

## A decision tree: which method?

| Case | Try first |
|---|---|
| A short series, a clear season | Seasonal naive, Holt–Winters |
| Trend + one season, no outside information | Holt–Winters or seasonal ARIMA |
| Two seasons (weekly + yearly) | Regression with Fourier terms, or ARIMA + Fourier |
| Known external factors (holiday, campaign, price) | Regression / ARIMA with external variables |
| Many features, non-linear effects | Tree models (target as a difference) |
| A random walk (a price) | Naive; the real work is the interval |
