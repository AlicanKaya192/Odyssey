# Overall Review

Over twenty-two sections you learnt tools one at a time: reading dates,
resampling, decomposing, forecasting, giving intervals, catching anomalies.
There is no new tool in this section. You use them all in **a single job**,
from start to finish.

The job: a city's bike rental system hands over three years of daily rental
records and asks: **how many bikes will be rented on each of the next 28
days?**

## The flow

<figure class="fig">
<div class="flow">
<span class="node">Raw dump</span><span class="arrow">→</span>
<span class="node">Regular series</span><span class="arrow">→</span>
<span class="node">Diagnosis</span><span class="arrow">→</span>
<span class="node">Baseline</span><span class="arrow">→</span>
<span class="node">Rig</span><span class="arrow">→</span>
<span class="node">Model</span><span class="arrow">→</span>
<span class="node">Interval</span><span class="arrow">→</span>
<span class="node acc">Monitoring</span>
</div>
<figcaption>Every time series job moves in this order. Skipping steps is tempting; the most expensive mistakes come from the steps skipped.</figcaption>
</figure>

## 1. From the raw dump to a regular series

The dump (`bike_raw.csv`) arrives the way it does in real life: dates written
as `29.01.2022`, rows out of order, some days written twice, some not there at
all.

```python
import pandas as pd

raw = pd.read_csv("bike_raw.csv")
raw["date"] = pd.to_datetime(raw["date"], format="%d.%m.%Y")     # Section 02

print(len(raw), int(raw.duplicated().sum()))                     # 1093 6

rentals = raw.drop_duplicates().set_index("date")["rentals"]
rentals = rentals.sort_index().asfreq("D")                       # Section 03

print(int(rentals.isna().sum()))                                 # 9
```

Three decisions, all three from earlier sections:

- **Write the format explicitly** (`format=`). Without it, whether
  `03.04.2022` is March or April would be left to pandas' guess.
- **`asfreq("D")` makes the gaps visible.** Nine days are missing; the longest
  gap is four days. Without `asfreq` those days would be skipped silently and
  `shift(7)` would take "seven rows back" for "seven days back".
- **Look at the outlier.** The lowest value is 9 rentals on 16 July 2024; a
  week earlier 600, a week later 311. A system fault: not real demand, so it
  counts as missing.

The missing days and the fault day were filled with the mean of a week before
and a week after (Section 13). The result: a series of 1096 days with no gaps.

## 2. Get to know the series

Before building a model, look at the series (Sections 05–12):

| Question | Tool | Finding |
|---|---|---|
| Is it growing? | `resample("YS").sum()` | +14.8% and +11.5% a year |
| A weekly pattern? | `groupby(dayofweek).mean()` | Saturday is 1.35 times Monday |
| A yearly pattern? | `groupby(month).mean()` | July is 2.4 times January |
| Stationary? | `adfuller` | p = 0.33 in levels (no); 0.00 once differenced |
| An external factor? | Join with the weather data | A rainy day is 0.55 of a dry one |

Three things were learnt: there are two seasonalities (weekly and yearly), the
swing grows with the level (multiplicative: **the logarithm**), and what moves
the series most is **rain**. The last one will shape the rest of the job.

## 3. The baseline and the rig

First the number to beat (Section 14), then the rig that will measure it
(Section 15): 13 origins through 2024, a 28-day forecast at each.

| Method | MAE | Worst experiment |
|---|---|---|
| Naive (last value) | 112.2 | 234.9 |
| Seasonal naive (last week) | 98.6 | 199.1 |
| Weekday mean of the last four weeks | 86.9 | 129.7 |

Daily rentals average about 410; seasonal naive is off by a quarter. Note: in
this series seasonal naive is a weak baseline, because "the same day last
week" may have been rainy. The mean of four weeks smooths the noise and does
better. **You choose the baseline to suit the series too.**

## 4. The model

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.0" x2="666" y2="210.0"/><text class="dim" x="38" y="213.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="172.8" x2="666" y2="172.8"/><text class="dim" x="38" y="176.3" font-size="10.5" text-anchor="end">25</text><line class="grid" x1="44" y1="135.6" x2="666" y2="135.6"/><text class="dim" x="38" y="139.1" font-size="10.5" text-anchor="end">50</text><line class="grid" x1="44" y1="98.4" x2="666" y2="98.4"/><text class="dim" x="38" y="101.9" font-size="10.5" text-anchor="end">75</text><line class="grid" x1="44" y1="61.2" x2="666" y2="61.2"/><text class="dim" x="38" y="64.7" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="24.0" x2="666" y2="24.0"/><text class="dim" x="38" y="27.5" font-size="10.5" text-anchor="end">125</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="104.2" y1="210" x2="104.2" y2="214"/><text class="dim" x="104.2" y="226" font-size="10.5" text-anchor="middle">naive</text><line class="line" x1="204.5" y1="210" x2="204.5" y2="214"/><text class="dim" x="204.5" y="226" font-size="10.5" text-anchor="middle">seasonal naive</text><line class="line" x1="304.8" y1="210" x2="304.8" y2="214"/><text class="dim" x="304.8" y="226" font-size="10.5" text-anchor="middle">4-week mean</text><line class="line" x1="405.2" y1="210" x2="405.2" y2="214"/><text class="dim" x="405.2" y="226" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="505.5" y1="210" x2="505.5" y2="214"/><text class="dim" x="505.5" y="226" font-size="10.5" text-anchor="middle">calendar</text><line class="line" x1="605.8" y1="210" x2="605.8" y2="214"/><text class="dim" x="605.8" y="226" font-size="10.5" text-anchor="middle">calendar + true weather</text><rect class="dim" x="73.1" y="43.0" width="62.2" height="167.0" rx="3" opacity="0.9"/><rect class="dim" x="173.4" y="63.3" width="62.2" height="146.7" rx="3" opacity="0.9"/><rect class="dim" x="273.7" y="80.7" width="62.2" height="129.3" rx="3" opacity="0.9"/><rect class="dot2" x="374.1" y="91.4" width="62.2" height="118.6" rx="3" opacity="0.9"/><rect class="dot" x="474.4" y="113.1" width="62.2" height="96.9" rx="3" opacity="0.9"/><rect class="dot3" x="574.7" y="178.9" width="62.2" height="31.1" rx="3" opacity="0.9"/><text class="ink" x="104.2" y="37.8" font-size="11.5" text-anchor="middle">112.2</text><text class="ink" x="204.5" y="58.1" font-size="11.5" text-anchor="middle">98.6</text><text class="ink" x="304.8" y="75.5" font-size="11.5" text-anchor="middle">86.9</text><text class="ink" x="405.2" y="86.2" font-size="11.5" text-anchor="middle">79.7</text><text class="ink" x="505.5" y="107.9" font-size="11.5" text-anchor="middle">65.1</text><text class="ink" x="605.8" y="173.7" font-size="11.5" text-anchor="middle">20.9</text></svg>
  <figcaption>The mean MAE of the 13 experiments. Grey: the baselines. Orange: Holt–Winters. Purple: the best model that can be built from what is known in the future. The green bar is not a model but a <b>limit</b>: what would happen if the weather were known in advance.</figcaption>
</figure>

| Method | MAE | Section |
|---|---|---|
| Holt–Winters (weekly season) | 79.7 | 16 |
| Calendar model: linear on the logarithm; weekday, trend, yearly Fourier, holiday | **65.1** | 18–19 |
| Calendar + weather (seasonal normals) | 66.2 | 18 |
| Calendar + weather (the weather **that occurred**) | 20.9 | — |

Four rows, four lessons:

**Holt–Winters only knows the week.** Over a 28-day horizon the time of year
matters; the calendar model, which knows the yearly pattern, is 18% better.

**The logarithm works.** The same model fitted on levels gives 67.6. The
effects are multiplicative (rain does not cut rentals by 40, it cuts them by
38%); the logarithm makes that additive.

**A seasonal normal is not information.** The weather columns are not known in
the future. Putting the seasonal normal in their place (the mean temperature
of that day, the rain rate of that month) does not lower the error: the normal
is already inside the Fourier terms. The rule of Section 18: a variable you
**do not know** in the future does not improve the model.

**The remaining error is a lack of information, not of model.** If the weather
were really known the error would fall from 65 to 21. A more complex model
(trees, ARIMA) cannot close that gap, because what is missing is not a method
but **whether it will rain**. Nobody can know the rain of a month from now.

This is the most important lesson of the track: before changing the model, ask
**where the error comes from**.

## 5. State the uncertainty

The point forecast is off by 16% and you know why. The honest thing is to say
so with an interval (Section 20). From the relative errors of the 13
experiments:

| | Value |
|---|---|
| Mean relative error | +0.3% (unbiased) |
| 10% quantile | −31% |
| 90% quantile | +26% |
| Coverage of the 80% interval (each experiment, with the errors of the other 12) | 0.80 |

The interval is wide and **not symmetric**: longer downwards. The reason is
rain again: the error of the model averages −28% on rainy days and +11% on dry
ones. The model forecasts "an average day" for every day; real days are either
dry or rainy.

The forecast for the first 28 days of January 2025:

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="219.3" x2="666" y2="219.3"/><text class="dim" x="38" y="222.8" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="188.0" x2="666" y2="188.0"/><text class="dim" x="38" y="191.5" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="156.6" x2="666" y2="156.6"/><text class="dim" x="38" y="160.1" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="125.3" x2="666" y2="125.3"/><text class="dim" x="38" y="128.8" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="94.0" x2="666" y2="94.0"/><text class="dim" x="38" y="97.5" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="62.6" x2="666" y2="62.6"/><text class="dim" x="38" y="66.1" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="31.3" x2="666" y2="31.3"/><text class="dim" x="38" y="34.8" font-size="10.5" text-anchor="end">600</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="89.1" y1="230" x2="89.1" y2="234"/><text class="dim" x="89.1" y="246" font-size="10.5" text-anchor="middle">25 Nov</text><line class="line" x1="215.3" y1="230" x2="215.3" y2="234"/><text class="dim" x="215.3" y="246" font-size="10.5" text-anchor="middle">9 Dec</text><line class="line" x1="341.5" y1="230" x2="341.5" y2="234"/><text class="dim" x="341.5" y="246" font-size="10.5" text-anchor="middle">23 Dec</text><line class="line" x1="467.7" y1="230" x2="467.7" y2="234"/><text class="dim" x="467.7" y="246" font-size="10.5" text-anchor="middle">6 Jan</text><line class="line" x1="593.9" y1="230" x2="593.9" y2="234"/><text class="dim" x="593.9" y="246" font-size="10.5" text-anchor="middle">20 Jan</text><polygon class="dot" opacity="0.2" style="stroke:none" points="422.6,118.7 431.6,116.0 440.6,112.9 449.7,89.2 458.7,108.2 467.7,123.9 476.7,119.1 485.7,119.7 494.7,117.0 503.7,113.9 512.8,90.2 521.8,109.0 530.8,124.5 539.8,119.6 548.8,120.2 557.8,117.3 566.8,114.1 575.9,90.5 584.9,109.1 593.9,124.5 602.9,119.5 611.9,120.0 620.9,117.1 629.9,113.8 639.0,89.9 648.0,108.5 657.0,123.9 666.0,118.8 666.0,164.0 657.0,166.9 648.0,158.4 639.0,148.2 629.9,161.3 620.9,163.1 611.9,164.7 602.9,164.5 593.9,167.2 584.9,158.7 575.9,148.5 566.8,161.5 557.8,163.3 548.8,164.8 539.8,164.5 530.8,167.2 521.8,158.7 512.8,148.4 503.7,161.3 494.7,163.1 485.7,164.6 476.7,164.2 467.7,166.9 458.7,158.2 449.7,147.8 440.6,160.8 431.6,162.5 422.6,164.0"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,100.9 53.0,82.7 62.0,74.5 71.0,70.2 80.1,91.2 89.1,145.7 98.1,104.0 107.1,115.0 116.1,114.6 125.1,152.6 134.1,81.8 143.2,144.1 152.2,155.1 161.2,119.3 170.2,101.5 179.2,102.4 188.2,85.5 197.2,119.0 206.3,92.1 215.3,129.4 224.3,126.2 233.3,142.5 242.3,114.0 251.3,162.3 260.3,81.8 269.4,124.4 278.4,131.6 287.4,130.6 296.4,131.9 305.4,136.0 314.4,155.4 323.4,104.0 332.5,151.0 341.5,129.7 350.5,163.5 359.5,126.6 368.5,158.8 377.5,153.8 386.6,137.2 395.6,102.7 404.6,126.6 413.6,162.0"/><polyline class="curve" style="stroke-width:2.2" points="422.6,139.3 431.6,137.1 440.6,134.7 449.7,115.8 458.7,130.9 467.7,143.5 476.7,139.6 485.7,140.1 494.7,137.9 503.7,135.5 512.8,116.7 521.8,131.6 530.8,143.9 539.8,140.0 548.8,140.5 557.8,138.2 566.8,135.7 575.9,116.9 584.9,131.7 593.9,143.9 602.9,140.0 611.9,140.3 620.9,138.0 629.9,135.4 639.0,116.4 648.0,131.2 657.0,143.4 666.0,139.4"/><line class="curve3" stroke-dasharray="4 4" x1="418.1" y1="30" x2="418.1" y2="230"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">actual</text><line class="curve" x1="142" y1="38" x2="160" y2="38"/><text class="ink" x="166" y="42" font-size="11">forecast</text><rect class="dot" x="244" y="33" width="18" height="10" opacity="0.3"/><text class="ink" x="268" y="42" font-size="11">80% interval</text></svg>
  <figcaption>The last six weeks of 2024 and the first 28 days of January 2025. The sharp drops in the past are rainy days; the forecast cannot know them, so it draws a smooth weekly pattern and states the uncertainty with the band.</figcaption>
</figure>

7541 rentals in total. For 1 January 255, with an 80% interval of 177–321. The
answer to how many bikes to keep ready is not the point forecast but a
**quantile**: the upper end, if running out of bikes is expensive.

## 6. After delivery: monitor

The job is not over when the forecast is delivered (Section 21):

- **Every day** compare what happened with the interval. Falling outside an
  80% interval one day in five is expected; falling outside on the same side
  several days in a row means something has changed.
- **Accumulate the error** (CUSUM): a small but lasting deviation is a level
  shift.
- **Flag anomalies and repair them before training**; after a level shift
  rebuild the model.
- **Retrain regularly.** The trend is 13% a year; coefficients from a year ago
  go stale.
- **Do better at a short horizon.** For tomorrow there is a weather forecast;
  the 28-day forecast and tomorrow's forecast need not be the same model.

## Section by section

| Section | The one thing to remember |
|---|---|
| 00 What Is a Time Series? | Order is information; you cannot shuffle the rows |
| 01 Dates and Times | A `datetime` is a moment, a `timedelta` a duration |
| 02 Dates in pandas | Write the format explicitly; see broken dates with `errors="coerce"` |
| 03 The Time Index | With dates as the index come slicing, alignment, `asfreq` |
| 04 Periods and Calendars | A moment and a span differ; business days and holiday calendars |
| 05 Resampling | When the frequency changes, **how you summarise** decides the result |
| 06 Shifts and Differences | `shift` carries the past to today; `diff` gives the change |
| 07 Rolling Windows | A window smooths noise; a centred window sees the future |
| 08 Many Series at Once | Long and wide form; alignment on the index |
| 09 Visualisation | Plot first; a separate chart for each question |
| 10 Components and Decomposition | Trend + season + residual; additive or multiplicative |
| 11 Stationarity | The logarithm tames the variance, the difference the trend |
| 12 Autocorrelation | How much a series resembles its own past; is the residual white noise |
| 13 Missing Data and Outliers | Make it visible first; do not delete the row, repair the value |
| 14 Baseline Forecasts | A model that cannot beat the baseline is no use |
| 15 Validating Forecasts | Split by time; do not trust a single split |
| 16 Exponential Smoothing | More weight on the recent past: level, trend, season |
| 17 ARIMA | Difference, model the autocorrelation; check the residual |
| 18 External Variables | Only a variable known in the future helps |
| 19 Forecasting with Machine Learning | Features from the past; a tree cannot extrapolate the level |
| 20 Prediction Intervals | One number is not enough; test the interval too |
| 21 Anomalies and Change Points | Flag what is temporary, rebuild around what is lasting |

## The ten rules of the track

1. **Plot first.** No statistic says what a chart shows at a glance.
2. **Build a regular index.** A missing day is an invisible error.
3. **Do not use the future.** In features, filling, scaling, validation:
   everywhere, the past only.
4. **Start with a baseline.** A model that cannot beat seasonal naive is just
   complexity.
5. **Do not trust a single split.** A rolling origin, several experiments, the
   worst experiment.
6. **Choose the measure to suit the job.** MAE, RMSE, MASE, pinball: each
   answers a different question.
7. **The gain comes from information.** In this track every big improvement
   came not from a new method but from new information: the calendar, a
   holiday, a campaign.
8. **Look at the residual.** A pattern in the residual means the model is
   missing something.
9. **State the uncertainty and test it.** A forecast with no interval is half
   a forecast.
10. **Monitor after delivery.** The series changes; the model goes stale.

## What you can do

- Turn a messy date column into a regular series with no gaps.
- Measure and plot the trend, the season and the autocorrelation of a series.
- Find missing values and outliers and repair them with a reason.
- Test a forecast against a baseline on a rig that respects time.
- Build forecasts with exponential smoothing, ARIMA, regression with external
  variables and tree models; say, by measuring, which works when.
- Add an interval to a forecast and measure whether the interval is honest.
- Tell an anomaly from a change point.

## What you cannot do yet

- **Forecasting many series.** Forecasting a thousand shops with one model
  (global models, hierarchical reconciliation).
- **Multivariate models.** Cases where series affect each other (VAR).
- **Volatility models.** Changing variance in financial series (GARCH).
- **Deep learning.** Neural networks on very long and very many series.
- **Causality.** "Did the campaign raise sales?" is a different question from
  forecasting and needs different tools.

All of these sit on the foundation of this track: a regular index, validation
that respects time, a baseline, the residual.

## A last word

In the bike example the best model did not know about **rain**, the source of
two thirds of its error, and could not have known. The job was done all the
same: a forecast a third better than the baseline, an honest interval and a
clear account of where the error comes from.

Forecasting a time series is not knowing the future. It is **using what is
known to the full, stating the size of what is not**, and telling the two
apart.
