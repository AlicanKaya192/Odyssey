You will select rows and columns **by position** with `iloc`.

**What you need to do:**

1. Print the value in the first column of the first row.
2. Print the `name` and `score` columns of **rows 1 and 2**.
3. Print the **first three rows** of the first and third columns.
4. Print the name in the **last row**.

**Expected output:**

```
Ada
    name  score
1  Kerem     74
2   Mina     91
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
Sila
```

**Careful:** `iloc[1:3]` gives **two** rows — the end is excluded, the Python
rule. `loc` does not behave this way, as you will see in the next exercise.
