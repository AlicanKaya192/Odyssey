## Reading and taking apart

| Code | What it does |
|---|---|
| `pd.to_datetime(s, format="%d.%m.%Y")` | turns text into dates |
| `errors="coerce"` | makes what cannot be read `NaT` |
| `s.dt.year` / `.month` / `.day` / `.hour` | the parts |
| `s.dt.dayofweek` | Monday = 0 … Sunday = 6 |
| `s.dt.day_name()` | the day's name |
| `s.dt.strftime("%d/%m")` | formatted text |
| `s.dt.to_period("M")` | a month period |
| `s.dt.tz_localize("UTC")` / `.dt.tz_convert(...)` | time zones on a column |

## A date index

| Code | What it does |
|---|---|
| `pd.date_range(start, periods=n, freq="D")` | evenly spaced dates |
| `s.loc["2026-02"]` | all of February |
| `s.loc["2026-03-10":"2026-03-12"]` | a range (both ends included) |
| `s.resample("ME").sum()` | monthly total |
| `s.asfreq("D")` | adds missing days as `NaN` |
| `s.shift(1)` / `diff()` / `pct_change()` | comparing with the previous value |
| `s.rolling(7).mean()` | the last 7 rows |
| `s.rolling("7D").mean()` | the last 7 days |

## Frequency codes

| Code | Meaning |
|---|---|
| `"D"` / `"h"` / `"min"` | day / hour / minute |
| `"W"` | week ending on Sunday |
| `"W-MON"` | Mondays |
| `"ME"` / `"MS"` | month end / month start |
| `"QE"` / `"YE"` | quarter end / year end |

## Errors

| Symptom | Cause |
|---|---|
| `doesn't match format` | mixed formats in the column |
| `'M' is no longer supported` | `"ME"` in pandas 3 |
| `Cannot compare tz-naive and tz-aware` | zoned and unzoned mixed |
| `Only valid with DatetimeIndex` in `resample` | the index is still text; `to_datetime` |
| A strange first-week average | the first bucket is short |
| The rolling average does not see a missing day | `rolling(n)` counts rows |
