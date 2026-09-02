You will use three methods that shorten long conditions, plus one shortcut.

**What you need to do:**

1. Print the `name` and `city` columns of those whose city is `Izmir` **or**
   `Bursa` — use `isin`.
2. Print the names of those aged **between** 21 and 22 as a list — use
   `between`.
3. Print the names of those **not** in Ankara as a list — invert the same
   mask.
4. Print the `name` and `score` columns of the **two rows** with the highest
   scores.

**Expected output:**

```
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
['Ada', 'Mina', 'Efe']
['Kerem', 'Deniz', 'Sila']
   name  score
2  Mina     91
4   Efe     88
```

**Things to know:**

- `isin` is the short way of chaining many values with `|`.
- `between(21, 22)` includes **both ends** — if you are used to Python
  slices you may read it as `21 <= x < 22`.
- `~` inverts a mask. Shorter than writing each `!=` out.
- `nlargest` does not sort everything, it just finds the largest; on large
  data you feel the difference.
