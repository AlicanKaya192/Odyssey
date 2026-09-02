You will find everyone in Ankara who scored 80 or above.

**What you need to do:**

1. Collect the rows whose city is `"Ankara"` **and** whose score is 80 or
   above into a table called `selected`.
2. Print the `name` and `score` columns of `selected`.
3. Print how many rows were selected.
4. Print the mean score of the selection (rounded to two places).
5. Print the index of `selected` as a list.

**Expected output:**

```
   name  score
0   Ada     82
2  Mina     91
4   Efe     88
3
87.0
[0, 2, 4]
```

**There are two traps:**

- `and` **does not work**; use `&` and put **each condition in
  parentheses**. Forget the parentheses and `&` runs before the comparison.
- On the last line the index is `[0, 2, 4]`, not `[0, 1, 2]`. Filtering
  **skips** the numbers of the rows that were not selected; it does not
  renumber.
