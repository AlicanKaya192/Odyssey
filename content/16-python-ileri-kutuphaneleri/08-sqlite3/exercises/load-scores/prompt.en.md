Write the function `load_scores(rows)`: build the table
`scores (name, score)` in memory, insert `rows` with **`executemany`** and
return the list `[row count, average score]` with a single query; round the
average in SQL with `ROUND(AVG(score), 1)`. With an empty list the average is
`None`.

**Expected output:**

```
[3, 82.3]
```
