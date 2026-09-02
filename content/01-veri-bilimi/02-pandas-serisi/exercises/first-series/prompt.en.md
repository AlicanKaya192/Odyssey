You will keep four students' scores in a Series — with the **names**
alongside the numbers.

**What you need to do:**

1. Import pandas as `pd`.
2. Put the scores `[82, 74, 91, 68]` into a Series with the labels
   `["Ada", "Kerem", "Mina", "Deniz"]` and call it `scores`.
3. Print, in order: the Series itself, Mina's score, the mean (rounded to two
   places), and **the name of the highest scorer**.

**Expected output:**

```
Ada      82
Kerem    74
Mina     91
Deniz    68
dtype: int64
91
78.75
Mina
```

**Hint:** for the last line there is `idxmax()`. In NumPy `argmax` gave a
position; in pandas `idxmax` gives the **label** directly — this is where the
index earns its place.
