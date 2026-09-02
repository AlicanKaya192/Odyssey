In pandas a single square bracket makes a difference. In this exercise you
will see it with your own eyes.

**What you need to do:**

1. Produce a table containing the `name` and `score` columns, called
   `subset`.
2. Print `subset`.
3. Print the **name of the type** of `data["score"]`.
4. Print the **name of the type** of `data[["score"]]`.

**Expected output:**

```
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
3  Deniz     68
4    Efe     88
Series
DataFrame
```

`type(x).__name__` gives the name of a type.

**The last two lines are the most important distinction in this section:**
you asked for the same column and got a **Series** in one case and a
**table** in the other. The difference is one square bracket. A Series has
its own methods (`str.lower()`, `value_counts()`) and a table has others
(`shape` gives two values). If you do not know which you got, you get an
`AttributeError` and spend a long time working out why.
