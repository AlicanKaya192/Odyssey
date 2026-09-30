# Baseline Forecasts

For fourteen sections you have been trying to **understand** the series:
dates, patterns, components, memory, cleaning. Now, for the first time, you
look into the future.

The starting point is surprisingly simple: four methods, one line each. They
are called **baseline forecasts**, and they have two jobs. First, they often
work better than you would think. Second, and more importantly, they set a
**bar**: every model you build from now on has to beat them first. If it
cannot, its complexity means nothing.

## 1. The language of forecasting

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Training data</span><span>The past you know when making the forecast. The model sees only this.</span></div>
<div class="anat-row"><span>Test data</span><span>The last stretch you pretend not to know and keep back to compare with the forecast.</span></div>
<div class="anat-row"><span>Origin</span><span>The last moment of the training data. The forecast goes forward from here.</span></div>
<div class="anat-row"><span>Horizon</span><span>How many steps ahead you forecast: 1 day, 28 days, 12 months.</span></div>
</div>
<figcaption>One rule: a forecast is made <b>with what is known up to the origin</b>. Any calculation that looks at the test data is cheating.</figcaption>
</figure>

Let us keep back the last 28 days of the daily shop sales:

```python
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D").loc[:"2024-12-03"]

train = s.iloc[:-28]          # 2022-01-01 ... 2024-11-05
test = s.iloc[-28:]           # 2024-11-06 ... 2024-12-03
h = len(test)                 # the horizon: 28 days
```

In a time series the training and test data are **not** split at random (no
shuffling as in machine learning): the test is always **at the end**, because
the future comes after the past.

A forecast is a series too; its index is the future dates:

```python
future = pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=h, freq="D")
```

## 2. Four baseline methods

**The mean.** The future will equal the average of the past.

```python
mean_fc = pd.Series(train.mean(), index=future)            # always 255.1
```

**Naive.** The future will equal the last observation.

```python
naive_fc = pd.Series(train.iloc[-1], index=future)         # always 267
```

**Seasonal naive.** Each day will equal the same day of the previous season:
copy the last week and repeat it as often as needed.

```python
last_week = train.iloc[-7:].to_numpy()
snaive_fc = pd.Series([last_week[i % 7] for i in range(h)], index=future)
```

`i % 7` cycles the remainder from 0 to 6: day 8 takes the value of day 1
again.

**Drift.** To the naive forecast add the average daily change from the first
day of the series to the last: extend the line joining the first and the last
point.

```python
slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
drift_fc = pd.Series(train.iloc[-1] + slope * np.arange(1, h + 1), index=future)
```

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="220.0" x2="666" y2="220.0"/><text class="dim" x="38" y="223.5" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="183.0" x2="666" y2="183.0"/><text class="dim" x="38" y="186.5" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="146.0" x2="666" y2="146.0"/><text class="dim" x="38" y="149.5" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="109.0" x2="666" y2="109.0"/><text class="dim" x="38" y="112.5" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="72.0" x2="666" y2="72.0"/><text class="dim" x="38" y="75.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="35.0" x2="666" y2="35.0"/><text class="dim" x="38" y="38.5" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">9 Oct</text><line class="line" x1="202.3" y1="240" x2="202.3" y2="244"/><text class="dim" x="202.3" y="256" font-size="10.5" text-anchor="middle">23 Oct</text><line class="line" x1="360.7" y1="240" x2="360.7" y2="244"/><text class="dim" x="360.7" y="256" font-size="10.5" text-anchor="middle">6 Nov</text><line class="line" x1="519.0" y1="240" x2="519.0" y2="244"/><text class="dim" x="519.0" y="256" font-size="10.5" text-anchor="middle">20 Nov</text><rect class="box" x="355.0" y="32" width="311.0" height="208" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,216.3 55.3,191.9 66.6,150.4 77.9,114.2 89.2,137.8 100.5,217.0 111.9,221.5 123.2,188.2 134.5,183.7 145.8,154.1 157.1,106.0 168.4,151.2 179.7,201.5 191.0,209.6 202.3,182.2 213.6,191.1 224.9,155.6 236.3,97.9 247.6,135.6 258.9,203.7 270.2,202.2 281.5,193.3 292.8,187.4 304.1,137.8 315.4,92.7 326.7,132.7 338.0,203.7 349.3,207.4 360.7,195.6 372.0,178.5 383.3,145.2 394.6,76.4 405.9,128.2 417.2,200.0 428.5,205.9 439.8,180.8 451.1,180.8 462.4,129.0 473.7,102.3 485.1,114.2 496.4,203.0 507.7,197.8 519.0,197.8 530.3,171.9 541.6,133.4 552.9,96.4 564.2,121.6 575.5,205.9 586.8,192.6 598.1,185.2 609.5,185.2 620.8,156.3 632.1,85.3 643.4,114.2 654.7,205.9 666.0,190.4"/><polyline class="curve4" style="stroke-width:2.2" points="360.7,216.2 372.0,216.2 383.3,216.2 394.6,216.2 405.9,216.2 417.2,216.2 428.5,216.2 439.8,216.2 451.1,216.2 462.4,216.2 473.7,216.2 485.1,216.2 496.4,216.2 507.7,216.2 519.0,216.2 530.3,216.2 541.6,216.2 552.9,216.2 564.2,216.2 575.5,216.2 586.8,216.2 598.1,216.2 609.5,216.2 620.8,216.2 632.1,216.2 643.4,216.2 654.7,216.2 666.0,216.2"/><polyline class="curve2" style="stroke-width:2.2" points="360.7,207.4 372.0,207.4 383.3,207.4 394.6,207.4 405.9,207.4 417.2,207.4 428.5,207.4 439.8,207.4 451.1,207.4 462.4,207.4 473.7,207.4 485.1,207.4 496.4,207.4 507.7,207.4 519.0,207.4 530.3,207.4 541.6,207.4 552.9,207.4 564.2,207.4 575.5,207.4 586.8,207.4 598.1,207.4 609.5,207.4 620.8,207.4 632.1,207.4 643.4,207.4 654.7,207.4 666.0,207.4"/><polyline class="curve" style="stroke-width:2.2" points="360.7,193.3 372.0,187.4 383.3,137.8 394.6,92.7 405.9,132.7 417.2,203.7 428.5,207.4 439.8,193.3 451.1,187.4 462.4,137.8 473.7,92.7 485.1,132.7 496.4,203.7 507.7,207.4 519.0,193.3 530.3,187.4 541.6,137.8 552.9,92.7 564.2,132.7 575.5,203.7 586.8,207.4 598.1,193.3 609.5,187.4 620.8,137.8 632.1,92.7 643.4,132.7 654.7,203.7 666.0,207.4"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve4" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">mean</text><line class="curve2" x1="216" y1="40" x2="234" y2="40"/><text class="ink" x="240" y="44" font-size="11">naive</text><line class="curve" x1="297" y1="40" x2="315" y2="40"/><text class="ink" x="321" y="44" font-size="11">seasonal naive</text></svg>
  <figcaption>The shaded area is the test period (28 days); everything to its left is training data. The mean and naive are flat lines; drift is not drawn because it sits almost on top of naive. Seasonal naive repeats the last week four times.</figcaption>
</figure>

## 3. Measure

The forecast error is the actual value minus the forecast. To reduce it to one
number, the plainest measure is the **mean absolute error** (MAE): drop the
sign of the errors and average them.

```python
def mae(actual, forecast):
    return (actual - forecast).abs().mean()
```

| Method | MAE (28 days) |
|---|---|
| Mean | 76.0 |
| Drift | 64.6 |
| Naive | 64.1 |
| Seasonal naive | 11.6 |

In a period averaging 331 units a day, seasonal naive is off by 12 units:
3.5%. With no model at all, just by copying the last week.

Why are the other three poor? They all draw a **flat line**; they do not know
the weekly pattern. The naive forecast says "267 were sold on Tuesday, so
Saturday will be 267 too". Drift does not help either: it computes its slope
from the first and last day only, and the first day (1 January 2022) happens
to be a high Saturday. **Drift looks at two points; if those two are unlucky,
the slope is meaningless.**

## 4. Every series has its own bar

Which baseline is best depends on the structure of the series. Three series,
three outcomes:

| Series | Structure | Mean | Naive | Drift | Seasonal naive |
|---|---|---|---|---|---|
| Daily sales, 28 days | A strong weekly pattern | 76.0 | 64.1 | 64.6 | **11.6** |
| Share price, 40 days | A random walk | 32.3 | 18.8 | **17.6** | no season |
| Monthly passengers, 12 months | Trend + yearly season | 167.8 | 55.8 | 48.2 | **40.4** |

- In a **random walk** (Section 11) the freshest information is the last
  value: naive and drift are neck and neck, the mean far behind.
- In a **seasonal series** seasonal naive is far ahead.
- In a **trending series the mean is the worst**: the average of 11 years
  (222) is far below today's level (345).

The general rule: get to know the series (Sections 09–12) and make the
baseline that fits its structure the bar.

## 5. Bias: is the error always on the same side?

Run the same 28-day experiment a month later: training up to 3 December, the
test being the rest of December.

```python
error = test - snaive_fc
print(round(error.abs().mean(), 2), round(error.mean(), 2))     # 40.25 40.25
```

The MAE went from 11.6 to 40.3. The second number matters even more: the
**mean** of the errors is also 40.25. If the mean comes out the same without
taking absolute values, **all the errors have the same sign**: the forecast
was too low on 28 days out of 28.

The mean of the error is called the **bias**:

- Close to zero: the forecast is sometimes high, sometimes low; no systematic
  drift.
- Positive: the forecast is systematically **low** (the actual is always
  above).
- Negative: the forecast is systematically **high**.

Why low? December is a month of rising sales; seasonal naive copies the week
at the end of November and cannot see the year-end climb. **Baselines repeat
what they know; they cannot foresee a new direction.**

The passenger series is the same: seasonal naive copies 2023 for 2024. MAE
40.4, bias +40.4: low in twelve months out of twelve. The series is growing
and the copy is a year behind.

## 6. Growing the baseline

If the cause of the bias is known, the fix is simple too. For the passenger
series, multiply last year's values by the growth rate:

```python
p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]

train, test = p.loc[:"2023"], p.loc["2024"]

growth = train.loc["2023"].sum() / train.loc["2022"].sum()      # 1.0993
forecast = train.loc["2023"].to_numpy() * growth
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Jan 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Jul 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Jan 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Jul 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Jan 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Jul 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve2" style="stroke-width:2.2" points="470.5,195.0 488.3,203.8 506.1,177.5 523.8,176.3 541.6,163.2 559.4,131.3 577.1,112.6 594.9,98.2 612.7,147.6 630.5,159.4 648.2,188.8 666.0,162.5"/><polyline class="curve" style="stroke-width:2.2" points="470.5,176.9 488.3,186.5 506.1,157.6 523.8,156.2 541.6,141.8 559.4,106.8 577.1,86.2 594.9,70.4 612.7,124.7 630.5,137.7 648.2,170.0 666.0,141.1"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve2" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">seasonal naive</text><line class="curve" x1="286" y1="40" x2="304" y2="40"/><text class="ink" x="310" y="44" font-size="11">seasonal naive × growth</text></svg>
  <figcaption>The forecast of 2024. Seasonal naive (orange) is a copy of 2023: the shape is right, the level low in all twelve months. Multiplied by the growth rate (purple) it sits on top of the actual values.</figcaption>
</figure>

| Method | MAE | Percentage error |
|---|---|---|
| Seasonal naive | 40.4 | 10.3% |
| Seasonal naive + drift | 18.5 | 4.6% |
| Seasonal naive × growth | 11.1 | 2.8% |

Because the growth is multiplicative (Section 10), multiplying does better
than adding. A 2.8% error: very good for a two-line forecast, and this is now
**the real bar**. The exponential smoothing of Section 16 is exactly the
careful version of this idea (level + trend + season).

## 7. The error grows with the horizon

Forecasting tomorrow is easier than forecasting next month. By how much? The
error of the naive forecast for the share price, by horizon:

```python
k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

for h in (1, 5, 10, 20, 40):
    print(h, round((k.shift(-h) - k).abs().mean(), 2))
# 1 1.83 | 5 4.5 | 10 6.42 | 20 8.76 | 40 12.16
```

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="201.8" x2="666" y2="201.8"/><text class="dim" x="38" y="205.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="148.0" x2="666" y2="148.0"/><text class="dim" x="38" y="151.5" font-size="10.5" text-anchor="end">4</text><line class="grid" x1="44" y1="94.2" x2="666" y2="94.2"/><text class="dim" x="38" y="97.7" font-size="10.5" text-anchor="end">8</text><line class="grid" x1="44" y1="40.3" x2="666" y2="40.3"/><text class="dim" x="38" y="43.8" font-size="10.5" text-anchor="end">12</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="44.0" y1="210" x2="44.0" y2="214"/><text class="dim" x="44.0" y="226" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="107.8" y1="210" x2="107.8" y2="214"/><text class="dim" x="107.8" y="226" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="187.5" y1="210" x2="187.5" y2="214"/><text class="dim" x="187.5" y="226" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="347.0" y1="210" x2="347.0" y2="214"/><text class="dim" x="347.0" y="226" font-size="10.5" text-anchor="middle">20</text><line class="line" x1="506.5" y1="210" x2="506.5" y2="214"/><text class="dim" x="506.5" y="226" font-size="10.5" text-anchor="middle">30</text><line class="line" x1="666.0" y1="210" x2="666.0" y2="214"/><text class="dim" x="666.0" y="226" font-size="10.5" text-anchor="middle">40</text><polyline class="curve3" stroke-dasharray="5 4" style="stroke-width:1.6" points="44.0,177.2 59.9,167.0 75.9,159.2 91.8,152.6 107.8,146.8 123.7,141.5 139.7,136.7 155.6,132.2 171.6,128.0 187.5,124.0 203.5,120.2 219.4,116.6 235.4,113.1 251.3,109.8 267.3,106.5 283.2,103.4 299.2,100.4 315.1,97.4 331.1,94.6 347.0,91.8 363.0,89.1 378.9,86.4 394.9,83.8 410.8,81.3 426.8,78.8 442.7,76.4 458.7,74.0 474.6,71.6 490.6,69.3 506.5,67.0 522.5,64.8 538.4,62.6 554.4,60.5 570.3,58.3 586.3,56.2 602.2,54.2 618.2,52.1 634.1,50.1 650.1,48.2 666.0,46.2"/><polyline class="curve" style="stroke-width:2.4" points="44.0,177.2 59.9,166.4 75.9,156.8 91.8,148.4 107.8,141.3 123.7,135.7 139.7,130.9 155.6,126.0 171.6,120.2 187.5,115.4 203.5,110.7 219.4,107.0 235.4,103.1 251.3,100.1 267.3,96.7 283.2,93.8 299.2,91.0 315.1,88.6 331.1,86.1 347.0,83.9 363.0,81.9 378.9,79.4 394.9,76.8 410.8,74.1 426.8,71.7 442.7,69.5 458.7,66.6 474.6,63.8 490.6,61.4 506.5,58.7 522.5,56.2 538.4,53.4 554.4,50.7 570.3,48.2 586.3,45.9 602.2,43.9 618.2,42.1 634.1,40.4 650.1,39.2 666.0,38.2"/><line class="curve" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">error of the naive forecast (MAE)</text><line class="curve3" x1="331" y1="38" x2="349" y2="38"/><text class="ink" x="355" y="42" font-size="11">square root curve</text></svg>
  <figcaption>The horizontal axis is the horizon (business days), the vertical one the mean absolute error. The error grows, but more and more slowly; the dashed line is the one-day error times the square root of the horizon.</figcaption>
</figure>

The error grows with the horizon, but **more and more slowly**: at a horizon
40 times as far the error is not 40 times but 6.7 times as large. Because
random steps partly cancel each other, the error grows like the square root of
the horizon (√40 = 6.3).

The error of seasonal naive on the daily sales: 13.4 for 1 week ahead, 17.5
for 4 weeks ahead, 22.9 for 8 weeks ahead.

**An error without its horizon says nothing.** "My model's error is 12" is
incomplete: "12 on average at a 28-day horizon" is complete.

## 8. One step and many steps

So far you have made **multi-step** forecasts: 28 days at once from a single
origin. In a system that runs daily, you mostly forecast only **tomorrow**
each day and start again the next day with new data: a **one-step** forecast.

For the baselines you can set up one-step forecasts for the whole past in a
single line with `shift`:

```python
naive_1 = s.shift(1)                          # tomorrow = today
snaive_1 = s.shift(7)                         # tomorrow = the same day last week
ma7_1 = s.shift(1).rolling(7).mean()          # tomorrow = the mean of the last 7 days
```

The rule from Section 07 is vital here: since `rolling` includes that day,
`shift(1)` comes first. Otherwise the forecast has seen the value it is
forecasting.

The one-step errors for the 366 days of 2024:

| Method | MAE |
|---|---|
| Mean of the past | 52.5 |
| Mean of the last 7 days | 42.7 |
| Naive | 41.1 |
| Seasonal naive | 13.9 |

366 separate forecasts, 366 separate errors: a far more reliable measurement
than a single 28-day window. Section 15 turns this idea (a rolling origin)
into a system.

## 9. The bar

The value of a model is how much better it is than the baseline:

$$\text{skill} = 1 - \frac{\text{MAE}_{\text{model}}}{\text{MAE}_{\text{baseline}}}$$

- 0: the same as the baseline. The model added nothing.
- 0.5: it halved the error.
- Negative: **worse** than the baseline.

For the passenger series the skill of "seasonal naive × growth" over seasonal
naive is 1 − 11.1 / 40.4 = 0.73.

The practical meaning of this is large. If a model you spent weeks building
gives an MAE of 11 on the daily sales, it looks like a success, until you see
that copying the last week gives 11.6. **Every forecasting job starts with the
table of baselines.**

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Splitting training and test at random | The model learns having seen the future | The test is always at the end |
| Computing the mean or the growth from all the data | The test data leaks into the forecast | From `train` only |
| Not comparing with a baseline | A poor model is taken for a good one | The table of four baselines first |
| Plain naive on a seasonal series | The pattern is ignored | Seasonal naive |
| The mean on a trending series | The level is left far behind | Naive, drift, or seasonal naive with growth |
| Looking only at the MAE | A systematic drift goes unseen | Look at the bias (the mean of the error) too |
| Not stating the horizon | Errors cannot be compared | Say "at a horizon of h steps" |
| Comparing a one-step error with a multi-step one | Apples and oranges | The same horizon, the same period |
| Forgetting `shift(1)` in a `rolling` forecast | The forecast sees its own target | `s.shift(1).rolling(n).mean()` |

## Summary

- **Training** is the past, **test** the last stretch kept back; the split
  follows the order of time.
- Four baselines: **mean**, **naive** (the last value), **seasonal naive**
  (the same position in the last season), **drift** (extend the first–last
  line).
- **MAE**: the mean of the absolute errors. **Bias**: the mean of the errors;
  if it is far from zero the forecast is systematically off.
- The best baseline depends on the structure of the series: naive for a random
  walk, seasonal naive for a seasonal series, seasonal naive with growth for a
  growing seasonal series.
- **The error grows with the horizon**; an error without its horizon says
  nothing.
- One-step baseline forecasts are set up with `shift`; `shift(1)` before
  `rolling`.
- The **bar** for every model is the baseline; skill = 1 − the ratio of MAEs.

A single 28-day window is at the mercy of chance. The next section teaches how
to **validate a forecast properly**: other error measures, a rolling origin,
and the most insidious mistake of all, leakage.
