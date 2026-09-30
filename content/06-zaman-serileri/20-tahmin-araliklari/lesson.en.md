# Prediction Intervals

"310 will be sold tomorrow" is a forecast. But nobody believes exactly 310
will be sold; the real question is **how far off it may be**. For whoever
holds the stock, 310 ± 5 and 310 ± 60 mean completely different decisions.

Every forecast you have produced so far was a single number (a **point
forecast**). In this section you add a width to it: a **prediction interval**.
Then you measure whether the interval is honest and turn uncertainty into a
decision.

## 1. What does an interval say?

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Point forecast</span><span>A single number: "310". Around the most likely value.</span></div>
<div class="anat-row"><span>Prediction interval</span><span>A range and a probability: "between 289 and 333 with 80% probability".</span></div>
<div class="anat-row"><span>Coverage</span><span>The share of actual values falling inside the interval. An 80% interval should contain 80% of the days.</span></div>
</div>
<figcaption>An interval is <b>honest</b> if its coverage equals the probability it states.</figcaption>
</figure>

Both ends of an interval are useful: the lower end answers "how little might I
sell in the worst case", the upper end "how much stock is enough".

## 2. The plainest route: look at past errors

The best indicator of how far a method will be off in the future is **how far
it was off in the past**. The one-day-ahead errors of seasonal naive in 2023:

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)                 # actual - forecast
past = error.loc["2023"]

low, high = past.quantile([0.10, 0.90])
print(low, high)                       # -21.0 23.0
```

In 2023, 80% of the errors were between −21 and +23. So the 80% interval for
every day of 2024 is **forecast − 21** to **forecast + 23**.

Is it honest? How many of the actual values of 2024 fell inside:

| Interval | Bounds (added to the forecast) | Coverage in 2024 |
|---|---|---|
| 50% | −10.0 … +13.0 | 0.533 |
| 80% | −21.0 … +23.0 | 0.825 |
| 95% | −35.9 … +31.9 | 0.945 |

All three are very close to what they claim. No assumption, no formula: only
the quantiles of past errors. This is called an **empirical interval**.

## 3. By formula: the standard deviation

If the errors are roughly normally distributed, the interval can be computed
from the standard deviation of the error:

$$\text{forecast} \pm z \times \sigma$$

| Interval | `z` |
|---|---|
| 50% | 0.674 |
| 80% | 1.282 |
| 95% | 1.960 |

On the same data this route gives coverages of 0.555, 0.842 and 0.954: almost
the same as the empirical interval. The intervals given by statistical models
rest on this formula.

Its weak point: if the errors are not normally distributed (heavy tails, skew)
or do not average zero (a biased forecast), the interval is wrong. An
empirical interval does not need those assumptions.

## 4. The interval widens with the horizon

Forecasting tomorrow is easier than forecasting next month (Section 14); the
interval should reflect that. In a random walk the standard deviation of the
error grows like the **square root** of the horizon:

$$\sigma_h = \sigma \sqrt{h}$$

For the share price the standard deviation of the daily change is 2.26 and the
last price 143.73:

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="205.5" x2="666" y2="205.5"/><text class="dim" x="38" y="209.0" font-size="10.5" text-anchor="end">120</text><line class="grid" x1="44" y1="161.3" x2="666" y2="161.3"/><text class="dim" x="38" y="164.8" font-size="10.5" text-anchor="end">140</text><line class="grid" x1="44" y1="117.1" x2="666" y2="117.1"/><text class="dim" x="38" y="120.6" font-size="10.5" text-anchor="end">160</text><line class="grid" x1="44" y1="72.9" x2="666" y2="72.9"/><text class="dim" x="38" y="76.4" font-size="10.5" text-anchor="end">180</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="414.7" y1="230" x2="414.7" y2="234"/><text class="dim" x="414.7" y="246" font-size="10.5" text-anchor="middle">+0</text><line class="line" x1="477.5" y1="230" x2="477.5" y2="234"/><text class="dim" x="477.5" y="246" font-size="10.5" text-anchor="middle">+10</text><line class="line" x1="540.3" y1="230" x2="540.3" y2="234"/><text class="dim" x="540.3" y="246" font-size="10.5" text-anchor="middle">+20</text><line class="line" x1="603.2" y1="230" x2="603.2" y2="234"/><text class="dim" x="603.2" y="246" font-size="10.5" text-anchor="middle">+30</text><line class="line" x1="666.0" y1="230" x2="666.0" y2="234"/><text class="dim" x="666.0" y="246" font-size="10.5" text-anchor="middle">+40</text><polygon class="dot" opacity="0.16" style="stroke:none" points="414.7,153.1 421.0,143.3 427.3,139.3 433.5,136.2 439.8,133.5 446.1,131.2 452.4,129.1 458.7,127.2 464.9,125.4 471.2,123.8 477.5,122.2 483.8,120.7 490.1,119.2 496.4,117.8 502.6,116.5 508.9,115.2 515.2,114.0 521.5,112.8 527.8,111.6 534.1,110.5 540.3,109.3 546.6,108.3 552.9,107.2 559.2,106.2 565.5,105.2 571.8,104.2 578.0,103.2 584.3,102.3 590.6,101.3 596.9,100.4 603.2,99.5 609.5,98.6 615.7,97.8 622.0,96.9 628.3,96.1 634.6,95.2 640.9,94.4 647.2,93.6 653.4,92.8 659.7,92.0 666.0,91.2 666.0,215.0 659.7,214.2 653.4,213.4 647.2,212.6 640.9,211.8 634.6,211.0 628.3,210.1 622.0,209.3 615.7,208.4 609.5,207.6 603.2,206.7 596.9,205.8 590.6,204.9 584.3,203.9 578.0,203.0 571.8,202.0 565.5,201.0 559.2,200.0 552.9,199.0 546.6,197.9 540.3,196.9 534.1,195.7 527.8,194.6 521.5,193.4 515.2,192.2 508.9,191.0 502.6,189.7 496.4,188.4 490.1,187.0 483.8,185.5 477.5,184.0 471.2,182.4 464.9,180.8 458.7,179.0 452.4,177.1 446.1,175.0 439.8,172.7 433.5,170.0 427.3,166.9 421.0,162.9 414.7,153.1"/><polygon class="dot" opacity="0.22" style="stroke:none" points="414.7,153.1 421.0,146.7 427.3,144.0 433.5,142.0 439.8,140.3 446.1,138.8 452.4,137.4 458.7,136.2 464.9,135.0 471.2,133.9 477.5,132.9 483.8,131.9 490.1,130.9 496.4,130.0 502.6,129.2 508.9,128.3 515.2,127.5 521.5,126.7 527.8,126.0 534.1,125.2 540.3,124.5 546.6,123.8 552.9,123.1 559.2,122.4 565.5,121.8 571.8,121.1 578.0,120.5 584.3,119.8 590.6,119.2 596.9,118.6 603.2,118.1 609.5,117.5 615.7,116.9 622.0,116.3 628.3,115.8 634.6,115.2 640.9,114.7 647.2,114.2 653.4,113.7 659.7,113.1 666.0,112.6 666.0,193.6 659.7,193.1 653.4,192.5 647.2,192.0 640.9,191.5 634.6,191.0 628.3,190.4 622.0,189.9 615.7,189.3 609.5,188.7 603.2,188.1 596.9,187.6 590.6,187.0 584.3,186.3 578.0,185.7 571.8,185.1 565.5,184.4 559.2,183.8 552.9,183.1 546.6,182.4 540.3,181.7 534.1,181.0 527.8,180.2 521.5,179.5 515.2,178.7 508.9,177.9 502.6,177.0 496.4,176.2 490.1,175.3 483.8,174.3 477.5,173.3 471.2,172.3 464.9,171.2 458.7,170.0 452.4,168.8 446.1,167.4 439.8,165.9 433.5,164.2 427.3,162.1 421.0,159.5 414.7,153.1"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,100.5 50.3,91.6 56.6,100.5 62.8,106.8 69.1,100.3 75.4,105.6 81.7,111.0 88.0,114.7 94.3,108.2 100.5,105.4 106.8,108.0 113.1,108.3 119.4,101.8 125.7,107.6 132.0,110.0 138.2,121.6 144.5,117.6 150.8,115.2 157.1,126.8 163.4,128.5 169.7,143.6 175.9,146.8 182.2,144.4 188.5,154.1 194.8,162.3 201.1,160.3 207.4,165.5 213.6,167.4 219.9,164.4 226.2,155.9 232.5,159.1 238.8,155.5 245.1,144.0 251.3,141.9 257.6,142.1 263.9,147.0 270.2,141.9 276.5,142.9 282.7,137.2 289.0,128.0 295.3,130.9 301.6,130.0 307.9,128.7 314.2,125.3 320.4,124.1 326.7,131.5 333.0,132.1 339.3,131.8 345.6,131.7 351.9,136.9 358.1,141.5 364.4,137.9 370.7,150.1 377.0,147.1 383.3,148.2 389.6,148.4 395.8,156.6 402.1,157.8 408.4,160.1 414.7,153.1"/><polyline class="curve3" stroke-dasharray="5 4" style="stroke-width:1.6" points="414.7,153.1 421.0,141.7 427.3,141.4 433.5,128.2 439.8,123.2 446.1,123.2 452.4,117.7 458.7,116.8 464.9,112.0 471.2,103.6 477.5,107.1 483.8,109.4 490.1,101.8 496.4,106.2 502.6,114.5 508.9,118.3 515.2,118.1 521.5,115.9 527.8,111.2 534.1,105.8 540.3,104.4 546.6,96.9 552.9,109.1 559.2,108.8 565.5,114.2 571.8,115.5 578.0,108.1 584.3,113.5 590.6,108.7 596.9,113.4 603.2,111.2 609.5,117.4 615.7,114.3 622.0,102.6 628.3,98.8 634.6,103.1 640.9,104.0 647.2,101.9 653.4,99.6 659.7,97.9 666.0,102.9"/><polyline class="curve" style="stroke-width:2" points="414.7,153.1 421.0,153.1 427.3,153.1 433.5,153.1 439.8,153.1 446.1,153.1 452.4,153.1 458.7,153.1 464.9,153.1 471.2,153.1 477.5,153.1 483.8,153.1 490.1,153.1 496.4,153.1 502.6,153.1 508.9,153.1 515.2,153.1 521.5,153.1 527.8,153.1 534.1,153.1 540.3,153.1 546.6,153.1 552.9,153.1 559.2,153.1 565.5,153.1 571.8,153.1 578.0,153.1 584.3,153.1 590.6,153.1 596.9,153.1 603.2,153.1 609.5,153.1 615.7,153.1 622.0,153.1 628.3,153.1 634.6,153.1 640.9,153.1 647.2,153.1 653.4,153.1 659.7,153.1 666.0,153.1"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">price</text><line class="curve" x1="135" y1="40" x2="153" y2="40"/><text class="ink" x="159" y="44" font-size="11">naive forecast</text><rect class="dot" x="279" y="35" width="18" height="10" opacity="0.3"/><text class="ink" x="303" y="44" font-size="11">80% and 95% intervals</text></svg>
  <figcaption>The naive forecast is a flat line; the interval around it opens out like the square root of the horizon. The dashed line is the price that then occurred: well above the forecast and, in the first weeks, outside the 95% interval too. An interval is not a guarantee.</figcaption>
</figure>

| Horizon | 95% interval | Width |
|---|---|---|
| 1 day | 139.3 – 148.2 | 8.9 |
| 10 days | 129.7 – 157.7 | 28.0 |
| 40 days | 115.7 – 171.7 | 56.0 |

Is this widening real? Check it starting from every day of the series:

| Horizon | Coverage with the square root rule | Coverage with a constant width |
|---|---|---|
| 1 day | 0.953 | 0.953 |
| 10 days | 0.925 | 0.411 |
| 40 days | 0.969 | 0.190 |

Use the one-day width for 40 days ahead and the interval you call "95%" holds
the truth only 19% of the time. **An interval that ignores the horizon gives
false confidence at a distant horizon.**

## 5. The interval a model gives

statsmodels models compute the interval themselves:

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()
result = fit.get_forecast(28)

mean = result.predicted_mean
interval = result.conf_int(alpha=0.05)        # 95%; alpha=0.2 -> 80%
print(interval.iloc[0].round(1).tolist())     # [267.1, 318.7]
```

`alpha` is the probability of falling **outside** the interval: 0.05 → 95%,
0.2 → 80%.

For the first day the forecast is 292.9 and the interval 267.1 – 318.7; the
actual value is 283, inside. The interval widens with the horizon:

| Day | 1 | 7 | 14 | 28 |
|---|---|---|---|---|
| 95% width | 51.6 | 56.7 | 65.0 | 83.8 |

<figure class="fig">
  <svg viewBox="0 0 680 270" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="222.5" x2="666" y2="222.5"/><text class="dim" x="38" y="226.0" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="185.8" x2="666" y2="185.8"/><text class="dim" x="38" y="189.3" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="149.2" x2="666" y2="149.2"/><text class="dim" x="38" y="152.7" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="112.5" x2="666" y2="112.5"/><text class="dim" x="38" y="116.0" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="75.9" x2="666" y2="75.9"/><text class="dim" x="38" y="79.4" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="39.2" x2="666" y2="39.2"/><text class="dim" x="38" y="42.7" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="240" x2="666" y2="240"/><line class="line" x1="44.0" y1="240" x2="44.0" y2="244"/><text class="dim" x="44.0" y="256" font-size="10.5" text-anchor="middle">9 Oct</text><line class="line" x1="202.3" y1="240" x2="202.3" y2="244"/><text class="dim" x="202.3" y="256" font-size="10.5" text-anchor="middle">23 Oct</text><line class="line" x1="360.7" y1="240" x2="360.7" y2="244"/><text class="dim" x="360.7" y="256" font-size="10.5" text-anchor="middle">6 Nov</text><line class="line" x1="519.0" y1="240" x2="519.0" y2="244"/><text class="dim" x="519.0" y="256" font-size="10.5" text-anchor="middle">20 Nov</text><polygon class="dot" opacity="0.2" style="stroke:none" points="360.7,172.2 372.0,162.7 383.3,128.0 394.6,82.3 405.9,116.3 417.2,180.0 428.5,181.3 439.8,166.8 451.1,157.4 462.4,122.6 473.7,76.9 485.1,110.8 496.4,174.4 507.7,175.7 519.0,161.2 530.3,151.7 541.6,116.9 552.9,71.1 564.2,105.0 575.5,168.6 586.8,169.9 598.1,155.4 609.5,145.8 620.8,111.0 632.1,65.1 643.4,99.0 654.7,162.5 666.0,163.8 666.0,225.2 654.7,223.1 643.4,158.7 632.1,124.0 620.8,169.0 609.5,202.9 598.1,211.6 586.8,224.2 575.5,222.1 564.2,157.8 552.9,123.1 541.6,168.1 530.3,202.1 519.0,210.8 507.7,223.4 496.4,221.4 485.1,157.1 473.7,122.4 462.4,167.5 451.1,201.5 439.8,210.2 428.5,222.8 417.2,220.9 405.9,156.6 394.6,122.1 383.3,167.1 372.0,201.2 360.7,210.0"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,218.8 55.3,194.6 66.6,153.6 77.9,117.6 89.2,141.1 100.5,219.6 111.9,224.0 123.2,191.0 134.5,186.6 145.8,157.2 157.1,109.6 168.4,154.3 179.7,204.2 191.0,212.2 202.3,185.1 213.6,193.9 224.9,158.7 236.3,101.5 247.6,138.9 258.9,206.4 270.2,204.9 281.5,196.1 292.8,190.2 304.1,141.1 315.4,96.4 326.7,136.0 338.0,206.4 349.3,210.0 360.7,198.3 372.0,181.4 383.3,148.4 394.6,80.3 405.9,131.6 417.2,202.7 428.5,208.6 439.8,183.6 451.1,183.6 462.4,132.3 473.7,105.9 485.1,117.6 496.4,205.6 507.7,200.5 519.0,200.5 530.3,174.8 541.6,136.7 552.9,100.1 564.2,125.0 575.5,208.6 586.8,195.4 598.1,188.0 609.5,188.0 620.8,159.4 632.1,89.1 643.4,117.6 654.7,208.6 666.0,193.2"/><polyline class="curve" style="stroke-width:2.2" points="360.7,191.1 372.0,182.0 383.3,147.6 394.6,102.2 405.9,136.5 417.2,200.4 428.5,202.1 439.8,188.5 451.1,179.4 462.4,145.0 473.7,99.7 485.1,133.9 496.4,197.9 507.7,199.5 519.0,186.0 530.3,176.9 541.6,142.5 552.9,97.1 564.2,131.4 575.5,195.4 586.8,197.0 598.1,183.5 609.5,174.4 620.8,140.0 632.1,94.6 643.4,128.8 654.7,192.8 666.0,194.5"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">ARIMA forecast</text><rect class="dot" x="286" y="35" width="18" height="10" opacity="0.3"/><text class="ink" x="310" y="44" font-size="11">95% interval</text></svg>
  <figcaption>The 28-day forecast and its 95% interval. The band widens from week to week; 27 of the 28 actual values are inside.</figcaption>
</figure>

## 6. Test the interval

On the single split (5 November) the coverage of this interval is 0.964: very
close to 95%. But the lesson of Section 15 holds here too: a single split is
at the mercy of chance. Across 13 experiments:

| | Stated | Measured coverage |
|---|---|---|
| The 95% interval | 0.95 | **0.874** |
| The 80% interval | 0.80 | 0.777 |

The interval is **too narrow**: it says 95% and holds 87%. Looking experiment
by experiment shows why:

```text
0.00  0.96  1.00  1.00  0.96  1.00  1.00  1.00  0.93  1.00  1.00  0.96  0.54
```

In eleven experiments the coverage is close to perfect. In the first (January)
it is **zero**, in the last (December) 0.54. These are the two bad periods you
have known since Section 15: the model does not know the turn of the year.

**An interval measures the uncertainty the model knows about; it cannot
measure what the model does not know.** If the model is wrong (a missing
variable, a changing pattern), its interval is wrong too, and usually too
narrow. That is why a model's interval is not trusted blindly; its coverage is
backtested.

The fixes: add the missing information (the calendar variables of Section 18),
or build the interval not from the model's formula but **from the real errors
on a rolling origin**. The latter corrects the model's optimism about itself.

## 7. Quantile forecasts

Sometimes you need not the whole interval but one end of it: "how many do I
need for the stock to be enough with 90% probability?" That is a forecast of
**the 0.9 quantile**.

In its simplest form: add that quantile of the past errors to the point
forecast.

```python
shift = past.quantile(0.90)            # 23.0
q90 = s.shift(7) + shift               # "with 90% probability fewer than this are sold"
```

Did the actual value stay below this limit in 2024? On 91.3% of the days: very
close to the stated 90%.

The MAE is no use for measuring a quantile forecast (it rewards the median).
Its measure is the **pinball loss**:

```python
import numpy as np


def pinball(actual, forecast, q):
    diff = actual - forecast
    return np.mean(np.maximum(q * diff, (q - 1) * diff))
```

For `q = 0.9`, the actual value ending up **above** (an under-forecast) is
penalised by 0.9 and ending up below by 0.1: exceeding the limit is nine times
as costly. For `q = 0.5` the loss is half the absolute error.

| `q` | Added share | Pinball loss | Loss of the point forecast at the same `q` |
|---|---|---|---|
| 0.5 | +2 | 6.92 | 6.94 |
| 0.8 | +16 | 4.68 | 7.21 |
| 0.9 | +23 | 2.84 | 7.30 |
| 0.95 | +28 | 1.68 | 7.35 |

## 8. From uncertainty to a decision

Think of a bakery. Every loaf it cannot sell is a loss of 1 unit (waste);
every demand it cannot meet is a loss of 4 units (the lost profit and the
customer). How many should it bake each morning?

If it bakes as many as the point forecast, the bread runs out on half the
days. If it bakes far too many, the waste grows. The right answer is a
**quantile**:

$$q = \frac{\text{cost of being short}}{\text{cost of being short} + \text{cost of being over}} = \frac{4}{4 + 1} = 0.8$$

Four production rules over the 366 days of 2024:

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="200.0" x2="666" y2="200.0"/><text class="dim" x="38" y="203.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="148.4" x2="666" y2="148.4"/><text class="dim" x="38" y="151.9" font-size="10.5" text-anchor="end">4,000</text><line class="grid" x1="44" y1="96.9" x2="666" y2="96.9"/><text class="dim" x="38" y="100.4" font-size="10.5" text-anchor="end">8,000</text><line class="grid" x1="44" y1="45.3" x2="666" y2="45.3"/><text class="dim" x="38" y="48.8" font-size="10.5" text-anchor="end">12,000</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="132.9" y1="200" x2="132.9" y2="204"/><text class="dim" x="132.9" y="216" font-size="10.5" text-anchor="middle">q = 0.5</text><line class="line" x1="281.0" y1="200" x2="281.0" y2="204"/><text class="dim" x="281.0" y="216" font-size="10.5" text-anchor="middle">q = 0.8</text><line class="line" x1="429.0" y1="200" x2="429.0" y2="204"/><text class="dim" x="429.0" y="216" font-size="10.5" text-anchor="middle">q = 0.9</text><line class="line" x1="577.1" y1="200" x2="577.1" y2="204"/><text class="dim" x="577.1" y="216" font-size="10.5" text-anchor="middle">q = 0.95</text><rect class="dot2" x="86.9" y="44.5" width="91.9" height="155.5" rx="3" opacity="0.9"/><rect class="dot" x="235.0" y="89.6" width="91.9" height="110.4" rx="3" opacity="0.9"/><rect class="dim" x="383.1" y="81.0" width="91.9" height="119.0" rx="3" opacity="0.9"/><rect class="dim" x="531.2" y="64.6" width="91.9" height="135.4" rx="3" opacity="0.9"/><text class="ink" x="132.9" y="40.0" font-size="11.5" text-anchor="middle">12062</text><text class="ink" x="281.0" y="85.1" font-size="11.5" text-anchor="middle">8566</text><text class="ink" x="429.0" y="76.5" font-size="11.5" text-anchor="middle">9233</text><text class="ink" x="577.1" y="60.1" font-size="11.5" text-anchor="middle">10508</text></svg>
  <figcaption>The total cost in 2024 of four production rules (short 4 units, over 1). Orange: baking as many as the point forecast. Purple: the quantile the formula says. Being even more cautious swells the waste and raises the cost again.</figcaption>
</figure>

| Rule | Days the stock ran out | Unmet demand | Waste | Total cost |
|---|---|---|---|---|
| The point forecast (`q = 0.5`) | 178 | 2333 | 2730 | 12062 |
| **`q = 0.8`** | 73 | 609 | 6130 | **8566** |
| `q = 0.9` | 32 | 230 | 8313 | 9233 |
| `q = 0.95` | 14 | 119 | 10032 | 10508 |

The lowest cost is exactly where the formula says. The same forecasting
method, the same data; merely taking the uncertainty into account cut the cost
by 29%.

**The right forecast depends on the costs.** A high quantile if being short is
expensive, a low one if being over is. "The best forecast" means nothing on
its own; the question is "for which decision?"

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Giving only a point forecast | The decision-maker cannot see the risk | Add an interval or a quantile |
| Not testing the interval | False confidence | Measure coverage on a rolling origin |
| Using the one-day width for the whole horizon | Far too narrow at a distant horizon | Widen with the horizon |
| Trusting the model's interval blindly | If the model is wrong so is the interval | An empirical interval from real errors |
| An interval from the training residual | Too narrow (in-sample is optimistic) | From out-of-sample errors |
| A symmetric interval around a biased forecast | One end is always exceeded | Fix the bias first, or use quantiles |
| Measuring a quantile with the MAE | The wrong model is chosen | The pinball loss |
| Writing `alpha=0.95` | A 5% interval | `alpha` is the share left outside: 0.05 |
| Not turning back the interval of a log model | The wrong unit | `np.exp` on the ends too |

## Summary

- A **prediction interval** is a range and a probability; **coverage** is the
  share of actual values falling inside. In an honest interval the two are
  equal.
- An **empirical interval**: the quantiles of past errors. Assumption-free and
  sturdy.
- **By formula**: forecast ± `z` × the standard deviation; if the errors are
  normally distributed.
- The interval **widens with the horizon**; like the square root in a random
  walk.
- From a model: `get_forecast(h).conf_int(alpha=...)`.
- An interval is **tested**: across 13 experiments "95%" held only 87%,
  because the model did not know the turn of the year. An interval cannot
  measure what the model does not know.
- A **quantile forecast** gives one end; its measure is the **pinball loss**.
- The right quantile for a decision comes from the costs: short / (short +
  over).

A day that falls outside the interval is either bad luck or a sign that
something **has changed**. The next section teaches you to tell the two apart:
anomalies and change points.
