The sales of some days were written in two parts on two separate rows.
Find them and merge them.

**What to do:**

1. Read the file with a date index and sort it.
2. Print the number of repeated dates (`index.duplicated().sum()`).
3. Print the repeated dates as a list in `"%Y-%m-%d"` form.
4. Print the values of 5 March 2024 as a list (`.tolist()`).
5. Add the parts: `groupby(level=0).sum()`. Print the new series' number of
   rows and whether its index has no repeats (`is_unique`) on one line.
6. Print the new value of 5 March 2024.

**Expected output:**

```
4
['2024-03-05', '2024-06-18', '2024-09-09', '2024-11-30']
[157, 105]
358 True
262
```

157 and 105 were two parts of the same day; together they make 262, the value
in the clean file. Had you dropped one of the parts, that day's sales would
have fallen by nearly half.
