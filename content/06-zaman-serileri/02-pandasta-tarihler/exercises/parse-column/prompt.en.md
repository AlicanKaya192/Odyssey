The `date` column in `store_sales.csv` arrives as text. Turn it into
real dates and show that the column now knows the calendar.

**What to do:**

1. Read the file and convert the `date` column with `pd.to_datetime`.
2. Confirm that the conversion worked: print the result of
   `pd.api.types.is_datetime64_any_dtype(sales["date"])`.
3. Print the earliest and the latest date as `"%Y-%m-%d"` on one line.
4. Print the number of days between the two.
5. Print the day name of the first date (`day_name()`).

**Expected output:**

```
True
2022-01-01 2024-12-31
1095
Saturday
```

Three years are 1096 days, but the first and the last day are 1095 apart:
the number of **steps** between them is one less than the number of days.
