You will see what happens to the index when you sort — one of the most
surprising behaviours in pandas.

**What you need to do:**

1. Sort the table by score, **largest first**, into a variable called
   `ranked`.
2. Print the **first three rows** of the `name` and `score` columns of
   `ranked`.
3. Print the name of the highest scorer — find it with `idxmax()` on `data`,
   **independently of the sorting**.
4. Print the index of `ranked` as a list.

**Expected output:**

```
   name  score
2  Mina     91
4   Efe     88
0   Ada     82
Mina
[2, 4, 0, 1, 3]
```

**Look at the last line:** the index is `[2, 4, 0, 1, 3]`, not
`[0, 1, 2, 3, 4]`. The rows moved but **their labels moved with them**. That
is a good thing — you do not lose where each row came from — but if you are
going to combine a sorted table with another one, that gapped index can
produce surprise `NaN`s.

To renumber: `ranked.reset_index(drop=True)`.
