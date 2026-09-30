These words will come up again and again throughout the track. You will
meet them under these names in other sources and in library documentation.

## The series itself

| Term | Meaning |
|---|---|
| Time series | Measurements ordered in time |
| Timestamp | The moment a measurement was taken: `2022-01-01` or `2024-03-01 14:00` |
| Observation | One (time, value) pair; one row of the table |
| Frequency | The gap between two observations: hourly, daily, monthly |
| Regular series | Evenly spaced observations; exactly one row per day |
| Irregular series | Uneven gaps; recorded as events arrive |
| Univariate | One value at each timestamp (sales only) |
| Multivariate | Several values at each timestamp (sales, price, weather) |

## Patterns

| Term | Meaning |
|---|---|
| Trend | The long-term direction: up, down, flat |
| Seasonality | A repeat with a fixed length, tied to the calendar |
| Period | How many steps the pattern takes to repeat: 7 for a weekly pattern in daily data |
| Cycle | Ups and downs that repeat without a fixed length |
| Noise | What is left that no pattern explains |
| Level | The current "average height" of the series |
| Structural break | The rules of the series changing all at once |

## Forecasting

| Term | Meaning |
|---|---|
| Forecast | An estimate of future values |
| Horizon | How many steps ahead you forecast: 30 for "the next 30 days" |
| Lag | A past value: sales one day earlier is lag 1 |
| Splitting by time | Train on the past, test on the future; instead of a random split |
| Backtesting | Measuring again and again at different points in the past, as if you had forecast on that day |
| Leakage | The model seeing future information that would not be known at that moment |

## Coming in later sections

For now just know these by name; each gets its own section.

| Term | Where |
|---|---|
| Resampling | Section 05 |
| Rolling window | Section 07 |
| Decomposition | Section 10 |
| Stationarity | Section 11 |
| Autocorrelation | Section 12 |
| Exponential smoothing | Section 16 |
| ARIMA | Section 17 |
| Prediction interval | Section 20 |
