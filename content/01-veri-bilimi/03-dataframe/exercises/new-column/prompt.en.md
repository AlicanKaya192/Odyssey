You will add two computed columns to the table — **without a loop**.

**What you need to do:**

1. Add a `passed` column holding `True` for scores of **75 or above**.
2. Add a `bonus` column that adds 10 to everyone's score.
3. Print the `name`, `score`, `passed` and `bonus` columns together.
4. Print how many people passed.

**Expected output:**

```
    name  score  passed  bonus
0    Ada     82    True     92
1  Kerem     74   False     84
2   Mina     91    True    101
3  Deniz     68   False     78
4    Efe     88    True     98
3
```

**Careful:** selecting four columns together needs **nested square
brackets**: `data[["name", "score", "passed", "bonus"]]`. A single bracket
means a single column.

The last line adds up the `True` values — `True` counts as 1 when summing.
