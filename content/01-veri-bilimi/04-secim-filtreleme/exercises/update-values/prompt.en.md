The pass mark has been raised to 75: everyone below it gets their score set
to 75.

**What you need to do:**

1. Set the `score` of rows **below 75** to `75`.
2. Print the `name` and `score` columns.
3. Print how many people now have exactly 75.
4. Print the new mean score (rounded to two places).

**Expected output:**

```
    name  score
0    Ada     82
1  Kerem     75
2   Mina     91
3  Deniz     75
4    Efe     88
5   Sila     76
2
81.17
```

**The real subject of this exercise:** the line below **does nothing.**

```python
data[data["score"] < 75]["score"] = 75
```

The square brackets produce an intermediate table, the assignment goes into
it, and it is thrown away immediately. You do not even get an error — the
code runs and the table is unchanged.

The correct way is to do the selection and the assignment in **a single
`loc` call**. The rule: never use square brackets twice in a row when
modifying a table.
