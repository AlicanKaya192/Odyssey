Before touching the data you are going to **look** at it. That is the first
step of cleaning.

**What you need to do:**

1. Print the shape of the table.
2. Print the column names **as a list**.
3. Print the column types as a list.
4. Print how many empty cells the table has in total.
5. Print how many duplicated rows there are.

**Expected output:**

```
(7, 3)
[' Name ', 'city', 'score']
['str', 'str', 'str']
0
0
```

**Look carefully at the output; two problems are visible:**

- The column is called `' Name '` — with **spaces** at both ends. It looks
  like `Name` on screen, but `raw["Name"]` gives you a `KeyError`.
- The `score` column is of type **text**, not numeric. It contains values
  like `"abc"` and `"-1"`.

The missing and duplicate counts come out as zero, but that does not mean the
data is clean: the gaps are hidden inside **fake values** like `"abc"` and
`"-1"`, and the duplicates are invisible because of inconsistent spelling.
