Compare the sales of 9 March 2024 with last year: first by going back
365 days, then 364.

**What to do:**

1. Read the file as a series `s` with a date index.
2. For `day = pd.Timestamp("2024-03-09")` print three day names on one line:
   the day itself, 365 days earlier, 364 days earlier (`day_name()`).
3. Compute that day's yearly growth as a percentage in two ways and print
   them rounded to one decimal on one line: with `s.shift(365)` and with
   `s.shift(364)`.
4. Compute the same two growth rates for **every day** of 2024; print the
   standard deviation of each, rounded to one decimal, on one line.

**Expected output:**

```
Saturday Friday Saturday
44.9 18.9
18.7 7.2
```

Going back 365 days compares a Saturday with a Friday and inflates the growth
to more than double. In the last line the spread with 365 is far wider: most
of that swing is not growth but days of the week getting mixed up.
