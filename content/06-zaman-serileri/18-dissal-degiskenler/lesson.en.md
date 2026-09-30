# External Variables

Section 17 ended at a limit: two very different models arrived at the same
error, because both looked only at **the series' own past**. The past does
not know there will be a campaign tomorrow. It does not know next Thursday is
a public holiday. It does not know the weather will warm up next week.

You do. The way to give the model that information is **external variables**:
columns from outside the series that affect it. In this section you build
them, give them to the model and ask the most important question: **will I
have this information at forecast time?**

## 1. Three kinds of outside information

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Calendar</span><span>Holidays, weekends, day of the month, school terms. Their future is known <b>for certain</b>.</span></div>
<div class="anat-row"><span>Planned</span><span>Campaigns, price, advertising budget, opening hours. <b>You decide</b> their future.</span></div>
<div class="anat-row"><span>Measured</span><span>Air temperature, exchange rate, a competitor's price. Their future is <b>unknown</b>; it needs a forecast of its own.</span></div>
</div>
<figcaption>The first two are ready at forecast time. The third is the hard part of the section.</figcaption>
</figure>

The data of this section is a café in a business district (`cafe_daily.csv`),
with one variable of each kind:

```python
import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
print(c.head(3))
```

```text
            sales  temp_c  promo  holiday
date
2022-01-01     46     7.1      0        1
2022-01-02     86     6.1      0        0
2022-01-03    205     8.6      0        0
```

`promo` and `holiday` are **dummy variables**: 1 if the event is on, 0 if not.
Over three years there are 84 campaign days and 41 public holidays.

## 2. Measuring an effect roughly, and the trap

How many sales does a campaign bring? The first thing that comes to mind:

```python
print(round(c.loc[c["promo"] == 1, "sales"].mean(), 1))     # 284.0
print(round(c.loc[c["promo"] == 0, "sales"].mean(), 1))     # 227.1
```

A difference of 57. But the comparison is **not fair**: campaigns always run
Thursday to Saturday, and sales on those days differ from the average anyway.
The day of the week is a **confounder** standing in between.

A fairer comparison: compare each campaign day with **the same weekday** a
week before and a week after.

| | Rough difference | Against neighbours on the same weekday |
|---|---|---|
| Campaign | +57.0 | +50.8 |
| Holiday | −67.3 | −76.2 |

Measured roughly, the effect of a holiday looks **smaller** than it is: most
holidays fall in spring and summer, the warm months when sales are high
anyway. Temperature is a second confounder.

Separating all the effects **at once** takes a model.

## 3. ARIMA with external variables

You give ARIMA a table through `exog`. The model does two jobs together: it
estimates the effect of the external variables with a regression and models
**what is left** with an ARIMA.

```python
from statsmodels.tsa.arima.model import ARIMA

train = c.loc[:"2024-10-31"]
columns = ["promo", "holiday", "temp_c"]

fit = ARIMA(
    train["sales"], exog=train[columns],
    order=(1, 0, 0), seasonal_order=(0, 1, 1, 7),
).fit()
print(fit.summary().tables[1])
```

```text
                 coef    std err          z      P>|z|      [0.025      0.975]
promo         49.3391      1.636     30.163      0.000      46.133      52.545
holiday      -75.2347      1.403    -53.612      0.000     -77.985     -72.484
temp_c         5.5143      0.089     61.619      0.000       5.339       5.690
ar.L1          0.5077      0.027     18.896      0.000       0.455       0.560
ma.S.L7       -0.9139      0.014    -64.185      0.000      -0.942      -0.886
```

The first three rows read directly:

- **A campaign day is +49 sales.** (The rough calculation said 57.)
- **A public holiday is −75 sales.** The business district empties.
- **Each degree is +5.5 sales.** That is why summer is busy.

The last two rows are familiar ARIMA terms: the short memory and the weekly
pattern left in the part the external variables cannot explain.

The AIC fell from 9464 to 7569: nearly two thousand points. In Section 17 you
worked for "a few points"; new information does what tuning the order cannot.

## 4. Forecasting: the future variables are needed too

To get a forecast from a model with external variables you have to supply
their **future** values as well:

```python
test = c.loc["2024-11-01":"2024-11-28"]
forecast = fit.forecast(28, exog=test[columns])
```

The number of rows must match the horizon and the columns must be in the same
order as in training. The model takes this table and can say "there is a
campaign on 14–16 November, add 49".

But there is a problem: in this code `test[columns]` holds the **actual
temperatures** of November. On 31 October you could not have known them.

## 5. Known and unknown in the future

<figure class="fig">
<div class="versus">
<div class="ok"><h4>Ready at forecast time</h4><p>Calendar: the list of holidays is known years ahead.</p><p>Plan: the campaign calendar, the price list.</p><p>You write their future values directly.</p></div>
<div class="no"><h4>Unknown at forecast time</h4><p>Weather, exchange rate, competitors, demand.</p><p>Their future needs <b>a forecast of its own</b>.</p><p>The error of that forecast is added to yours.</p></div>
</div>
<figcaption>Before putting a variable into the model, ask: will I have this number on the day I make the forecast?</figcaption>
</figure>

Three options for the temperature, and the result of each across 13
experiments (a 28-day horizon):

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="216.0" x2="666" y2="216.0"/><text class="dim" x="38" y="219.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="164.6" x2="666" y2="164.6"/><text class="dim" x="38" y="168.1" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="113.3" x2="666" y2="113.3"/><text class="dim" x="38" y="116.8" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="61.9" x2="666" y2="61.9"/><text class="dim" x="38" y="65.4" font-size="10.5" text-anchor="end">30</text><line class="line" x1="44" y1="216" x2="666" y2="216"/><line class="line" x1="95.8" y1="216" x2="95.8" y2="220"/><text class="dim" x="95.8" y="232" font-size="10.5" text-anchor="middle">seasonal naive</text><line class="line" x1="182.2" y1="216" x2="182.2" y2="220"/><text class="dim" x="182.2" y="232" font-size="10.5" text-anchor="middle">Holt–Winters</text><line class="line" x1="268.6" y1="216" x2="268.6" y2="220"/><text class="dim" x="268.6" y="232" font-size="10.5" text-anchor="middle">ARIMA</text><line class="line" x1="355.0" y1="216" x2="355.0" y2="220"/><text class="dim" x="355.0" y="232" font-size="10.5" text-anchor="middle">+ calendar</text><line class="line" x1="441.4" y1="216" x2="441.4" y2="220"/><text class="dim" x="441.4" y="232" font-size="10.5" text-anchor="middle">+ last temp.</text><line class="line" x1="527.8" y1="216" x2="527.8" y2="220"/><text class="dim" x="527.8" y="232" font-size="10.5" text-anchor="middle">+ seasonal normal</text><line class="line" x1="614.2" y1="216" x2="614.2" y2="220"/><text class="dim" x="614.2" y="232" font-size="10.5" text-anchor="middle">+ actual temp.</text><rect class="dot2" x="69.1" y="51.4" width="53.5" height="164.6" rx="3" opacity="0.9"/><rect class="dot2" x="155.4" y="65.7" width="53.6" height="150.3" rx="3" opacity="0.9"/><rect class="dot2" x="241.8" y="65.7" width="53.6" height="150.3" rx="3" opacity="0.9"/><rect class="dot" x="328.2" y="91.2" width="53.6" height="124.8" rx="3" opacity="0.9"/><rect class="dot" x="414.6" y="125.3" width="53.6" height="90.7" rx="3" opacity="0.9"/><rect class="dot" x="501.0" y="138.9" width="53.6" height="77.1" rx="3" opacity="0.9"/><rect class="dim" x="587.4" y="167.7" width="53.5" height="48.3" rx="3" opacity="0.9"/><text class="ink" x="95.8" y="45.2" font-size="11.5" text-anchor="middle">32.1</text><text class="ink" x="182.2" y="59.6" font-size="11.5" text-anchor="middle">29.3</text><text class="ink" x="268.6" y="59.6" font-size="11.5" text-anchor="middle">29.3</text><text class="ink" x="355.0" y="85.1" font-size="11.5" text-anchor="middle">24.3</text><text class="ink" x="441.4" y="119.1" font-size="11.5" text-anchor="middle">17.7</text><text class="ink" x="527.8" y="132.8" font-size="11.5" text-anchor="middle">15.0</text><text class="ink" x="614.2" y="161.6" font-size="11.5" text-anchor="middle">9.4</text></svg>
  <figcaption>The mean MAE of 13 experiments. Orange: the past of the series only. Purple: external variables, with what is known at forecast time. Grey: with the actual future temperature; not attainable, a ceiling.</figcaption>
</figure>

| Method | Mean MAE | Worst experiment |
|---|---|---|
| Seasonal naive | 32.06 | 54.1 |
| Holt–Winters | 29.26 | 76.5 |
| ARIMA, no external variables | 29.26 | 75.6 |
| + calendar (campaign, holiday) | 24.30 | 38.7 |
| + temperature: the last known value | 17.67 | 31.5 |
| + temperature: the seasonal normal | **15.01** | 18.8 |
| + temperature: the actual value (cheating) | 9.40 | 11.4 |

Three conclusions from the table:

**New information changes a lot.** The three models without external variables
were stuck between 29 and 32; with the calendar and the seasonal normal the
error halves and the worst experiment drops from 76 to 19.

**A sensible proxy is enough for an unknown variable.** Nobody can know the
temperature 28 days ahead, but the average of that calendar day in past years
(the seasonal normal) is a good estimate:

```python
normal = train["temp_c"].groupby(train.index.dayofyear).mean()
future["temp_c"] = [normal[day] for day in future.index.dayofyear]
```

"The last known temperature" is worse: it carries the same number for 28 days
and gets it wrong as the season turns.

**The last row is not a forecast, it is a ceiling.** 9.40 with the actual
temperature: that is where you could get to with a perfect weather forecast.
Reporting it as your performance is **leakage**: you would have used a future
measurement. Its use lies elsewhere: the gap between 15.01 and 9.40 tells you
the most a better weather forecast could gain you.

## 6. A long season: Fourier terms

Seasonal ARIMA and Holt–Winters took a single, short season. On daily data you
got the weekly pattern; you could not get the **yearly** one (a season of 365
days). In the café the temperature did that job. What if you have no variable
like temperature?

A smooth yearly wave can be described as the sum of a few sines and cosines.
Those too are external variables:

```python
import numpy as np


def fourier(index, K, period=365.25):
    day = index.dayofyear.to_numpy()
    columns = {}
    for k in range(1, K + 1):
        columns[f"sin{k}"] = np.sin(2 * np.pi * k * day / period)
        columns[f"cos{k}"] = np.cos(2 * np.pi * k * day / period)
    return pd.DataFrame(columns, index=index)
```

`K = 1` is a single gentle wave (one peak, one trough); `K = 2` a shape that
can bend twice a year. Each `K` adds two columns. Being tied to the calendar,
their future is known **for certain**: `fourier(future_index, K)`.

Go back to the daily shop sales of Section 17. There the worst experiments of
ARIMA were at the turn of the year. Add two pieces of calendar information:
the yearly wave (Fourier, `K = 2`) and the year-end climb in December (a
column that grows as the day of the month advances).

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="220.0" x2="666" y2="220.0"/><text class="dim" x="38" y="223.5" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="187.2" x2="666" y2="187.2"/><text class="dim" x="38" y="190.7" font-size="10.5" text-anchor="end">10</text><line class="grid" x1="44" y1="154.5" x2="666" y2="154.5"/><text class="dim" x="38" y="158.0" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="121.7" x2="666" y2="121.7"/><text class="dim" x="38" y="125.2" font-size="10.5" text-anchor="end">30</text><line class="grid" x1="44" y1="89.0" x2="666" y2="89.0"/><text class="dim" x="38" y="92.5" font-size="10.5" text-anchor="end">40</text><line class="grid" x1="44" y1="56.2" x2="666" y2="56.2"/><text class="dim" x="38" y="59.7" font-size="10.5" text-anchor="end">50</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="76.5" y1="220" x2="76.5" y2="224"/><text class="dim" x="76.5" y="236" font-size="10.5" text-anchor="middle">2 Jan</text><line class="line" x1="169.3" y1="220" x2="169.3" y2="224"/><text class="dim" x="169.3" y="236" font-size="10.5" text-anchor="middle">27 Feb</text><line class="line" x1="262.2" y1="220" x2="262.2" y2="224"/><text class="dim" x="262.2" y="236" font-size="10.5" text-anchor="middle">23 Apr</text><line class="line" x1="355.0" y1="220" x2="355.0" y2="224"/><text class="dim" x="355.0" y="236" font-size="10.5" text-anchor="middle">18 Jun</text><line class="line" x1="447.8" y1="220" x2="447.8" y2="224"/><text class="dim" x="447.8" y="236" font-size="10.5" text-anchor="middle">13 Aug</text><line class="line" x1="540.7" y1="220" x2="540.7" y2="224"/><text class="dim" x="540.7" y="236" font-size="10.5" text-anchor="middle">8 Oct</text><line class="line" x1="633.5" y1="220" x2="633.5" y2="224"/><text class="dim" x="633.5" y="236" font-size="10.5" text-anchor="middle">3 Dec</text><rect class="dot2" x="58.9" y="49.0" width="16.7" height="171.0" rx="3" opacity="0.9"/><rect class="dot2" x="105.3" y="186.1" width="16.7" height="33.9" rx="3" opacity="0.9"/><rect class="dot2" x="151.7" y="179.5" width="16.7" height="40.5" rx="3" opacity="0.9"/><rect class="dot2" x="198.1" y="187.6" width="16.7" height="32.4" rx="3" opacity="0.9"/><rect class="dot2" x="244.5" y="181.0" width="16.7" height="39.0" rx="3" opacity="0.9"/><rect class="dot2" x="290.9" y="181.9" width="16.8" height="38.1" rx="3" opacity="0.9"/><rect class="dot2" x="337.4" y="190.9" width="16.7" height="29.1" rx="3" opacity="0.9"/><rect class="dot2" x="383.8" y="191.6" width="16.7" height="28.4" rx="3" opacity="0.9"/><rect class="dot2" x="430.2" y="152.2" width="16.7" height="67.8" rx="3" opacity="0.9"/><rect class="dot2" x="476.6" y="192.9" width="16.7" height="27.1" rx="3" opacity="0.9"/><rect class="dot2" x="523.0" y="185.7" width="16.7" height="34.3" rx="3" opacity="0.9"/><rect class="dot2" x="569.5" y="185.7" width="16.7" height="34.3" rx="3" opacity="0.9"/><rect class="dot2" x="615.9" y="117.3" width="16.7" height="102.7" rx="3" opacity="0.9"/><rect class="dot" x="77.4" y="191.3" width="16.7" height="28.7" rx="3" opacity="0.9"/><rect class="dot" x="123.8" y="189.0" width="16.7" height="31.0" rx="3" opacity="0.9"/><rect class="dot" x="170.3" y="179.8" width="16.7" height="40.2" rx="3" opacity="0.9"/><rect class="dot" x="216.7" y="191.2" width="16.7" height="28.8" rx="3" opacity="0.9"/><rect class="dot" x="263.1" y="186.5" width="16.7" height="33.5" rx="3" opacity="0.9"/><rect class="dot" x="309.5" y="182.8" width="16.7" height="37.2" rx="3" opacity="0.9"/><rect class="dot" x="355.9" y="192.7" width="16.7" height="27.3" rx="3" opacity="0.9"/><rect class="dot" x="402.3" y="190.9" width="16.8" height="29.1" rx="3" opacity="0.9"/><rect class="dot" x="448.8" y="179.0" width="16.7" height="41.0" rx="3" opacity="0.9"/><rect class="dot" x="495.2" y="194.6" width="16.7" height="25.4" rx="3" opacity="0.9"/><rect class="dot" x="541.6" y="189.8" width="16.7" height="30.2" rx="3" opacity="0.9"/><rect class="dot" x="588.0" y="183.5" width="16.7" height="36.5" rx="3" opacity="0.9"/><rect class="dot" x="634.4" y="173.0" width="16.7" height="47.0" rx="3" opacity="0.9"/><line class="curve2" x1="54" y1="38" x2="72" y2="38"/><text class="ink" x="78" y="42" font-size="11">ARIMA</text><line class="curve" x1="135" y1="38" x2="153" y2="38"/><text class="ink" x="159" y="42" font-size="11">ARIMA + calendar</text></svg>
  <figcaption>Daily shop sales, the MAE of 13 experiments; the horizontal axis is the day the training ends. Calendar information changes little in ordinary periods, yet removes the two giant errors at the turn of the year.</figcaption>
</figure>

| Model | Mean MAE | Worst experiment |
|---|---|---|
| ARIMA (0,1,1)(0,1,1)₇ | 15.94 | 52.2 |
| + trend + Fourier (`K = 2`) | 13.16 | 33.0 |
| + Fourier + the December climb | **10.23** | 14.4 |

In Section 17 we said "the limit is in the data". Once you tell the model what
the data does not (where in the year we are), the limit moves: the mean error
fell by a third and the worst experiment from 52 to 14.

How did we know about the December column? In Section 15 you saw that the
worst experiments were **always at the turn of the year**. Where the bad
experiments sit in the calendar tells you which variable is missing.

## 7. Traps

**Leakage.** The value of an external variable for **the same day** you are
forecasting cannot be used if it is not known at forecast time. "That day's
number of customers" explains sales very well, but today you do not know
tomorrow's number of customers. Such variables can only be used **lagged**:
`visitors.shift(1)`.

**Confounders.** A coefficient is the effect "with the other variables held
fixed". Leave an important variable out and its effect sticks to its
neighbours: drop the temperature and the campaign coefficient drifts from 49
to 53.

**Values never seen in training.** The model does not know what happens at
−5 degrees, or in a three-week campaign instead of a three-day one; it extends
the linear effect as it is.

**Few examples.** The effect of an event that happens once a year (New Year)
is estimated from three observations in three years of data. Look at the
confidence interval of the coefficient.

**The effect is not constant.** The same campaign may not have the same effect
the fifth time round. Refit the model regularly and watch the coefficients.

**Many variables.** Every column is a coefficient; a few are a decision, many
are memorising. Put in the variables whose effect you can explain.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Not giving `exog` to `forecast` | An error: the future variables are missing | `fit.forecast(h, exog=future)` |
| A different order or number of columns in the future table | An error, or multiplication by the wrong coefficient | The training columns, in the same order |
| Using the actual measurements of the test period | Leakage; an unbelievably good result | Forecast the unknown variable too |
| Reporting the "actual value" result as performance | A model that collapses in production | Show it as a ceiling, report it separately |
| An unknown variable for the same day | Leakage | Lagged, with `shift` |
| Taking a rough difference of means for an effect | Biased because of confounders | A model, or a comparison with similar days |
| 7 dummies plus a seasonal difference for a weekly season | The same information twice; the model cannot be fitted | Choose one |
| A very large `K` | The wave memorises noise | `K` of 1–3; choose with a rolling origin |

## Summary

- An **external variable** is information from outside the series' own past:
  calendar, plan, measurement.
- `ARIMA(y, exog=X, ...)` models the effects with a regression and the rest
  with an ARIMA. The coefficients read directly: "campaign +49".
- A forecast needs the **future** `X`: `fit.forecast(h, exog=X_future)`.
- The future of calendar and plan variables is known. The future of a
  **measured** variable is not: use a proxy such as the seasonal normal; the
  result with the actual value is a ceiling, not performance.
- **Fourier terms** describe a long (yearly) season with a few columns.
- Where the bad experiments sit in the calendar points to the missing
  variable.
- In the café the error went from 29 to 15, in the shop from 16 to 10: the
  gain came not from the model but from **new information**.

External variables are a table: each row a day, each column a piece of
information. That is the native language of machine learning. In the next
section you turn forecasting into a table problem and use the tools of the
Machine Learning track.
