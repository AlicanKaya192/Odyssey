Before building a model, ask the clean series (`bike_clean.csv`) five
questions.

In the starter code `y` (daily rentals) and `weather` (`temp_c`, `rain`) are
ready.

**What to do:**

1. **Is it growing?** Print the yearly totals (a list of whole numbers) and
   the year-on-year percentage change (one decimal, a list of two values) on
   one line.
2. **A weekly pattern?** Print the weekday means (Monday to Sunday, a list of
   whole numbers) and the ratio of Saturday to Monday (two decimals) on one
   line.
3. **A yearly pattern?** Among the monthly means print the number of the
   highest and of the lowest month and the ratio of the two (two decimals) on
   one line.
4. **Stationary?** Print the `adfuller` p-value for the level and for the
   first difference with three decimals on one line.
5. **An external factor?** Print the ratio of the mean of rainy days to the
   mean of dry days and the correlation between rentals and temperature (both
   with two decimals) on one line.

**Expected output:**

```
[116942, 134269, 149699] [14.8, 11.5]
[329, 343, 343, 353, 366, 443, 383] 1.35
7 1 2.37
0.325 0.0
0.55 0.78
```

The series grows 12–15 per cent a year, is high at the weekend, and in summer
is more than twice the winter. It is not stationary in levels (p = 0.33);
differenced, it is. And a rainy day is about half a dry one: the largest
source of movement in the series is something not written in the calendar.
