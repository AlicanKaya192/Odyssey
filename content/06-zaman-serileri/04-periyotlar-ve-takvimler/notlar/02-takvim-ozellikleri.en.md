Columns derived from the calendar are called **calendar features**. In
analysis they are grouping keys; later (Section 19) they become inputs to a
machine learning model. All of them **are known in advance for the day being
forecast**, so they carry no leakage risk.

## The basic features

```python
idx = s.index

features = pd.DataFrame({
    "year": idx.year,
    "quarter": idx.quarter,
    "month": idx.month,
    "day": idx.day,
    "dayofweek": idx.dayofweek,
    "dayofyear": idx.dayofyear,
    "week": idx.isocalendar().week.to_numpy(),
    "is_weekend": idx.dayofweek >= 5,
    "is_month_start": idx.is_month_start,
    "is_month_end": idx.is_month_end,
}, index=idx)
```

## Position within the month

| Feature | Code | What it is for |
|---|---|---|
| Day of the month | `idx.day` | Payday and billing-day effects |
| Days left until month end | `((idx + MonthEnd(0)) - idx).days` | The month-end close |
| Week of the month | `(idx.day - 1) // 7 + 1` | A "first week of the month" effect |
| Days in the month | `idx.days_in_month` | Adjusting the monthly total |

## Holidays and working days

```python
holidays = pd.read_csv("holidays_2024.csv", parse_dates=["date"])["date"]

is_holiday = idx.isin(holidays)
is_workday = (idx.dayofweek < 5) & ~is_holiday
day_before_holiday = (idx + pd.Timedelta(days=1)).isin(holidays)
day_after_holiday = (idx - pd.Timedelta(days=1)).isin(holidays)
```

The days **before and after** a holiday matter as much as the holiday itself:
shopping rises the day before, the shop is closed on the day, and the day
after starts slowly. Three separate features, three separate effects.

## Preparing a holiday list

pandas ships only US federal holidays (`USFederalHolidayCalendar`). For
another country you keep the list yourself. Things to watch:

- **Religious holidays fall on different days each year.** One year's list is
  not valid for the next; write each year's dates separately.
- **A holiday on a weekend.** It does not change the number of business days
  but can change the sales pattern.
- **Half days** (the eve of a holiday). They do not behave like full days;
  mark them with a separate column.
- **Bridge days.** When a holiday falls on a Thursday, Friday is officially a
  working day but in practice empty.
- **Write the future too.** If you do not know the holidays of the period you
  are forecasting, the model cannot use them.

## Comparing months fairly

| Case | Divide by |
|---|---|
| Something that happens every day (shop sales, consumption) | Days in the month: `idx.days_in_month` |
| Something that happens only on business days (invoices, production) | Business days in the month |
| Weekdays and weekends differ a lot | Also check how many Saturdays the month has |

```python
monthly = s.groupby(s.index.to_period("M")).sum()
per_day = monthly / monthly.index.days_in_month

workdays = pd.Series(1, index=pd.bdate_range("2024-01-01", "2024-12-31"))
workdays_per_month = workdays.groupby(workdays.index.to_period("M")).sum()
```

**The month with five Saturdays.** A month can have 4 or 5 Saturdays. If
Saturday sales are 1.5 times Monday's, a five-Saturday month gives a higher
total with nothing else changing. This is called the **trading day effect**.

## Comparing the same day with last year

```python
last_year = s.copy()
last_year.index = last_year.index + pd.DateOffset(years=1)
change = s / last_year - 1
```

Careful: "the same date last year" falls on **a different day of the week**
(9 March 2024 is a Saturday, 9 March 2023 a Thursday). In a series with a
strong weekly pattern, going back 364 days (exactly 52 weeks) is fairer:
`s.shift(364)` (Section 06).
