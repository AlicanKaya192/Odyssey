How much do sales move from one day to the next, and how much of that
comes from the weekly pattern?

**What to do:**

1. Read the file and compute the daily difference: `s.diff()`.
2. Print the mean of the absolute differences, rounded to one decimal.
3. Print the date (`"%Y-%m-%d"`) and the size of the biggest rise on one
   line.
4. Print the date and the size of the biggest fall on one line.
5. For 9 March 2024 print the difference against the same day last week
   (`s.diff(7)`).
6. Print the standard deviations of `s.diff()` and `s.diff(7)`, rounded to
   one decimal, on one line.

**Expected output:**

```
36.8
2023-12-30 106.0
2024-01-01 -139.0
12.0
46.1 17.1
```

The spread of the day-to-day difference is nearly three times that of the
week-to-week difference. The gap is the week's pattern: comparing Saturday
with Friday measures that pattern, comparing Saturday with Saturday measures
the real change.
