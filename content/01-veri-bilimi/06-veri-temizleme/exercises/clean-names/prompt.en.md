The **first job** of cleaning is the column names. Nothing else can be
written until they are fixed.

**What you need to do:**

1. Take a **copy** of `raw` and call it `data`.
2. Strip the spaces from the column names and lowercase them.
3. Print the new column names as a list.
4. Print the values of the `name` column as a list.

**Expected output:**

```
['name', 'city', 'score']
[' Ada ', 'kerem', 'MINA', 'Ada ', 'Deniz', 'efe ', 'Sila']
```

**Why this comes first:** `" Name "` and `"name"` are two different names and
both look the same on screen. Until they are fixed you cannot write
`data["name"]`.

The column names behave like a Series, so the `.str` methods work on them
too.

**The second line shows the next job:** the values still have spaces and
inconsistent case. That is what comes next.
