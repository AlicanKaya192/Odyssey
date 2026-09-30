## Calendar variables

Their future is known for certain; they are ready at forecast time.

```python
X = pd.DataFrame(index=index)

X["weekend"] = (index.dayofweek >= 5).astype(int)
X["month_end"] = index.is_month_end.astype(int)
X["payday"] = index.day.isin([1, 15]).astype(int)
X["holiday"] = index.isin(holiday_dates).astype(int)
```

| Variable | What for |
|---|---|
| Weekend / day of the week | The weekly pattern (if you are not using a seasonal model) |
| Day of the month, month end, payday | The pattern within a month: rent, bills, salaries |
| Public holiday | A one-day break |
| Before / after a holiday | The shopping rush, bridge days |
| School term, season opening | Long-lasting regimes |
| Month, or Fourier terms | The yearly pattern |

**A holiday window.** The effect is usually not limited to the holiday itself:

```python
holiday = pd.Series(index.isin(holiday_dates).astype(int), index=index)
X["holiday"] = holiday
X["before_holiday"] = holiday.shift(-1, fill_value=0)     # the day before a holiday
X["after_holiday"] = holiday.shift(1, fill_value=0)       # the day after a holiday
```

Here `shift(-1)` is **not** leakage: the holiday calendar is known in advance.

**Moving holidays.** Religious holidays move back by about 11 days every year;
"day of the month" or a seasonal component cannot catch them. An explicit list
of holidays is needed.

**Not every holiday is the same.** A single `holiday` column gives every
holiday the same effect. If there is enough data, split them by kind:
`religious`, `national`, `new_year`.

## The dummy variable trap

If you open a separate column for every value of a category (the 7 days of the
week) and also keep a constant in the model, the columns determine each other
exactly and the model cannot be fitted. Leave one out (6 columns); it becomes
the baseline for comparison.

For the same reason: **a seasonal difference and seasonal dummies are not used
together.** Adding day-of-week dummies when you have
`seasonal_order=(0, 1, 1, 7)` gives the same information twice.

## Fourier terms

```python
def fourier(index, K, period=365.25):
    day = index.dayofyear.to_numpy()
    columns = {}
    for k in range(1, K + 1):
        columns[f"sin{k}"] = np.sin(2 * np.pi * k * day / period)
        columns[f"cos{k}"] = np.cos(2 * np.pi * k * day / period)
    return pd.DataFrame(columns, index=index)
```

| `K` | Columns | Shape |
|---|---|---|
| 1 | 2 | A single gentle wave |
| 2 | 4 | Two bends; an asymmetric peak |
| 3 | 6 | Sharper detail |
| 6+ | 12+ | Almost a level of its own for each month; a risk of memorising |

- Sine and cosine come **together**: the pair sets both the size and the shift
  of the wave.
- For a daily pattern in hourly data use `period=24` and the hour; for a
  weekly one `period=168`.
- Fourier terms cannot catch sharp, short-lived effects (the week of New
  Year); those need a column of their own.
- Choose `K` with a rolling origin. On this series `K = 3` made the error
  **worse**.

## Planned variables

| Variable | Form | Note |
|---|---|---|
| Campaign | 0 / 1 | Separate columns if length and kind differ |
| Discount rate | A number (0.20) | The effect may not be linear |
| Price | A number; often `log` | If sales are `log` too, the coefficient is an elasticity |
| Advertising spend | A number; with a delayed effect | `shift(1)`, `shift(2)` or a rolling sum |
| Stock / capacity | An upper limit | Sales show not demand but **what could be sold** |

You write the future of a planned variable; that makes it possible to ask
**scenarios**: for "what if we do not run the campaign?" run the same model
with `promo = 0`.

## Measured variables

| Variable | What to use for the future |
|---|---|
| Temperature (long horizon) | The seasonal normal |
| Temperature (1–7 days) | A weather forecast service; use the **forecast** in training too |
| Exchange rate, price index | The last value (a random walk) |
| Competitor's price, traffic | A lagged value: `shift(h)` |

**Training and forecasting must be of the same kind.** If you use the actual
temperature in training and a weather forecast when forecasting, the model is
tuned to a more reliable variable than the one it gets. If possible, use that
day's weather **forecast** in training too.

## Lagged external variables

The way to use an unknown variable without leakage:

```python
X["temp_lag1"] = temp.shift(1)       # yesterday's temperature: known for a 1-step forecast
X["temp_lag7"] = temp.shift(7)       # known for a 7-step forecast too
```

The rule: if you forecast `h` steps ahead, the variable must be lagged by at
least `h` steps. At a 28-day horizon `shift(1)` is still leakage.

## Which variable, and is it ready at forecast time?

| Variable | Ready? |
|---|---|
| Day of the week, month, holiday, Fourier | Yes |
| Campaign calendar, price list | Yes (if the plan does not change) |
| Yesterday's sales, yesterday's temperature | Only for a 1-step forecast |
| Today's number of customers, today's temperature | No |
| Next week's weather forecast | Yes, but with error; use the forecast in training too |
