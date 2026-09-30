Compare February 2024 with March 2024. By total one month is ahead, by
daily mean the other.

**What to do:**

1. Read the file and compute the monthly totals (`to_period("M")`).
2. Print the February and March 2024 totals on one line.
3. Print the two months' number of days on one line. A period's day count:
   `pd.Period("2024-02", "M").days_in_month`.
4. For each month divide the total by the number of days and round to one
   decimal; print both on one line.
5. Print the month with the higher daily mean as `February` or `March`.

**Expected output:**

```
8491 8919
29 31
292.8 287.7
February
```

The total puts March ahead, the daily mean February. The difference comes not
from sales but from March being two days longer.
