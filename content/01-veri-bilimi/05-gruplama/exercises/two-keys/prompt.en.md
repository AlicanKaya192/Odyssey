This time group by two keys: the city and the grade letter.

**What you need to do:**

1. Group by `city` **and** `grade`, compute the mean score and **round to one
   place**; keep the result in a Series called `result`.
2. Print `result`.
3. Flatten `result` and print its **shape**.

**Expected output:**

```
city    grade
Ankara  A        86.5
        B        88.0
Bursa   B        70.0
        C        68.0
Izmir   A        76.0
        B        74.0
        C        64.0
Name: score, dtype: float64
(7, 3)
```

**Two things to notice:**

- The index has **two levels**. The cells that look empty mean "the same as
  above"; pandas does not repeat them.
- `reset_index()` turns those levels into columns and leaves you with an
  ordinary table: 7 rows and 3 columns (`city`, `grade`, `score`).

A MultiIndex is awkward to work with, so flattening it is usually the first
thing you do.
