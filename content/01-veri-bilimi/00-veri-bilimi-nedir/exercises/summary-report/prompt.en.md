Real data does not arrive as ready-made dictionaries; it usually arrives as
text, line by line, from a file. In this exercise you will do a small
analysis from end to end: **parse it, turn it into a table, summarise it.**

Each line in `raw_lines` is a CSV row: `name,city,score`.

**What you need to do:**

1. Split each line on the comma and turn it into a dictionary shaped like
   `{"name": ..., "city": ..., "score": ...}`. Collect these in a list called
   `records`. **The score must be a number**, not text.
2. Pull the scores into a list called `scores`.
3. Compute the average and keep it in a variable called `average`.
4. Print these four lines:

```
Records: 5
Lowest: 68
Highest: 91
Average: 80.6
```

**Careful:** if you do not convert the score with `int()`, `max` compares the
text alphabetically and `"88"` can come out larger than `"91"`. This is one
of the most common mistakes in real data work.
