Turn the raw dump of the rental system (`bike_raw.csv`) into a regular daily
series with no gaps. The dates are written as `29.01.2022` and the rows are
out of order.

**What to do:**

1. Read the file and convert the `date` column to dates with
   `format="%d.%m.%Y"`. Print the number of rows and the number of fully
   identical (duplicate) rows on one line.
2. Drop the duplicates, make the date the index, sort, take the `rentals`
   column and bring it to daily frequency with `asfreq("D")`. Print the number
   of missing days and the length of the longest gap in days on one line.
3. Print the day of the lowest value (`"%Y-%m-%d"`), the value, and the values
   a week before and a week after (whole numbers) on one line.
4. Treat that day as missing too (make it `NaN`). Fill all the gaps with the
   mean of a week before and a week after, and round the result to whole
   numbers.
5. Print the filled values for 5–8 June 2023 as a list.
6. Print the length of the final series, the number of gaps left and the
   total on one line.

**Expected output:**

```
1093 6
9 4
2024-07-16 9 600 311
[348, 491, 476, 485]
1096 0 400910
```

An unordered dump of 1093 rows became a regular series of 1096 days. The 9
rentals on 16 July, next to the 600 and 311 of the neighbouring weeks, are
plainly a fault: a measurement, not demand. Even the four-day gap was filled,
because a week before and a week after were in place.
