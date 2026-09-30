# ARIMA

Exponential smoothing described a series by its **components**: level, slope,
season. ARIMA takes another route: it describes the series by **its own
past**. "Today is this much of yesterday plus that much of last week's
surprise."

You already know everything it needs. In Section 11 you made a series
stationary; in Section 12 you read its memory with the ACF and PACF and met
the fingerprints of AR and MA. ARIMA is those two sections turned into a
model.

## 1. Three letters, three numbers

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>AR · p</span><span>Autoregressive: today depends on a weighted sum of the last <code>p</code> values.</span></div>
<div class="anat-row"><span>I · d</span><span>Differencing: the model makes the series stationary by differencing it <code>d</code> times and turns the forecast back into levels itself.</span></div>
<div class="anat-row"><span>MA · q</span><span>Moving average: today depends on a weighted sum of the last <code>q</code> surprises (forecast errors).</span></div>
</div>
<figcaption>The model is written <code>ARIMA(p, d, q)</code>. You choose the three numbers; the model finds the coefficients.</figcaption>
</figure>

```python
from statsmodels.tsa.arima.model import ARIMA

fit = ARIMA(train, order=(1, 0, 0)).fit()
```

## 2. AR: the series remembers itself

The simplest form is AR(1): $y_t = c + \phi\,(y_{t-1} - c) + e_t$. Today
carries `φ` times yesterday's deviation from the mean.

For the deviation of the temperature from the seasonal normal (whose PACF was
a single bar in Section 12):

```python
fit = ARIMA(anomaly, order=(1, 0, 0)).fit()
print(fit.params.round(3).to_dict())
# {'const': -0.005, 'ar.L1': 0.724, 'sigma2': 2.06}
```

`φ = 0.724`: 72% of today's deviation carries over to tomorrow. On the last
day the deviation is +1.32 degrees; the forecast:

```python
print(fit.forecast(5).round(2).tolist())     # [0.95, 0.69, 0.5, 0.36, 0.26]
```

Multiplied by 0.724 each day, it **returns to the mean**: 1.32 × 0.724 = 0.95,
0.95 × 0.724 = 0.69...

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="212.8" x2="666" y2="212.8"/><text class="dim" x="38" y="216.3" font-size="10.5" text-anchor="end">−4</text><line class="grid" x1="44" y1="195.4" x2="666" y2="195.4"/><text class="dim" x="38" y="198.9" font-size="10.5" text-anchor="end">−3</text><line class="grid" x1="44" y1="178.0" x2="666" y2="178.0"/><text class="dim" x="38" y="181.5" font-size="10.5" text-anchor="end">−2</text><line class="grid" x1="44" y1="160.6" x2="666" y2="160.6"/><text class="dim" x="38" y="164.1" font-size="10.5" text-anchor="end">−1</text><line class="line" x1="44" y1="143.2" x2="666" y2="143.2"/><text class="dim" x="38" y="146.7" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="125.9" x2="666" y2="125.9"/><text class="dim" x="38" y="129.4" font-size="10.5" text-anchor="end">1</text><line class="grid" x1="44" y1="108.5" x2="666" y2="108.5"/><text class="dim" x="38" y="112.0" font-size="10.5" text-anchor="end">2</text><line class="grid" x1="44" y1="91.1" x2="666" y2="91.1"/><text class="dim" x="38" y="94.6" font-size="10.5" text-anchor="end">3</text><line class="grid" x1="44" y1="73.7" x2="666" y2="73.7"/><text class="dim" x="38" y="77.2" font-size="10.5" text-anchor="end">4</text><line class="grid" x1="44" y1="56.3" x2="666" y2="56.3"/><text class="dim" x="38" y="59.8" font-size="10.5" text-anchor="end">5</text><line class="grid" x1="44" y1="38.9" x2="666" y2="38.9"/><text class="dim" x="38" y="42.4" font-size="10.5" text-anchor="end">6</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="74.3" y1="220" x2="74.3" y2="224"/><text class="dim" x="74.3" y="236" font-size="10.5" text-anchor="middle">5 Nov</text><line class="line" x1="180.5" y1="220" x2="180.5" y2="224"/><text class="dim" x="180.5" y="236" font-size="10.5" text-anchor="middle">12 Nov</text><line class="line" x1="286.7" y1="220" x2="286.7" y2="224"/><text class="dim" x="286.7" y="236" font-size="10.5" text-anchor="middle">19 Nov</text><line class="line" x1="392.9" y1="220" x2="392.9" y2="224"/><text class="dim" x="392.9" y="236" font-size="10.5" text-anchor="middle">26 Nov</text><line class="line" x1="499.1" y1="220" x2="499.1" y2="224"/><text class="dim" x="499.1" y="236" font-size="10.5" text-anchor="middle">3 Dec</text><line class="line" x1="605.3" y1="220" x2="605.3" y2="224"/><text class="dim" x="605.3" y="236" font-size="10.5" text-anchor="middle">10 Dec</text><rect class="box" x="461.2" y="32" width="204.8" height="188" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.5" points="44.0,162.7 59.2,121.5 74.3,154.8 89.5,157.7 104.7,177.5 119.9,204.7 135.0,197.5 150.2,175.1 165.4,133.7 180.5,106.7 195.7,110.5 210.9,145.9 226.0,106.4 241.2,123.0 256.4,140.4 271.6,156.0 286.7,143.5 301.9,102.4 317.1,86.4 332.2,66.7 347.4,62.9 362.6,109.9 377.8,105.0 392.9,93.1 408.1,92.5 423.3,113.4 438.4,150.2 453.6,120.3"/><polyline class="curve2" stroke-dasharray="5 4" style="stroke-width:2" points="453.6,120.3 468.8,120.3 484.0,120.3 499.1,120.3 514.3,120.3 529.5,120.3 544.6,120.3 559.8,120.3 575.0,120.3 590.1,120.3 605.3,120.3 620.5,120.3 635.7,120.3 650.8,120.3 666.0,120.3"/><polyline class="curve" style="stroke-width:2.4" points="453.6,120.3 468.8,126.7 484.0,131.3 499.1,134.6 514.3,137.0 529.5,138.8 544.6,140.0 559.8,140.9 575.0,141.6 590.1,142.1 605.3,142.4 620.5,142.7 635.7,142.9 650.8,143.0 666.0,143.1"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">anomaly (°C)</text><line class="curve2" x1="184" y1="40" x2="202" y2="40"/><text class="ink" x="208" y="44" font-size="11">naive</text><line class="curve" x1="265" y1="40" x2="283" y2="40"/><text class="ink" x="289" y="44" font-size="11">AR(1) forecast</text></svg>
  <figcaption>The shaded area is the 14-day forecast. Naive carries the last deviation unchanged; AR(1) multiplies it by 0.724 each day, bringing it towards zero, that is, towards the seasonal normal.</figcaption>
</figure>

This is a forecast that sits between two baselines. Naive says "the deviation
stays as it is"; the mean says "back to normal tomorrow"; AR(1) says "back
little by little". The error of one-day-ahead forecasts through 2024:

| Mean (deviation = 0) | Naive | AR(1) |
|---|---|---|
| 1.63 | 1.26 | **1.14** |

## 3. MA: the echo of a surprise

MA(1): $y_t = c + e_t + \theta\,e_{t-1}$. Today carries `θ` times yesterday's
**surprise**; the surprise of two days ago is completely forgotten.

Recall the two artificial series of Section 12: `x` was produced by an AR(1)
and `y` by an MA(1), both with a coefficient of 0.7. The model finds them
again:

```python
print(ARIMA(w["x"], order=(1, 0, 0)).fit().params["ar.L1"].round(3))   # 0.691
print(ARIMA(w["y"], order=(0, 0, 1)).fit().params["ma.L1"].round(3))   # 0.7
```

What happens if you try the wrong kind? The **AIC** tells you:

| | AR(1) | MA(1) |
|---|---|---|
| Series `x` | **1622.9** | 1744.9 |
| Series `y` | 1722.5 | **1625.2** |

The **AIC** (Akaike information criterion) rewards the fit of the model to the
data and penalises the number of coefficients. **Smaller is better.** Only the
difference means anything: a gap of a few points does not matter, a gap of a
hundred is clear.

## 4. I: differencing

The lesson of Section 11: AR and MA make sense on a **stationary** series. If
the series is not stationary it is differenced first. `d` is how many times.

ARIMA takes the difference for you and turns the forecast back into levels;
you do not have to deal with `diff` and `cumsum`.

The plainest example is `ARIMA(0, 1, 0)`: difference, and do nothing else.
That is a **random walk**; its forecast is naive. Does the share price need
more than that?

| Model | AIC | Coefficients |
|---|---|---|
| (0, 1, 0) | 3503.1 | |
| (1, 1, 0) | 3503.8 | AR 0.04 |
| (0, 1, 1) | 3503.9 | MA 0.04 |
| (1, 1, 1) | 3503.1 | AR 0.63, MA −0.57 |

None beats the plain model: the differences have no memory (Ljung–Box said so
in Section 12). Note the last row: AR 0.63 and MA −0.57 **cancel each other**.
AR and MA coefficients that are close in size and opposite in sign are the
mark of a model saying nothing with two unnecessary terms.

## 5. Choosing the order

<figure class="fig">
<div class="flow">
<span class="node">Make it stationary<br><code>d</code></span><span class="arrow">→</span>
<span class="node">Look at ACF and PACF<br>candidate <code>p</code>, <code>q</code></span><span class="arrow">→</span>
<span class="node">Fit the candidates<br>compare the AIC</span><span class="arrow">→</span>
<span class="node">Check the residual<br>Ljung–Box</span><span class="arrow">→</span>
<span class="node acc">Test out of sample</span>
</div>
<figcaption>No single step decides. The AIC weeds out candidates; the rolling origin has the last word.</figcaption>
</figure>

1. **`d`:** as in Section 11. 0 or 1 for most series.
2. **Candidates:** the ACF and PACF of the differenced series (Section 12). If
   the PACF cuts off after lag `p`, AR(p); if the ACF cuts off after lag `q`,
   MA(q). On real data the shapes are not clean: you get **two or three
   candidates**.
3. **AIC:** the smallest among the candidates. Only models fitted **on the
   same data with the same `d`** can be compared.
4. **Residual:** the Ljung–Box p-value should be large (no memory left).
5. **Test:** the rig of Section 15. A model that does not clear the bar is
   useless whatever its AIC.

Keep it small: `p` and `q` rarely exceed 2. A model with many terms memorises
the training data.

## 6. Seasonal ARIMA

The same three ideas for the season, **one season back**:

$$\text{ARIMA}(p, d, q)(P, D, Q)_m$$

- `D`: the number of seasonal differences (`diff(m)`).
- `P`: seasonal AR: the **value** one season earlier.
- `Q`: seasonal MA: the **surprise** one season earlier.
- `m`: the length of the season.

```python
fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
```

**The passenger series.** The recipe of Section 11: the waves grow
(logarithm), there is a yearly season (`D = 1`), there is a trend (`d = 1`).
The ACF of the transformed series:

| Lag | 1 | 2 | 3 | 12 |
|---|---|---|---|---|
| ACF | −0.54 | 0.05 | 0.01 | −0.38 |

A single bar at lag 1, then it cuts off: `q = 1`. A single bar at lag 12:
`Q = 1`. The two fingerprints you met in Section 12. The result is the classic
for this kind of series:

```python
import numpy as np

fit = ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
forecast = np.exp(fit.forecast(12))
```

<figure class="fig">
  <svg viewBox="0 0 680 260" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="221.9" x2="666" y2="221.9"/><text class="dim" x="38" y="225.4" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="190.7" x2="666" y2="190.7"/><text class="dim" x="38" y="194.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="159.4" x2="666" y2="159.4"/><text class="dim" x="38" y="162.9" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="128.2" x2="666" y2="128.2"/><text class="dim" x="38" y="131.7" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="97.0" x2="666" y2="97.0"/><text class="dim" x="38" y="100.5" font-size="10.5" text-anchor="end">450</text><line class="grid" x1="44" y1="65.7" x2="666" y2="65.7"/><text class="dim" x="38" y="69.2" font-size="10.5" text-anchor="end">500</text><line class="grid" x1="44" y1="34.5" x2="666" y2="34.5"/><text class="dim" x="38" y="38.0" font-size="10.5" text-anchor="end">550</text><line class="line" x1="44" y1="230" x2="666" y2="230"/><line class="line" x1="44.0" y1="230" x2="44.0" y2="234"/><text class="dim" x="44.0" y="246" font-size="10.5" text-anchor="middle">Jan 2022</text><line class="line" x1="150.6" y1="230" x2="150.6" y2="234"/><text class="dim" x="150.6" y="246" font-size="10.5" text-anchor="middle">Jul 2022</text><line class="line" x1="257.3" y1="230" x2="257.3" y2="234"/><text class="dim" x="257.3" y="246" font-size="10.5" text-anchor="middle">Jan 2023</text><line class="line" x1="363.9" y1="230" x2="363.9" y2="234"/><text class="dim" x="363.9" y="246" font-size="10.5" text-anchor="middle">Jul 2023</text><line class="line" x1="470.5" y1="230" x2="470.5" y2="234"/><text class="dim" x="470.5" y="246" font-size="10.5" text-anchor="middle">Jan 2024</text><line class="line" x1="577.1" y1="230" x2="577.1" y2="234"/><text class="dim" x="577.1" y="246" font-size="10.5" text-anchor="middle">Jul 2024</text><rect class="box" x="461.6" y="32" width="204.4" height="198" opacity="0.55" style="stroke:none"/><polyline class="curve3" style="stroke-width:1.6" points="44.0,213.1 61.8,219.4 79.5,194.4 97.3,187.5 115.1,183.8 132.9,156.9 150.6,128.8 168.4,133.8 186.2,161.9 203.9,186.3 221.7,201.3 239.5,185.7 257.3,195.0 275.0,203.8 292.8,177.5 310.6,176.3 328.3,163.2 346.1,131.3 363.9,112.6 381.7,98.2 399.4,147.6 417.2,159.4 435.0,188.8 452.7,162.5 470.5,175.0 488.3,188.2 506.1,150.7 523.8,140.7 541.6,135.7 559.4,108.2 577.1,73.8 594.9,78.2 612.7,109.4 630.5,141.9 648.2,165.0 666.0,146.3"/><polyline class="curve" style="stroke-width:2.4" points="470.5,176.5 488.3,183.5 506.1,156.7 523.8,149.3 541.6,136.9 559.4,107.5 577.1,76.3 594.9,70.2 612.7,117.6 630.5,141.1 648.2,164.0 666.0,143.6"/><line class="curve3" x1="54" y1="40" x2="72" y2="40"/><text class="ink" x="78" y="44" font-size="11">actual</text><line class="curve" x1="142" y1="40" x2="160" y2="40"/><text class="ink" x="166" y="44" font-size="11">log + (0,1,1)(0,1,1)₁₂</text></svg>
  <figcaption>The forecast of 2024. A model with two coefficients runs alongside the truth in all twelve months; the mean error is 1.6%.</figcaption>
</figure>

| Model | MAE | Percentage error | AIC | Ljung–Box p |
|---|---|---|---|---|
| Seasonal naive × growth | 11.11 | 2.8% | | |
| Holt–Winters (multiplicative) | 6.53 | 1.7% | | |
| (0,1,0)(0,1,0)₁₂ | 10.67 | 2.7% | −485.0 | 0.000 |
| (1,1,0)(0,1,1)₁₂ | 6.59 | 1.7% | −579.0 | 0.016 |
| **(0,1,1)(0,1,1)₁₂** | **6.14** | **1.6%** | **−613.0** | 0.988 |
| (1,1,1)(0,1,1)₁₂ | 6.19 | 1.6% | −611.4 | 0.987 |

Four criteria point to the same model: the smallest AIC, a clean residual, the
smallest test error. Adding an extra AR term (the last row) gains nothing.

Had you skipped the logarithm, the error of the same model would be 11.05: the
transformation is part of the model.

## 7. Reading the summary

```python
print(fit.summary().tables[1])
```

```text
                 coef    std err          z      P>|z|      [0.025      0.975]
ma.L1         -0.9435      0.047    -19.942      0.000      -1.036      -0.851
ma.S.L12      -0.9511      0.380     -2.504      0.012      -1.695      -0.207
sigma2         0.0003   9.56e-05      2.693      0.007       7e-05       0.000
```

- **coef:** the coefficient. `ma.L1` is the short-term and `ma.S.L12` the
  seasonal MA term.
- **P>|z|:** how well the coefficient can be told from zero. Above 0.05 the
  term is probably unnecessary.
- **[0.025, 0.975]:** the confidence interval of the coefficient. If it
  contains zero, the same conclusion.
- **sigma2:** the variance of the residual.

## 8. The daily sales

In the ACF of the seasonal difference (`diff(7)`) lag 1 is 0.16 and lag 7 is
−0.43 (Section 12). The candidates, on the single split (5 November):

| Model | AIC | Ljung–Box p | MAE |
|---|---|---|---|
| (0,0,0)(0,1,0)₇ | 8782.5 | 0.000 | 11.64 |
| (1,0,0)(0,1,1)₇ | 8423.1 | 0.000 | 14.90 |
| (0,1,1)(0,1,1)₇ | 8265.8 | 0.035 | 10.48 |
| (1,1,1)(0,1,1)₇ | 8258.7 | 0.311 | 10.44 |

The first row is familiar: a seasonal difference only, no other term. That is
**seasonal naive itself** (MAE 11.64). The baselines are the plainest members
of the ARIMA family.

The second row is a warning: its AIC is far better than the first, yet its
test error is **worse** and memory is left in its residual. With `d = 0` it
cannot follow the shift in level. The AIC alone is not enough.

The last two models are good on AIC, residual and test alike.

## 9. The test

The rig of Section 15: 13 origins, a 28-day horizon.

| Method | Mean MAE | Worst experiment |
|---|---|---|
| Seasonal naive | 17.95 | 41.3 |
| Holt–Winters | 15.91 | 38.6 |
| ARIMA (0,1,1)(0,1,1)₇ | 15.94 | 52.2 |
| ARIMA (1,1,1)(0,1,1)₇ | 15.87 | 52.7 |

ARIMA beats seasonal naive in 11 of the 13 experiments. Against Holt–Winters
the difference is −0.02 with a variation of 5.1 between experiments: **a dead
heat.**

This result matters. Two completely different models (one modelling
components, the other memory) arrive at the same error. So the limit is not in
the model but **in the data**: the past of this series says only this much
about 28 days ahead. Going further takes not a more complex model but **new
information**: the calendar, holidays, campaigns. That is exactly Section 18.

The worst experiment of ARIMA is markedly worse than that of Holt–Winters (52
against 39): `d = 1` carries the year-end level into January. When the mean
error is the same and the worst case differs, the risk-averse choice is clear.

## 10. Which one when?

| | Exponential smoothing | ARIMA |
|---|---|---|
| How it describes the series | Level, slope, season | Past values and surprises |
| Where it is strong | A marked trend and season | Short-term memory; sensor and deviation series |
| Multiplicative structure | Directly (`"mul"`) | Through the logarithm |
| Settings | Choice of components | Choice of `p, d, q, P, D, Q` |
| External variables | Cannot take them | Can (Section 18) |

In practice fit both, test them on the same rig, and if they tie choose the
simpler one.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| `d = 0` on a non-stationary series | Memory in the residual, a drifting forecast | `d` and `D` by the recipe of Section 11 |
| More differences than needed | Volatility rises, the MA coefficient sticks to −1 | The fewest differences |
| Large `p` and `q` | Memorising; coefficients that cancel | Keep it small; look at the AIC and the p-values |
| Comparing AIC across different `d` | Meaningless | Same data, same differencing only |
| Trusting the AIC alone | A model that is poor out of sample | The residual and a rolling origin |
| Forgetting the logarithm on a multiplicative series | Twice the error | `np.log` → model → `np.exp` |
| Forgetting `m` in `seasonal_order` | The season is not modelled | `(P, D, Q, m)` |
| Including the first residuals in the check | The start-up effect spoils the test | Drop the first `d + D × m` values |

## Summary

- **AR(p)**: past values. **MA(q)**: past surprises. **I(d)**: differencing.
- An AR(1) forecast returns to the mean at the rate `φ`; the effect of an
  MA(1) ends in one step; `ARIMA(0,1,0)` is a random walk.
- The seasonal version `(p,d,q)(P,D,Q)ₘ`: the same ideas one season back.
- The order: `d` from stationarity, candidates from the ACF/PACF, weeding out
  by the **AIC**, confirmation by the **residual** (Ljung–Box) and the
  **rolling origin**.
- `ARIMA(train, order=..., seasonal_order=...).fit()`; `.params`,
  `.summary()`, `.forecast(h)`, `.resid`, `.aic`.
- For the passenger series `log` + (0,1,1)(0,1,1)₁₂ brings the error down to
  1.6%.
- On the daily sales ARIMA and Holt–Winters **tie**: the limit is in the data,
  not in the model.

The next section goes past that limit: you give the model information other
than the series' own past. Holidays, campaigns, the weather.
