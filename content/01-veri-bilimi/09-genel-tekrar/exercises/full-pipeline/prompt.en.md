The whole module is in this exercise. The raw table has seven rows and
three separate problems: inconsistent city names, scores that arrived as
text, one duplicated record and two missing values.

**What you need to do:**

1. Take a copy of the raw data.
2. Clean the `city` column and unify it in title case.
3. Convert the `score` column to numbers — anything unconvertible becomes
   blank.
4. Keep **how many rows you started with** in a variable.
5. Drop records duplicated by `id` and keep the remaining row count in a
   variable.
6. Count **how many records are left with a blank score**.
7. Drop the rows with a blank score.
8. Print the four numbers **side by side on one line**: start, deduplicated,
   missing, remaining.
9. Print the count and mean by city.

**Expected output:**

```
7 6 2 4
        count  mean
city
Ankara      2  86.5
Izmir       2  71.0
```

**Three things to notice:**

- **The order:** group before fixing the city and `"Izmir "` and `"Izmir"`
  become separate groups.
- **`"abc"` is not a bug**, it is dirt that came with the data.
  `errors="coerce"` turns it into a blank and lets the program continue.
- **The numbers go in the report:** you started with seven records and
  finished with four. An analysis that does not say so is hiding something
  the reader does not know.

And look at the last line: Bursa disappeared entirely, because its only
record had a blank score.
