You will answer the question "is this student above their own city's
average?"

`mean()` cannot answer it: `mean()` gives **one row per group**, while you
need each row's own group average next to it. That is exactly what
`transform` is for.

**What you need to do:**

1. Write each row's own city average beside it in a column called
   `city_mean`, **rounded to one place**.
2. Add an `above` column holding `True` for those scoring above their own
   city's average.
3. Print the `name`, `city`, `score`, `city_mean` and `above` columns.
4. Print how many people are above their own city's average.

**Expected output:**

```
    name    city  score  city_mean  above
0    Ada  Ankara     82       87.0  False
1  Kerem   Izmir     74       71.3   True
2   Mina  Ankara     91       87.0   True
3  Deniz   Bursa     68       69.0  False
4    Efe  Ankara     88       87.0   True
5   Sila   Izmir     76       71.3   True
6   Kaan   Bursa     70       69.0   True
7    Ela   Izmir     64       71.3  False
5
```

**The difference:**

- `groupby(...).mean()` gives 3 rows (one per group). The table shrinks.
- `groupby(...).transform("mean")` gives 8 rows (one per row). The table
  stays the same size and can be added as a column directly.

Look at Ada: she scored 82, above the overall average, but her **own city's**
average is 87, so she is `False`. This is where grouping earns its meaning.
