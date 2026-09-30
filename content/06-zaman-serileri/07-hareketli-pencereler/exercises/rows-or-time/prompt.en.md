In a series with missing days, "the total of the last 7 days" can be two
different things.

**What to do:**

1. Read `sales_messy.csv`, sort it and add up the repeats → `fixed`.
2. Print the total for 20 July 2024 with a row window:
   `fixed.rolling(7).sum()`.
3. Find the stretch those seven rows cover, in days: find the date of the
   seventh row counting back from 20 July in `fixed`, and add 1 to the number
   of days between it and 20 July. Print the result.
4. For the same day print the total with a time window and the number of
   records in that window on one line: `fixed.rolling("7D").sum()` and
   `.count()`.
5. Print the number of days that have fewer than 7 records in the time window
   (`fixed.rolling("7D").count() < 7`).

**Expected output:**

```
2092.0
10
1200.0 4.0
36
```

The row window adds up seven records, but those records are spread over 10
days. The time window really looks at the last 7 days and finds only four
records. Neither is "weekly sales" on its own, but the second at least says
how many observations it rests on.
