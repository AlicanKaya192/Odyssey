A courier promises "delivery within 3 business days".
`holidays_2024.csv` holds Turkey's public holidays for 2024 (`date`,
`name`).

**What to do:**

1. Read the holiday dates: `pd.read_csv(..., parse_dates=["date"])["date"]`.
2. Build `workday = CustomBusinessDay(holidays=holidays)`.
3. Find the number of working days in 2024 in two ways and print them on one
   line: skipping weekends only (`pd.bdate_range`) and skipping holidays as
   well (`pd.date_range(..., freq=workday)`).
4. For these three order days compute the delivery day in two ways
   (`+ BDay(3)` and `+ 3 * workday`) and print
   `order without with` (`"%Y-%m-%d"`):

   ```python
   orders = ["2024-03-08", "2024-04-09", "2024-06-14"]
   ```

**Expected output:**

```
262 250
2024-03-08 2024-03-13 2024-03-13
2024-04-09 2024-04-12 2024-04-17
2024-06-14 2024-06-19 2024-06-24
```

For the March order both methods give the same day: no holiday comes in
between. For the April and June orders the calculation without holidays
promises a day that is itself a public holiday.
