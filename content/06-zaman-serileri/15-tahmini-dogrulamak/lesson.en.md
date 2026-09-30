# Validating a Forecast

In Section 14 you measured the error of seasonal naive: 11.6 at a 28-day
horizon. How far can you trust that number?

Repeat the same experiment from **thirteen different origins** through 2024
and the average error comes out as 17.9; 9.4 in the best period, 41.3 in the
worst. The 11.6 you measured first was not wrong, but it was the number of
**a lucky period**.

This section teaches you to measure a forecast honestly: which error measure,
how many experiments, on which data. Every model from here on (exponential
smoothing, ARIMA, machine learning) will be graded by the rig you build here.

## 1. Error measures

The error is always the same: **actual − forecast**. The difference is in how
you reduce those errors to one number.

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>MAE</span><span>The mean of the absolute errors. In the unit of the series, the easiest to read.</span></div>
<div class="anat-row"><span>RMSE</span><span>The square root of the mean squared error. Punishes large errors heavily.</span></div>
<div class="anat-row"><span>MAPE</span><span>The mean of the absolute percentage errors. Unit-free; breaks down near zero.</span></div>
<div class="anat-row"><span>MASE</span><span>The MAE relative to the error of the naive method on the training data. Unit-free and sturdy; below 1 beats naive.</span></div>
<div class="anat-row"><span>Bias</span><span>The mean of the errors. It shows not the size but the <b>direction</b>.</span></div>
</div>
<figcaption>None of them is "the right one"; each answers a different question.</figcaption>
</figure>

```python
import numpy as np


def mae(actual, forecast):
    return np.mean(np.abs(actual - forecast))


def rmse(actual, forecast):
    return np.sqrt(np.mean((actual - forecast) ** 2))


def mape(actual, forecast):
    return np.mean(np.abs(actual - forecast) / np.abs(actual)) * 100
```

For the experiment of Section 14 (training up to 5 November, 28 days, seasonal
naive):

| MAE | RMSE | MAPE | Bias |
|---|---|---|---|
| 11.64 | 13.98 | 3.46% | +6.79 |

## 2. MAE or RMSE?

The RMSE is always greater than or equal to the MAE. The **gap** between them
carries information: if the errors are alike the two are close; with a few
large errors the RMSE pulls away.

The one-step error of seasonal naive on the web traffic:

| | MAE | RMSE | RMSE / MAE |
|---|---|---|---|
| The whole year | 307.2 | 728.6 | 2.37 |
| Without the 6 days affected by the three outliers | 225.3 | 303.3 | 1.35 |

6 days out of 366 inflate the MAE by 36% and the RMSE by **140%**. (Three
outlier days produce six errors: the forecast misses on the day itself and
misses again a week later, when it copies that day.)

Which one to choose depends on **the cost of a large error**:

- If a large error costs many times a small one (a stock-out, a power cut):
  **RMSE**. It does not forgive a big miss.
- If every unit of error costs the same and the data has outlier days:
  **MAE**. A few bad days do not decide the whole grade.

## 3. MAPE and its traps

A percentage error is tempting: "we are off by 3.5 percent" is a sentence
everyone understands, and it allows series of different scales to be compared.
But it has three traps.

**It blows up at zero.** If the actual value is zero the division is
undefined. For shop C, which is closed on Sundays, the MAPE of the naive
forecast is `inf`: the denominator is zero on 52 Sundays.

**It swells for small values.** If the actual is 2 and the forecast 4, the
error is 100%. For a product selling a few units a day the MAPE grows
meaninglessly.

**It is not symmetric.** The same miss of 50 units is punished differently
depending on its direction:

| Actual | Forecast | Percentage error |
|---|---|---|
| 100 | 150 | 50% |
| 150 | 100 | 33% |

A forecast that is too high is punished more than one that is too low; a model
chosen by MAPE leans towards **forecasting low**.

Use MAPE for series that are always positive and far from zero. For the rest,
MASE.

## 4. MASE: scale-free and sturdy

The idea: divide the error by **the typical error of the naive method on the
same series**.

$$\text{MASE} = \frac{\text{MAE}_{\text{forecast}}}{\text{one-step MAE of seasonal naive on the training data}}$$

```python
def mase(actual, forecast, train, m):
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return mae(actual, forecast) / scale
```

`train[m:] - train[:-m]` is the difference of each value from the one a season
earlier. The denominator comes from the training data; it does not touch the
test data and does not come out as zero even if the series contains zeros.

The same table for three different series:

| Series and method | MAE | MAPE | MASE |
|---|---|---|---|
| Daily sales, seasonal naive | 11.6 | 3.5% | 0.88 |
| Monthly passengers, seasonal naive | 40.4 | 10.3% | 1.82 |
| Monthly passengers, with growth | 11.1 | 2.8% | 0.50 |
| Share, naive (40 days) | 18.8 | 11.5% | 10.36 |

The MAEs cannot be compared (different units). The MASE can: **below 1** means
"off by less than one-step naive". The 10.36 on the share row says this:
forecasting 40 days ahead is ten times harder than forecasting tomorrow.

## 5. One split is not enough: a rolling origin

A single training/test split is a single experiment. Its result depends on
whether those 28 days were easy or hard. The fix is to repeat the experiment:
move the origin forward through the past, forecast again at every stop and
measure. This is called **backtesting**, or a **rolling origin**.

<figure class="fig">
  <svg viewBox="0 0 680 228" width="680" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="86" y="48" font-size="11.5" text-anchor="end">experiment 1</text><rect class="dot" x="96.0" y="34" width="236.7" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="334.7" y="34" width="64.2" height="20" rx="4"/><text class="dim" x="86" y="80" font-size="11.5" text-anchor="end">experiment 2</text><rect class="dot" x="96.0" y="66" width="302.9" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="400.9" y="66" width="64.3" height="20" rx="4"/><text class="dim" x="86" y="112" font-size="11.5" text-anchor="end">experiment 3</text><rect class="dot" x="96.0" y="98" width="369.2" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="467.2" y="98" width="64.3" height="20" rx="4"/><text class="dim" x="86" y="144" font-size="11.5" text-anchor="end">experiment 4</text><rect class="dot" x="96.0" y="130" width="435.5" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="533.5" y="130" width="64.2" height="20" rx="4"/><text class="dim" x="86" y="176" font-size="11.5" text-anchor="end">experiment 5</text><rect class="dot" x="96.0" y="162" width="501.7" height="20" rx="4" opacity="0.28"/><rect class="dot2" x="599.7" y="162" width="64.3" height="20" rx="4"/><rect class="dot" x="96" y="5" width="22" height="10" rx="3" opacity="0.28"/><text class="ink" x="124" y="14" font-size="11.5">training</text><rect class="dot2" x="196" y="5" width="22" height="10" rx="3"/><text class="ink" x="224" y="14" font-size="11.5">test</text><line class="line" x1="96" y1="202" x2="658" y2="202"/><polygon class="ink" points="664,202 656,198 656,206"/><text class="dim" x="664" y="218" font-size="11" text-anchor="end">time</text></svg>
  <figcaption>A rolling origin with an expanding window. In each experiment the training gets a little longer and the test follows right after it. The test is never inside the training.</figcaption>
</figure>

```python
def backtest(y, forecast, first, step, h, count):
    scores = []
    for i in range(count):
        cut = pd.Timestamp(first) + pd.Timedelta(days=step * i)
        train = y.loc[:cut]
        test = y.loc[cut + pd.Timedelta(days=1):].iloc[:h]
        scores.append(mae(test.to_numpy(), forecast(train, h)))
    return scores
```

`forecast` is a function: it takes the training data and the horizon and
returns `h` forecasts. On every round it sees only the data up to that moment.

13 experiments, starting on 2 January 2024 and moving 28 days at a time:

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.0" x2="666" y2="210.0"/><text class="dim" x="38" y="213.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="170.0" x2="666" y2="170.0"/><text class="dim" x="38" y="173.5" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="130.0" x2="666" y2="130.0"/><text class="dim" x="38" y="133.5" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="90.0" x2="666" y2="90.0"/><text class="dim" x="38" y="93.5" font-size="10.5" text-anchor="end">30</text><line class="grid" x1="44" y1="50.0" x2="666" y2="50.0"/><text class="dim" x="38" y="53.5" font-size="10.5" text-anchor="end">40</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="72.3" y1="210" x2="72.3" y2="214"/><text class="dim" x="72.3" y="226" font-size="10.5" text-anchor="middle">2 Jan</text><line class="line" x1="166.5" y1="210" x2="166.5" y2="214"/><text class="dim" x="166.5" y="226" font-size="10.5" text-anchor="middle">27 Feb</text><line class="line" x1="260.8" y1="210" x2="260.8" y2="214"/><text class="dim" x="260.8" y="226" font-size="10.5" text-anchor="middle">23 Apr</text><line class="line" x1="355.0" y1="210" x2="355.0" y2="214"/><text class="dim" x="355.0" y="226" font-size="10.5" text-anchor="middle">18 Jun</text><line class="line" x1="449.2" y1="210" x2="449.2" y2="214"/><text class="dim" x="449.2" y="226" font-size="10.5" text-anchor="middle">13 Aug</text><line class="line" x1="543.5" y1="210" x2="543.5" y2="214"/><text class="dim" x="543.5" y="226" font-size="10.5" text-anchor="middle">8 Oct</text><line class="line" x1="637.7" y1="210" x2="637.7" y2="214"/><text class="dim" x="637.7" y="226" font-size="10.5" text-anchor="middle">3 Dec</text><rect class="dot" x="57.7" y="44.9" width="29.2" height="165.1" rx="3" opacity="0.9"/><rect class="dot" x="104.8" y="166.0" width="29.2" height="44.0" rx="3" opacity="0.9"/><rect class="dot" x="151.9" y="146.7" width="29.2" height="63.3" rx="3" opacity="0.9"/><rect class="dot" x="199.0" y="139.4" width="29.2" height="70.6" rx="3" opacity="0.9"/><rect class="dot" x="246.2" y="169.1" width="29.2" height="40.9" rx="3" opacity="0.9"/><rect class="dot" x="293.3" y="157.0" width="29.2" height="53.0" rx="3" opacity="0.9"/><rect class="dot" x="340.4" y="172.4" width="29.2" height="37.6" rx="3" opacity="0.9"/><rect class="dot" x="387.5" y="169.7" width="29.2" height="40.3" rx="3" opacity="0.9"/><rect class="dot" x="434.6" y="110.3" width="29.3" height="99.7" rx="3" opacity="0.9"/><rect class="dot" x="481.8" y="159.9" width="29.2" height="50.1" rx="3" opacity="0.9"/><rect class="dot" x="528.9" y="148.6" width="29.2" height="61.4" rx="3" opacity="0.9"/><rect class="dot" x="576.0" y="163.4" width="29.2" height="46.6" rx="3" opacity="0.9"/><rect class="dot" x="623.1" y="49.0" width="29.2" height="161.0" rx="3" opacity="0.9"/><line class="curve2" stroke-dasharray="4 4" x1="44" y1="138.2" x2="666" y2="138.2"/><text class="ink" x="378.6" y="129.4" font-size="11.5" text-anchor="middle">mean 18.0</text><text class="ink" x="72.3" y="38.9" font-size="11" text-anchor="middle">41.3</text><text class="ink" x="637.7" y="43.0" font-size="11" text-anchor="middle">40.2</text></svg>
  <figcaption>The 28-day error of seasonal naive from 13 different origins. The horizontal axis is the day the training ends. The first and the last experiment are three times the others: the turn of the year.</figcaption>
</figure>

| | MAE |
|---|---|
| Mean of the 13 experiments | 17.95 |
| Standard deviation | 10.94 |
| The best experiment | 9.39 |
| The worst experiment | 41.29 |
| The single experiment of Section 14 | 11.64 |

The right answer is not "11.6" but "**18 on average, between 9 and 41
depending on the period**". The two bad experiments are at the start and the
end of the year: the year-end climb and the drop that follows. That is a
finding too: the baseline struggles most around the turn of the year.

## 6. Comparing two methods fairly

Seasonal naive, or the mean of the last four weeks?

| Experimental design | Seasonal naive | Mean of four weeks |
|---|---|---|
| A single split (5 November) | **11.64** | 14.84 |
| 13 origins, 28 days apart | 17.95 | **17.20** |
| 48 origins, 7 days apart | **15.05** | 15.42 |

Three designs, three different "winners". Seasonal naive is ahead in 5 of the
13 experiments, the other in 8. The gap between them (0.4–0.8) is tiny next to
the variation between experiments (11).

The honest conclusion: **a tie.** Had you looked at the single split you would
have said "seasonal naive is 22% better", and you would have been wrong.

To say one method is better than another, the difference has to go **the same
way in most experiments** and must not be small compared with the variation
between experiments.

## 7. Error by horizon

Backtesting gives one more thing: a separate error for each horizon. Average
the errors of the 13 experiments by the week of the horizon:

| Horizon | Week 1 | Week 2 | Week 3 | Week 4 |
|---|---|---|---|---|
| Seasonal naive MAE | 15.9 | 17.0 | 18.2 | 20.7 |

Look at the row for the horizon your decision depends on. Week 1 matters to
whoever plans tomorrow's shift, week 4 to whoever places next month's order;
the best model for the two may not be the same.

## 8. Expanding and sliding windows

How far back should the training data go in each experiment?

<figure class="fig">
<div class="versus">
<div><h4>Expanding window</h4><p>Training always starts at the very beginning; it grows with each experiment.</p><p>Pro: uses all the data.</p><p>Con: if old periods do not represent today, they drag the forecast back.</p></div>
<div><h4>Sliding window</h4><p>Training has a fixed length; its start moves forward too.</p><p>Pro: adapts quickly to a changing series.</p><p>Con: less data; cannot see long patterns.</p></div>
</div>
<figcaption>The <code>backtest</code> above is an expanding window. For a sliding one: <code>train = y.loc[:cut].iloc[-n:]</code>.</figcaption>
</figure>

For the mean forecast the difference is marked: the mean of all the past gives
53.1, the mean of the last 56 days 43.3. Because the series is growing, the
days of three years ago pull today's level down.

## 9. Validation and test

The moment you choose a setting (a window length, a kind of model, a
coefficient) **by looking at the error**, that error is no longer an honest
measurement: you chose the one that looked best, and you chose some of its
luck too.

That is why the data is split in three:

<figure class="fig">
<div class="flow">
<span class="node">Training<br>the model learns</span><span class="arrow">→</span>
<span class="node">Validation<br>you choose settings</span><span class="arrow">→</span>
<span class="node acc">Test<br>you measure once, at the end</span>
</div>
<figcaption>No decision is made on the test data. The moment one is, the test has turned into validation.</figcaption>
</figure>

An example: what should `k` be in the "mean of the last `k` weeks" method? The
first 10 of the 13 experiments are validation, the last 3 the test:

| `k` | Validation MAE | Test MAE |
|---|---|---|
| 1 | 16.61 | **22.42** |
| 2 | 15.84 | 22.50 |
| 3 | **15.16** | 22.97 |
| 5 | 15.40 | 25.13 |
| 8 | 16.17 | 29.76 |

By validation you choose `k = 3`. The number to report is not the 15.16 of
validation but the **22.97** of the test. Looking at the test column, saying
"actually `k = 1` was better" and reporting 22.42 is cheating: you made that
decision having seen the test data.

(Why is the test so much worse? The last three experiments are the final
quarter of the year, the hardest period. Validation and test need not be
equally hard; that goes in the report too.)

## 10. A leakage check

The most dangerous mistake in validation is the model seeing something it
could not know at forecast time. The result looks unbelievably good and
collapses in real use.

1. **Is the split by time?** No random shuffling.
2. **Does every number come from training only?** A mean, a scale, a growth
   rate, a seasonal factor: all are recomputed from `train` in every
   experiment.
3. **Do the features look backwards?** `shift(1)` first, then `rolling`. No
   `center=True`, `shift(-k)`, `interpolate` or `bfill`.
4. **Is the preprocessing inside the experiment?** If outlier repair, filling
   or decomposition was applied once to the whole series, the future has
   leaked.
5. **Is the horizon realistic?** If you will forecast 28 days ahead, a feature
   using yesterday's value will not be available at forecast time.

scikit-learn provides the same splitting ready-made:

```python
from sklearn.model_selection import TimeSeriesSplit

splitter = TimeSeriesSplit(n_splits=5, test_size=28)
for train_idx, test_idx in splitter.split(s):
    train, test = s.iloc[train_idx], s.iloc[test_idx]
```

The test blocks are lined up one after another, from the end backwards; the
training is everything before the test each time. In Section 19 you will test
machine learning models with it.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Trusting a single split | The number of a lucky or unlucky period | Many experiments with a rolling origin |
| Reporting only the mean | The variation is hidden | The mean, the spread, the worst experiment |
| Declaring a "winner" on a small gap | Taking noise for a finding | Does the difference go the same way in most experiments? |
| MAPE on a series with zeros | `inf`, or days silently skipped | MAE or MASE |
| Comparing MAE across series of different scales | Meaningless | MASE |
| Choosing settings on the test | An optimistic result that does not repeat | Settings on validation, report on the test |
| Applying preprocessing once to the whole series | Leakage | On the training data only, in every experiment |
| Reporting a one-step error for multi-step use | Far worse in reality | Measure at the horizon that will be used |

## Summary

- **MAE** is readable and robust; **RMSE** punishes a large error; **MAPE** is
  unit-free but breaks down at zero and for small values; **MASE** is
  unit-free and sturdy, below 1 beats naive. **Bias** shows the direction.
- A single split is one experiment. A **rolling origin** runs many; report the
  mean, the spread and the worst case together.
- If the difference between two methods is smaller than the variation between
  experiments, it is **a tie**.
- Look at the error **by horizon**, separately.
- An **expanding** window uses all the data, a **sliding** one only the recent
  past.
- Settings are chosen on **validation**; the result is measured once on the
  **test**.
- An unbelievably good result = look for **leakage** first.

The rig is ready. In Section 16 you build your first real model: exponential
smoothing, which tracks the level, the trend and the season together. The
tools of this section will grade it.
