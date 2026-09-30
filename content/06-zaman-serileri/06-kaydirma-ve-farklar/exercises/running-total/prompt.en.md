Compare 2023 and 2024 cumulatively: which reached 50 thousand units
sooner?

**What to do:**

1. Read the file as a series `s` with a date index.
2. Compute the running total of each year:
   `s.loc["2023"].cumsum()` and `s.loc["2024"].cumsum()`.
3. Print the date (`"%Y-%m-%d"`) each year first reached 50000, one per line.
   Hint: `(ytd >= 50000).idxmax()` gives the first date the condition holds.
4. Print the running totals on 30 June (2023 first, then 2024) on one line.
5. Print by what percentage the first half of 2024 is above the first half of
   2023, rounded to one decimal.

**Expected output:**

```
2023-07-24
2024-06-28
44299 50659
14.4
```

2024 reached the same threshold about four weeks sooner. A running total
wipes out the daily ups and downs and shows how the gap between the two years
opens up.
