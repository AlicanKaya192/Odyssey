# Exponential Smoothing

The baselines of Section 14 had two extremes. **Naive** looks only at the last
observation: very agile, but fooled by every bit of noise. **The mean** gives
all the past equal weight: calm, but it treats a day three years ago the same
as yesterday.

There is a sensible path in between: **look at all the past, but trust what is
recent more.** That is exactly what exponential smoothing is. It has been in
use since the 1950s, takes one line to set up, and in real forecasting
competitions runs neck and neck with far more complex methods. In this section
you build it in three steps: first the level, then the trend, then the season.

## 1. The idea: decaying weights

The forecast is a **weighted average** of past observations. The newest
observation gets a weight of `α` (alpha); the one before gets `(1 − α)` times
that, the one before that `(1 − α)` times again...

For `α = 0.3` the weights are: 0.30, 0.21, 0.147, 0.103, 0.072, 0.050...

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="200.0" x2="666" y2="200.0"/><text class="dim" x="38" y="203.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="169.6" x2="666" y2="169.6"/><text class="dim" x="38" y="173.1" font-size="10.5" text-anchor="end">0.2</text><line class="grid" x1="44" y1="139.3" x2="666" y2="139.3"/><text class="dim" x="38" y="142.8" font-size="10.5" text-anchor="end">0.4</text><line class="grid" x1="44" y1="108.9" x2="666" y2="108.9"/><text class="dim" x="38" y="112.4" font-size="10.5" text-anchor="end">0.6</text><line class="grid" x1="44" y1="78.6" x2="666" y2="78.6"/><text class="dim" x="38" y="82.1" font-size="10.5" text-anchor="end">0.8</text><line class="grid" x1="44" y1="48.2" x2="666" y2="48.2"/><text class="dim" x="38" y="51.7" font-size="10.5" text-anchor="end">1</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="63.4" y1="200" x2="63.4" y2="204"/><text class="dim" x="63.4" y="216" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="160.6" y1="200" x2="160.6" y2="204"/><text class="dim" x="160.6" y="216" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="257.8" y1="200" x2="257.8" y2="204"/><text class="dim" x="257.8" y="216" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="355.0" y1="200" x2="355.0" y2="204"/><text class="dim" x="355.0" y="216" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="452.2" y1="200" x2="452.2" y2="204"/><text class="dim" x="452.2" y="216" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="549.4" y1="200" x2="549.4" y2="204"/><text class="dim" x="549.4" y="216" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="646.6" y1="200" x2="646.6" y2="204"/><text class="dim" x="646.6" y="216" font-size="10.5" text-anchor="middle">12</text><polyline class="curve2" style="stroke-width:2" points="63.4,63.4 112.0,186.3 160.6,198.6 209.2,199.9 257.8,200.0 306.4,200.0 355.0,200.0 403.6,200.0 452.2,200.0 500.8,200.0 549.4,200.0 598.0,200.0 646.6,200.0"/><circle class="dot2" cx="63.4" cy="63.4" r="3"/><circle class="dot2" cx="112.0" cy="186.3" r="3"/><circle class="dot2" cx="160.6" cy="198.6" r="3"/><circle class="dot2" cx="209.2" cy="199.9" r="3"/><circle class="dot2" cx="257.8" cy="200.0" r="3"/><circle class="dot2" cx="306.4" cy="200.0" r="3"/><circle class="dot2" cx="355.0" cy="200.0" r="3"/><circle class="dot2" cx="403.6" cy="200.0" r="3"/><circle class="dot2" cx="452.2" cy="200.0" r="3"/><circle class="dot2" cx="500.8" cy="200.0" r="3"/><circle class="dot2" cx="549.4" cy="200.0" r="3"/><circle class="dot2" cx="598.0" cy="200.0" r="3"/><circle class="dot2" cx="646.6" cy="200.0" r="3"/><polyline class="curve4" style="stroke-width:2" points="63.4,124.1 112.0,162.1 160.6,181.0 209.2,190.5 257.8,195.3 306.4,197.6 355.0,198.8 403.6,199.4 452.2,199.7 500.8,199.9 549.4,199.9 598.0,200.0 646.6,200.0"/><circle class="dot3" cx="63.4" cy="124.1" r="3"/><circle class="dot3" cx="112.0" cy="162.1" r="3"/><circle class="dot3" cx="160.6" cy="181.0" r="3"/><circle class="dot3" cx="209.2" cy="190.5" r="3"/><circle class="dot3" cx="257.8" cy="195.3" r="3"/><circle class="dot3" cx="306.4" cy="197.6" r="3"/><circle class="dot3" cx="355.0" cy="198.8" r="3"/><circle class="dot3" cx="403.6" cy="199.4" r="3"/><circle class="dot3" cx="452.2" cy="199.7" r="3"/><circle class="dot3" cx="500.8" cy="199.9" r="3"/><circle class="dot3" cx="549.4" cy="199.9" r="3"/><circle class="dot3" cx="598.0" cy="200.0" r="3"/><circle class="dot3" cx="646.6" cy="200.0" r="3"/><polyline class="curve" style="stroke-width:2" points="63.4,169.6 112.0,175.7 160.6,180.6 209.2,184.5 257.8,187.6 306.4,190.1 355.0,192.0 403.6,193.6 452.2,194.9 500.8,195.9 549.4,196.7 598.0,197.4 646.6,197.9"/><circle class="dot" cx="63.4" cy="169.6" r="3"/><circle class="dot" cx="112.0" cy="175.7" r="3"/><circle class="dot" cx="160.6" cy="180.6" r="3"/><circle class="dot" cx="209.2" cy="184.5" r="3"/><circle class="dot" cx="257.8" cy="187.6" r="3"/><circle class="dot" cx="306.4" cy="190.1" r="3"/><circle class="dot" cx="355.0" cy="192.0" r="3"/><circle class="dot" cx="403.6" cy="193.6" r="3"/><circle class="dot" cx="452.2" cy="194.9" r="3"/><circle class="dot" cx="500.8" cy="195.9" r="3"/><circle class="dot" cx="549.4" cy="196.7" r="3"/><circle class="dot" cx="598.0" cy="197.4" r="3"/><circle class="dot" cx="646.6" cy="197.9" r="3"/><line class="curve2" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">α = 0.9</text><line class="curve4" x1="149" y1="38" x2="167" y2="38"/><text class="ink" x="173" y="42" font-size="11">α = 0.5</text><line class="curve" x1="244" y1="38" x2="262" y2="38"/><text class="ink" x="268" y="42" font-size="11">α = 0.2</text></svg>
  <figcaption>The horizontal axis is how many steps back the observation is (0 is the newest), the vertical one the weight it gets. With a large α nearly all the weight is on the last observation; with a small α it spreads over a long past.</figcaption>
</figure>

- With a large `α` the weight gathers in the last few observations: **agile**,
  exposed to noise.
- With a small `α` the weight spreads over a long past: **calm**, slow to
  adapt to change.
- `α = 1` is the naive forecast; as `α` approaches zero it resembles the mean.

## 2. Simple exponential smoothing

There is no need to compute the weights one by one. A single update rule gives
the same result:

$$\text{new level} = \alpha \times \text{observation} + (1 - \alpha) \times \text{old level}$$

At every new observation, pull the level towards it by `α`.

```python
def smooth(values, alpha):
    level = values[0]
    levels = []
    for value in values:
        level = alpha * value + (1 - alpha) * level
        levels.append(level)
    return levels
```

Five days with `α = 0.5`:

| Observation | 351 | 223 | 223 | 264 | 264 |
|---|---|---|---|---|---|
| Level | 351.0 | 287.0 | 255.0 | 259.5 | 261.8 |

When the observation drops to 223 on the second day, the level goes halfway
down to 287; on the third day another half step. The same in pandas:

```python
levels = s.ewm(alpha=0.5, adjust=False).mean()
```

**The forecast is the last level itself**, the same for the whole horizon: a
flat line. Simple exponential smoothing is for series with no trend and no
season.

## 3. What should alpha be?

For the daily sales with the weekly share removed (the adjusted series of
Section 10), the error one day ahead, by `α`:

| `α` | 0.05 | 0.1 | 0.2 | 0.5 | 1.0 (naive) |
|---|---|---|---|---|---|
| MAE | 12.55 | 11.46 | **11.21** | 11.83 | 13.53 |

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="180.2" x2="666" y2="180.2"/><text class="dim" x="38" y="183.7" font-size="10.5" text-anchor="end">260</text><line class="grid" x1="44" y1="139.2" x2="666" y2="139.2"/><text class="dim" x="38" y="142.7" font-size="10.5" text-anchor="end">280</text><line class="grid" x1="44" y1="98.2" x2="666" y2="98.2"/><text class="dim" x="38" y="101.7" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="57.2" x2="666" y2="57.2"/><text class="dim" x="38" y="60.7" font-size="10.5" text-anchor="end">320</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">1 Jul</text><line class="line" x1="139.7" y1="220" x2="139.7" y2="224"/><text class="dim" x="139.7" y="236" font-size="10.5" text-anchor="middle">15 Jul</text><line class="line" x1="255.9" y1="220" x2="255.9" y2="224"/><text class="dim" x="255.9" y="236" font-size="10.5" text-anchor="middle">1 Aug</text><line class="line" x1="351.6" y1="220" x2="351.6" y2="224"/><text class="dim" x="351.6" y="236" font-size="10.5" text-anchor="middle">15 Aug</text><line class="line" x1="467.8" y1="220" x2="467.8" y2="224"/><text class="dim" x="467.8" y="236" font-size="10.5" text-anchor="middle">1 Sep</text><line class="line" x1="563.5" y1="220" x2="563.5" y2="224"/><text class="dim" x="563.5" y="236" font-size="10.5" text-anchor="middle">15 Sep</text><polyline class="curve3" style="stroke-width:1.2" points="44.0,209.8 50.8,193.3 57.7,194.5 64.5,156.2 71.3,133.1 78.2,160.2 85.0,157.1 91.8,185.2 98.7,189.2 105.5,184.2 112.4,131.6 119.2,172.0 126.0,164.3 132.9,148.9 139.7,166.8 146.5,140.0 153.4,165.7 160.2,156.2 167.0,153.6 173.9,166.3 180.7,165.3 187.5,150.3 194.4,156.4 201.2,173.9 208.0,158.3 214.9,102.3 221.7,149.9 228.5,167.3 235.4,150.3 242.2,117.4 249.1,159.6 255.9,158.3 262.7,161.8 269.6,168.4 276.4,144.8 283.2,129.8 290.1,140.0 296.9,147.3 303.7,185.0 310.6,153.6 317.4,154.0 324.2,196.1 331.1,162.6 337.9,129.7 344.7,165.7 351.6,158.3 358.4,98.2 365.3,104.8 372.1,97.6 378.9,113.4 385.8,121.5 392.6,137.0 399.4,121.4 406.3,96.1 413.1,102.7 419.9,114.0 426.8,131.9 433.6,109.2 440.4,141.1 447.3,86.5 454.1,98.2 460.9,113.0 467.8,68.9 474.6,168.8 481.5,174.8 488.3,108.3 495.1,133.7 502.0,126.9 508.8,76.1 515.6,75.0 522.5,72.4 529.3,105.1 536.1,130.9 543.0,96.8 549.8,110.5 556.6,88.4 563.5,64.8 570.3,86.8 577.1,150.2 584.0,83.7 590.8,98.8 597.6,81.8 604.5,88.4 611.3,103.8 618.2,119.6 625.0,88.7 631.8,104.2 638.7,102.9 645.5,65.4 652.3,74.0 659.2,114.0 666.0,90.9"/><polyline class="curve2" style="stroke-width:1.8" points="44.0,203.9 50.8,194.4 57.7,194.4 64.5,160.1 71.3,135.8 78.2,157.7 85.0,157.1 91.8,182.4 98.7,188.5 105.5,184.6 112.4,136.9 119.2,168.5 126.0,164.7 132.9,150.5 139.7,165.1 146.5,142.5 153.4,163.4 160.2,157.0 167.0,153.9 173.9,165.1 180.7,165.3 187.5,151.8 194.4,155.9 201.2,172.1 208.0,159.7 214.9,108.0 221.7,145.7 228.5,165.2 235.4,151.8 242.2,120.9 249.1,155.7 255.9,158.0 262.7,161.4 269.6,167.7 276.4,147.1 283.2,131.6 290.1,139.1 296.9,146.5 303.7,181.1 310.6,156.3 317.4,154.2 324.2,191.9 331.1,165.6 337.9,133.3 344.7,162.5 351.6,158.7 358.4,104.2 365.3,104.7 372.1,98.3 378.9,111.9 385.8,120.6 392.6,135.4 399.4,122.8 406.3,98.8 413.1,102.3 419.9,112.8 426.8,130.0 433.6,111.3 440.4,138.1 447.3,91.7 454.1,97.5 460.9,111.4 467.8,73.1 474.6,159.2 481.5,173.3 488.3,114.8 495.1,131.8 502.0,127.4 508.8,81.2 515.6,75.7 522.5,72.7 529.3,101.9 536.1,128.0 543.0,99.9 549.8,109.4 556.6,90.5 563.5,67.4 570.3,84.8 577.1,143.7 584.0,89.7 590.8,97.9 597.6,83.4 604.5,87.9 611.3,102.2 618.2,117.8 625.0,91.6 631.8,103.0 638.7,102.9 645.5,69.1 652.3,73.5 659.2,110.0 666.0,92.8"/><polyline class="curve" style="stroke-width:2.4" points="44.0,178.7 50.8,181.6 57.7,184.2 64.5,178.6 71.3,169.5 78.2,167.6 85.0,165.5 91.8,169.5 98.7,173.4 105.5,175.6 112.4,166.8 119.2,167.8 126.0,167.1 132.9,163.5 139.7,164.1 146.5,159.3 153.4,160.6 160.2,159.7 167.0,158.5 173.9,160.0 180.7,161.1 187.5,158.9 194.4,158.4 201.2,161.5 208.0,160.9 214.9,149.2 221.7,149.3 228.5,152.9 235.4,152.4 242.2,145.4 249.1,148.2 255.9,150.3 262.7,152.6 269.6,155.7 276.4,153.5 283.2,148.8 290.1,147.0 296.9,147.1 303.7,154.7 310.6,154.4 317.4,154.3 324.2,162.7 331.1,162.7 337.9,156.1 344.7,158.0 351.6,158.1 358.4,146.1 365.3,137.8 372.1,129.8 378.9,126.5 385.8,125.5 392.6,127.8 399.4,126.5 406.3,120.4 413.1,116.9 419.9,116.3 426.8,119.4 433.6,117.4 440.4,122.1 447.3,115.0 454.1,111.6 460.9,111.9 467.8,103.3 474.6,116.4 481.5,128.1 488.3,124.1 495.1,126.0 502.0,126.2 508.8,116.2 515.6,108.0 522.5,100.8 529.3,101.7 536.1,107.5 543.0,105.4 549.8,106.4 556.6,102.8 563.5,95.2 570.3,93.5 577.1,104.9 584.0,100.6 590.8,100.3 597.6,96.6 604.5,94.9 611.3,96.7 618.2,101.3 625.0,98.8 631.8,99.8 638.7,100.5 645.5,93.4 652.3,89.6 659.2,94.4 666.0,93.7"/><line class="curve3" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">adjusted sales</text><line class="curve2" x1="198" y1="38" x2="216" y2="38"/><text class="ink" x="222" y="42" font-size="11">level, α = 0.9</text><line class="curve" x1="342" y1="38" x2="360" y2="38"/><text class="ink" x="366" y="42" font-size="11">level, α = 0.2</text></svg>
  <figcaption>α = 0.9 follows every zigzag: it takes the noise for signal too. α = 0.2 filters the noise out and leaves the slowly changing level.</figcaption>
</figure>

The best value is around 0.2 and 17% better than naive: in this series most of
the day-to-day movement is noise and the level changes slowly. A very small
`α` (0.05), on the other hand, misses the real movement of the level.

There is no need to search by hand; statsmodels finds `α` itself, so as to
minimise the one-step error on the training data:

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

fit = ExponentialSmoothing(train).fit()
print(round(fit.params["smoothing_level"], 3))     # 0.186
forecast = fit.forecast(28)
```

The `α` it finds is also a diagnosis of the series. For the share price the
result is **1.0**: the model says "trust nothing but the last value". The best
forecast of a random walk (Section 11) is naive; exponential smoothing found
that out by itself.

## 4. Trend: Holt's method

On a trending series a flat line always lags behind. Holt's method tracks a
second number: the **slope**. The level is updated with `α` and the slope with
`β` (beta) separately, and the forecast becomes a line:

$$\text{forecast}_h = \text{level} + h \times \text{slope}$$

For the yearly passenger totals (training 2013–2022, test 2023–2024):

```python
fit = ExponentialSmoothing(train, trend="add").fit()
```

| Model | 2023 | 2024 | MAE |
|---|---|---|---|
| Actual | 4195 | 4680 | |
| No trend | 3816 | 3816 | 621.5 |
| Additive trend (`trend="add"`) | 4071 | 4326 | 239.3 |
| Multiplicative trend (`trend="mul"`) | 4233 | 4690 | 23.5 |

An additive trend adds **a constant amount** every year; a multiplicative
trend grows by **a constant rate**. Because passenger numbers grow 10% a year
(Section 11), the multiplicative one is ten times more accurate.

**A damped trend.** A linear trend carries on at the same slope for ever; at a
long horizon that is usually too optimistic. `damped_trend=True` shrinks the
slope a little at every step (by the coefficient `φ`) and the forecast flattens
out over time. It is the safe choice for long-horizon forecasts.

## 5. Season: Holt–Winters

The third component is the season. The model now tracks three things at once,
each with its own coefficient:

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Level · α</span><span>The current, seasonally adjusted level of the series.</span></div>
<div class="anat-row"><span>Slope · β</span><span>The change of the level per step. Optional.</span></div>
<div class="anat-row"><span>Season · γ</span><span>A share for each position in the season (7 days of the week, 12 months of the year).</span></div>
</div>
<figcaption>The same as the decomposition of Section 10, except that the components are <b>updated</b> with every new observation and can be carried forward.</figcaption>
</figure>

For the daily sales (training up to 5 November 2024), the model with no trend
and an additive season:

```python
fit = ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()

print(round(fit.level.iloc[-1], 1))                 # 314.0
print(fit.season.iloc[-7:].round(1).tolist())
# [-23.2, -11.1, 35.3, 96.0, 48.3, -39.3, -41.3]   (Wednesday ... Tuesday)
```

The forecast is the sum of those two parts: 314.0 + 96.0 = **410.0** for the
first Saturday, 314.0 − 41.3 = 272.7 for the first Tuesday.

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="210.9" x2="666" y2="210.9"/><text class="dim" x="38" y="214.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="175.7" x2="666" y2="175.7"/><text class="dim" x="38" y="179.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="140.5" x2="666" y2="140.5"/><text class="dim" x="38" y="144.0" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="105.3" x2="666" y2="105.3"/><text class="dim" x="38" y="108.8" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="70.1" x2="666" y2="70.1"/><text class="dim" x="38" y="73.6" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="34.9" x2="666" y2="34.9"/><text class="dim" x="38" y="38.4" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">9 Oct</text><line class="line" x1="202.3" y1="230" x2="202.3" y2="234"/><text class="dim" x="202.3" y="246" font-size="10.5" text-anchor="middle">23 Oct</text><line class="line" x1="360.7" y1="230" x2="360.7" y2="234"/><text class="dim" x="360.7" y="246" font-size="10.5" text-anchor="middle">6 Nov</text><line class="line" x1="519.0" y1="230" x2="519.0" y2="234"/><text class="dim" x="519.0" y="246" font-size="10.5" text-anchor="middle">20 Nov</text><rect class="box" x="355.0" y="32" width="311.0" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,207.4 55.3,184.2 66.6,144.7 77.9,110.2 89.2,132.8 100.5,208.1 111.9,212.3 123.2,180.7 134.5,176.4 145.8,148.3 157.1,102.5 168.4,145.4 179.7,193.3 191.0,201.1 202.3,175.0 213.6,183.5 224.9,149.7 236.3,94.7 247.6,130.6 258.9,195.4 270.2,194.0 281.5,185.6 292.8,180.0 304.1,132.8 315.4,89.8 326.7,127.8 338.0,195.4 349.3,199.0 360.7,187.7 372.0,171.5 383.3,139.8 394.6,74.3 405.9,123.6 417.2,191.9 428.5,197.6 439.8,173.6 451.1,173.6 462.4,124.3 473.7,99.0 485.1,110.2 496.4,194.7 507.7,189.8 519.0,189.8 530.3,165.2 541.6,128.5 552.9,93.3 564.2,117.3 575.5,197.6 586.8,184.9 598.1,177.8 609.5,177.8 620.8,150.4 632.1,82.8 643.4,110.2 654.7,197.6 666.0,182.8"/><polyline class="curve" style="stroke-width:2.4" points="360.7,182.2 372.0,173.7 383.3,141.0 394.6,98.3 405.9,131.9 417.2,193.5 428.5,194.2 439.8,182.2 451.1,173.7 462.4,141.0 473.7,98.3 485.1,131.9 496.4,193.5 507.7,194.2 519.0,182.2 530.3,173.7 541.6,141.0 552.9,98.3 564.2,131.9 575.5,193.5 586.8,194.2 598.1,182.2 609.5,173.7 620.8,141.0 632.1,98.3 643.4,131.9 654.7,193.5 666.0,194.2"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">Holt–Winters forecast</text></svg>
  <figcaption>The shaded area is the 28-day test. The forecast is the same seven numbers every week: the level (314) plus that day's seasonal share. Having no trend component, it cannot follow the rise at the end of November.</figcaption>
</figure>

How does it differ from seasonal naive? Seasonal naive copies **a single
week**; the surprises of that week go into the forecast too. Holt–Winters
learns the weekly shares from all the past, giving recent weeks more weight.

## 6. Additive or multiplicative?

The decision of Section 10 holds here too: if the waves grow with the level,
multiplicative. The forecast of 2024 for the monthly passenger series:

| Model | MAE | Percentage error |
|---|---|---|
| Seasonal naive × growth (the bar from Section 14) | 11.11 | 2.8% |
| Additive trend + additive season | 9.90 | 2.4% |
| Additive trend + multiplicative season | 8.61 | 2.2% |
| Multiplicative trend + multiplicative season | **6.53** | 1.7% |

```python
fit = ExponentialSmoothing(
    train, trend="mul", seasonal="mul", seasonal_periods=12
).fit()
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Jan 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Jul 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Jan 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Jul 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Jan 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Jul 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve2" style="stroke-width:2.2" points="470.5,174.7 488.3,182.6 506.1,156.3 523.8,153.9 541.6,141.5 559.4,110.8 577.1,91.0 594.9,79.6 612.7,126.8 630.5,140.3 648.2,167.8 666.0,145.4"/><polyline class="curve" style="stroke-width:2.2" points="470.5,176.7 488.3,183.8 506.1,156.1 523.8,149.9 541.6,137.2 559.4,107.0 577.1,76.1 594.9,69.4 612.7,117.7 630.5,140.2 648.2,164.3 666.0,142.6"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve2" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">additive</text><line class="curve" x1="244" y1="40" x2="262" y2="40"/><text class="ink" x="268" y="44" font-size="11">multiplicative</text></svg>
  <figcaption>The forecast of 2024. Both models capture the pattern; the multiplicative one also gets the height of the summer peak right, because it grows the season with the level.</figcaption>
</figure>

The model that fits the structure of the series (percentage growth, a
proportional season) beats the bar by 41%. Multiplicative components only work
on series whose values are **always positive**.

## 7. Reading the coefficients

The coefficients found tell you how "volatile" the series is:

| Coefficient | Small (close to 0) | Large (close to 1) |
|---|---|---|
| `α` (level) | The level is stable; daily movement is noise | The level keeps drifting; the last value matters |
| `β` (slope) | The slope is constant | The slope changes often |
| `γ` (season) | The pattern is the same from year to year | The pattern is evolving |

In the passenger model all three are **0.00**: the model never changes the
growth rate it found at the start (0.85% a month) or the twelve monthly
factors. That does not mean "the model did not learn"; it means "the pattern
is so stable that no updating is needed".

For the daily sales `α = 0.18`, `γ = 0.13`: both the level and the weekly
shares are updated little by little.

If `α` comes out very close to 1, the model has in fact turned into the naive
forecast; it found nothing to smooth.

## 8. The test: does it clear the bar?

The rig of Section 15: 13 origins, a 28-day horizon.

| Method | Mean MAE | Worst experiment | Experiments in which it beats seasonal naive |
|---|---|---|---|
| Seasonal naive | 17.95 | 41.3 | |
| Holt–Winters, no trend + additive season | **15.91** | 38.6 | 12 / 13 |
| Additive trend + additive season | 16.81 | 51.3 | 12 / 13 |
| Additive trend + multiplicative season | 15.45 | 46.9 | 11 / 13 |

Three things show:

**The gain is real but modest.** The model with no trend is ahead in 12 of the
13 experiments; the difference averages 2.0 with a variation of 1.9 between
experiments. Unlike the "tie" of Section 15, here the difference is
**consistent**. The skill is 1 − 15.91 / 17.95 = 0.11.

**A single split would not have shown it.** On the 5 November split the MAEs
are 11.73 and 11.64: almost the same. The difference only emerged with many
experiments.

**Adding a trend raises the risk.** The worst experiment of the models with a
trend is 47–51; without a trend it is 38.6. The trend extends the year-end
rise 28 days ahead and misses badly in January. The mean error is similar;
**the worst case** is not. Look at both when choosing.

## 9. Its limits

- **One season.** `seasonal_periods` is a single number. On daily data you get
  the weekly pattern; you cannot get the yearly one.
- **A long season is hard.** It learns a separate share for every position;
  three years of data are not enough for a season with `365` positions.
- **It does not know the calendar.** Holidays, campaigns: the worst experiment
  is still at the turn of the year.
- **It cannot take outside information.** Variables such as price or weather
  cannot enter the model.

Section 17 (ARIMA) adds short-term memory, Section 18 the calendar and
external variables.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Not giving `seasonal` on a seasonal series | A flat or linear forecast; no pattern | `seasonal="add"` / `"mul"` and `seasonal_periods` |
| Giving the wrong `seasonal_periods` | The pattern slips | By number of rows: daily–weekly 7, monthly–yearly 12 |
| A multiplicative component on a series with zero or negative values | An error | Additive, or transform first |
| An index with missing days | The seasonal positions slip | `asfreq`, then fill (Section 13) |
| An undamped trend at a long horizon | Unrealistic growth | `damped_trend=True` |
| Choosing the model by its training fit | The complex model always "wins" | The out-of-sample error, a rolling origin |
| Looking only at the mean error | The worst case is hidden | Look at the worst experiment too |
| Not comparing with a baseline | The size of the gain is unknown | Seasonal naive on the same rig |

## Summary

- Exponential smoothing is a **weighted average** of the past; the weights
  decay exponentially going back. `α` sets the speed.
- The **simple** version tracks only the level; its forecast is a flat line.
  `α = 1` is naive.
- **Holt** adds the slope; an additive trend is a constant amount, a
  multiplicative one a constant rate. A **damped** trend is safe at a long
  horizon.
- **Holt–Winters** adds the season; multiplicative if the waves grow with the
  level.
- `ExponentialSmoothing(train, trend=..., seasonal=..., seasonal_periods=m)
  .fit()`; the coefficients are in `fit.params`, the forecast is
  `fit.forecast(h)`.
- The coefficients give a diagnosis: close to 0 is stable, close to 1
  volatile.
- On the daily sales it beats seasonal naive in 12 of 13 experiments; the gain
  is 11%. On the passenger series it beats the bar by 41%.

Exponential smoothing describes a series by its components. The next model
takes another route: it models the **memory** of the series (Section 12)
directly. ARIMA.
