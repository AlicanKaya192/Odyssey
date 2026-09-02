The last two steps of cleaning: dropping the duplicates and deciding what to
do with the missing scores.

The names, text and types were already cleaned in the starter code.

**What you need to do:**

1. Print how many rows are duplicated by the `name` column.
2. Drop the duplicates by `name`, then drop the rows with a missing score.
   Reset the index and keep the result in a table called `clean`.
3. Print the shape of `clean`.
4. Print `clean`.
5. Print the mean score of the cleaned data (rounded to two places).

**Expected output:**

```
1
(4, 3)
    name    city  score
0    Ada  Ankara   82.0
1  Kerem   Izmir   74.0
2   Mina  Ankara   91.0
3    Efe   Izmir   88.0
83.75
```

**Two things to notice:**

- **The duplicate only becomes visible after the text is cleaned.** In the
  first exercise `duplicated()` said zero, because one was `"Ada "` and the
  other `" Ada "`. The order matters.
- We wrote `dropna(subset=["score"])`, not a bare `dropna()`. The bare form
  drops a row if **any** column is empty; on a table with twenty columns that
  means losing half your data.

You started with seven rows and finished with four. You lost three, and
**you have to say so in your report** — which decision cost how many
records.
