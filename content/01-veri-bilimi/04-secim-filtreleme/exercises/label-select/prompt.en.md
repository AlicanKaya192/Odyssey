`loc` goes by **label**, not by position. In this exercise you will see the
most important difference between them.

**What you need to do:**

1. Produce a table called `by_name` with the `name` column as its index.
2. Print Mina's score.
3. Print the scores of the rows **between** `Ada` and `Mina`.
4. Print Kerem's city.
5. Print **how many rows** the selection in step three has.

**Expected output:**

```
91
name
Ada      82
Kerem    74
Mina     91
Name: score, dtype: int64
Izmir
3
```

**The last line is the whole point:** `"Ada":"Mina"` gives **three** rows,
Mina included. `iloc[0:2]` would have given two.

`loc` includes the end because with labels "the one before Mina" is
meaningless — labels need not have a numeric order.
