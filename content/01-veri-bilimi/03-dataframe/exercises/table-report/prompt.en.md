In this exercise you will bring the pieces of the section together and
produce a small report.

**What you need to do:**

1. Produce a new table with the `name` column as its index, called `report`.
2. Print **Mina's score** through `report`.
3. Print the distribution of cities (how many people per city).
4. Print the city **with the most people**.
5. Print how many **missing values** the whole table has.
6. On the last line print the mean score (rounded to two places) and the
   highest score **side by side**.

**Expected output:**

```
91
city
Ankara    3
Izmir     1
Bursa     1
Name: count, dtype: int64
Ankara
0
80.6 91
```

**You are using three things together:**

- **A column can be the index.** After `set_index("name")` you call a row by
  its name; instead of counting positions you write `loc["Mina", "score"]`.
- **`value_counts()` returns a Series**, which is why you can call `idxmax()`
  on it.
- **`isna().sum()` gives a count per column**, so you have to sum once more
  for the whole table. The result is zero — this data is clean, but in real
  data this is the first number to look at.
