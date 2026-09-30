# Forecasting with Machine Learning

At the end of Section 18 you had a table: each row a day, each column a piece
of information about that day. Every model in the Machine Learning track works
with exactly such a table.

In this section you turn forecasting into a **table problem**. The good news:
every model you know, from linear regression to gradient boosting, can be
used. The bad news: there are three traps specific to time series, and all
three are silent. The results may not come out as you expect either: the most
important lesson of this section is that **the gain comes from the features,
not from the model**.

## 1. Turning a series into a table

A time series is a single column. For a model to learn, you write next to each
day the information you **will have when forecasting** that day.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Lags</span><span>Past values of the series: yesterday, the same day last week. <code>shift(k)</code></span></div>
<div class="anat-row"><span>Windows</span><span>A summary of the recent past: the mean of the last 7 days. <code>shift(1).rolling(n)</code></span></div>
<div class="anat-row"><span>Calendar</span><span>Day of the week, month, holiday, Fourier terms. Their future is known.</span></div>
<div class="anat-row"><span>External variables</span><span>Campaign, price, temperature (Section 18).</span></div>
</div>
<figcaption>Four families of features. The target column is that day's value.</figcaption>
</figure>

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    X = pd.DataFrame(index=y.index)
    for k in (1, 2, 7, 14):
        X[f"lag{k}"] = y.shift(k)
    X["mean7"] = y.shift(1).rolling(7).mean()
    X["mean28"] = y.shift(1).rolling(28).mean()
    X["dow"] = y.index.dayofweek
    X["month"] = y.index.month
    return X


table = features(s).join(s.rename("y")).dropna()
print(table.shape, table.index[0].date())      # (1068, 9) 2022-01-29
```

The first 28 rows are gone: there is not enough past for `mean28`. Every lag
and window costs rows at the start.

In `mean7`, **`shift(1)` first, then `rolling`**: the rule from Sections 07
and 14. Otherwise "the mean of the last 7 days" includes the day to be
forecast.

## 2. A first model

Once the table is ready, the rest is familiar. Training up to the end of 2023,
the test being 2024; each day is forecast **one day ahead**:

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression

train, test = table.loc[:"2023"], table.loc["2024"]
columns = [c for c in table.columns if c != "y"]

model = LinearRegression().fit(train[columns], train["y"])
predicted = model.predict(test[columns])
```

| Method | Test MAE | Training MAE |
|---|---|---|
| Naive | 41.10 | |
| Seasonal naive | 13.87 | |
| Linear regression | **11.51** | 10.89 |
| Random forest | 12.87 | 4.31 |
| Gradient boosting | 14.63 | 4.79 |

Three observations:

- The linear model beats seasonal naive by 17%.
- **The simplest model is the best.** The two tree-based models are behind
  linear regression; gradient boosting does not even beat seasonal naive.
- The training error of the trees (4–5) is a third of their test error:
  **memorising**. A table of 700 rows is not enough to feed a model with
  thousands of leaves.

This result is no accident; the next part shows why.

## 3. Trees cannot extrapolate the level

A decision tree gives as its forecast **the mean of values it saw in
training**. It cannot say anything higher than the highest value it saw.

The shop is growing. The highest sales in the training data are 462; in
December 2024 they reach 503.

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="234.6" x2="666" y2="234.6"/><text class="dim" x="38" y="238.1" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="202.5" x2="666" y2="202.5"/><text class="dim" x="38" y="206.0" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="170.4" x2="666" y2="170.4"/><text class="dim" x="38" y="173.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="138.2" x2="666" y2="138.2"/><text class="dim" x="38" y="141.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="106.1" x2="666" y2="106.1"/><text class="dim" x="38" y="109.6" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="74.0" x2="666" y2="74.0"/><text class="dim" x="38" y="77.5" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="41.9" x2="666" y2="41.9"/><text class="dim" x="38" y="45.4" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">18 Nov</text><line class="line" x1="145.3" y1="240" x2="145.3" y2="244"/><text class="dim" x="145.3" y="256" font-size="10.5" text-anchor="middle">25 Nov</text><line class="line" x1="246.5" y1="240" x2="246.5" y2="244"/><text class="dim" x="246.5" y="256" font-size="10.5" text-anchor="middle">2 Dec</text><line class="line" x1="347.8" y1="240" x2="347.8" y2="244"/><text class="dim" x="347.8" y="256" font-size="10.5" text-anchor="middle">9 Dec</text><line class="line" x1="449.0" y1="240" x2="449.0" y2="244"/><text class="dim" x="449.0" y="256" font-size="10.5" text-anchor="middle">16 Dec</text><line class="line" x1="550.3" y1="240" x2="550.3" y2="244"/><text class="dim" x="550.3" y="256" font-size="10.5" text-anchor="middle">23 Dec</text><line class="line" x1="651.5" y1="240" x2="651.5" y2="244"/><text class="dim" x="651.5" y="256" font-size="10.5" text-anchor="middle">30 Dec</text><line class="curve3" stroke-dasharray="4 4" x1="44" y1="98.4" x2="666" y2="98.4"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,219.9 58.5,215.4 72.9,215.4 87.4,192.9 101.9,159.5 116.3,127.3 130.8,149.2 145.3,222.4 159.7,210.9 174.2,204.4 188.7,204.4 203.1,179.4 217.6,117.7 232.0,142.7 246.5,222.4 261.0,208.9 275.4,196.7 289.9,193.5 304.4,165.9 318.8,106.8 333.3,131.8 347.8,206.4 362.2,191.6 376.7,201.9 391.2,163.3 405.6,145.3 420.1,96.5 434.6,116.4 449.0,201.9 463.5,197.4 478.0,187.7 492.4,189.7 506.9,132.5 521.3,81.1 535.8,119.0 550.3,198.7 564.7,174.2 579.2,176.8 593.7,166.5 608.1,122.8 622.6,72.1 637.1,110.0 651.5,177.4 666.0,172.3"/><polyline class="curve" style="stroke-width:2" points="44.0,212.2 58.5,217.9 72.9,201.2 87.4,193.8 101.9,159.8 116.3,121.9 130.8,143.3 145.3,212.5 159.7,214.5 174.2,201.8 188.7,190.7 203.1,156.2 217.6,130.5 232.0,139.4 246.5,213.8 261.0,208.8 275.4,202.7 289.9,191.2 304.4,164.7 318.8,122.0 333.3,138.2 347.8,213.5 362.2,204.2 376.7,192.6 391.2,190.8 405.6,164.4 420.1,111.0 434.6,129.0 449.0,204.3 463.5,194.5 478.0,190.6 492.4,171.0 506.9,150.9 521.3,100.5 535.8,116.8 550.3,195.9 564.7,189.2 579.2,185.2 593.7,168.5 608.1,134.3 622.6,88.2 637.1,109.8 651.5,190.9 666.0,179.3"/><polyline class="curve2" style="stroke-width:2" points="44.0,206.2 58.5,208.3 72.9,204.7 87.4,198.5 101.9,149.9 116.3,137.3 130.8,139.5 145.3,209.0 159.7,205.6 174.2,199.5 188.7,188.4 203.1,149.7 217.6,140.7 232.0,130.1 246.5,207.3 261.0,206.1 275.4,204.7 289.9,195.0 304.4,156.5 318.8,128.1 333.3,132.2 347.8,207.3 362.2,207.3 376.7,193.3 391.2,186.6 405.6,147.3 420.1,132.2 434.6,132.2 449.0,206.2 463.5,190.0 478.0,196.5 492.4,165.2 506.9,142.4 521.3,130.1 535.8,132.2 550.3,204.0 564.7,191.4 579.2,185.5 593.7,164.8 608.1,135.9 622.6,132.2 637.1,132.2 651.5,193.9 666.0,184.6"/><text class="dim" x="48.3" y="94.6" font-size="11" text-anchor="start">highest value in training: 462</text><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">linear regression</text><line class="curve2" x1="307" y1="40" x2="325" y2="40"/><text class="ink" x="331" y="44" font-size="11">gradient boosting</text></svg>
  <figcaption>December 2024, one-day-ahead forecasts. The dashed line is the highest sales in the training data. Gradient boosting stays well below that line; the linear model follows the Saturday peaks, the tree cannot.</figcaption>
</figure>

| | Highest value | December 2024 MAE |
|---|---|---|
| Actual (December 2024) | 503 | |
| Linear regression forecast | 478 | 14.52 |
| Gradient boosting forecast | 416 | 22.47 |

The forecast of gradient boosting **hits a ceiling** at 416. On the 20 highest
days it is 27 units low on average. The linear model, on the other hand, can
raise its forecast as `lag7` grows.

This is the basic problem of tree-based models on any trending series. The fix
is familiar from Section 11: **forecast the change, not the level.**

```python
target = table["y"] - table["lag7"]          # the change on last week
# the model learns this difference; forecast = model output + lag7
```

With the difference as the target, the test error of gradient boosting goes
from 14.63 to 11.74 and its December error from 22.47 to 10.87. The difference
is stationary; there is no level left for the tree to extrapolate.

## 4. Validation: no shuffling

The default cross-validation of scikit-learn **shuffles** the rows. In a time
series that means the model sees 14 and 16 March in training while forecasting
15 March.

```python
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score

model = HistGradientBoostingRegressor(random_state=0)
for cv in (KFold(5, shuffle=True, random_state=0), TimeSeriesSplit(5)):
    scores = -cross_val_score(model, table[columns], table["y"], cv=cv,
                              scoring="neg_mean_absolute_error")
    print(round(scores.mean(), 2))
# 11.88   15.78
```

The same model, the same data: shuffled validation gives 11.88, validation by
time 15.78. The first measures the model's skill at **filling gaps in the
past**; the second its skill at **forecasting the future**. Your job is the
second.

`TimeSeriesSplit` is the ready-made rolling origin of Section 15: in every
split the training comes before the test.

## 5. Leakage: a one-line mistake

```python
X["mean7"] = y.rolling(7).mean()              # shift(1) forgotten
```

With this one line the test error of the linear model "improves" from 11.51 to
10.55. No warning, the code runs, the result is better. Yet the feature
contains the very day being forecast.

One question for every feature: **could I have computed this number at the
moment I made the forecast?** When you see an unexpected improvement, ask this
first.

## 6. Multi-step forecasts: three routes

So far you have always forecast tomorrow. For 28 days ahead you do not have
`lag1`: the yesterday of 27 days from now has not happened yet.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Recursive</span><span>Forecast tomorrow, treat the forecast as data, forecast the day after. One model; errors <b>accumulate</b>.</span></div>
<div class="anat-row"><span>Direct, safe features</span><span>Use only information as old as the horizon: <code>lag28</code>, <code>lag35</code>, the calendar. One model; no accumulation.</span></div>
<div class="anat-row"><span>Direct, a model per horizon</span><span>A separate model for each horizon: 1 day, 2 days, ..., 28 days. The most flexible; the most expensive.</span></div>
</div>
<figcaption>At a 28-day horizon a "safe" feature is anything at least 28 days old, plus the calendar.</figcaption>
</figure>

The second route is the plainest. The features:

```python
def safe_features(full):
    X = pd.DataFrame(index=full.index)
    for k in (28, 35, 42, 56):
        X[f"lag{k}"] = full.shift(k)
    X["level28"] = full.shift(28).rolling(28).mean()
    X["dow"] = X.index.dayofweek
    # + calendar: day counter, the December climb, Fourier terms (Section 18)
    return X
```

`lag28` is **the same weekday** as the day to be forecast: 28 is a multiple
of 7. That is why the weekly pattern is kept.

## 7. The test: all together

The rig of Section 15: 13 origins, a 28-day horizon.

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="206.0" x2="666" y2="206.0"/><text class="dim" x="38" y="209.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="163.1" x2="666" y2="163.1"/><text class="dim" x="38" y="166.6" font-size="10.5" text-anchor="end">5</text><line class="grid" x1="44" y1="120.3" x2="666" y2="120.3"/><text class="dim" x="38" y="123.8" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="77.4" x2="666" y2="77.4"/><text class="dim" x="38" y="80.9" font-size="10.5" text-anchor="end">15</text><line class="grid" x1="44" y1="34.6" x2="666" y2="34.6"/><text class="dim" x="38" y="38.1" font-size="10.5" text-anchor="end">20</text><line class="line" x1="44" y1="206" x2="666" y2="206"/><line class="line" x1="104.2" y1="206" x2="104.2" y2="210"/><text class="dim" x="104.2" y="222" font-size="10.5" text-anchor="middle">seasonal naive</text><line class="line" x1="204.5" y1="206" x2="204.5" y2="210"/><text class="dim" x="204.5" y="222" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="304.8" y1="206" x2="304.8" y2="210"/><text class="dim" x="304.8" y="222" font-size="10.5" text-anchor="middle">ARIMA</text><line class="line" x1="405.2" y1="206" x2="405.2" y2="210"/><text class="dim" x="405.2" y="222" font-size="10.5" text-anchor="middle">boosting + calendar</text><line class="line" x1="505.5" y1="206" x2="505.5" y2="210"/><text class="dim" x="505.5" y="222" font-size="10.5" text-anchor="middle">linear + calendar</text><line class="line" x1="605.8" y1="206" x2="605.8" y2="210"/><text class="dim" x="605.8" y="222" font-size="10.5" text-anchor="middle">ARIMA + calendar</text><rect class="dot2" x="73.1" y="52.1" width="62.2" height="153.9" rx="3" opacity="0.9"/><rect class="dot2" x="173.4" y="69.6" width="62.2" height="136.4" rx="3" opacity="0.9"/><rect class="dot2" x="273.7" y="69.4" width="62.2" height="136.6" rx="3" opacity="0.9"/><rect class="dot" x="374.1" y="87.7" width="62.2" height="118.3" rx="3" opacity="0.9"/><rect class="dot" x="474.4" y="114.8" width="62.2" height="91.2" rx="3" opacity="0.9"/><rect class="dot" x="574.7" y="118.3" width="62.2" height="87.7" rx="3" opacity="0.9"/><text class="ink" x="104.2" y="46.1" font-size="11.5" text-anchor="middle">17.9</text><text class="ink" x="204.5" y="63.6" font-size="11.5" text-anchor="middle">15.9</text><text class="ink" x="304.8" y="63.4" font-size="11.5" text-anchor="middle">15.9</text><text class="ink" x="405.2" y="81.7" font-size="11.5" text-anchor="middle">13.8</text><text class="ink" x="505.5" y="108.8" font-size="11.5" text-anchor="middle">10.6</text><text class="ink" x="605.8" y="112.3" font-size="11.5" text-anchor="middle">10.2</text></svg>
  <figcaption>The mean MAE of 13 experiments, a 28-day horizon. Orange: the past of the series only. Purple: with calendar information. The step is climbed by information, not by the kind of model.</figcaption>
</figure>

| Method | Mean MAE | Worst experiment |
|---|---|---|
| Seasonal naive | 17.95 | 41.3 |
| Holt–Winters | 15.91 | 38.6 |
| ARIMA | 15.94 | 52.2 |
| ARIMA + calendar | 10.23 | 14.4 |
| Recursive linear (no calendar) | 16.66 | 45.4 |
| Direct linear, **no calendar** | 18.98 | 41.4 |
| Direct gradient boosting, **no calendar** | 27.09 | 63.6 |
| Direct gradient boosting + calendar | 13.80 | 21.1 |
| **Direct linear + calendar** | **10.64** | 16.9 |

Read the table carefully:

**Features matter more than the model.** The same linear model gives 18.98
without the calendar and 10.64 with it. The same gradient boosting gives 27.09
and 13.80. Changing the model moves things by 3 points at most; adding
features by 8–13.

**Machine learning is no miracle.** The best machine learning result (10.64)
is neck and neck with the ARIMA that gets the same calendar information
(10.23). Without the calendar they are **worse** than seasonal naive.

**The complex model loses on this data.** A single series, a thousand rows, a
marked trend: these are not the conditions in which gradient boosting is
strong.

## 8. So when is machine learning the choice?

| Case | Why |
|---|---|
| **Many series** (hundreds of products, shops) | One model learns from all of them; no separate ARIMA per series |
| **Many external variables** | Trees find dozens of columns and the interactions between them by themselves |
| **Non-linear effects** | Thresholds such as "sales fall once the temperature passes 25" |
| **New series with a short past** | A pattern learnt from similar series carries over |
| **Long, rich data** | Tens of thousands of rows make memorising harder |

For a single, short, regular series the classical methods (Sections 16–18) are
usually enough and need less maintenance. The order is always the same:
**baseline → classical model → machine learning if needed**, all on the same
rig.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Forgetting `shift` before `rolling` | Leakage; a fake improvement | `y.shift(1).rolling(n)` |
| Shuffled cross-validation | An optimistic error | `TimeSeriesSplit` |
| Lags shorter than the horizon | Information not available at forecast time | At least a lag of `h` for `h` steps |
| Forecasting the level with a tree on a trending series | The forecast hits a ceiling | Make the target a difference or a ratio |
| Fitting a scaler on all the data | Test information leaks into training | `fit` on the training data only |
| Being pleased with the training error | Memorising | The out-of-sample error, a rolling origin |
| Not comparing with a baseline | A loss taken for a gain | Seasonal naive on the same rig |
| Only ever swapping the model | Small movements | Enrich the features first |

## Summary

- Forecasting is turned into a **table problem**: lags, windows, calendar,
  external variables; the target is that day's value.
- Every feature must be **computable** at forecast time: `shift` first, a lag
  at least as long as the horizon.
- **Trees cannot extrapolate the level**; on a trending series turn the target
  into a difference.
- Validation is **by time**: `TimeSeriesSplit`, a rolling origin.
- Multi-step forecasts: recursive (errors accumulate), direct with safe
  features, or a model per horizon.
- On this series the best result is **a linear model + the calendar**: 10.64.
  Gradient boosting is behind; without the calendar every model is worse than
  seasonal naive.
- **The gain comes from the features.** Machine learning comes into its own on
  problems with many series and many variables.

Until now every forecast has been a single number. Yet saying "310 will be
sold tomorrow" is not enough; you need to say "between 280 and 340". The next
section measures uncertainty.
