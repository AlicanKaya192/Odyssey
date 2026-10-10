`scores_long(table)` takes a dictionary like `{"id": [...], "score_2024":
[...], ...}`; the year is inside the column name. It should turn it into the
long form with `pd.wide_to_long` (`stubnames="score"`, `i="id"`, `j="year"`,
`sep="_"`), `reset_index()`, sort by `["id", "year"]` and return the rows as
an `[id, year, score]` list. **Do not write a loop.**

**Expected output:**

```
[1, 2024, 60]
[1, 2025, 70]
[2, 2024, 75]
[2, 2025, 80]
```
