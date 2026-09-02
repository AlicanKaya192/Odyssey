You will do in one line what took ten lines in the first section.

**What you need to do:**

1. Compute the mean score of each city into a Series called `averages`.
2. Print `averages` **rounded to two places**.
3. Print how many people there are in each city.
4. Print the name of the city with the highest average.

**Expected output:**

```
city
Ankara    87.00
Bursa     69.00
Izmir     71.33
Name: score, dtype: float64
city
Ankara    3
Bursa     2
Izmir     3
dtype: int64
Ankara
```

**Two things to notice:**

- The groups come out **alphabetically**, regardless of their order in the
  data.
- The result is a Series and the city names are in the **index**. That is why
  `idxmax()` can hand you the city's name directly.
